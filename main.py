import pathlib
from rich.console import Console
import os
import sys

console = Console()
print = console.print
ignored_files = [".gitignore", "requirements.txt", "README.md"]

# CONFIGURATION
category_map = {
    "media": [".mp4", ".mp3", ".m4a", ".mov", ".jfif", ".webm"],
    "images": [".png", ".jpg", ".gif", ".jpeg"],
    "executables": [".jar", ".exe", ".bin", ".bat"],
    "installers": [".msi", ".appinstaller", ".iso"],
    "code": [".py", ".js", ".json", ".java", ".bash", ".sh", ".lua"],
}
# DONT EDIT BELOW THIS LINE UNLESS YOU KNOW WHAT YOU ARE DOING
# ======================================================


def get_all_files(directory: str):
    filemap = {}
    for i in pathlib.Path(directory).glob("*"):
        if i.is_dir():
            print(f"'{i}' is a directory! Skipping.")
            continue

        if str(i.absolute()) == __file__:
            continue
        if i.name == "reset.py":
            continue
        if i.name in ignored_files:
            continue
        category: list = filemap.get(i.suffix, [])

        category.append(i)
        filemap[i.suffix] = category

    return filemap


def sort_categories(filemap: dict[str, pathlib.WindowsPath]):
    obj = {"other": []}
    for extension in filemap:
        for file in filemap[extension]:
            found = False
            for category in category_map:
                if file.suffix.lower() in category_map[category]:
                    cat: list = obj.get(category, [])
                    cat.append(file)
                    obj[category] = cat
                    found = True
            if not found:
                obj["other"].append(file)

    return obj


def move_files(sorted_files: dict[str, list[pathlib.WindowsPath]]):
    moved_files = 0
    download_dir = os.path.join("C:\\Users", os.getlogin(), "Downloads")
    for category in sorted_files:
        try:
            os.mkdir(os.path.join(download_dir, category))
        except FileExistsError:
            pass

        files_to_move = sorted_files[category].copy()

        for file in files_to_move:
            print(
                f"Moved: '{file.name}' to '{os.path.join(download_dir, category, file.name)}'"
            )
            file.rename(os.path.join(download_dir, category, file.name))
            moved_files += 1
    print(f"Moved {moved_files} files to their approrpiate folders!")


if __name__ == "__main__":
    argv = sys.argv.copy()

    directory = "."
    if len(argv) > 1:
        directory = argv[1]
    directory = str(pathlib.Path(directory).absolute())
    filemap = get_all_files(directory)
    sorted_files = sort_categories(filemap)

    move_files(sorted_files)
