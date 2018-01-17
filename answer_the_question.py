# -*- coding: utf-8 -*-

# @Author  : Allen_Liang
# @Time    : 2018/1/14 15:38
import sys
from numpy import ma
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
from aip import AipOcr
import requests
import json
import time
from PIL import Image, ImageDraw
import os
import matplotlib.pyplot as plt
import webbrowser
import math
import random
import urlparse
# 命令行颜色包
from colorama import init, Fore
try:
    import config
    import screenshot
except Exception as ex:
    print(ex)
    print('请将配置脚本放在项目根目录中运行')
    exit(-1)

init()
cfg = config.open_brain_config()
print(cfg)

# 百度OCR_api定义常量
# 输入你的API信息
APP_ID = '10706210'
API_KEY = 'kh6kczBGNeE6zFDDFS6U6zC4'
SECRET_KEY = 'L8D6xMO5BkVlISKGaG2TP90vhM0yd1eV'
aipOcr = AipOcr(APP_ID, API_KEY, SECRET_KEY)


# 定义参数变量
options = {
    'detect_direction': 'true',
    'language_type': 'CHN_ENG',
}


def image_cut_chongding():
    img = Image.open("./screenshot.png")
    # 区域由一个4元组定义，表示为坐标是 (x0, y0, x1, x2)
    # 问题区域
    question = img.crop((50, 700, 1400, 2200))
    draw = ImageDraw.Draw(question)
    draw.rectangle((20, 360, 1330, 450), fill=(0, 0, 0))
    question.save('question.png')

# 西瓜视频割


def image_cut_xigua():
    img = Image.open("./screenshot.png")
    # 区域由一个4元组定义，表示为坐标是 (x0, y0, x1, x2)
    # 问题区域
    question = img.crop((38, 300, 1017, 624))
    question.save('question.png')
    # 选线区域
    choices = img.crop((38, 624, 1017, 1257))
    choices.save('choices.png')


# 芝士超人图片切割
def image_cut_zhishi():
    img = Image.open("./screenshot.png")
    # 区域由一个4元组定义，表示为坐标是 (x0, y0, x1, x2)
    # 问题区域
    question = img.crop((21, 285, 1056, 570))
    question.save('question.png')
    # 选线区域
    choices = img.crop((21, 578, 1063, 1172))
    choices.save('choices.png')


# 读取问题图片
def get_file_content(q_filePath):
    with open(q_filePath, 'rb') as fp:
        return fp.read()
# OCR识别问题文字


def question_words(q_filePath, options):
    # 调用通用文字识别接口
    result = aipOcr.basicGeneral(get_file_content(q_filePath), options)
    print(json.dumps(result).decode("unicode-escape"))
    q_Result_s = ''
    c_list = []
    words_result_num = result['words_result_num']
    for i in range(words_result_num):
        if words_result_num - i <= 4:
            c_list.append(result['words_result'][i]['words'])
            continue
        else:
            q_Result_s = q_Result_s + result['words_result'][i]['words']
    return q_Result_s, c_list

# 读取选项图片


def get_file_content(c_filePath):
    with open(c_filePath, 'rb') as fp:
        return fp.read()

# OCR识别问题文字


def choices_words(c_filePath, options):
    # 调用通用文字识别接口
    result = aipOcr.basicGeneral(get_file_content(c_filePath), options)
    print(json.dumps(result).decode("unicode-escape"))
    c_Result_s = ''
    words_list = []
    for word_s in result['words_result']:
        words_list.append(word_s['words'])
    return words_list

# 网页分析统计


def guess_answer(question, choices):
    # print('题目搜索结果包含选项词频计数')
    # 请求
    req = requests.get(url='http://www.baidu.com/s', params={'wd': question})
    content = req.text
    print('问题: %s' % question)
    max_ans = 0
    result_num = 0
    for i in range(len(choices)):
        ans_num = content.count(choices[i])
        if ans_num > max_ans:
            max_ans = ans_num
            result_num = i
        print('Research result, No: %s ,count: %s, choice: %s' %
              (i, ans_num, str(choices[i]).decode('string_escape')))
    print('The answer is : %s' %
          str(choices[result_num]).decode('string_escape'))
    return result_num


def game_fun(image_cut):
    screenshot.check_screenshot()
    while True:
        start = time.time()
        screenshot.pull_screenshot()
        # 截图参数
        image_cut()
        q_filePath = "question.png"
#        c_filePath = "choices.png"
        question, choices = question_words(q_filePath, options)
#        choices = choices_words(c_filePath, options)
        ans = guess_answer(question, choices)
        rush_ans(ans)
        end = time.time()
        print(Fore.YELLOW + '+++++++++++++++++++++++++++++++++++++++++' + Fore.RESET)
        print(Fore.GREEN + '+++' + '程序用时：' +
              str(end - start) + '秒' + '+++' + Fore.RESET)
        print(Fore.YELLOW + '+++++++++++++++++++++++++++++++++++++++++' + Fore.RESET)
        go = raw_input('输入回车继续运行,输入 n 回车结束运行:')
        if go == 'n':
            break


def set_button_position(ans):
    """
    按钮的位置
    """
    global swipe_x1, swipe_y1, swipe_x2, swipe_y2
    left = cfg[str(ans)]['x']
    top = cfg[str(ans)]['y']
    right = int(random.uniform(left - 50, left + 50))
    buttom = int(random.uniform(top - 10, top + 10))    # 随机防 ban
    swipe_x1, swipe_y1, swipe_x2, swipe_y2 = left, top, right, buttom


def rush_ans(ans):
    """
    抢答
    """
    set_button_position(ans)
    cmd = 'adb shell input swipe {x1} {y1} {x2} {y2} {duration}'.format(
        x1=swipe_x1,
        y1=swipe_y1,
        x2=swipe_x2,
        y2=swipe_y2,
        duration=int(random.uniform(150, 250))
    )
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    init()
    print('请输入你要运行的助手对应的数字，并按回车键运行')
    print('头脑王者：1')
    print('西瓜视频：2')
    print('芝士超人：3')

    print("There is '1'")
    game_fun(image_cut_chongding)
    go_to = input('请输入你要运行的助手对应的数字，并按回车键运行: ')
    print("您输入了：%s" % go_to)
    if go_to == 1:
        print("There is '1'")
        game_fun(image_cut_chongding)
    elif go_to == 2:
        game_fun(image_cut_xigua)
    elif go_to == 3:
        game_fun(image_cut_zhishi)
