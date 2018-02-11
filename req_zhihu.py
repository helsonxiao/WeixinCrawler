import json
import requests


class SimpleCrawler:
    init_url = "https://zhuanlan.zhihu.com/api/columns/floveluy/followers"
    offset = 0

    def crawl(self, params=None):
        headers = {
            "host": "zhuanlan.zhihu.com",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        }
        response = requests.get(self.init_url, headers=headers, params=params)
        print(response.url)
        data = response.json()

        while self.offset < 200:
            self.parse(data)
            self.offset += 20
            params = {"limit": 20, "offset": self.offset}
            self.crawl(params)

    @staticmethod
    def parse(data):
        with open("followers.json", "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item))
                f.write('\n')


SimpleCrawler().crawl()
