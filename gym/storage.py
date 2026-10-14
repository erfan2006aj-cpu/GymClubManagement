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