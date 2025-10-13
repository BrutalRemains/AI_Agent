import os
def is_sub_path(base_path, target_path):
    base_path = os.path.abspath(base_path)
    target_path = os.path.abspath(target_path)
    return os.path.commonpath([base_path]) == os.path.commonpath([base_path, target_path])

def write_file(working_directory, file_path, content):    
    target = os.path.realpath(os.path.join(working_directory, file_path))
    if not is_sub_path(working_directory, target):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    try:
        dirpath = os.path.dirname(target)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
               
        with open(target, "w") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"