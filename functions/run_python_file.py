import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        if os.path.commonpath([working_dir_abs, target_file_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file_path]
        if args != None:
            command.extend(args)
        command_output = subprocess.run(command, cwd = working_dir_abs, capture_output = True, text = True, timeout = 30.0)
        if command_output.returncode != 0:
            return f"Process exited with code {command_output.returncode}"
        if command_output.stdout == None and command_output.stderr == None:
            return "No output produced"
        return f"STDOUT: {command_output.stdout} \nSTDERR: {command_output.stderr}"

    except Exception as e:
        return f"Error: executing Python file: {e}"
    