import subprocess
import traceback
import tempfile


# FFPROBE = "D:\\code\\Picmanger\\ffprobe"
FFPROBE = "ffprobe"


# 获取cmd的执行结果
def get_cmd_result(cmd):
    try:
        out_temp = tempfile.SpooledTemporaryFile()
        fileno = out_temp.fileno()
        obj = subprocess.Popen(cmd, stdout=fileno, stderr=fileno, shell=True)
        obj.wait()
        out_temp.seek(0)
        lines = out_temp.readlines()
        # print(lines)
    except Exception:
        print(traceback.format_exc())
    finally:
        if out_temp:
            out_temp.close()
    return lines


# 输入：文件名(filename)
# 输出：文件的拍摄时间:20181207_031034
# 失败: 空
def get_video_time(fileabspath):
    # cmd = 'ffprobe D:\\life\\Photo\\photo\\100APPLE\\AFJX7823.MP4'
    cmd = FFPROBE + " " + '"' + fileabspath + '"'  # 可以直接在命令行中执行的命令
    # p, f = os.path.split(fileabspath)
    cmdRet = get_cmd_result(cmd)
    time = ""
    for line in cmdRet:  # 按行遍历
        # creation_time   : 2018-09-08T03:50:42.000000Z
        line = line.decode(encoding="gbk").strip()  # 去除空格已经使用utf-8编码
        if line.find("creation_time") != -1:
            # [creation_time   : 2018-09-08T03:50:42,000000Z]
            ll = line.split(".")
            if len(ll) > 1:
                ret = ll[0].split(" ")  # [creation_time,:,2018-09-08T03:50:42]
                time = (
                    ret[-1].replace("-", "").replace("T", "_").replace(":", "")
                )  # 20180908_035042
                break
    return time


if __name__ == "__main__":
    time = get_video_time("C:\\Users\\guoxingbao\\Desktop\\IMG_2995.MOV")
    print(time)
