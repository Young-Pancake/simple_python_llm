import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_file = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_file, file_path))
        valid_target_file = os.path.commonpath([abs_file, target_file]) == abs_file
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite files",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to work with"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to write or modify"
            ),
        },
    ),
)
