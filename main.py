from fastapi import FastAPI

from db.db_define import POOL
from db_opt.process_report import report_message
from db_opt.process_report import report_notice
from mylog.log_define import get_logger

logger = get_logger("server", "/server.log")

app = FastAPI()


@app.post("/collect_message")
def collect_message(msg: dict):
    post_type = msg.get("post_type")
    meta_event_type = msg.get("meta_event_type")
    if post_type != "meta_event":
        logger.info(msg)
    if post_type == "meta_event" and meta_event_type == "heartbeat":
        print("heartbeat ok")
    elif post_type == "message":
        report_message(pool=POOL, data=msg, logger=logger)
    elif post_type == "notice":
        report_notice(pool=POOL, data=msg, logger=logger)

    return {"code": 200}
