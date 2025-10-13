import os
from google import genai
from google.genai import types


def is_sub_path(working_directory, path): # function to check for is sub_path to raise an error if isnt later
    working_directory = os.path.abspath(working_directory)
    path = os.path.abspath(path)
    return os.path.commonpath([working_directory, path]) == working_directory

def get_files_info(working_directory, directory="."): #
    try:
        full_path = os.path.join(working_directory, directory)
        get_files = []
        all_entries = os.listdir(full_path)
        
        if is_sub_path(working_directory, full_path) == False: #use for earlier function
            return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
        elif os.path.isdir(full_path) == False:
            return f'Error: "{directory}" is not a directory'
        
        for entry in all_entries:    # iterates each entry in the directory. obtains the relevant info
            file_path = os.path.join(full_path, entry) #
            file_size = os.path.getsize(file_path)
            file_or_dir = f"is_dir={os.path.isdir(file_path)}" #returns a true or false that can than then be used in a string
            txt = f"- {entry}: file_size={file_size} bytes, {file_or_dir}"
            get_files.append(txt) # appends each entry to a list
        contents = "\n".join(get_files) # joins each entry into a string, resulting in a format that present info like txt variable
        return contents
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first 10000 characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file within the working directory. Creates the file if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file",
            ),
        },
        required=["file_path", "content"],
    ),
)


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info, 
        schema_get_file_content, 
        schema_write_file,
        schema_run_python_file
    ]
)
