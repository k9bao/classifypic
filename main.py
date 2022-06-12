import os
import shutil
import argparse
from process_video import get_video_time
from process_picture import get_picture_time


video_exts = [
    "vob",
    "ifo",
    "mpg",
    "mpeg",
    "dat",
    "mp4",
    "3gp",
    "mov",
    "rm",
    "ram",
    "rmvb",
    "wmv",
    "asf",
    "avi",
    "asx",
]
picture_exts = [
    "bmp",
    "jpg",
    "png",
    "tif",
    "gif",
    "pcx",
    "tga",
    "exif",
    "fpx",
    "svg",
    "psd",
    "cdr",
    "pcd",
    "dxf",
    "ufo",
    "eps",
    "ai",
    "raw",
    "WMF",
    "webp",
]


# 功能：遍历指定目录下所有的图片文件，返回图片及图片拍摄时间
# 输入：图片目录文件
# 输出：返回二个列表：文件，文件拍摄时间
def get_file_time(imgpath):
    olds = []
    news = []
    for filename in os.listdir(imgpath):  # 遍历目录下的所有照片或视频文件
        full_file_name = os.path.join(imgpath, filename)
        if os.path.isfile(full_file_name):  # 只处理文件，不处理目录
            time = "", ""
            ext = full_file_name.split(".")[-1].lower()  # 文件后缀
            if ext in picture_exts:  # 图片文件
                time = get_picture_time(full_file_name)
                print(full_file_name, ":", time)
                olds.append(filename)
                news.append(time)
            elif ext in video_exts:  # 视频文件
                time = get_video_time(full_file_name)
                print(full_file_name, ":", time)
                olds.append(filename)
                news.append(time)
            else:
                print("do not support file type")
    return olds, news


# 功能：创建指定目录，如果存在跳过，不存在则创建
# 输入：计划创建的目录
def create_dir(dir):
    ret = os.path.exists(dir)
    if not ret:
        os.makedirs(dir)
    else:
        pass


# 存放归档文件的所有目录，包含各级子目录
def get_all_dirs(dir):
    imgPaths = []  # 存放归档文件的所有目录，包含各级子目录
    imgPaths.append(srcDir)
    for parent, dirnames, filenames in os.walk(srcDir, followlinks=True):
        for dirname in dirnames:
            print("文件名：%s" % parent + "\\" + dirname)
            imgPaths.append(parent + "\\" + dirname)
    imgPaths.sort(reverse=True)
    return imgPaths


# 测试执行
# python3 "D:\\life\\srcDir" "D:\\life\\dstDir" ""D:\\life\\dstTmp"
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=str, help="src dir")  # 相册归档目录
    parser.add_argument("dst", type=str, help="dst dir")  # 无法获取照片或视频时间的归档目录
    parser.add_argument("tmp", type=str, help="other dir")  # 准备归档的目录，支持递归查找

    # parser.add_argument("-l", "--limit", type=int, default=5000, help="db limit")
    args = parser.parse_args()
    print("args.src: ", args.src)
    print("args.dst: ", args.dst)
    print("args.tmp: ", args.tmp)
    # print("args.fun: ", args.limit)

    srcDir = args.src
    dstDir = args.dst
    dstDirOther = args.tmp

    create_dir(dstDirOther)
    imgDirs = get_all_dirs(srcDir)
    for imgDir in imgDirs:
        if not os.path.isdir(imgDir):
            continue
        filelist, timelist = get_file_time(imgDir)  # 获取目录下所有的照片列表
        for index, fileName in enumerate(filelist):
            if timelist[index] == "":
                print("not find time", fileName)
                continue
            year = timelist[index][0:4]
            mounth = timelist[index][4:6]
            newImgDir = os.path.join(dstDir, year, mounth)
            create_dir(newImgDir)
            oldAbsFile = os.path.join(imgDir, fileName)
            dstAbsFile = os.path.join(newImgDir, timelist[index] + "_" + fileName)
            if imgDir == newImgDir:
                print("srcPath == dstPath")
                continue
            if not os.path.exists(dstAbsFile):
                shutil.move(oldAbsFile, dstAbsFile)
            elif os.path.isfile(dstAbsFile):
                if os.path.getsize(oldAbsFile) == os.path.getsize(dstAbsFile):
                    os.remove(oldAbsFile)
                else:
                    print("file name same,but not same file")
                    shutil.move(
                        oldAbsFile,
                        os.path.join(newImgDir, timelist[index] + "_same" + fileName),
                    )
            else:
                print("same dir name is exist.")
        if len(os.listdir(imgDir)) == 0:
            print(imgDirs, "dir is empty")
        else:
            print(imgDir, "is not exist\n")
