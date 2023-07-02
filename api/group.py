import requests


def get_group_list() -> dict:
    url = "http://127.0.0.1:5700/get_group_list"
    json_body = {
        "no_cache": False
    }
    res = requests.post(data=json_body, url=url)
    res = res.json()
    return res


def get_group_member_list(group_id: int) -> dict:
    url = "http://127.0.0.1:5700/get_group_member_list"
    json_body = {
        "no_cache": False,
        "group_id": group_id,
    }
    res = requests.post(data=json_body, url=url)
    res = res.json()
    return res


def get_group_member_info(group_id: int, user_id: int) -> dict:
    url = "http://127.0.0.1:5700/get_group_member_info"
    json_body = {
        "no_cache": False,
        "group_id": group_id,
        "user_id": user_id
    }
    res = requests.post(data=json_body, url=url)
    res = res.json()
    return res
