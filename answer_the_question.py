# -*- coding: utf-8 -*-

# @Author  : Allen_Liang
# @Time    : 2018/1/14 15:38
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
from aip import AipOcr
import requests
import json
import time
from PIL import Image
import os
import matplotlib.pyplot as plt
import webbrowser
#import urllib.parse
import urlparse
# improt screenshot
# 命令行颜色包
from colorama import init, Fore
init()


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

# 利用adb从手机中获取屏幕事实截图，并pull到计算机上


def pull_screenshot():
  #  screenshot.pull_screenshot()
    os.system('adb shell screencap -p /sdcard/screenshot.png')
    os.system('adb pull /sdcard/screenshot.png .')

# 根据你的手机配置屏幕截图信息，我的测试手机是meizu_pro6s,配置如下
# 冲顶大会图片切割


def image_cut_chongding():
    img = Image.open("./screenshot.png")
    # 区域由一个4元组定义，表示为坐标是 (x0, y0, x1, x2)
    # 问题区域
    question = img.crop((50, 700, 1400, 1000))
    question.save('question.png')
    # 选线区域
    choices = img.crop((250, 1100, 1200, 2200))
    choices.save('choices.png')


# 西瓜视频图片切割
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
    print('There is question_words')
    result = aipOcr.basicGeneral(get_file_content(q_filePath), options)
    print('The result: %s' % result)
    print(json.dumps(result).decode("unicode-escape"))
    q_Result_s = ''
    words_list = []
    for word_s in result['words_result']:
        words_list.append(word_s['words'])
    q_Result_s = q_Result_s.join(words_list)
    # print(q_Result_s)
    return q_Result_s

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


def count_base(question, choices):
    # print('题目搜索结果包含选项词频计数')
    # 请求
    req = requests.get(url='http://www.baidu.com/s', params={'wd': question})
    content = req.text
    print('问题: %s' % question)
    for i in range(len(choices)):
      #  dic[i] = [choices[i], content.count(choices[i])]
        
        if content.count(choices[i]) > MaxAnswer
        
        print(dic[i])
    # for i in dic:
        #    print('%s: %s' % (i, dic[i]))
        #   print(i, str(dic[i]).decode("unicode-escape"))
        #print(i, dic.decode("unicode-escape"))
    return max(dic, key=dic.get)


def game_fun(image_cut):
    while True:
        start = time.time()
        print("Start time is: %s" % start)
#        pull_screenshot()
        # 截图参数
        image_cut()
        q_filePath = "question.png"
        c_filePath = "choices.png"
        question = question_words(q_filePath, options)
        choices = choices_words(c_filePath, options)
        count_base(question, choices)

        #webbrowser.open('https://baidu.com/s?wd=' + urllib.parse.quote(question))
        end = time.time()
        print(Fore.YELLOW + '+++++++++++++++++++++++++++++++++++++++++' + Fore.RESET)
        print(Fore.GREEN + '+++' + '程序用时：' +
              str(end - start) + '秒' + '+++' + Fore.RESET)
        #print('程序用时：' + str(end - start) + '秒')
        print(Fore.YELLOW + '++++++++++++++++++++++++++' + Fore.RESET)
        go = input(Fore.RED + '输入回车继续运行,输入 n 回车结束运行: ' + Fore.RESET)
        if go == 'n':
            break


if __name__ == '__main__':
    init()
    print('请输入你要运行的助手对应的数字，并按回车键运行')
    print('头脑王者：1')
    print('西瓜视频：2')
    print('芝士超人：3')
    go_to = input('请输入你要运行的助手对应的数字，并按回车键运行: ')
    print("您输入了：%s" % go_to)
    if go_to == 1:
        print("There is '1'")
        game_fun(image_cut_chongding)
    elif go_to == 2:
        game_fun(image_cut_xigua)
    elif go_to == 3:
        game_fun(image_cut_zhishi)
