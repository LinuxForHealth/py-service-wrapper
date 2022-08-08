from setuptools import setup, find_packages

setup(
    description="test project",
    license="BSD license",
    include_package_data=True,
    keywords="fhir, resources, python, hl7, health IT, healthcare",
    name="test-project",
    packages=find_packages(".", exclude=["*tests*"]),
    version="0.0.1",
    install_requires=["asyncpg==0.26.0", "minio==7.1.11"],
    python_requires=">=3.8",
)
