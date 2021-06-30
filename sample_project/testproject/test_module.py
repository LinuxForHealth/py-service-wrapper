from typing import Dict, Optional
from pydantic import BaseModel
from typing import Union
import asyncpg
from minio import Minio
import io

dsn_str = f"postgresql://postgres:postgres@postgres:5432/postgres"


class MinioClient:
    _client = None

    def init(self):
        if self._client is None:
            self._client = Minio(
                "minio:9000",
                secure=False,
                access_key="minioadmin",
                secret_key="minioadmin",
            )

    def upload(self, bucket, object, data):
        if not self._client.bucket_exists(bucket):
            self._client.make_bucket(bucket)

        return self._client.put_object(
            bucket,
            object,
            io.BytesIO(data.encode()),
            length=-1,
            part_size=10 * 1024 * 1024,
        )

    def download(self, bucket, object):
        return self._client.get_object(bucket, object).read()


class Database:
    _pool = None

    async def create_pool(self):
        if self._pool is None:
            self._pool = await asyncpg.create_pool(dsn=dsn_str)

    async def insert_user(self, fname, lname):
        await self._pool.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id serial PRIMARY KEY,
                first_name text,
                last_name text
            )
        """
        )

        # Insert a record into the created table.
        result = await self._pool.execute(
            """
            INSERT INTO users(first_name, last_name) VALUES($1, $2)
        """,
            fname,
            lname,
        )

        return result

    async def fetch_users(self, fname):
        row = await self._pool.fetch("SELECT * FROM users WHERE first_name = $1", fname)
        return row

    async def close(self):
        await self._pool.close()


def hello_name(name):
    return f"Hello, {name}!"


def hello_name_and_age(name, age: int):
    return f"Hello, {name}! You are {age} years old"


def hello_world():

    return f"Hello, World!"


def hello_post(data: Dict):
    return f"hello {data}"


class TestModel(BaseModel):
    name: str
    age: int
    year: int


def hello_pydantic(data: TestModel):
    return f"hello {data.name}! You are {data.age} years old"


def hello_dynamic(name: str, age: Union[int, float]):
    return f"Hello, {name}! You are {age} years old"


def hello_header(name: Optional[str], age: int = 100):
    return {
        "Hello": f"{name}!",
        "Age": f"{age}!",
    }


# Example init connection to postgres
dao = Database()
minio = MinioClient()


async def postgres_connect():
    await dao.create_pool()


def minio_connect():
    minio.init()


async def close():
    await dao.close()


async def insert_user(fname: str, lname: str):
    minio.upload("users", fname + lname, fname)
    return await dao.insert_user(fname, lname)


async def fetch_users(fname):
    return await dao.fetch_users(fname)


def upload(bucket, name, data):
    return minio.upload(bucket, name, data)


def download(bucket, name):
    return minio.download(bucket, name)
