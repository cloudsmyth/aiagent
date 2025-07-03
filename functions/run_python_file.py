from pathlib import Path
from subprocess import run


def run_python_file(working_directory, file_path):
    working_dir = Path(working_directory).resolve()

    if Path(file_path).is_absolute():
        target_path = Path(file_path).resolve()
    else:
        target_path = (working_dir / file_path).resolve()

    try:
        target_path.relative_to(working_dir)
    except ValueError:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not target_path.exists():
        return f'Error: File "{file_path}" not found'

    if not target_path.suffix == '.py':
        return f'Error: "{file_path}" is not a Python file.'

    try:
        result = run(
            ['python3', file_path],
            timeout=30,
            capture_output=True,
            text=True,
            cwd=working_directory
        )

        output = []
        if result.stdout.strip():
            output.append(f"STDOUT: {result.stdout.strip()}")
        if result.stderr.strip():
            output.append(f"STDERR: {result.stderr.strip()}")
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if output:
            return '\n'.join(output)
        else:
            return "No ouput produced"
    except Exception as e:
        return f"Error: executing Python file: {e}"
