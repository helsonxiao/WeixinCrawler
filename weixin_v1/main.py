# -*- coding: utf-8 -*-
import requests

url = "https://mp.weixin_v4.qq.com/mp/profile_ext?action=home&__biz=MjM5MzgyODQxMQ==&scene=124&"

raw_headers = """
    Host :
    mp.weixin_v4.qq.com
    Connection :
    keep-alive
    User-Agent :
    Mozilla/5.0 (Linux; Android 7.1.1; MIX 2 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043906 Mobile Safari/537.36 MicroMessenger/6.6.2.1240(0x26060236) NetType/WIFI Language/en
    x-wechat-key :
    7d1a1ab500ed546bb37361bc00230e4d0e88a693c0f6469ed2445c30c47742341bfca8e98aca288fdfda67b24283480f7bada809042c6805989d8301e1c6255c6c3b3391b6991f9854c5d3d252aa6cd8
    x-wechat-uin :
    MjEyNjQ5Mjgw
    Accept :
    text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8
    Accept-Encoding :
    gzip, deflate
    Accept-Language :
    en,en-US;q=0.8
    Cookie :
    rewardsn=; wxtokenkey=22abd5d4578ac7c48c7256ddd8d22b2d66c2f75e96eea44f722458a0f72f3a69; wxuin=212649280; devicetype=android-25; version=26060236; lang=en; pass_ticket=zwg3mpHIRGMIB2ooqPBPJiTf1MxyYlvZCnx8l/D4fFU=; wap_sid2=CMCKs2USXG00ZUhiajZKQXlrbEZKYUNrWWRveHJHNjZhbDlxVzk3RmZfOE1pWVlNLVdaUm53Qmw4X2ZIZ2pPdDJySnJhNzhhOHJGM3lZb2RJU1ZLOVVPbi1mZ2VLOERBQUF+MLL779MFOA1AlU4=
    Q-UA2 :
    QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.2&TBSVC=43603&CO=BK&COVC=043906&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= MIX2 &RL=1080*2030&OS=7.1.1&API=25
    Q-GUID :
    a9449cdb29fbafd377d7730913b788cb
    Q-Auth :
    31045b957cf33acf31e40be2f3e71c5217597676a9729f1b
    """


def transform_headers_to_dict(headers):
    headers = headers.replace(" :\n    ", ": ")
    headers = headers.split("\n    ")
    headers_dict = {}
    for h in headers:
        if h:
            key, value = h.split(": ", 1)
            headers_dict[key] = value

    return headers_dict


def extract_data(html_content):
    import re
    import html
    import json

    rex = "msgList = '({.*?})'"
    pattern = re.compile(pattern=rex, flags=re.S)
    match = pattern.search(html_content)
    if match:
        data = match.group(1)
        data = html.unescape(data)
        data = json.loads(data)
        articles = data.get("list")
        return articles


def crawl():
    headers = transform_headers_to_dict(raw_headers)
    response = requests.get(url, headers=headers, verify=False)
    try:
        # with open('./weixin_history.html', "w", encoding="utf-8") as f:
        #     f.write(response.text)

        data = extract_data(response.text)
        for item in data:
            print(item)
            print()
    except:
        print("err!")


if __name__ == '__main__':
    crawl()