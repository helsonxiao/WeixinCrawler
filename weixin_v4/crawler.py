# -*- coding: utf-8 -*-
import requests
import logging
import json
import html
import time
from datetime import datetime
from urllib.parse import urlsplit

import utils
from document import Post

logging.basicConfig(level=logging.INFO)
# log this module
logger = logging.getLogger(__name__)
requests.packages.urllib3.disable_warnings()


class WeiXinCrawler(object):
    def crawl(self, offset=0):
        url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5MzgyODQxMQ==&f=json" \
              "&offset={offset}" \
              "&count=10&is_ok=1&scene=124&uin=777&key=777&pass_ticket=AkMhAnsldKsfxzJkAnHCiESaQeJVYjmj0hP8tS9q25I%3D" \
              "&wxtoken=&appmsg_token=943_yK3mgvUptDGoMzQxcbODvDNiDwFt-IQqMR4mhw~~&x5=1" \
              "&f=json".format(offset=offset)

        # 使用前需更新
        headers = """
Host :
mp.weixin.qq.com
Connection :
keep-alive
User-Agent :
Mozilla/5.0 (Linux; Android 7.1.1; MIX 2 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043906 Mobile Safari/537.36 MicroMessenger/6.6.2.1240(0x26060236) NetType/WIFI Language/en
x-wechat-key :
f766f1cd6ee0ff272aaa9ca1de9643ab6a550a2418bf556db3359bb82336b6651661d32734bef2ceed0ab1eb339172a6499805acac52ca20b50eb48ff1d0b270077418e376f6557c75753730341336af
x-wechat-uin :
MjEyNjQ5Mjgw
Accept :
text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,image/wxpic,image/sharpp,image/apng,*/*;q=0.8
Accept-Encoding :
gzip, deflate
Accept-Language :
en,en-US;q=0.8
Cookie :
rewardsn=; wxtokenkey=464343167f4bf0fead5da274c8b1f7968f1a4f1901a6b8e86af44ad2085a9bed; wxuin=212649280; devicetype=android-25; version=26060236; lang=en; pass_ticket=AkMhAnsldKsfxzJkAnHCiESaQeJVYjmj0hP8tS9q25I=; wap_sid2=CMCKs2UScHBPWktxdGNPbVozc2xuT203aWd3RU9kdUs2MGtPajFFYnlnMnRWMVl5MkJrU1piWjFHZEpiQVczSmdiRXFGcENjYThhVWtUZzltNmkwdGNkcm9rVUF1Tmh2dkRFSTIwVnRKZERXZVcwRTUtdkF3QUEw+J720wU4DUCVTg==
Q-UA2 :
QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.2&TBSVC=43603&CO=BK&COVC=043906&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= MIX2 &RL=1080*2030&OS=7.1.1&API=25
Q-GUID :
a9449cdb29fbafd377d7730913b788cb
Q-Auth :
31045b957cf33acf31e40be2f3e71c5217597676a9729f1b
"""

        headers = utils.generate_headers_dict(headers)
        response = requests.get(url, headers=headers, verify=False)
        result = response.json()
        if result.get("ret") == 0:
            next_offset = result.get("next_offset")
            msg_list = result.get("general_msg_list")
            logger.info("抓取数据：next_offset=%s, data=%s" % (next_offset, msg_list))
            self.save(msg_list)
            has_next = result.get("can_msg_continue")
            if has_next == 1:
                next_offset = result.get("next_offset")
                print("\n5s 后抓取下一页(next_offset=%s)" % next_offset)
                time.sleep(5)
                self.crawl(next_offset)
        else:
            # 错误消息
            # {"ret":-3,"errmsg":"no session","cookie_count":1}
            logger.error("无法正确获取内容，请重新获取请求参数和请求头")
            exit()

    @staticmethod
    def _insert(item, p_date):
        keys = ('title', 'author', 'content_url', 'digest', 'cover', 'source_url')
        sub_data = utils.sub_dict(item, keys)
        post = Post(**sub_data)
        p_date = datetime.fromtimestamp(p_date)
        post['p_date'] = p_date
        logger.info('save %s' % post.title)
        try:
            post.save()
        except Exception as e:
            logger.error('fail to save %s' % post.to_json(), exc_info=True)

    @staticmethod
    def save(msg_list):
        msg_list = msg_list.replace("\/", "/")
        data = json.loads(msg_list)
        msg_list = data.get("list")
        for msg in msg_list:
            p_date = msg.get("comm_msg_info").get("datetime")
            msg_info = msg.get("app_msg_ext_info")  # 非图文消息没有此字段
            if msg_info:
                WeiXinCrawler._insert(msg_info, p_date)
                multi_msg_info = msg_info.get("multi_app_msg_item_list")  # 多图文推送，把第二条第三条也保存
                for msg_item in multi_msg_info:
                    WeiXinCrawler._insert(msg_item, p_date)
            else:
                logger.warning("此消息不是图文推送，data=%s" % json.dumps(msg.get("comm_msg_info")))

    @staticmethod
    def update_post(post):
        # appmsg_token 具有时效性
        data_url_params = {'__biz': 'MjM5MzgyODQxMQ==', 'appmsg_type': '9', 'mid': '2650367727',
                           'sn': '08ce54f6f36873e74c638421012bb495', 'idx': '1', 'scene': '0',
                           'title': '2017%E5%B9%B4%EF%BC%8C%E6%84%9F%E8%B0%A2%E4%BD%A0%E4%BB%AC%EF%BC%8C2018%E5%B9%B4%EF%BC%8C%E6%88%91%E4%BB%AC%E7%BB%A7%E7%BB%AD%E5%8A%AA%E5%8A%9B%E5%89%8D%E8%A1%8C',
                           'ct': '1514796292',
                           'abtest_cookie': 'AwABAAoADAANAAgAJIgeALuIHgDhiB4A/IgeAPqJHgANih4ATYoeAF6KHgAAAA==',
                           'devicetype': 'android-24',
                           'version': '/mmbizwap/zh_CN/htmledition/js/appmsg/index3a9713.js', 'f': 'json',
                           'r': '0.6452677228890584', 'is_need_ad': '1', 'comment_id': '1741225191',
                           'is_need_reward': '1', 'both_ad': '0', 'reward_uin_count': '24', 'msg_daily_idx': '1',
                           'is_original': '0', 'uin': '777', 'key': '777',
                           'pass_ticket': 'mXHYjLnkYux1rXx8BxNrZpgW4W%252ByLZxcuvpDWlxbBrjvJo3ECB%252BckDAsy%252FTJJK6P',
                           'wxtoken': '1805512665', 'clientversion': '26060133',
                           'appmsg_token': '943_lDTYE8ntCYyYLeGQ5ImwjrpABLhUt4nWqxgAayapdlwwqghAk6DXHxCuCE0~',
                           'x5': '1'}

        # 使用前需更新
        headers = """
Host :
mp.weixin.qq.com
Connection :
keep-alive
Origin :
https://mp.weixin.qq.com
X-Requested-With :
XMLHttpRequest
User-Agent :
Mozilla/5.0 (Linux; Android 7.1.1; MIX 2 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043906 Mobile Safari/537.36 MicroMessenger/6.6.2.1240(0x26060236) NetType/WIFI Language/en
Content-Type :
application/x-www-form-urlencoded; charset=UTF-8
Accept :
*/*
Referer :
https://mp.weixin.qq.com/s?__biz=MjM5MjAwODM4MA==&mid=2650694172&idx=1&sn=3205466fdf86acb122192681a9d0e0f1&chksm=bea613cf89d19ad944279f6009fa2168f99feb2d140f696d53e0de4e2ac7143358e46fcce2e2&scene=0&ascene=7&devicetype=android-25&version=26060236&nettype=WIFI&abtest_cookie=AwABAAgACgAMAAgAnoYeAJaKHgCmih4A74oeAAGLHgA9ix4AU4seAGqLHgAAAA%3D%3D&lang=en&pass_ticket=AkMhAnsldKsfxzJkAnHCiESaQeJVYjmj0hP8tS9q25I%3D&wx_header=1
Accept-Encoding :
gzip, deflate
Accept-Language :
en,en-US;q=0.8
Cookie :
rewardsn=; wxtokenkey=601fa6073365a55cc0e9707f581740df2948cf01f8222cb62c9387a951735603; wxuin=212649280; devicetype=android-25; version=26060236; lang=en; pass_ticket=AkMhAnsldKsfxzJkAnHCiESaQeJVYjmj0hP8tS9q25I=; wap_sid2=CMCKs2UScHBPWktxdGNPbVozc2xuT203aWd3RUNwZHEzRVBhZFVReUdMX0cwRFdNQzhaaFNXVzAyWHN1ME1aOG51Z0ZhN3l0VVhjbjFiZFplLVdTWEMyMVIyZFp3aEJHOHlDaWdOYno4Q2ozUHRNQVZxdkF3QUEwg7X20wU4DUAB
Q-UA2 :
QV=3&PL=ADR&PR=WX&PP=com.tencent.mm&PPVN=6.6.2&TBSVC=43603&CO=BK&COVC=043906&PB=GE&VE=GA&DE=PHONE&CHID=0&LCID=9422&MO= MIX2 &RL=1080*2030&OS=7.1.1&API=25
Q-GUID :
a9449cdb29fbafd377d7730913b788cb
Q-Auth :
31045b957cf33acf31e40be2f3e71c5217597676a9729f1b
"""

        content_url = html.unescape(post.content_url)
        content_url_params = urlsplit(content_url).query
        content_url_params = utils.generate_params_dict(content_url_params, "&", "=")
        data_url_params.update(content_url_params)

        body = "is_only_read=1&req_id=09201q2NjaQXuSIHoO4NCJSL&pass_ticket=AkMhAnsldKsfxzJkAnHCiESaQeJVYjmj0hP8tS9q25I%25253D&is_temp_url=0"
        data = utils.generate_params_dict(body, "&", "=")
        headers = utils.generate_headers_dict(headers)
        data_url = "https://mp.weixin.qq.com/mp/getappmsgext"

        r = requests.post(data_url, data=data, verify=False, params=data_url_params, headers=headers)
        result = r.json()
        if result.get("appmsgstat"):
            post['read_num'] = result.get("appmsgstat").get("read_num")
            post['like_num'] = result.get("appmsgstat").get("like_num")
            post['reward_num'] = result.get("reward_total_count")
            post['u_date'] = datetime.now()
            logger.info("「%s」read_num: %s like_num: %s reward_num: %s" %
                        (post.title, post['read_num'], post['like_num'], post['reward_num']))
            post.save()
        else:
            logger.warning(r.status_code)
            logger.warning("没有获取的真实数据，请检查请求参数是否正确，返回的数据为：data=%s" % r.text)
            exit()
