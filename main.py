import os
import shutil
import argparse
from py_utils.src.av.probe import AVProp
from py_utils.src.av.av_common import (
    video_ext,
    pic_ext,
)
from py_utils.src.av.pic_opt import get_pic_time
from py_utils.src.fs.dir import (
    get_all_files,
    del_assign_file,
    del_empty_dir,
)


def get_video_time(vidopath):
    prop = AVProp(vidopath)
    return prop.get_create_time()


# 输出：返回视频或图片拍摄时间
def get_file_time(filename):
    ext = os.path.splitext(filename)[-1].lower()  # 文件后缀
    if ext in pic_ext:  # 图片文件
        return get_pic_time(filename)
    elif ext in video_ext:  # 视频文件
        return get_video_time(filename)
    else:
        print("do not support file type", ext, filename)
    return ""


def process_pic(src_dir, dst_dir):
    if src_dir == dst_dir:
        print("src == dst", src_dir, dst_dir)
        return
    os.makedirs(dst_dir, exist_ok=True)
    abs_filenames = get_all_files(src_dir)
    for abs_filename in abs_filenames:
        filename = os.path.basename(abs_filename)
        if len(filename) > 0 and filename[0] == ".":  # 跳过隐藏文件
            continue
        create_time = get_file_time(abs_filename)  # 获取目录下所有的照片列表
        if not create_time:
            print("not find time", abs_filename)
            continue
        if len(create_time) < 6:  # 20181207_031034
            print(f"create_time is not right, {create_time}, {abs_filename}")
            continue
        year = create_time[0:4]
        mounth = create_time[4:6]
        new_dir = os.path.join(dst_dir, year, mounth)
        os.makedirs(new_dir, exist_ok=True)
        dst_abs_filename = os.path.join(new_dir, filename)
        if not os.path.exists(dst_abs_filename):
            shutil.move(abs_filename, dst_abs_filename)
            print(f"mv {abs_filename} to {dst_abs_filename}")
        elif os.path.isfile(dst_abs_filename):
            if os.path.getsize(abs_filename) == os.path.getsize(dst_abs_filename):
                os.remove(abs_filename)
            else:
                print(f"file name same,but not same file {abs_filename}")
                dst_abs_filename = os.path.join(new_dir, "same_" + filename)
                shutil.move(abs_filename, dst_abs_filename)
                print(f"mv {abs_filename} to {dst_abs_filename}")
        else:
            print("same dir name is exist.")


# 测试执行
# python3 main.py "D:\\life\\srcDir" "D:\\life\\dstDir"
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str, help="src dir")  # 相册归档目录
    parser.add_argument("dst", type=str, help="dst dir")  # 无法获取照片或视频时间的归档目录

    # parser.add_argument("-l", "--limit", type=int, default=5000, help="db limit")
    args = parser.parse_args()
    print("args.src: ", args.src)
    print("args.dst: ", args.dst)
    # print("args.fun: ", args.limit)
    process_pic(args.src, args.dst)

    del_assign_file(args.src, ".DS_Store")
    del_empty_dir(args.src)
