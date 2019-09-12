# coding: utf-8

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

NAME = "wallee"
VERSION = "2.0.0"

REQUIRES = [
    "certifi>=2017.4.17",
    "python-dateutil>=2.1",
    "six>=1.10",
    "urllib3>=1.23",
    "enum34>=1.1.6"
]
    

setuptools.setup(
    name=NAME,
    version=VERSION,
    author="customweb GmbH",
    description="SDK that allows you to access wallee",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    keywords=["wallee", "Payment", "Payment Integration"],
    install_requires=REQUIRES,
    include_package_data=True,
    license='Apache-2.0',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Office/Business :: Financial :: Point-Of-Sale',
    ],
    python_requires='>=3.4',
)
