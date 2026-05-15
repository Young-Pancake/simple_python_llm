import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    info = []
    try:
        abs_path = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_path, directory))
        valid_target_dir = os.path.commonpath([abs_path, target_path]) == abs_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_path):
            return f'Error: "{directory}" is not a directory'

        for path in os.listdir(target_path):
            item = os.path.join(target_path, path)
            info.append(f"- {path}: file_size={os.path.getsize(item)} bytes, is_dir={os.path.isdir(item)}")
    except Exception as e:
        return f"Error: {e}"

    return "\n".join(info)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)
