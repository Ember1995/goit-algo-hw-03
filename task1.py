import argparse
from pathlib import Path
from shutil import copyfile


parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", required=True, help="Source folder")
parser.add_argument("--output", "-o", default="dist", help="Output folder")
args = vars(parser.parse_args())
source = args.get("source")
output = args.get("output")


def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PermissionError as e:
            print(f"Permission denied for {args[0]}: {e}")
        except FileNotFoundError:
            print(f"File not found: {args[0]}")
        except Exception as e:
            print(f"Error processing {args[0]}: {e}")
    return wrapper


@handle_exceptions
def read_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            read_folder(el)
        else:
            copy_file(el)

@handle_exceptions
def copy_file(file: Path) -> None:
    ext = file.suffix.lower().strip('.')
    new_path = Path(output) / ext
    new_path.mkdir(exist_ok=True, parents=True)
    copyfile(file, new_path / file.name)

read_folder(Path(source))
