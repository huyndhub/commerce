import time

from .utils import get_filename_ext


def base_upload(filename, path="default/file"):
    new_filename = time.time()
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "{path}/{final_filename}".format(
        path=path,
        final_filename=final_filename
    )
