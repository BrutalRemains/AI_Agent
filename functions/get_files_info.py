import os
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