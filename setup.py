import os
from setuptools import setup, find_packages

requirements = [
    'fastapi==0.62.0',
    'uvicorn==0.13.1',
    'pyyaml==5.3.1'
]

test_requirements = [
    'pytest==4.6.3',
    'pytest-cov==2.7.1'
]


setup(
    description="Wraps python projects and serves them over HTTPs",
    license="BSD license",
    include_package_data=True,
    keywords="fhir, resources, python, hl7, health IT, healthcare",
    name="py-web-wrapper",
    packages=find_packages('.', exclude=["*tests*"]),
    install_requires=requirements,
    tests_require=test_requirements + requirements,
    url="https://github.ibm.com/ebaron/dicom-fhir-converter",
    version="0.0.1",
    python_requires=">=3.6"
)