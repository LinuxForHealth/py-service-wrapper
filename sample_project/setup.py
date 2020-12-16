from setuptools import setup, find_packages

setup(
    description="test project",
    license="BSD license",
    include_package_data=True,
    keywords="fhir, resources, python, hl7, health IT, healthcare",
    name="test-project",
    packages=find_packages('.', exclude=["*tests*"]),
    url="https://github.ibm.com/ebaron/dicom-fhir-converter",
    version="0.0.1",
    python_requires=">=3.6"
)