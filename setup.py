from pathlib import Path
from setuptools import find_packages, setup


def load_version():
    package_path = Path(__file__).parent.resolve() / "director"
    with open(package_path / "VERSION", encoding="utf-8") as f:
        return f.readline().rstrip()


def load_long_description():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


def load_requirements():
    with open("requirements.txt", encoding="utf-8") as f:
        return [r.rstrip() for r in f.readlines()]


setup(
    name="celery-director-linius",
    version=load_version(),
    description="Celery Director Linius",
    long_description=load_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/LiniusAustPty/celery-director",
    author_email="engineering@linius.com",
    author="Linius",
    license="BSD",
    packages=find_packages(),
    include_package_data=True,
    install_requires=load_requirements(),
    python_requires="~=3.8",
    extras_require={
        "dev": [
            "tox==3.5.3",
            "black==20.8b1",
        ],
        "doc": [
            "mkdocs==1.0.4",
            "mkdocs-material==4.6.3",
        ],
        "ci": [
            "pytest",
            "pytest-cov",
        ]
    },
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: System :: Monitoring",
    ],
    entry_points={
        "console_scripts": [
            "director=director.cli:cli"
        ]
    },
)
