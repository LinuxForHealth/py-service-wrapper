import requests
import json
import os

SERVICE_HOST = os.getenv("SERVICE_HOST", "127.0.0.1")


def test_insert_user():
    response = requests.post(
        f"http://{SERVICE_HOST}:5000/insert_user?fname=goku&lname=son"
    )
    assert response.status_code == 200


def test_fetch_user():
    response = requests.get(f"http://{SERVICE_HOST}:5000/fetch_users?fname=goku")
    assert response.status_code == 200

    expected = {"id": 1, "first_name": "goku", "last_name": "son"}

    assert sorted(expected.items()) == sorted(json.loads(response.content)[0].items())


def test_upload_download():
    bucket = "dbz"
    name = "songoku"
    data = "kamehameha"
    response = requests.post(
        f"http://{SERVICE_HOST}:5000/upload?bucket={bucket}&name={name}&data={data}"
    )
    assert response.status_code == 200

    response = requests.get(
        f"http://{SERVICE_HOST}:5000/download?bucket={bucket}&name={name}"
    )

    assert response.status_code == 200

    assert f'"{data}"'.encode() == response.content
