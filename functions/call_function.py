from google import genai
from google.genai import types
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .write_file import write_file
from .run_python_file import run_python_file

def call_function(function_call_part, verbose=False):
    function_dict = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    function_name = function_call_part.name
    args = dict(function_call_part.args)  # make a copy

    if "working_directory" not in args:
        args["working_directory"] = "./calculator"

    # normalize possible key names from the model
    if function_name == "write_file":
        if "filename" in args and "file_path" not in args:
            args["file_path"] = args.pop("filename")

    if verbose:
        print(f"Calling function: {function_name}({args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_dict:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )],
        )

    function_result = function_dict[function_name](**args)
    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )],
    )
