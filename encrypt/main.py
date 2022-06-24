import argparse
import os
import re
import shutil
import time
from typing import List

from loguru import logger

CUR_DIR = os.path.dirname(os.path.abspath(__file__))


class Encryption:
    def __init__(self):
        pass

    @staticmethod
    def __traver_dirs(
        dir_path: str, filter_rule_list: List[str], recursive: bool
    ) -> None:
        """
        遍历目标目录，找出所有需要加密的 python 脚本，并将这些脚本的路径暂存到 tmp_file.txt 文件中
        :param dir_path:         str       目标目录
        :param filter_rule_list: List[str] 过滤规则列表
        :param recursive:     bool      是否递归获取该目录下的所有 python 脚本文件
        :return: None
        """
        file_path_list = []
        compiler_list = [
            re.compile(r"{}".format(filter_rule)) for filter_rule in filter_rule_list
        ]
        if recursive:
            for path, _, file_list in os.walk(dir_path):
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
                path = os.path.join(dir_path, file_path)
                # Only if it is a file
                if os.path.isfile(path):
                    file_path_list.append(path)

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
            build_dir_path = "build"

            for dirname in os.listdir(build_dir_path):
                if dirname.startswith("temp."):
                    continue
                build_dir = os.path.join(build_dir_path, dirname)
                for subdirname in os.listdir(build_dir):
                    subpath = os.path.join(build_dir, subdirname)
                    logger.info("mv {} {}".format(subpath, output_dir))
                    os.system("mv {} {}".format(subpath, output_dir))

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

            for path, _, file_list in os.walk(dir_path):
                for file_path in file_list:
                    if file_path.endswith(".c"):
                        logger.info("rm {}".format(os.path.join(path, file_path)))
                        os.system("rm {}".format(os.path.join(path, file_path)))

    def run(
        self,
        dir_path: str,
        filter_rule: str,
        output_dir: str,
        inplace: bool,
        recursive: bool,
    ):
        # Set directory path
        if type(dir_path) == str:
            if dir_path == "":
                raise AttributeError("The param dir_path must be specified!")
            if not os.path.isabs(dir_path):
                dir_path = os.path.join(os.getcwd(), dir_path)
            if not os.path.exists(dir_path):
                raise AttributeError(
                    f"The {dir_path} corresponding to the parameter dir_path does not exist!"
                )
        else:
            raise AttributeError(
                f"The param dir_path's type should be str not {type(dir_path)}"
            )

        # Set filter paths
        try:
            filter_rule = eval(filter_rule)
            logger.info("过滤规则格式转换成功！(str -> list)")
        except:
            pass

        if type(filter_rule) == str:
            if os.path.isfile(filter_rule):
                filter_path = (
                    filter_rule
                    if os.path.isabs(filter_rule)
                    else os.path.join(os.getcwd(), filter_rule)
                )

                if os.path.exists(filter_path):
                    with open(filter_path, "r", encoding="utf-8") as file:
                        filter_rule_list = [
                            line.replace("\n", "") for line in file.readlines()
                        ]
                else:
                    raise AttributeError(
                        f"The {filter_path} corresponding to the parameter filter_rule does not exist!"
                    )
            else:
                filter_rule_list = [filter_rule]
        elif type(filter_rule) == list:
            filter_rule_list = filter_rule
        else:
            filter_rule_list = []

        self.__traver_dirs(dir_path, filter_rule_list, recursive)

        logger.info(f"执行命令 --> python {CUR_DIR}/encrypt.py build_ext")
        os.system(f"python {CUR_DIR}/encrypt.py build_ext")
        self.__clean_(dir_path, "other")

        if inplace:
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
    parser.add_argument("-i", "--inplace", default=False, action="store_true")
    parser.add_argument("-r", "--recursive", default=False, action="store_true")
    arg_dict = parser.parse_args()
    encryption = Encryption()
    encryption.run(
        dir_path=arg_dict.dir,
        filter_rule=arg_dict.filter,
        output_dir=arg_dict.output,
        inplace=arg_dict.inplace,
        recursive=arg_dict.recursive,
    )
