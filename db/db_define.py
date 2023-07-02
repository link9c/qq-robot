import sqlite3
import os
from dbutils.pooled_db import PooledDB

db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "master.db")
print(f"数据库文件地址:{db_path}")
POOL = PooledDB(
    creator=sqlite3,  # 使用链接数据库的模块
    maxconnections=12,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建

    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错

    # ping=0,
    # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    # host='10.6.1.100',
    # port=1433,
    # user='datateam_developer',
    # password='MP-it226',
    database=db_path,
    check_same_thread=False
    # charset='utf8',

)
