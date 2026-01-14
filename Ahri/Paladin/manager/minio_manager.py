import asyncio
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from loguru import logger
from minio import Minio
from minio.error import S3Error

from Ahri.Paladin.config.config import settings


class MinioManager(object):

    def __init__(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        bucket_name=settings.MINIO_BUCKET_NAME,
        secure: bool = True,
    ):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)
        self.bucket_name = bucket_name

        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)

    def list_objects(self, prefix: str = "", filter=[]) -> list:
        try:
            objects = []
            for obj in self.client.list_objects(bucket_name=self.bucket_name, prefix=prefix, recursive=True):
                if not obj.object_name.endswith("/") and obj.object_name.lower().endswith(filter):
                    objects.append(obj)
            logger.info(f"Bucket {self.bucket_name} contains {len(objects)} files")
            return objects
        except S3Error as e:
            logger.error(f"Failed to get minio object list `{self.bucket_name}`: {e}")
            return []
        except Exception as e:
            logger.error(f"Unknown error when getting file list `{self.bucket_name}`: {e}")
            return []

    async def list_objects_async(self, prefix: str = "", filter=[]) -> list:
        return await asyncio.to_thread(self.list_objects, prefix, filter)

    def download_file(self, object_name: str, file_path: Path) -> Path | None:
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            if file_path.exists():
                logger.debug(f"File already exists: {file_path}")
                return file_path

            self.client.fget_object(bucket_name=self.bucket_name, object_name=object_name, file_path=str(file_path))
            logger.info(f"File downloaded, minio: `{self.bucket_name}/{object_name}` -> local: `{file_path}`")
            return file_path

        except S3Error as e:
            logger.error(f"File download `{self.bucket_name}/{object_name}` minio error: {e}")
            return None
        except Exception as e:
            logger.error(f"File download `{self.bucket_name}/{object_name}` unknown error: {e}")
            return None

    async def download_file_async(self, object_name: str, file_path: Path) -> Path | None:
        return await asyncio.to_thread(self.download_file, object_name, file_path)

    def upload_file(self, file_path: Path, object_name: str | None = None):
        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return None

            final_object_name = object_name or file_path.name

            self.client.fput_object(
                bucket_name=self.bucket_name, object_name=final_object_name, file_path=str(file_path)
            )
            minio_url = self.client.presigned_get_object(bucket_name=self.bucket_name, object_name=final_object_name)

            logger.info(f"File uploaded, local: {file_path} -> minio: {minio_url}")
            return minio_url
        except S3Error as e:
            logger.error(f"File upload `{self.bucket_name}/{object_name}` minio error: {e}")
            return None
        except Exception as e:
            logger.error(f"File upload `{self.bucket_name}/{object_name}` unknown error: {e}")
            return None

    async def upload_file_async(self, file_path: Path, object_name: str | None = None):
        return await asyncio.to_thread(self.upload_file, file_path, object_name)

    def upload_files(self, file_paths_and_object_names: dict[Path, str]):
        upload_file_urls = []

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(self.upload_file, file_path=file_path, object_name=object_name)
                for file_path, object_name in file_paths_and_object_names.items()
            ]

            for future in as_completed(futures):
                upload_file_urls.append(future.result())

        return upload_file_urls

    async def upload_files_async(self, file_paths_and_object_names: dict[Path, str]):
        upload_tasks = []

        for file_path, object_name in file_paths_and_object_names.items():
            upload_task = self.upload_file(file_path=file_path, object_name=object_name)
            upload_tasks.append(upload_task)
        results = await asyncio.gather(*upload_tasks)

        upload_file_urls = [result for result in results if result is not None]
        return upload_file_urls

    def delete_file(self, object_name: str) -> bool:
        try:
            self.client.remove_object(bucket_name=self.bucket_name, object_name=object_name)
            logger.info(f"File deleted, minio: `{self.bucket_name}/{object_name}`")
            return True
        except S3Error as e:
            logger.error(f"File delete `{self.bucket_name}/{object_name}` minio error: {e}")
            return False
        except Exception as e:
            logger.error(f"File delete `{self.bucket_name}/{object_name}` unknown error: {e}")
            return False

    async def delete_file_async(self, object_name: str) -> bool:
        return await asyncio.to_thread(self.delete_file, object_name)


minio_manager = MinioManager(
    endpoint=settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False,
)
