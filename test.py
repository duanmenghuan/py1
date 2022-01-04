import time
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import numpy as np
from PIL import Image

import jieba

url_lianjia = f'https://wannianli.tianqi.com/jieri/zhufuyu/3535.html'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
html = requests.get(url=url_lianjia, headers=headers)
html.encoding = "utf-8"
if html.status_code == 200:
    time.sleep(1)
    soup = BeautifulSoup(html.text, "html.parser")
    string = soup.find("div", class_='texts').text
    mask = np.array(Image.open("img.png"))

    # 数据清洗
    # 屏蔽45
    # STOPWORDS.add('45')
    stopwords = {}.fromkeys(['的','个','为','句子'])
    font = r'simhei.ttf'
    segs = jieba.cut(string,cut_all=False)
    final = ''
    for seg in segs:
        if seg not in stopwords:
            final += seg

    sep_list = jieba.lcut_for_search(final, )
    sep_list = " ".join(sep_list)
    wc = WordCloud(
        scale=4,  # 调整图片大小---（如果设置太小图会很模糊）
        font_path=font,  # 使用的字体库
        max_words=200,  # 词云显示的最大词数
        margin=2,  # 字体之间的间距
        mask=mask,  # 背景图片
        background_color='white',  # 背景颜色
        max_font_size=200,
        # min_font_size=1,
        # stopwords=STOPWORDS, #屏蔽的内容
        collocations=False,  # 避免重复单词
        width=1600, height=1200  # 图像宽高，字间距
    )

    wc.generate(sep_list)  # 制作词云
    wc.to_file('词云.jpg')  # 保存到当地文件

    # 图片展示
    plt.figure(dpi=100)  # 通过这里可以放大或缩小
    plt.imshow(wc, interpolation='catrom')
    plt.axis('off')
    plt.show()

else:
    print("请求失败")
