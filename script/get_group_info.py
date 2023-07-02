import requests

from api.group import get_group_list, get_group_member_info
from api.group import get_group_member_list
from mylog.log_define import get_logger
from db.db_define import POOL
from db_opt.process_group import update_group_info
from db_opt.process_group import update_group_users_info

logger = get_logger("script", "/script_process.log")


def get_group_info(group_list: list):
    # url = "http://127.0.0.1:5700/get_group_info"
    # json_body = {
    #     "group_id": group_id,
    #     "no_cache": False
    # }
    # res = requests.post(data=json_body, url=url)
    # res = res.json()
    # logger.info(str(res))
    # data = res["data"]
    for data in group_list:
        update_group_info(pool=POOL, data=data, logger=logger)


def get_group_users_info(group_list: list):
    for group_id in group_list:
        res = get_group_member_list(group_id)
        logger.info(str(res))
        for data in res["data"]:
            update_group_users_info(pool=POOL, data=data, logger=logger)


def run_job():
    # 更新群列表
    group_list_origin = get_group_list()
    group_list = group_list_origin["data"]
    g_list = [r["group_id"] for r in group_list]
    get_group_info(group_list)
    get_group_users_info(g_list)


if __name__ == '__main__':
    run_job()
