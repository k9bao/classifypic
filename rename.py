import argparse
from py_utils.src.fs.dir import rename_dir_files


# 测试执行
# python3 rename.py /Users/tianwenhui/Documents/pic_classify1
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str, help="src dir")  # 相册归档目录
    args = parser.parse_args()
    print("args.src: ", args.src)

    rename_dir_files(args.src)
