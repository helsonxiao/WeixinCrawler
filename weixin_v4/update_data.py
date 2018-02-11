import time

from crawler import WeiXinCrawler
from document import Post


if __name__ == '__main__':
    for post in Post.objects(reward_num=0):
        WeiXinCrawler.update_post(post)
        time.sleep(5)
