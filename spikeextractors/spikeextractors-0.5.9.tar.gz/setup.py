import setuptools

d = {}
exec(open("spikeextractors/version.py").read(), None, d)
version = d['version']
pkg_name = "spikeextractors"
long_description = open("README.md").read()

setuptools.setup(
    name=pkg_name,
    version=version,
    author="Cole Hurwitz, Jeremy Magland, Alessio Paolo Buccino, Matthias Hennig",
    author_email="colehurwitz@gmail.com",
    description="Python module for extracting recorded and spike sorted extracellular data from different file types and formats",
    url="https://github.com/SpikeInterface/spikeextractors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={},
    install_requires=[
        'numpy',
    ],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    )
)
