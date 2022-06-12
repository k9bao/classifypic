import exifread


# 输入：文件名(filename)
# 输出：文件的拍摄时间:20181207_031034
# 失败: 空
def get_picture_time(fileabspath):
    timeFomrt = ""
    try:
        FIELD = "EXIF DateTimeOriginal"
        fd = open(fileabspath, "rb")
        # print(fileabspath)
        tags = exifread.process_file(fd)
        if FIELD in tags:
            time = str(tags[FIELD])  # 获取到的结果格式类似为：2018:12:07 03:10:34
            timeFomrt = time.replace(":", "").replace(
                " ", "_"
            )  # 获取结果格式类似为：20181207_031034
    except KeyError as e:
        print("error", fileabspath, e)
    finally:
        fd.close()

    # 显示图片所有的exif信息
    # print("showing res of getExif: \n")
    # print(tags)
    return timeFomrt


if __name__ == "__main__":
    time = get_picture_time("G:\\Life\\Photo\\QQ相册\\说说和日志相册\\2016-04-14.jpg")
    print(time + "456")
    time = get_picture_time("G:\\Life\\Photo\\QQ相册\\说说和日志相册\\2016-05-30.jpg")
    print(time + "123")
