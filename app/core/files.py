import random
import string
import os
import time
import hashlib


async def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


async def get_file_extension(filename):
    return filename[filename.rfind(".") + 1:]


async def generate_filename(file_ext, prefix="itc_upl_", custom_name=None):
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
            if not md5_name:
                file_name = await generate_filename(file_ext, custom_name=custom_name)
            else:
                file_name = await md5_hash_file(contents)
                # print("FILE NAME: ", file_name)
                file_name = f"{file_name}.{file_ext}"
            if write:
                with open(os.path.join(upload_path, file_name), "wb") as file_descr:
                    file_descr.write(contents)
                return {"status": True, "file_name": file_name, "extension": file_ext}
            else:
                return {"status": True, "file_content": contents}
        else:
            return {"status": False, "info": "Files with such extensions are forbidden"}
    else:
        return {"status": False, "info": "no file in request"}
