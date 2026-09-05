import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, target_file_path]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        with open(target_file_path,"w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"ERROR: {e}"
    

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write and overwrite specified file relative to the working directory, providing count of the characters written",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to write into, relative to the working directory (default is the working directory itself)",
                },
                "content": {
                    "type": "string",
                    "description":"content to write into a specified file"
                },
            },
        },
    },
}    