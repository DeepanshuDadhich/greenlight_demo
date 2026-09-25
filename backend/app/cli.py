import subprocess
import sys


def dev() -> None:
    subprocess.run(
        ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        check=True,
    )


def test() -> None:
    result = subprocess.run(["pytest"], check=False)
    sys.exit(result.returncode)
