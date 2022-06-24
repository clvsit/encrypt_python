from Cython.Build import cythonize
from setuptools import setup


def encrypt():
    with open("tmp_file.txt", "r", encoding="utf-8") as file:
        file_path_list = [line.replace("\n", "") for line in file.readlines()]

    setup(ext_modules=cythonize(file_path_list))


if __name__ == "__main__":
    encrypt()
