import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    result = ""
    try:
        abs_working_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_path, file_path))
        if os.path.commonpath([abs_working_path, target_path]) != abs_working_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_path]
        if args != None:
            command.extend(args)
        process = subprocess.run(command, cwd=working_directory,
			         capture_output=True, text=True,
				 timeout=30)
        if process.returncode != 0:
            result += f"Process exited with code {process.returncode}\n"
        if not process.stdout and not process.stderr:
            result += "No output produced"
        else:
            if process.stdout:
                result += f"STDOUT: {process.stdout}\n"
            if process.stderr:
                result += f"STDERR: {process.stderr}"
        return result
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to work with"
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="args to work with"
            ),
        },
    ),
)
