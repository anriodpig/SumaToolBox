# SumaTools - Rebuild 2021-08-09
# 更新日志：
# 2021-09-27 v3.1： 1.修复了菜单3中功能2不可用的问题@LiFang
# @LiFang           2.更新了metadata信息 改进了metadata合成方式
#                   3.新增别名MaBox，同时推出HyBox（换源Box）
#                   4.集成了TTplayer到Lib文件夹下
# @LiFang 2022-06-06: 开源到GitHub

"""
主要功能：
1.从 excel读取与参赛编号关联的歌词，从网易获取 lrc文件
2.将 lrc文件转换为 ass文件
3.调用 ffmpeg进行压制或者生成 ffmpeg的压制脚本
"""

import os
import json
import re
import time
import requests
import xlrd
from xlrd import XLRDError


# import tempfile
# from urllib import parse


def test():
    pass
    # xls_read("demo.xlsx")
    # xls_read("demo_old.xls")
    # convert_wyid_to_lrc("https://music.163.com/#/song?id=1346104315", "name1")
    # convert_wyid_to_lrc("1346104315", "name1")
    # convert_wyid_to_lrc(
    #     "分享YOASOBI的单曲《夜に駆ける (向夜晚奔去)》: https://y.music.163.com/m/song?id=1409311773&userid=000000000 (来自@网易云音乐)", "name")
    # convert_wyid_to_lrc("https://y.music.163.com/m/song?id=1409311773&userid=000000000", "name")


def main():
    # 检查FFmpeg状态
    if 'ffmpeg.exe' in os.listdir(path_lib):
        print("FFmpeg.exe 状态： 文件存在")
        os_shell_ffmpeg(" -version")
    else:
        print("警告：FFmpeg.exe文件缺失")
    print()

    a = os_count_file(path_res_ass, '.ass')
    print(f'字幕      文件夹内有 {a[0]} 个 ass 文件，总共 {a[1]} 个文件')
    a = os_count_file(path_res_lrc, '.lrc')
    print(f'歌词      文件夹内有 {a[0]} 个 lrc 文件，总共 {a[1]} 个文件')
    a = os_count_file(path_res_mp4, '.mp4')
    print(f'无字幕视频 文件夹内有 {a[0]} 个 mp4 文件，总共 {a[1]} 个文件')
    a = os_count_file(path_output, '.mp4')
    print(f'输出      文件夹内有 {a[0]} 个 mp4 文件，总共 {a[1]} 个文件')
    input("自检完成， 按Enter进入主菜单……")

    while True:
        menu_main()
        os_pause()

    # print('py_End')


def menu_main():
    os_cls()
    os_set_title("Suma工具箱3 - 主菜单")
    print("SumaToolBox_V3.0.0    主菜单")
    print("1.歌词功能")
    print("2.字幕功能")
    print("3.压制功能")
    print("4.设置")
    print("")

    a = input("请输入你的选择：")
    if a == '1':
        print("")
        menu_sub_1()
    elif a == '2':
        print("")
        menu_sub_2()
    elif a == '3':
        print("")
        menu_sub_3()
    elif a == '4':
        print('')
        menu_sub_4()
    else:
        print("")
        print("错误输入！")


def menu_sub_1():
    os_set_title("Suma工具箱3 - 歌词菜单")
    print("SumaToolBox_V3.0.0    1 - 歌词菜单")
    print("1.键盘输入网易云链接  获取LRC歌词  [单次]")
    print("2.从excel中导入网易云链接  批量获取LRC歌词")
    print("3.从download.json导入网易云链接  批量获取LRC歌词  [高级]")
    print("0.返回主菜单")
    a = input("请输入你的选择：")
    if a == '0':
        return
    elif a == '1':
        lrc_link = str(input("请粘贴网易云歌曲id或链接："))
        lrc_name = str(input("请为LRC文件命名（一般为投稿编号）："))
        convert_wyid_to_lrc(lrc_link, lrc_name)
        pass
    elif a == '2':
        xls_path = str(input("请输入xls的名称："))
        xls_content = xls_read(xls_path)
        for job in xls_content:
            # print(job)
            lrc_link = job[1]
            lrc_name = job[0]
            convert_wyid_to_lrc(lrc_link, lrc_name)
        pass
    elif a == '3':
        down_json_path = str(input("请输入json路径："))
        down_json_file = open(down_json_path, 'r', encoding='utf-8')
        down_json_info = json.load(down_json_file)
        for j in down_json_info:
            try:
                convert_wyid_to_lrc(j[0], j[1])
            except:
                print(f"下载失败-任务：{j}")
            time.sleep(0.5)
        pass
    else:
        return


