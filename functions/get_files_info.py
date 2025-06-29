from pathlib import Path


def get_files_info(working_directory, directory=None):
    working_dir = Path(working_directory).resolve()

    if directory is None:
        target_dir = working_dir
    else:
        if Path(directory).is_absolute():
            target_dir = Path(directory).resolve()
        else:
            target_dir = (working_dir / directory).resolve()

    if not target_dir.is_dir():
        return f'Error: "{directory}" is not a directory'

    try:
        target_dir.relative_to(working_dir)
    except ValueError:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    contents = []
    try:
        items = sorted(target_dir.iterdir(), key=lambda x: x.name.lower())
        for item in items:
            file_size = item.stat().st_size
            is_directory = item.is_dir()
            line = f"- {item.name}: file_size={file_size} bytes, is_dir={is_directory}"
            contents.append(line)
        return '\n'.join(contents)
    except PermissionError:
        return f'Error: Permission denied to access "{target_dir}"'
    except Exception as e:
        return f'Error: Unable to read directory contents: {str(e)}'
