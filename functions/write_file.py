from pathlib import Path
from google.genai import types


def write_file(working_directory, file_path, content):
    working_dir = Path(working_directory).resolve()

    if Path(file_path).is_absolute():
        target_path = Path(file_path).resolve()
    else:
        target_path = (working_dir / file_path).resolve()

    try:
        target_path.relative_to(working_dir)
    except ValueError:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    try:
        print(target_path)
        if not target_path.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.touch()
    except PermissionError:
        return f"Error: Permission denied: Cannot create {target_path}"
    except FileExistsError:
        return f"Error: File exists where directory expected: {target_path}"
    except OSError as e:
        return f"Error: OS error creating {target_path}: {str(e)}"
    except Exception as e:
        return f"Error: Unexpected error creating {target_path}: {str(e)}"

    try:
        with open(target_path, "w") as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Could not write to file at "{file_path}": {str(e)}'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a file to target path with spcified content"
                ", constrained to the working directory.",
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
