from lib.util import log
from lib.util import dateutil

logger = log.get_logger("token.core")

def get_token(db, vers):
    list_token = db.token.aggregate([{'$match': {'type': vers}}, {'$sample': {'size': 1}}])
    token = [key for key in list_token]
    if token:
        token = token[0]
    else:
        logger.info("Token Not Found")
    return token

def list_token_ready(db_pool, vers):
    list_token = db_pool.token.aggregate(
        [{'$match': {'time_limit': {'$lte': int(dateutil.fifteen_minutes_ago_ts())}, 'type': vers}},
         {'$sample': {'size': 1}}])
    token = [key for key in list_token]
    if token:
        token = token[0]
    else:
        logger.info("Token Not Ready")
    return token

def update_token_time(db_pool, vers, id):
    db_pool.token.update_one({'_id': id}, {'$set': {'time_limit': int(dateutil.today_timestamp())}})