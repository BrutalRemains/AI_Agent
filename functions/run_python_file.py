import os
import subprocess
import sys

def is_sub_path(working_directory, path):
    wd = os.path.realpath(working_directory)
    p = os.path.realpath(path)
    return os.path.commonpath([wd, p]) == wd

def run_python_file(working_directory, file_path, args=[]):
    target = os.path.realpath(os.path.join(working_directory, file_path))
    
    # error coverage
    if not is_sub_path(working_directory, target):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target):
        return f'Error: File "{file_path}" not found.'
    if not target.lower().endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    

    completed = subprocess.run([sys.executable, target, *args],
                               cwd = working_directory,
                               capture_output=True,
                               text=True,
                               timeout=30,
    )
    #return string construction
   
    stdout = completed.stdout.strip()
    stderr = completed.stderr.strip()

    if not stdout and not stderr:
        return 'No output produced.'
    

    parts = [] # construction list
    if stdout:
        parts.append(f"STDOUT:\n{stdout}")
    if stderr:
        parts.append(f"STDERR:\n{stderr}")
    if completed.returncode != 0:
        parts.append(f"Process exited with code {completed.returncode}")

    return "\n".join(parts)