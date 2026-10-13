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