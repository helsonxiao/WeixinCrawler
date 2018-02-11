import html


def sub_dict(dict_data, eligible_keys):
    return {key: html.unescape(dict_data[key]) for key in dict_data if key in eligible_keys}


def generate_headers_dict(headers):
    """
    生成请求头字典
    输入格式如下
Host :
mp.weixin_v4.qq.com
Connection :
keep-alive
    """
    headers = headers.replace(" :\n", ": ")
    headers = headers.split("\n")
    d_headers = dict()
    for h in headers:
        if h:
            k, v = h.split(":", 1)
            d_headers[k] = v.strip()
    return d_headers


def generate_params_dict(s, join_symbol="\n", split_symbol=":"):
    """
    key与value通过split_symbol连接， key,value 对之间使用join_symbol连接
    例如： a=b&c=d   join_symbol是&, split_symbol是=
    :param s: 原字符串
    :param join_symbol: 连接符
    :param split_symbol: 分隔符
    :return: 字典
    """
    s_list = s.split(join_symbol)
    data = dict()
    for item in s_list:
        item = item.strip()
        if item:
            k, v = item.split(split_symbol, 1)
            data[k] = v.strip()
    return data
