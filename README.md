# py-service-wrapper

This project allows the user to build a docker container that wraps a python library as a service. It uses [FastAPI](https://fastapi.tiangolo.com/) and [uvicorn](https://www.uvicorn.org/) to wrap the project as a web service in the container.

There are only two requirements for the project that is being wrapped:
1. It is packaged in a pip installable format such as sdist or a python wheel.
2. It provides a YAML file that lists the entrypoints into the library that need to be exposed as a service. The format of the YAML file is discussed below in more detail.

The py-service-wrapper project consists of two parts:

1. The python code that parses the YAML file and creates the appropriate endpoints. This code can be found under the webwrapper package in this repository.
2. The script that set up the project and create the final docker container. This script can be found under the scripts folder in the repository.

Both the python code and the script are packaged as a builder style docker image, that can be invoked directly from the library project, or integrated into the CICD pipeline for automation.

## py-service-wrapper Builder Docker Image
To build the builder docker image simple execute the following command from the root of this repository

`docker build -t py-service-wrapper-build-utils .`

## Format of the entrypoints YAML file
The YAML file has a simple format that lists the module and entrypoints that need to be exposed. A sample YAML file might look like:
```
version: 1
project:
  name: testProject
  version: 1
  module: testproject.api_module
  startup:
    - serviceone_connect
    - servicetwo_connect
  shutdown:
    - close
  entrypoints:
    - name: hello_world_endpoint
      entrypoint: hello_world
      path: 'hello'
    - name: hello_name_endpoint
      entrypoint: hello_name
      path: 'hello/{name}'
    - name: hello_post
      entrypoint: hello_post
      path: hellopost
      methods: 
      - POST
      - PUT
    - name: hello_header_endpoint
      entrypoint: hello_header
      path: helloheader
      headers:
      - name_in_header
```
- The `version` on line 1 defines the version of the YAML file format being used. Currently the version is ignored since this project only supports 1 version.
- The `project` section provides the actual details about the entrypoints into the project such as `name` and `version`.
- the `project.module` defines the module under which the functions that need to be exposed as the services reside
- the `startup` and `shutdown` are lists of functions to be called during startup and shutdown respectively
- entrypoints is a list where each entry is a separate endpoint for the service and each entry contains:
  - A unique `name`.
  - The `entrypoint` which is the name of the function in the `project.module` which needs to be exposed.
  - A `path` which is the url at which the endpoint will be exposed. This path can also contain any path parameters that will be passed to the exposed function.
  - Optionally `methods` as a list of HTTP methods to expose for the endpoint (defaults to GET)
  - Optionally `headers` as a list of parameters of the entrypoint that need to be treated as HTTP header values. Any underscores in the parameter name will be converted to dashes when looking for HTTP headers, so `name_in_header` will be passed the value of the header `name-in-header`

## Build a wrapper container for a project
To use the builder docker image to create a wrapper image for a python project the following command can be executed from that projects root:

`docker run -v $(pwd):/tmp/project -v /var/run/docker.sock:/var/run/docker.sock -e PROJECT_ROOT=/tmp/project -e PROJECT_DIST=<dist package> -e PROJECT_YAML=<YAML file> -e IMAGE_NAME=<final image tag> py-service-wrapper-build-utils:latest`

where:
- `<dist package>` is the path of the pip installable package of the project relative to the `PROJECT_ROOT`
- `<YAML file>` is the path of the YAML file relative to the `PROJECT_ROOT`
- `<final image tag>` is what that the wrapper docker image will be tagged as

## Run the wrapper docker image
The wrapper image exposes the service on port `5000` so the following docker run command can be used to run the container in a local environment:

`docker run -p 5000:5000 <final image tag>`

## TODO:
- Currently the `name`, `entrypoint`, and `path` for each entrypoint need to be explicitly defined in the YAML file. These should be made dynamic so that only `entrypoint` is the required.
  - `name` if not defined can be same as the entrypoint
  - `path` can be computed using the python `inspect` module (for GET endpoints)
- Currently we can only define a single module in the YAML file and all entrypoints must be in that module. We should support multiple modules, each with its own list of entrypoints.
- The endpoints are currently serviced of insecure http. HTTPs should be supported and should be the default
- Setup the github actions to automatically build the builder image and push to a docker registry
- Add unit tests to the webwrapper

# Sample Project
The repository also contains a sample project under the `sample_project` directory. To wrap this project as a service run the following command from the `sample_project` directory:

`docker run -v $(pwd):/tmp/project -v /var/run/docker.sock:/var/run/docker.sock -e PROJECT_ROOT=/tmp/project -e PROJECT_DIST=dist/test_project-0.0.1-py3-none-any.whl -e PROJECT_YAML=project.yaml -e IMAGE_NAME=sampleproject:1.0 py-service-wrapper-build-utils:latest`

To the wrapped sample project run the following command:

`docker run -p 5000:5000 sampleproject:1.0`

You can then access the exposed endpoints at:
- http://localhost:5000/hello
- http://localhost:5000/hello/myname
- http://localhost:5000/hello/myname/50

Sample Queries To experiment with sample project

```bash
curl -X 'GET' \
  'http://localhost:5000/insert_user?fname=goku&lname=son' \
  -H 'accept: application/json'

curl -X 'GET' \
'http://localhost:5000/fetch_users?fname=goku' \
-H 'accept: application/json'
```