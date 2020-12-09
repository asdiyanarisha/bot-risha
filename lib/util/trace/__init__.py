"""
Merupakan trace log untuk mempermudah melakukan tracing/debugging
pada history operasi yang dilakukan oleh system.
"""

import time
import dbutil


def log(clazz, message, keywords, data=None):
    """
    @param clazz log class.
    @param message log information message.
    @param keywords log keywords.
    @param data additional meta data to be included
        must be in pair str : str
    """
    if data is None:
        data = {}

    # validate data
    for k, v in data.items():
        if type(k) != str and type(v) != str:
            raise Exception("data pair type must be str : str")

    doc = {
        "clazz": clazz,
        "message": message,
        "keywords": keywords,
        "data": data,
        "ts": time.time()
    }

    dbutil.get_db().AQLQuery("INSERT @doc IN trace", bindVars={"doc": doc})


def get_list(offset, limit):
    db = dbutil.get_db()
    return db.AQLQuery("FOR a IN trace SORT a.createdTime, a._key DESC LIMIT @offset, @limit RETURN a",
                       bindVars={"offset": offset, "limit": limit}, rawResults=True)


