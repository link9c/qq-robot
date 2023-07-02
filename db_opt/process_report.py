from logging import Logger

from dbutils.pooled_db import PooledDB

from db_opt.process_group import update_group_users_info
from api.group import get_group_member_info


class Data:

    def __init__(self, data: dict):
        self.data = data

    def get_or_else(self, item, default):
        it = self.data.get(item)
        if it is None or it == "":
            it = default
        return it


def report_message(pool: PooledDB, data: dict, logger: Logger):
    data = Data(data)
    anonymous = data.get_or_else("anonymous", "")
    # font = data.get_or_else("font", 0)
    group_id = data.get_or_else("group_id", 0)
    message = data.get_or_else("message", "")
    message_id = data.get_or_else("message_id", 0)
    message_seq = data.get_or_else("message_seq", 0)
    message_type = data.get_or_else("message_type", "")
    raw_message = data.get_or_else("raw_message", "")
    self_id = data.get_or_else("self_id", 0)
    time = data.get_or_else("time", 0)
    user_id = data.get_or_else("user_id", 0)
    post_type = data.get_or_else("post_type", "")

    sql = f"""
            INSERT INTO "main"."message_master"
            ("anonymous", "group_id", "message", "message_id", "message_seq", "message_type", "raw_message",  
            "self_id", "time", "user_id", "post_type") 
            VALUES 
            ('{anonymous}', '{group_id}', '{message}', '{message_id}', '{message_seq}',  '{message_type}', 
            '{raw_message}', '{self_id}', '{time}', '{user_id}', '{post_type}');

                        """
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
        conn.commit()


def report_notice(pool: PooledDB, data: dict, logger: Logger):
    logger.info(f"save notice:{str(data)}")
    data = Data(data)
    group_id = data.get_or_else("group_id", 0)
    notice_type = data.get_or_else("notice_type", "")
    sub_type = data.get_or_else("sub_type", "")
    self_id = data.get_or_else("self_id", 0)
    time = data.get_or_else("time", 0)
    user_id = data.get_or_else("user_id", 0)
    operator_id = data.get_or_else("operator_id", 0)
    post_type = data.get_or_else("post_type", "")

    with pool.connection() as conn:
        with conn.cursor() as cur:
            # 储存notice信息
            sql = f"""
                       INSERT INTO "main"."message_master"
                       ("group_id", "notice_type", "sub_type", "self_id", "time", "user_id", "operator_id", "post_type") 
                       VALUES 
                       ('{group_id}', '{notice_type}', '{sub_type}', '{self_id}', '{time}', '{user_id}',  '{operator_id}', 
                       '{post_type}');

                                   """
            cur.execute(sql)
            # 更新群成员信息
            if notice_type == "group_decrease":
                logger.info("群成员减少")
                sql = f"""
                        UPDATE "main"."message_group_users" SET "status" = 0 WHERE 
                        "group_id" = {group_id} AND "user_id" = {user_id};
                        """
                cur.execute(sql)
            if notice_type == "group_increase":
                res = get_group_member_info(group_id, user_id)
                logger.info(f"群成员增加:{str(res)}")
                data = res["data"]
                update_group_users_info(pool=pool, data=data, logger=logger)
        conn.commit()
