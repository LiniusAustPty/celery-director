<p align="center">
  <img alt="Celery Director logo" src="https://raw.githubusercontent.com/ovh/celery-director/master/logo.png">
</p>
<p align="center">
  <a href="https://github.com/ovh/celery-director/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/ovh/celery-director/workflows/Tests/badge.svg"></a>
  <a href="https://www.python.org/"><img alt="Python versions" src="https://img.shields.io/badge/python-3.8%2B-blue.svg"></a>
  <a href="https://github.com/ovh/depc/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/badge/license-BSD%203--Clause-blue.svg"></a>
</p>
<p align="center">
  <a href="https://raw.githubusercontent.com/ovh/celery-director/master/director.gif"><img alt="Celery Director" src="https://raw.githubusercontent.com/ovh/celery-director/master/director.gif"></a>
</p>

----------------

Director is a simple and rapid framework used to manage tasks and build workflows using Celery.

The objective is to make Celery easier to use by providing :

- a WebUI to track the tasks states,
- an API and a CLI to manage and execute the workflows,
- a YAML syntax used to combine tasks into workflows,
- the ability to periodically launch a whole workflow,
- and many others.

See how to use Director with the quickstart and guides in the [documentation](https://ovh.github.io/celery-director/).

## Installation

Install the latest version of Director with pip (requires `Python 3.8` at least):

```bash
pip install celery-director
```

## Usage

### Write your code in Python

```python
# tasks/orders.py
from director import task
from .utils import Order, Mail

@task(name="ORDER_PRODUCT")
def order_product(*args, **kwargs):
    order = Order(
      user=kwargs["payload"]["user"],
      product=kwargs["payload"]["product"]
    ).save()
    return {"id": order.id}

@task(name="SEND_MAIL")
def send_mail(*args, **kwargs):
    order_id = args[0]["id"]
    mail = Mail(
      title=f"Your order #{order_id} has been received",
      user=kwargs["payload"]["user"]
    )
    mail.send()
```

### Build your workflows in YAML or JSON
```bash
export DIRECTOR_WORKFLOW_FORMAT=json
```

```yaml
# workflows.yml
product.ORDER:
  tasks:
    - ORDER_PRODUCT
    - SEND_MAIL
```

```json
# workflows.json
{
    "product.ORDER": {
        "tasks": [
            "ORDER_PRODUCT",
            "SEND_MAIL"
        ]
    }
}
```

### Run it

You can simply test your workflow in local :

```bash
$ director workflow run product.ORDER '{"user": 1234, "product": 1000}'
```

And run it in production using the director API :

```bash
$ curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"project": "product", "name": "ORDER", "payload": {"user": 1234, "product": 1000}}' \
  http://localhost:8000/api/workflows
```

Read the [documentation](https://ovh.github.io/celery-director/) to try the quickstart and see advanced usages of Celery Director.

## Project layout

    .env                # The configuration file.
    workflows.yml       # The yaml workflows definition.
    workflows.json      # The json workflows definition.
    tasks/
        example.py      # A file containing some tasks.
        ...             # Other files containing other tasks.

## Commands

* `director init [path]` - Create a new project.
* `director celery [worker|beat|flower]` - Start Celery daemons.
* `director webserver` - Start the webserver.
* `director workflow [list|show|run]` - Manage your project workflows.

## License

See https://github.com/ovh/celery-director/blob/master/LICENSE


## CodeArtifact - Release a new version
On a merge to main, a CircleCI workflow will be triggered that will publish this package to the `prod` CodeArtifact repository. To bump the version number, modify `director/VERSION` file.

pytest is run on push to non main branches

CircleCI workflow [here](https://app.circleci.com/pipelines/github/LiniusAustPty/celery-director)