def menu_sub_2():
    os_set_title("Suma工具箱3 - 字幕菜单")
    print("SumaToolBox_V3.0.0    2-字幕菜单")
    print("1.将LRC文件转为ASS  [单次]")
    print("2.将全部LRC转换为ASS  [会覆盖已存在的ASS文件]")
    print("3.从convert.json批量导入转换任务  [高级]")
    print("4.将suma文件转为ASS  [高级]")
    print("0.返回主菜单")
    a = input("请输入你的选择：")
    print("")
    if a == '0':
        return
    elif a == '1':
        lrc_name = str(input("请输入LRC文件的名称："))
        if not lrc_name.endswith('.lrc'):
            suma_name = lrc_name + '.suma'
            ass_name = lrc_name + '.ass'
            lrc_name = lrc_name + '.lrc'
        else:
            suma_name = lrc_name.replace('.lrc', '')
            suma_name = suma_name + '.suma'
            ass_name = lrc_name.replace('.lrc', '')
            ass_name = ass_name + '.ass'
        # 转换为路径
        lrc_path = path_res_lrc + lrc_name
        suma_path = path_res_suma + suma_name
        ass_path = path_res_ass + ass_name
        # 执行操作
        convert_lrc_to_suma(lrc_path, suma_path)
        convert_suma_to_ass(suma_path, ass_path)
        return
    elif a == '2':
        list_path_lrc = os.listdir(path_res_lrc)
        print(list_path_lrc)
        for lrc_name in list_path_lrc:
            lrc_path = path_res_lrc + lrc_name
            suma_name = lrc_name.replace('.lrc', '') + '.suma'
            ass_name = lrc_name.replace('.lrc', '') + '.ass'
            # 转换为路径
            suma_path = path_res_suma + suma_name
            ass_path = path_res_ass + ass_name
            # 执行操作
            convert_lrc_to_suma(lrc_path, suma_path)
            convert_suma_to_ass(suma_path, ass_path)
        return
        pass
    elif a == '3':
        print("Not Available")
        pass
    elif a == '4':
        print("Not Available")
        pass
    else:
        return


def convert_mp3_to_mp4(mp3_in_path, mp4_in_path, mp4_out_path):
    ffargs = []
    ffargs.append('-i "' + mp4_in_path + '"')
    ffargs.append('-i "' + mp3_in_path + '"')
    ffargs.append('-vcodec ' + 'copy')
    ffargs.append(
        '-metadata comment="'+ffmpeg_metadata+'"')
    ffargs.append(mp4_out_path)
    try:
        os_shell_ffmpeg(ffargs)
    except:
        pass


def convert_ass_to_mp4(ass_in_path, mp4_in_path, mp3_in_path, mp4_out_path):
    ffargs = []
    ffargs.append('-i "' + mp4_in_path + '"')
    if mp3_in_path == 0 or mp3_in_path == '0':
        pass
    else:
        ffargs.append('-i "' + mp3_in_path + '"')
    if ass_in_path[1] == ':':
        ass_in_path = ass_in_path.replace('\\', '\\\\')
        ass_in_path = ass_in_path.replace(':', '\\:')
    ffargs.append('-vf "ass = \'' + ass_in_path + '\'"')
    ffargs.append('-vcodec ' + os_get_accel())
    ffargs.append('-b:v 12000k')
    ffargs.append('-b:a 320k')
    ffargs.append(
        '-metadata comment="'+ffmpeg_metadata+'"')
    ffargs.append(mp4_out_path)
    try:
        os_shell_ffmpeg(ffargs)
    except:
        pass
    pass


