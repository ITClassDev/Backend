import random
import string
import os
import time
import hashlib
import pathlib
import zipfile
import io
from typing import List, Dict

async def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


async def get_file_extension(filename):
    return filename[filename.rfind(".") + 1:]


async def generate_filename(file_ext, prefix="shtp_upl_", custom_name=None):
    base_name = f"{prefix}{int(time.time())}{await get_random_string(8)}"
    if custom_name:
        base_name = custom_name
    return f"{base_name}.{file_ext}"


async def md5_hash_file(content):
    return hashlib.md5(content).hexdigest()



async def upload_file(file, allowed_extensions: list, upload_path: str = None, custom_name: str = None, write: bool = True, md5_name: bool = False):
    if file:
        file_ext = await get_file_extension(file.filename)
        if file_ext and file_ext in allowed_extensions:
            contents = file.file.read()
            size = len(contents)
            if not md5_name:
                file_name = await generate_filename(file_ext, custom_name=custom_name)
            else:
                file_name = await md5_hash_file(contents)
                # print("FILE NAME: ", file_name)
                file_name = f"{file_name}.{file_ext}"
            if write:
                with open(os.path.join(upload_path, file_name), "wb") as file_descr:
                    file_descr.write(contents)
                return {"status": True, "file_name": file_name, "extension": file_ext, "size": size}
            else:
                return {"status": True, "file_content": contents, "size": size}
        else:
            return {"status": False, "info": "Files with such extensions are forbidden"}
    else:
        return {"status": False, "info": "no file in request"}


async def read_file(file_name: str, upload_path: str):
    return pathlib.Path(os.path.join(upload_path, file_name)).read_text()

async def create_archive(source_path: str, file_pathes: List[str], extra_files: List[Dict[str, str]] = []) -> io.BytesIO:
    zip_bytes_io = io.BytesIO()
    with zipfile.ZipFile(zip_bytes_io, 'w', zipfile.ZIP_DEFLATED) as zipped:
        # Write path based files
        for file_name in file_pathes:
            zipped.write(os.path.join(source_path, file_name), file_name, zipfile.ZIP_DEFLATED)
        # Write extra files
        for file_ in extra_files:
            zipped.writestr(file_["name"], file_["content"])

    return zip_bytes_io
