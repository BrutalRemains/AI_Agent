import os 
from functions import config
def is_sub_path(working_directory, path):
    wd = os.path.realpath(working_directory)
    p = os.path.realpath(path)
    return os.path.commonpath([wd, p]) == wd

def get_file_content(working_directory, file_path):
    target = os.path.realpath(os.path.join(working_directory, file_path))
    if not is_sub_path(working_directory, target):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target, "r") as f:
            data = f.read(config.MAX_CHARS + 1)
    except Exception as e:
        return f"Error: {e}"
    
    if len(data) <= config.MAX_CHARS:
        return data
    return data[:config.MAX_CHARS] + f'[...File "{file_path}" truncated at {config.MAX_CHARS} characters]'