def menu_sub_3():
    os_set_title("Suma工具箱3 - 压制菜单")
    print("SumaToolBox_V3.0.0    3-压制菜单")
    print("1.压制/换源单个视频  [单次]")
    print("2.压制所有匹配的对  [会覆盖已存在的ASS文件]")
    print("3.不压制仅换源（快速更换bgm）")
    print("4.从convert.json批量导入转换任务  [高级]")

    print("0.返回主菜单")
    a = input("请输入你的选择：")
    if a == '0':
        return
    elif a == '1':
        target_name = input("请输入目标名称（即字幕文件和无字幕视频相同的名称）：")
        ass_file = target_name + '.ass'
        mp4_file_in = target_name + '.mp4'
        mp4_file_out = target_name + "_OUT.mp4"
        ass_path = path_res_ass + ass_file
        mp4_path_in = path_res_mp4 + mp4_file_in
        mp4_path_out = path_output + mp4_file_out
        if (target_name + '.mp3') in os.listdir(path_res_mp3):
            print("检测到对应的MP3文件，要使用该音频吗？  是[Y]  否[N或任意内容]")
            choice = input("请输入选项：")
            if choice == 'Y' or choice == 'y':
                mp3_file = target_name + '.mp3'
                mp3_path = path_res_mp3 + mp3_file
                convert_ass_to_mp4(ass_path, mp4_path_in, mp3_path, mp4_path_out)
        else:
            convert_ass_to_mp4(ass_path, mp4_path_in, 0, mp4_path_out)
            pass
        pass
    elif a == '2':
        list_comp_ass = os.listdir(path_res_ass)
        for i in range(0,len(list_comp_ass)):
            list_comp_ass[i] = get_first_num(list_comp_ass[i])
        list_comp_mp4 = os.listdir(path_res_mp4)
        for i in range(0,len(list_comp_mp4)):
            list_comp_mp4[i] = get_first_num(list_comp_mp4[i])
        list_exec = []
        for i in list_comp_ass:
            if i in list_comp_mp4:
                list_exec.append(i)
        print(list_comp_ass)
        print(list_comp_mp4)
        print(list_exec)
        if len(list_exec) == 0:
            print('无文件!')
            os_pause()
            return
        for x in list_exec:
            ass_file = x + '.ass'
            mp4_file_in = x + '.mp4'
            mp4_file_out = x + "_OUT.mp4"
            ass_path = path_res_ass + ass_file
            mp4_path_in = path_res_mp4 + mp4_file_in
            mp4_path_out = path_output + mp4_file_out
            convert_ass_to_mp4(ass_path, mp4_path_in, 0, mp4_path_out)
        pass

    elif a == '3':
        target_name = input("请输入目标名称（即字幕文件和无字幕视频相同的名称）：")
        mp4_file_in = target_name + '.mp4'
        mp4_file_out = target_name + "_Hy.mp4"
        mp3_file = target_name + '.mp3'
        mp3_path = path_res_mp3 + mp3_file
        convert_mp3_to_mp4(mp3_path, mp4_file_in, mp4_file_out)
        pass
    else:
        return


def menu_sub_4():
    print("1.更改硬件加速选项")
    print("0.返回主菜单")
    a = input("请输入你的选择：")
    if a == '0':
        return
    elif a == '1':
        print("1.无硬件加速")
        print("2.intel:h264_qsv加速")
        print("3.nvidia:h264_nvenc加速")
        print("4.amd:h264_amf加速")
        print("0.不更改")
        print('')
        a = input("请输入你的选择：")
        if a == '0':
            return
        else:
            fp = open(cwd + '\\config\\hw_accel.conf', mode='w')
            fp.seek(0)
            if a == '1':
                fp.write('null')
            elif a == '2':
                fp.write('intel:h264_qsv')
            elif a == '3':
                fp.write('nvidia:h264_nvenc')
            elif a == '4':
                fp.write('amd:h264_amf')
            fp.close()
            exit(0)


def os_cls():
    os.system("cls")


def os_pause():
    os.system('pause')


def os_shell(args):
    # os.system('chcp 936')   #使用简体中文
    # os.system('chcp 437')   #使用英语（美国）
    ret = os.system(args)
    return ret


def os_set_title(text):
    if isinstance(text, str):
        os.system("title " + text)
    elif isinstance(text, int):
        os.system("title " + str(text))


