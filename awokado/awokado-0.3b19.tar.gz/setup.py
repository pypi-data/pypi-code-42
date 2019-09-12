import imp
from os import path

from setuptools import setup

VERSION = imp.load_source("version", path.join(".", "awokado", "version.py"))
VERSION = VERSION.__version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="awokado",
    version=VERSION,
    description="Fast and flexible API framework based on Falcon and SQLAlchemy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/5783354/awokado",
    author="Dmitry Karnei",
    author_email="5783354@gmail.com",
    classifiers=(
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ),
    keywords=" ".join(
        sorted(
            {"api", "rest", "wsgi", "falcon", "sqlalchemy", "sqlalchemy-core"}
        )
    ),
    packages=["awokado", "awokado.documentation", "awokado.exceptions"],
    install_requires=(
        "bcrypt",
        "bulky",
        "boto3",
        "dynaconf",
        "falcon==2.0.0",
        "marshmallow>=3.0.0rc3",
        "pyaml",
        "clavis",
        "apispec",
        "jinja2",
        "SQLAlchemy>=1.3.0",
        "m2r",
    ),
    python_requires=">=3.6",
)
