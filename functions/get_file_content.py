from pathlib import Path


def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000
    working_dir = Path(working_directory).resolve()

    if Path(file_path).is_absolute():
        target_file = Path(file_path).resolve()
    else:
        target_file = (working_dir / file_path).resolve()

    if not Path(target_file).is_file():
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        target_file.relative_to(working_dir)
    except ValueError:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    try:
        with open(target_file, "r", encoding="UTF-8") as f:
            content = f.read(MAX_CHARS + 1)
            if len(content) > MAX_CHARS:
                return content[:MAX_CHARS] + f'...File "{file_path}" truncated at 10000 characters'
            else:
                return content

    except UnicodeDecodeError:
        return f"Error: Cannot read '{file_path}' - not a text file or encoding issue"
    except PermissionError:
        return f"Error: Permission denied to read '{file_path}'"
    except Exception as e:
        return f"Error reading file: {str(e)}"