def os_count_file(path, filetype):
    count_all = 0
    count_valid = 0
    ret = []
    cache = os.listdir(path)
    for i in cache:
        count_all = count_all + 1
        if i.endswith(filetype):
            count_valid = count_valid + 1
    ret.append(count_valid)
    ret.append(count_all)
    return ret


def os_shell_ffmpeg(args):
    if isinstance(args, str):
        os.system(exec_lib_ffmpeg + ' ' + args)
    elif isinstance(args, list):
        a = exec_lib_ffmpeg + ' '
        for i in args:
            a = a + i + ' '
        print(f"执行命令行：{a}吗?")
        # os_pause()
        os.system(a)
    else:
        print("Wrong Input Type !")


def os_get_accel():
    if hw_accel == 'null':
        return 'libx264'
    if hw_accel == 'intel:h264_qsv':
        return 'h264_qsv'
    if hw_accel == 'nvidia:h264_nvenc':
        return 'h264_nvenc'
    if hw_accel == 'amd:h264_amf':
        return 'h264_amf'

def get_first_num(string):
    a = re.findall(r"\d+", string)
    # print(a)
    if isinstance(a, str):
        return a
    elif isinstance(a, list):
        if a == []:
            return ""
        else:
            return str(a[0])


# ---- imported pyLib Start ----


