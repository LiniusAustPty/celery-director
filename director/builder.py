from uuid import uuid4
from functools import cached_property

import celery

from director.exceptions import WorkflowSyntaxError
from director.extensions import cel, cel_workflows
from director.models import StatusType
from director.models.tasks import Task
from director.models.workflows import Workflow
from director.tasks.workflows import start, end


class WorkflowBuilder(object):
    def __init__(self, workflow_id):
        self.workflow_id = workflow_id
        self.canvas = []
        # Pointer to the previous task(s)
        self.previous = []

    @property
    def tasks(self):
        return self.template.get('tasks')

    @property
    def default_queue(self):
        return self.template.get('queue', 'celery')

    @cached_property
    def workflow(self):
        return Workflow.query.filter_by(id=self.workflow_id).first()

    @cached_property
    def template(self):
        return cel_workflows.get_by_name(self.workflow)

    def new_task(self, task_name, queue=None, single=True):
        task_id = str(uuid4())

        # We create the Celery task specifying its UID
        signature = cel.tasks.get(task_name).subtask(
            kwargs={"workflow_id": self.workflow_id, "payload": self.workflow.payload},
            queue=queue or self.default_queue,
            task_id=task_id,
        )

        # Director task has the same UID
        task = Task(
            id=task_id,
            key=task_name,
            previous=self.previous,
            workflow_id=self.workflow.id,
            status=StatusType.pending,
        )
        task.save()

        if single:
            self.previous = [signature.id]

        return signature

    def parse(self, tasks):
        canvas = []
        for task in tasks:
            if type(task) is str:
                signature = self.new_task(task)
                canvas.append(signature)
                continue
            if type(task) is dict:
                data = list(task.values())[0]
                sub_canvas = self.parse_sub_canvas(**data)
                canvas.append(sub_canvas)
                continue

            raise WorkflowSyntaxError()
        return canvas

    def parse_sub_canvas(self, tasks, **kwargs):
        celery_type, is_single = self._parse_celery_type(kwargs.get("type"))
        params = {'single': is_single, 'queue': kwargs.get('queue')}
        sub_tasks = [self.new_task(t, **params) for t in tasks]
        if not is_single:
            self.previous = [s.id for s in sub_tasks]
        return celery_type(*sub_tasks, task_id=str(uuid4()))

    def build(self):
        start_task = start.si(self.workflow.id).set(queue=self.default_queue)
        end_task = end.si(self.workflow.id).set(queue=self.default_queue)
        self.canvas = self.parse(self.tasks)
        self.canvas.insert(0, start_task)
        self.canvas.append(end_task)

    def run(self, **kwargs):
        if not self.canvas:
            self.build()

        canvas = celery.chain(*self.canvas, task_id=str(uuid4()))

        try:
            return canvas.apply_async(**kwargs)
        except Exception as e:
            self.workflow.status = StatusType.error
            self.workflow.save()
            raise e

    def _parse_celery_type(self, name):
        if name not in ['group', 'chain']:
            raise WorkflowSyntaxError
        is_single = name == 'chain'
        return getattr(celery, name), is_single
