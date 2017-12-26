# !/usr/bin/env python
# -*- coding: utf-8 -*-

from wordcloud import WordCloud, get_single_color_func, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np


class SimpleGroupedColorFunc(object):

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color
                              for (color, words) in color_to_words.items()
                              for word in words}

        self.default_color = default_color

    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


class GroupedColorFunc(object):

    def __init__(self, color_to_words, default_color):
        self.color_func_to_words = [
            (get_single_color_func(color), set(words))
            for (color, words) in color_to_words.items()]

        self.default_color_func = get_single_color_func(default_color)

    def get_color_func(self, word):
        """Returns a single_color_func associated with the word"""
        try:
            color_func = next(
                color_func for (color_func, words) in self.color_func_to_words
                if word in words)
        except StopIteration:
            color_func = self.default_color_func

        return color_func

    def __call__(self, word, **kwargs):
        return self.get_color_func(word)(word, **kwargs)


# 图片颜色 爱丽丝
alice_coloring = np.array(Image.open("img/heart.jpg"))

# 自定义所有单词的颜色
color_to_words = {
    'red': ['China', 'Chinese', 'world', 'Republic', 'Beijing', 'Taiwan'],
}
# 默认的颜色
default_color = 'white'

# 颜色集
# grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)
# grouped_color_func = GroupedColorFunc(color_to_words, default_color)
grouped_color_func = ImageColorGenerator(alice_coloring)

# 设置停用词
stopwords = set(STOPWORDS)
stopwords.add("said")

# 云词的基本设置
wc = WordCloud(background_color="white",
               width=500,
               height=500,
               margin=2,
               mask=alice_coloring,
               random_state=40
               )

# 打开需要分析的文本文件
with open('text/test.txt', 'r') as f:
    wc.generate(f.read())
    wc.recolor(color_func=grouped_color_func)

    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()

    wc.to_file('cloud_cn.png')
