import os
from google.genai import types

def get_file_content(working_directory, file_path):
    item = ""
    MAX_CHARS = 10000
    try:
        abs_content = os.path.abspath(working_directory)
        target_content = os.path.normpath(os.path.join(abs_content, file_path))
        valid_target_content = os.path.commonpath([abs_content, target_content]) == abs_content
        if not valid_target_content:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_content):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_content, "r") as f:
            item = f.read(MAX_CHARS)
            if f.read(1):
                item += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    except Exception as e:
        return f"Error: {e}"
    return item
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to work with"
            ),
        },
    ),
)