lrc_web_headers = {'Referer': 'http://music.163.com/',
                   'Host': 'music.163.com',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8', }

ass_header = '''[Script Info]
Title: SumaToolBox v1 output file
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None
PlayResX: 1920
PlayResY: 1080

[SumaToolBox LRC2ASS converter]
Version: 3.0.1

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Constant,仓耳今楷01-27533 W05,46,&H0098999B,&H00FAF9F9,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,10,10,10,1
Style: Active,仓耳今楷01-27533 W05,46,&H00FAF9F9,&H0098999B,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,10,10,10,1


[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
'''


def convert_wyid_to_ass(netease_id, filename):  # 一键处理函数
    convert_wyid_to_lrc(netease_id, filename)
    convert_lrc_to_suma(filename, filename)
    convert_suma_to_ass(filename, filename)


def os_create_dir_safe(dirname):  # 安全创建文件夹
    try:
        os.listdir(dirname)
    except:
        os.mkdir(dirname)


def convert_wyid_to_lrc(netease_link, filename):
    # print(netease_link)
    wyid = ''
    if len(netease_link) == '':
        print("输入的链接有误")
    elif netease_link.isdigit():
        # print(int(netease_link))
        wyid = str(netease_link)
        pass
    elif netease_link.startswith("http"):
        if '&' in netease_link:
            a = netease_link.split('&')
            wyid = str((a[0].split('='))[-1])
        else:
            wyid = (netease_link.split('='))[-1]
    else:
        print("LRC下载失败：输入有误")
        return
    if len(filename) == 0:
        filename = wyid
        print(f"警告：文件名为空，使用网易歌曲id作为文件名：{wyid}")
    url = "http://music.163.com/api/song/lyric?os=pc&id=" + \
          str(wyid) + "&lv=-1&kv=-1&tv=-1"
    a = requests.get(url=url, headers=lrc_web_headers)
    lrc_raw = str(a.content, encoding='utf-8')
    lrc_json = json.loads(lrc_raw)
    lrc_content = lrc_json['lrc']['lyric']
    lrc_path = path_res_lrc + filename + '.lrc'
    fp = open(lrc_path, mode='w+', encoding='utf-8')
    fp.writelines(lrc_content)
    fp.close()
    print(f"LRC已保存为：{lrc_path}")
    time.sleep(0.5)
    # return lrc_content
    if flag_debug_lrc_show_content == 1:
        print(lrc_content)


def lrc_check_filename(str_to_check):
    str_to_check = str_to_check.rstrip("\n") + ".lrc"
    str_to_check = str_to_check.replace('\\', '')
    str_to_check = str_to_check.replace('/', '')
    str_to_check = str_to_check.replace(':', '')
    str_to_check = str_to_check.replace('*', '')
    str_to_check = str_to_check.replace('?', '')
    str_to_check = str_to_check.replace('"', '')
    str_to_check = str_to_check.replace('<', '')
    str_to_check = str_to_check.replace('>', '')
    str_to_check = str_to_check.replace('|', '')
    return str_to_check


# new:Style: Default,仓耳今楷01-27533 W05,46,&H00FAF9F9,&H0098999B,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,10,10,10,1
# old:Style: Default,仓耳今楷01-27533 W05,46,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,8,10,10,10,1
# TODO:  Dialogue: 0,timeStart{h:min:sec:msec},timeEnd{h:min:sec:msec},style,,0,0,0,,{\move(960,AzisBegin,960,AzisEnd)}
def ass_get_move_to(x, y, xE, yE):  # 生成位移动作标签
    x = str(x) + ','
    y = str(y) + ','
    xE = str(xE) + ','
    yE = str(yE)
    return "{\\move(" + x + y + xE + yE + ")}"


def ass_get_move_tag(x, y):  # 生成定位标签
    x = str(x) + ','
    y = str(y)
    return "{\\pos(" + x + y + ")}"


def ass_decode_to_ssa(stamp):  # 解码至SSA格式时间戳
    stamp = int(stamp)
    mi = int(stamp / (60 * 100))
    stamp = stamp - (60 * 100 * mi)
    s = int(stamp / 100)
    ms = stamp - (100 * s)
    q = ass_gen_ssa_style_time_stamp(0, mi, s, ms)
    return q


# Dialogue: 0, 0: 00:00.00, 0: 00:00.02, Default,, 0, 0, 0,, {\move(960.0, 540.0, 960.0, 495.0, )}作词:
def ass_get_line(content, tStart, tEnd, x, y, xE, yE):  # 生成单行ASS字幕
    if int(y) > 1080 + 90:
        return 0
    if int(y) < 0 - 90:
        return 0
    if int(yE) > 1080 + 90:
        return 0
    if int(yE) < 0 - 90:
        return 0

    a = "Dialogue: 0, "
    line = a + ass_decode_to_ssa(tStart) + ", " + \
           ass_decode_to_ssa(tEnd) + ", STYLEMARKER,, 0, 0, 0,, "
    line = line + ass_get_move_to(x, y, xE, yE)
    line = line.replace(' ', '')
    line = line + content + "\\N"
    return line


def ass_get_basic_line(content, tStart, tEnd, x, y):
    if int(y) > 1080 + 90:
        return 0
    if int(y) < 0 - 90:
        return 0

    a = "Dialogue: 0, "
    line = a + ass_decode_to_ssa(tStart) + ", " + \
           ass_decode_to_ssa(tEnd) + ", STYLEMARKER,, 0, 0, 0,, "
    line = line + ass_get_move_tag(x, y)
    line = line.replace(' ', '')
    line = line + content + "\\N"
    return line


def lrc_calc_offset(lineHeights, lyc, frame):
    lyc = int(lyc)
    frame = int(frame)
    lyc_offset = 0
    frame_offset = 0
    if lyc == 0:
        lyc_offset = 0
    else:
        for l in range(0, lyc):
            lyc_offset = lyc_offset + int(lineHeights[l])
    if frame == 0:
        frame_offset = 0
    else:
        for f in range(0, frame):
            frame_offset = frame_offset + int(lineHeights[f])
    return int(frame_offset - lyc_offset)
    # return int(lyc_offset - frame_offset)


def convert_suma_to_ass(suma_file_in, ass_file_out):
    # 容器初始化
    index = []
    timeS = []
    timeE = []
    content = []
    lineHeight = []
    fp = open(suma_file_in, mode='r', encoding='utf-8')
    a = fp.readlines()
    fp.close()
    for lines in a:
        if lines != '\n':
            l = lines.split('|')
            index.append(l[0])
            timeS.append(l[1])
            timeE.append(l[2])
            content.append(l[3])
            lineHeight.append(l[4])
    orginX = 1350
    orginY = 540
    fontSize = 45
    eLineSize = 20
    # clipBoarder = ["0,", "435,", "1920,", "900,"]  # x,y,x下,y下
    clipBoarder = ["0,", "435,", "1920,", "800,"]  # x,y,x下,y下
    clipText = "{\\clip(" + clipBoarder[0] + clipBoarder[1] + \
               clipBoarder[2] + clipBoarder[3] + ")}"
    newLineHeight = []
    for i in range(len(lineHeight)):
        if lineHeight[i] == '0':
            newLineHeight.append(fontSize)
        if lineHeight[i] == '1':
            newLineHeight.append(eLineSize)
    fp = open(ass_file_out, mode='w', encoding='utf-8')
    fp.writelines(ass_header)
    # 写入初始帧
    for lyc in range(len(index)):
        frame = 0
        y = orginY - int(lrc_calc_offset(newLineHeight, lyc, frame))
        cuContent = clipText + content[lyc]
        x = ass_get_line(cuContent, 0, timeS[frame], orginX, y + 45, orginX, y)
        # x = ass_get_basic_line(cuContent, 0, timeS[frame], orginX, y)
        if x != 0:
            x = x.replace("STYLEMARKER", "Constant")
            fp.write(x + '\n')
    # 写入结尾帧
    for lyc in range(len(index)):
        frame = len(index) - 1
        y = orginY - int(lrc_calc_offset(newLineHeight, lyc, frame))
        yE = y - int(newLineHeight[frame])
        cuContent = clipText + content[lyc]
        x = ass_get_line(cuContent, timeE[frame], int(
            timeE[frame]) + (30 * 100), orginX, yE, orginX, int(yE) - 360)
        # x = ass_get_basic_line(cuContent, timeE[frame], int(timeS[frame]) + 10000, orginX, yE)
        if x != 0:
            x = x.replace("STYLEMARKER", "Constant")
            fp.write(x + '\n')
    # 写入常规帧
    for lyc in range(len(index)):
        for frame in range(len(index)):
            y = orginY - int(lrc_calc_offset(newLineHeight, lyc, frame))
            yE = y - int(newLineHeight[frame])
            cuContent = clipText + content[lyc]
            if lyc == frame:
                cuContent = "{\\K" + \
                            str(int(timeE[frame]) -
                                int(timeS[frame]) + 0) + "}" + cuContent
            x = ass_get_line(cuContent, timeS[frame],
                             timeE[frame], orginX, y, orginX, yE)
            if x != 0:
                if lyc == frame:
                    x = x.replace("STYLEMARKER", "Active")
                else:
                    x = x.replace("STYLEMARKER", "Constant")
                fp.write(x + '\n')
    fp.close()
    print(f"ASS文件保存至：{ass_file_out}")


# 函数：生成 SSA 格式的时间戳
# 输入：str：|h|小时|；|m|分钟|；|s|秒 |；|ms|毫秒|；
# 返回：str：ASS用时间戳
def ass_gen_ssa_style_time_stamp(h, m, s, ms):
    a = ""
    a = str(h) + ":" + str(m) + ":" + str(s) + "." + str(ms)
    return a


# method:0,返回数组[min,sec,ms];1,返回类UNIX时间戳;2,返回SSA格式时间戳
def lrc_encode_stamp(stamp, method):
    if lrc_check_stamp(stamp) == 0:
        return -1
    else:
        a = stamp.split(':')
        mi = a[0].replace('[', '')
        a = a[1].split('.')
        s = a[0]
        ms = a[1].replace(']', '')
        ms = ms[0:2]
        mi = int(mi)
        s = int(s)
        ms = int(ms)
        if method == 0:
            q = []
            q.append(mi)
            q.append(s)
            q.append(ms)
            return q
        if method == 1:
            q = ms + (100 * s) + (60 * 100 * mi)
            return q
        if method == 2:
            q = ass_gen_ssa_style_time_stamp(0, mi, s, ms)
            return q


def lrc_get_stamps(line):
    f = re.findall("\[.*?]", line)
    return f


def lrc_get_lyrics(line):
    f = line.split(']')
    f = f[-1].lstrip()
    f = f.rstrip()
    f = f.replace('\n', '')
    return f


def lrc_check_stamp(stamp):
    a = stamp.split(':')
    a = a[0].replace('[', '')
    if a.isdigit() == 0:
        return 0  # invaild stamp
    else:
        return 1  # stamp available


def lrc_attach_index(list):
    q = []
    p = []
    for u in range(len(list)):
        q.append(u)
        q.extend(list[u])
        p.append(q)
        q = []
    return p


def lrc_calc_end_time(list):
    aa = []
    ab = []
    ac = []
    ad = []
    ae = []
    for u in list:
        aa.append(u[0])
        ab.append(u[1])
        ad.append(u[2])
    for u in range(len(list) - 1):
        ac.append(ab[u + 1])
    for u in range(len(list)):
        if ad[u] == "":
            ae.append(1)
        else:
            ae.append(0)
    ac.append(ab[len(list) - 1] + (100 * 5))
    b = []
    for u in range(len(list)):
        c = []
        c.append(aa[u])
        c.append(ab[u])
        c.append(ac[u])
        c.append(ad[u])
        c.append(ae[u])
        b.append(c)
    return b


def convert_lrc_to_suma(lrc_in_path, suma_out_path):
    # print(lrcInPath)
    try:
        fp = open(lrc_in_path, mode='r', encoding='utf-8')
        lrc = fp.readlines()
        fp.close()
    except:
        print(f"警告：LRC文件打开失败[{lrc_in_path}]")
        return -1
    list = []
    for lines in lrc:
        l = lrc_get_lyrics(lines)
        s = lrc_get_stamps(lines)
        a = []
        for c in s:
            a.append(c)
            a.append(l)
            if lrc_check_stamp(c) == 0:
                print("[警告] 无效行发现于：" + lrc_in_path)
            else:
                c = lrc_encode_stamp(c, 1)
                a[0] = c
                list.append(a)
            a = []
    list.sort()
    list = lrc_attach_index(list)
    list = lrc_calc_end_time(list)
    fp = open(suma_out_path, mode='w+', encoding='utf-8')
    for i in list:
        for x in i:
            fp.write(str(x))
            fp.write('|')
        fp.write('\n')
    fp.write('\n')
    fp.close()
    print(f"suma文件保存至：{suma_out_path}")


def xls_read(filename):
    try:
        wb = xlrd.open_workbook(filename)
    except XLRDError:
        print(f"EXCEL文件 {filename} 打开失败！请转换为XLS文件格式重试！")
        return
    head = []
    nums = []
    links = []
    table = wb.sheet_by_index(0)
    head_row = table.row(0)
    for i in head_row:
        head.append(i.value)
    # print(head)
    i = head.index("参赛编号")
    if i != -1:
        for x in table.col(i)[1:]:
            c = int(x.value)
            nums.append(str(c))
            if c == '':
                print("警告：在 参赛编号 数据中发现空的单元格")

    i = head.index("歌词链接")
    if i != -1:
        for x in table.col(i)[1:]:
            c = str(x.value)
            links.append(c)
            if c == '':
                print("警告：在 歌词链接 数据中发现空的单元格")

    ret = []
    for i in range(0, len(nums)):
        c = []
        if nums[i] == '':
            nums[i] = 0
        if links[i] == '':
            links[i] = 0
        c.append(nums[i])
        c.append(links[i])
        ret.append(c)
        # print(nums[i], links[i])
    # print(ret)
    return ret


# ----
if __name__ == '__main__':
    os_set_title("MaBox2022 - 初始化")
    cwd = os.getcwd()
    print(f'当前工作路径："{cwd}"')
    fp_conf_hw_accel = open(cwd + '\\config\\hw_accel.conf')
    hw_accel = fp_conf_hw_accel.readline()
    fp_conf_hw_accel.close()
    print(f"当前硬件加速配置为：{hw_accel}")
    path_lib = cwd + "\\lib\\"
    path_res_ass = cwd + "\\res\\ass\\"
    path_res_lrc = cwd + "\\res\\lrc\\"
    path_res_suma = cwd + "\\res\\suma\\"
    path_res_mp4 = cwd + "\\res\\mp4\\"
    path_res_mp3 = cwd + "\\res\\mp3\\"
    path_output = cwd + "\\output\\"

    exec_lib_ffmpeg = cwd + "\\lib\\ffmpeg.exe"

    flag_debug_lrc_show_content = 0

    ffmpeg_metadata = 'MaBox2022.OS_GH_0f18597,FFmpeg['+hw_accel+'],Copyright @SingUMA_Group'

    main()
    test()
