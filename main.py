import os
import sys
from google import genai
from google.genai import types, Client
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info, schema_get_file_content, schema_write_file, schema_run_python_file, available_functions
from functions.call_function import call_function
def main():
    load_dotenv()
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    
    if len(sys.argv) < 2: 
        print("Usage: python main.py '<your prompt here>'")
        sys.exit(1)

    verbose = False #verbose logic
    if "--verbose" in sys.argv:
        verbose = True
        sys.argv.remove("--verbose")
    
    
    system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files


All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    user_prompt = " ".join(sys.argv[1:])
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    response = client.models.generate_content(
        model = "gemini-2.0-flash-001", 
        contents = messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt))
    if verbose:
        print(f"User prompt: {user_prompt} ")
    
    
    
    if len(response.function_calls) > 0:
        for f in response.function_calls:
            results = call_function(f, verbose)
            if results.parts[0].function_response.response is None:
                raise Exception("fatal error")
            else:
                if verbose == True:
                    print(f"-> {results.parts[0].function_response.response['result']}")
            messages.append(results)


    else:
        print(response.text)
    
    
    
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count    

    if verbose:
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")





if __name__ == "__main__":
    main()
