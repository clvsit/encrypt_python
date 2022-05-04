import os
import re
import shutil
import time
from typing import List

from loguru import logger
import argparse


class Encryption:

    def __init__(self):
        pass

    @staticmethod
    def __traver_dirs(dir_path: str, filter_rule_list: List[str], is_recurrent: bool) -> None:
        """
        遍历目标目录，找出所有需要加密的 python 脚本，并将这些脚本的路径暂存到 tmp_file.txt 文件中
        :param dir_path:         str       目标目录
        :param filter_rule_list: List[str] 过滤规则列表
        :param is_recurrent:     bool      是否递归获取该目录下的所有 python 脚本文件
        :return: None
        """
        file_path_list = []
        compiler_list = [re.compile(r"{}".format(filter_rule)) for filter_rule in filter_rule_list]

        if is_recurrent:
            for path, dirs, file_list in os.walk(dir_path):
                for file_path in file_list:
                    is_filter = False

                    for compiler in compiler_list:
                        if compiler.search(file_path):
                            is_filter = True
                            break

                    if is_filter:
                        continue

                    file_path_list.append(os.path.join(path, file_path))
        else:
            for file_path in os.listdir(dir_path):
                file_path_list.append(os.path.join(dir_path, file_path))

        with open("tmp_file.txt", "w", encoding="utf-8") as file:
            file.writelines([line + "\n" for line in file_path_list])

    @staticmethod
    def __output(output_dir: str) -> None:
        """
        输出加密后的脚本文件
        :param output_dir: str 输出目录路径
        :return: None
        """
        if output_dir != "":
            path_split = output_dir.split("/")
            parent_dir_path = "/".join(path_split[:-1])
            dir_name = path_split[-1]
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

            build_dir_path = "build"

            for path, dirs, file_path in os.walk("build"):

                for _dir in dirs:
                    if "temp.linux-x86_64" in path:
                        continue

                    logger.info(_dir)
                    if _dir == dir_name:
                        build_dir_path = os.path.join(path, _dir)

            logger.info("mv {}/ {}".format(build_dir_path, parent_dir_path))
            os.system("mv {}/ {}".format(build_dir_path, parent_dir_path))

    @staticmethod
    def __clean_(dir_path: str, mode: str) -> None:
        """
        就地清理加密过程中产生的一些第三方文件
        :param dir_path: str 目标目录
        :param mode:     str 清理模式
        :return: None
        """
        if mode == "build":
            if os.path.exists("build"):
                shutil.rmtree("build")
        else:
            os.system("rm tmp_file.txt")

            for path, dirs, file_list in os.walk(dir_path):
                for file_path in file_list:
                    if file_path.endswith(".c"):
                        logger.info("rm {}".format(os.path.join(path, file_path)))
                        os.system("rm {}".format(os.path.join(path, file_path)))

    def run(self, dir_path: str, filter_rule: str, output_dir: str, is_replace: bool, is_recurrent: bool):
        if type(dir_path) == str:
            if dir_path == "":
                raise AttributeError("The param dir_path must be specified!")
            if not os.path.isabs(dir_path):
                dir_path = os.path.join(os.getcwd(), dir_path)
            if not os.path.exists(dir_path):
                raise AttributeError(f"The {dir_path} corresponding to the parameter dir_path does not exist!")
        else:
            raise AttributeError(f"The param dir_path's type should be str not {type(dir_path)}")

        if type(filter_rule) == str:
            if os.path.isfile(filter_rule):
                filter_path = filter_rule if os.path.isabs(filter_rule) else os.path.join(os.getcwd(), filter_rule)

                if os.path.exists(filter_path):
                    with open(filter_path, "r", encoding="utf-8") as file:
                        filter_rule_list = [line.replace("\n", "") for line in file.readlines()]
                else:
                    raise AttributeError(f"The {filter_path} corresponding to the parameter filter_rule does not exist!")
            else:
                filter_rule_list = [filter_rule]
        elif type(filter_rule) == list:
            filter_rule_list = filter_rule
        else:
            filter_rule_list = []

        self.__traver_dirs(dir_path, filter_rule_list, is_recurrent)
        os.system("python encrypt.py build_ext")
        self.__clean_(dir_path, "other")

        if is_replace:
            os.system("mv {} {}_{}".format(dir_path, dir_path, time.time()))
            self.__output(dir_path)
        else:
            self.__output(output_dir)

        self.__clean_(dir_path, "build")


def main():
    parser = argparse.ArgumentParser(description="Demo of encrypt")
    parser.add_argument("-d", "--dir", default="")
    parser.add_argument("-f", "--filter", default="")
    parser.add_argument("-o", "--output", default="")
    parser.add_argument("-p", "--is_replace", default=False)
    parser.add_argument("-r", "--is_recurrent", default=False)
    arg_dict = parser.parse_args()
    encryption = Encryption()
    encryption.run(
        dir_path=arg_dict.dir,
        filter_rule=arg_dict.filter,
        output_dir=arg_dict.output,
        is_replace=arg_dict.is_replace,
        is_recurrent=arg_dict.is_recurrent)
