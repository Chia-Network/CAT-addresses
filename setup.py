#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "rt") as fh:
    long_description = fh.read()

dependencies = [
    "aiohttp==3.9.0",
    "backoff==2.0.1",
    "click==8.1.3",
    "influxdb_client==1.29.1",
    "python-dotenv==0.20.0",
    "requests==2.28.0",
]

dev_dependencies = [
    "flake8",
    "mypy",
    "black==21.12b0",
    "pytest",
    "pytest-asyncio",
    "pytest-env",
]

setup(
    name="chia-transaction-exporter",
    packages=find_packages(exclude=("tests",)),
    author="Freddie",
    author_email="f.coleman@chia.net",
    setup_requires=["setuptools_scm"],
    install_requires=dependencies,
    url="https://github.com/Chia-Network/transaction-exporter",
    license="https://opensource.org/licenses/Apache-2.0",
    description="Exports historic transaction data to a database ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Security :: Cryptography",
    ],
    extras_require=dict(
        dev=dev_dependencies,
    ),
    project_urls={
        "Bug Reports": "https://github.com/Chia-Network/transaction-exporter",
        "Source": "https://github.com/Chia-Network/transaction-exporter",
    },
)
