# !/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import jieba
from wordcloud import WordCloud, ImageColorGenerator

"""
《芳华》豆瓣短评词云
"""
# 获取当前文件路径
# __file__ 为当前文件, 在ide中运行此行会报错,可改为
# d = path.dirname('.')
d = path.dirname(__file__)

isCN = 1  # 默认启用中文分词
back_coloring_path = "img/heart.jpg"  # 设置背景图片路径
text_path = 'text/fanghua.txt'  # 设置要分析的文本路径
font_path = 'font/微软雅黑.ttf'  # 为matplotlib设置中文字体路径没
stopwords_path = 'stopword/sw_fanghua.txt'  # 停用词词表
img_color = "芳华byColor.png"  # 保存的图片名字1(只按照背景图片形状)
img_img = "芳华byImg.png"  # 保存的图片名字2(颜色按照背景图片颜色布局生成)

my_words_list = ['芳华', '冯小刚', '严歌苓', '黄轩', '苗苗', '钟楚曦', '杨采钰',
                 '李晓峰', '王天辰', '王可如', '隋源', '张仁博', '苏岩',
                 '张国立']  # 在结巴的词库中添加新词

back_coloring = imread(path.join(d, back_coloring_path))  # 设置背景图片

# 设置词云属性
wc = WordCloud(
    font_path=font_path,  # 设置字体
    background_color="white",  # 背景颜色
    max_words=2000,  # 词云显示的最大词数
    mask=back_coloring,  # 设置背景图片
    max_font_size=80,  # 字体最大值
    random_state=70,
    width=1000,
    height=860,
    margin=2,  # 设置图片默认的大小,但是如果使用背景图片的话,那么保存的图片大小将会按照其大小保存,margin为词语边缘距离
)


# 添加自己的词库分词
def add_word(list):
    for item in list:
        jieba.add_word(item)


add_word(my_words_list)

# 获取分析文本
text = open(path.join(d, text_path)).read()


# 去除停用词
def jiebaclearText(text):
    mywordlist = []
    seg_list = jieba.cut(text, cut_all=False)
    liststr = "/ ".join(seg_list)
    f_stop = open(path.join(d, stopwords_path))
    try:
        f_stop_text = f_stop.read()
    finally:
        f_stop.close()
    f_stop_seg_list = f_stop_text.split('\n')
    for myword in liststr.split('/'):
        if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
            mywordlist.append(myword)
    return ''.join(mywordlist)


if isCN:
    jieba.enable_parallel(4)  # 开启并行分词模式，参数为并行进程数
    text = jiebaclearText(text)
else:
    jieba.enable_parallel()  # 关闭并行分词

# 生成词云, 可以用generate输入全部文本(wordcloud对中文分词支持不好,建议启用中文分词),也可以我们计算好词频后使用generate_from_frequencies函数
wc.generate(text)
# wc.generate_from_frequencies(txt_freq)
# txt_freq例子为[('词a', 100),('词b', 90),('词c', 80)]

# 普通情况
plt.figure()
plt.imshow(wc)
plt.axis("off")
# plt.show()
wc.to_file(path.join(d, img_color))

# 图片生成的情况
image_colors = ImageColorGenerator(back_coloring)
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors))  # 根据图片颜色去渲染
plt.axis("off")
# plt.show()
wc.to_file(path.join(d, img_img))
