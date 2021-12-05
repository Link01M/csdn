# -*- coding: utf-8 -*-
# @Time    : 2021/11/22 21:18
# @Author  : LIN
# @Site    :
# @File    : CSDN动态爬取.py
# @Software: PyCharm
# @Comment :
import requests
from lxml import etree
from flask import Flask,jsonify
import re

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}
def login():
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'cookie': 'p_uid=U010000;UserName=m0_53123578;'
    }
    url3 = 'https://blog.csdn.net/nav/watchers/'
    resp = requests.get(url3, headers=header)
    text = resp.text
    list1 = text.split('\n')
    i = 0
    while i < 166:
        i = i + 1
        list1.pop()
    # print(list1)
    text = '\n'.join(list1)

    html = etree.HTML(resp.text)
    return html
    # result = etree.tostring(html)
    # print(html)
    # lis = html.xpath('//*[@id="dynamicList"]/*[@class="clearfix"]//*[@class="title"]//text()')
    # lis2 = html.xpath('//*[@id="dynamicList"]/*[@class="clearfix"]//*[@class="name"]//text()')
    # lis4 = html.xpath('//*[@id="dynamicList"]/*[@class="clearfix"]//*[@target="_blank"]/@href')
    #
    # lis1 = ''.join(lis)
    # lis3 = ''.join(lis2)
    #
    # print(lis3)
    # print(lis1)
    # print(lis4)

    # print(type(lis))
    # url_lis = []
    # lis2 = resp.xpath('//li[@class="hotsearch-item even"]//span[@class="title-content-title"]/text()')
    # for li in lis:
    #     url_lis.append(li.get())
    # for li in lis2:
    #     url_lis.append(li.get())
    # print(url_lis)



html = login()



@app.route('/attention_title')
def attention_tittle(username):

    lis = html.xpath('//*[@id="dynamicList"]/*[@class="clearfix"]//*[@class="title"]//text()')
    lis = [x.strip() for x in lis if x.strip() != '']
    diary = {"msg": "Success", "statu": 200}
    diary['titlelist'] = lis
    return jsonify(diary)


@app.route('/attention_man')
def attention_man():

    lis = html.xpath('//*[@id="dynamicList"]/*[@class="clearfix"]//*[@class="name"]//text()')
    lis = [x.strip() for x in lis if x.strip() != '']
    return jsonify(man=lis)


@app.route('/attention_content/<int:number>')
def attention_content(number):

    lis = html.xpath('//*[@id="dynamicList"]/*[@class="clearfix"]//*[@target="_blank"]/@href')
    listcontent = []
    for url in lis:
        text1 = requests.get(url, headers=header)
        text1 = text1.text
        result = 'ie10' in text1
        if result:
            listcontent.append(' ')
        else:
            content = re.compile(r'<article class="baidu_pl">(.*?)</article>', re.S)
            content_ans = re.search(content, text1).group(1)
            listcontent.append(content_ans)
    diary = {}
    diary['content'] = listcontent[number-1]
    diary['msg'] = 'success'
    diary['statu'] = 200


    return jsonify(content=diary)








if __name__ == '__main__':
    # login()
    app.run()