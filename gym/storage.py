<<<<<<< HEAD
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE_PATH = os.path.join(DATA_DIR, "gym_data.txt")


class Storage:
    def __init__(self, file_path=FILE_PATH):
        self.file_path = file_path

        directory = os.path.dirname(self.file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w") as file:
                pass

    def read_lines(self):
        with open(self.file_path, "r") as file:
            return file.readlines()

    def append_line(self, data):
        with open(self.file_path, "a") as file:
            file.write(data + "\n")
=======
from pathlib import Path

class Storage:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def exists(self) -> bool:
        return self.file_path.is_file()

    def read_lines(self) -> list[str]:
        if not self.exists():
            return []

        with self.file_path.open("r", encoding="utf-8") as file:
            return [line.rstrip("\r\n") for line in file]

    def append_line(self, line: str) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("a", encoding="utf-8") as file:
            file.write(line.rstrip("\r\n") + "\n")

    def write_lines(self, lines: list[str]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("w", encoding="utf-8") as file:
            for line in lines:
                file.write(line.rstrip("\r\n") + "\n")
>>>>>>> 1a218b5 (fix: resolve merge conflicts)
