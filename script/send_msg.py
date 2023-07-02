import requests


def send_msg(message, target_id: int, message_type: str = "private"):
    """

    :param message:
    :param target_id: message_type为private时赋值user_id, group时值group_id
    :param message_type: private,group
    :return:
    """
    url = "http://127.0.0.1:5700/send_msg"
    json_body = {
        "message_type": message_type,
        "auto_escape": False,
        "message": message,

    }
    if message_type == "private":
        json_body["user_id"] = target_id
    else:
        json_body["group_id"] = target_id
    res = requests.post(data=json_body, url=url)
    res = res.json()
    print(res)


def send_news():
    url = "https://v2.alapi.cn/api/zaobao?token=Q5R4eLIaiAeyPPq3"
    res = requests.get(url=url)
    res = res.json()
    print(res)
    data = res["data"]
    date = data["date"]
    news = data["news"]
    news = "\n".join(news)
    msg = f"今日新闻{date}:\n{news}"
    print(msg)
    send_msg(message=msg, target_id=720679782, message_type="group")


if __name__ == '__main__':
    send_news()
