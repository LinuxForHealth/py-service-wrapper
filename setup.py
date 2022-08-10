import os
from setuptools import setup, find_packages

requirements = ["fastapi==0.79.0", "uvicorn==0.18.2", "pyyaml==6.0"]

test_requirements = ["pytest==7.1.2", "pytest-cov==3.0.0"]


setup(
    description="Wraps python projects and serves them over HTTPs",
    license="Apache 2.0",
    include_package_data=True,
    keywords="fhir, resources, python, hl7, health IT, healthcare",
    name="py-service-wrapper",
    packages=find_packages(".", exclude=["*tests*"]),
    install_requires=requirements,
    tests_require=test_requirements + requirements,
    url="https://github.com/LinuxForHealth/py-service-wrapper",
    version="0.0.1",
    python_requires=">=3.9",
)
