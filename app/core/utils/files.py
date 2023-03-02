import random
import string
import os
import time


async def get_random_string(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


async def get_file_extension(filename):
    return filename[filename.rfind(".") + 1:]


async def generate_filename(file_ext, prefix="itc_upl_", custom_name=None):
    base_name = f"{prefix}{int(time.time())}{await get_random_string(8)}"
    if custom_name:
        base_name = custom_name
    return f"{base_name}.{file_ext}"


async def upload_file(file, allowed_extensions, upload_path, custom_name=None):
    if file:
        file_ext = await get_file_extension(file.filename)
        if file_ext and file_ext in allowed_extensions:
            contents = file.file.read()
            file_name = await generate_filename(file_ext, custom_name=custom_name)
            with open(os.path.join(upload_path, file_name), "wb") as file_descr:
                file_descr.write(contents)
            return {"status": True, "file_name": file_name}
        else:
            return {"status": False, "info": "Files with such extensions are forbidden"}
    else:
        return {"status": False, "info": "no file in request"}
