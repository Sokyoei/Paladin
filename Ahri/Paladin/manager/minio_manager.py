import asyncio
from pathlib import Path
from typing import Dict, List, Optional

from loguru import logger
from minio import Minio
from minio.error import S3Error

from Ahri.Paladin.config.config import MINIO_ACCESS_KEY, MINIO_ENDPOINT, MINIO_SECRET_KEY


class MinioManager(object):

    def __init__(self, endpoint: str, access_key: str, secret_key: str, secure: bool = True):
        self.client = Minio(endpoint, access_key=access_key, secret_key=secret_key, secure=secure)
        self.http_prefix = "https://" if secure else "http://"

    async def list_objects(self, bucket_name: str, prefix: str = "", filter=[]) -> List:

        def _list_objects():
            try:
                objects = []
                for obj in self.client.list_objects(bucket_name=bucket_name, prefix=prefix, recursive=True):
                    if not obj.object_name.endswith("/") and obj.object_name.lower().endswith(filter):
                        objects.append(obj)
                logger.info(f"Bucket {bucket_name} contains {len(objects)} files")
                return objects
            except S3Error as e:
                logger.error(f"Failed to get minio object list `{bucket_name}`: {e}")
                return []
            except Exception as e:
                logger.error(f"Unknown error when getting file list `{bucket_name}`: {e}")
                return []

        return await asyncio.to_thread(_list_objects)

    async def download_file(self, bucket_name: str, object_name: str, file_path: Path) -> Optional[Path]:
        def _download_file() -> Optional[Path]:
            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)

                if file_path.exists():
                    logger.debug(f"File already exists: {file_path}")
                    return file_path

                self.client.fget_object(bucket_name=bucket_name, object_name=object_name, file_path=str(file_path))
                logger.info(f"File downloaded, minio: `{bucket_name}/{object_name}` -> local: `{file_path}`")
                return file_path

            except S3Error as e:
                logger.error(f"File download `{bucket_name}/{object_name}` minio error: {e}")
                return None
            except Exception as e:
                logger.error(f"File download `{bucket_name}/{object_name}` unknown error: {e}")
                return None

        return await asyncio.to_thread(_download_file)

    async def upload_file(self, bucket_name: str, file_path: Path, object_name: Optional[str] = None):
        def _upload_file() -> bool:
            try:
                if not file_path.exists():
                    logger.error(f"File not found: {file_path}")
                    return None

                final_object_name = object_name or file_path.name

                if not self.client.bucket_exists(bucket_name):
                    self.client.make_bucket(bucket_name)

                self.client.fput_object(
                    bucket_name=bucket_name, object_name=final_object_name, file_path=str(file_path)
                )
                minio_path = f"{self.http_prefix}{MINIO_ENDPOINT}/{bucket_name}/{final_object_name}"

                logger.info(f"File uploaded, local: {file_path} -> minio: {minio_path}")
                return minio_path
            except S3Error as e:
                logger.error(f"File upload `{bucket_name}/{object_name}` minio error: {e}")
                return None
            except Exception as e:
                logger.error(f"File upload `{bucket_name}/{object_name}` unknown error: {e}")
                return None

        return await asyncio.to_thread(_upload_file)

    async def upload_files(self, bucket_name: str, file_paths_and_object_names: Dict[Path, str]):
        upload_tasks = []

        for file_path, object_name in file_paths_and_object_names.items():
            upload_task = self.upload_file(bucket_name=bucket_name, file_path=file_path, object_name=object_name)
            upload_tasks.append(upload_task)
        results = await asyncio.gather(*upload_tasks)

        successful_uploads = [result for result in results if result is not None]
        return successful_uploads

    async def delete_file(self, bucket_name: str, object_name: str) -> bool:
        def _delete_file() -> bool:
            try:
                self.client.remove_object(bucket_name=bucket_name, object_name=object_name)
                logger.info(f"File deleted, minio: `{bucket_name}/{object_name}`")
                return True
            except S3Error as e:
                logger.error(f"File delete `{bucket_name}/{object_name}` minio error: {e}")
                return False
            except Exception as e:
                logger.error(f"File delete `{bucket_name}/{object_name}` unknown error: {e}")
                return False

        return await asyncio.to_thread(_delete_file)


minio_manager = MinioManager(
    endpoint=MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, secure=False
)
