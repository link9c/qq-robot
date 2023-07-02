from logging import Logger

from dbutils.pooled_db import PooledDB


def update_group_info(pool: PooledDB, data: dict, logger: Logger):
    """
    获取群信息
    :param pool: 数据库连接池
    :param data: 数据字典 example: {'group_create_time': 0, 'group_id': 578469285, 'group_level': 0, 'group_name': '火纹大佬不鸽群', 'max_member_count': 2000, 'member_count': 1314}
    :param logger: 日志模块
    :return:
    """
    group_create_time: int = data.get("group_create_time", 0)
    group_id: int = data.get("group_id", 0)
    group_level: int = data.get("group_level", 0)
    group_name: str = data.get("group_name", "")
    max_member_count: int = data.get("max_member_count", 0)
    member_count: int = data.get("member_count", 0)
    group_memo: str = data.get("group_memo", "")
    # 判断存在则更新 否则新增
    with pool.connection() as conn:
        with conn.cursor() as cur:
            sql = f"""select group_id from "main"."message_groups" where "group_id" = '{group_id}' """
            cur.execute(sql)
            res = cur.fetchall()
            print(res)
            if res:
                logger.info(f"已存在:更新群->{group_name}:{group_id}")
                sql = f"""
                        UPDATE "main"."message_groups" 
                        SET "group_name" = '{group_name}', 
                        "group_memo" = '{group_memo}', 
                        "group_create_time" = {group_create_time}, 
                        "group_level" = {group_level}, 
                        "member_count" = {member_count}, 
                        "max_member_count" = {max_member_count} 
                        WHERE "group_id" = {group_id};

                    """
            else:
                logger.info(f"不存在:新增群->{group_name}:{group_id}")
                sql = f"""
                    INSERT INTO "main"."message_groups"
                    ("group_id", "group_name", "group_memo", "group_create_time", "group_level", "member_count", "max_member_count") 
                    VALUES 
                    ({group_id}, '{group_name}', '{group_memo}', {group_create_time}, {group_level}, {member_count}, 
                    '{max_member_count}');
                    """
            cur.execute(sql)
            conn.commit()


def update_group_users_info(pool: PooledDB, data: dict, logger: Logger):
    """
    获取群信息
    :param pool: 数据库连接池
    :param data: 数据字典 example: {'group_create_time': 0, 'group_id': 578469285, 'group_level': 0, 'group_name': '火纹大佬不鸽群', 'max_member_count': 2000, 'member_count': 1314}
    :param logger: 日志模块
    :return:
    """
    print(data)
    group_id: int = data.get("group_id", 0)
    user_id: int = data.get("user_id", 0)
    nickname: str = data.get("nickname", "")
    nickname = nickname.replace("'", "''")
    level: str = data.get("level", "")
    level = level.replace("'", "''")
    card: str = data.get("card", "")
    card = card.replace("'", "''")
    sex: str = data.get("sex", "")
    age: int = data.get("age", 0)
    area: str = data.get("area", "")
    join_time: int = data.get("join_time", 0)
    last_sent_time: int = data.get("last_sent_time", 0)
    role: str = data.get("role", "")
    card = card.replace("'", "''")
    unfriendly: int = int(data.get("unfriendly", 0))
    title: str = data.get("title", "")
    title = title.replace("'", "''")
    title_expire_time: int = data.get("title_expire_time", 0)
    card_changeable: int = int(data.get("card_changeable", 0))
    shut_up_timestamp: int = data.get("shut_up_timestamp", 0)

    # 判断存在则更新 否则新增
    with pool.connection() as conn:
        with conn.cursor() as cur:
            sql = f"""select user_id from "main"."message_group_users" where "group_id" = {group_id} and "user_id" = {user_id} """
            cur.execute(sql)
            res = cur.fetchall()
            print(res)
            if res:
                logger.info(f"已存在人员:更新信息->{group_id}->{nickname}:{user_id}")
                sql = f"""
                        UPDATE "main"."message_group_users" 
                        SET  "nickname" = '{nickname}', 
                        "card" = '{card}', 
                        "sex" = '{sex}', 
                        "age" = '{age}', 
                        "area" = '{area}', 
                        "join_time" = '{join_time}', 
                        "last_sent_time" = '{last_sent_time}', 
                        "level" = '{level}', 
                        "role" = '{role}', 
                        "unfriendly" = '{unfriendly}', 
                        "title" = '{title}', 
                        "title_expire_time" = '{title_expire_time}', 
                        "card_changeable" = '{card_changeable}', 
                        "shut_up_timestamp" = '{shut_up_timestamp}',
                        "status" = 1
                        WHERE "group_id" = {group_id} and "user_id" = {user_id};


                    """
            else:
                logger.info(f"不存在人员:新增信息->{group_id}->{nickname}:{user_id}")
                sql = f"""
                    INSERT INTO "main"."message_group_users"
                    ("group_id", "user_id", "nickname", "card", "sex", "age", "area", "join_time", "last_sent_time", 
                    "level", "role", "unfriendly", "title", "title_expire_time", "card_changeable", "shut_up_timestamp",
                    "status") 
                    VALUES 
                    ('{group_id}', '{user_id}', '{nickname}', '{card}', '{sex}', '{age}', '{area}', '{join_time}', '{last_sent_time}', 
                    '{level}', '{role}', '{unfriendly}', '{title}', '{title_expire_time}', '{card_changeable}', '{shut_up_timestamp}',1);

                    """

            cur.execute(sql)
            conn.commit()
