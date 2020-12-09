import os
from elasticsearch import Elasticsearch


def setup(conf):
    os.environ['ES_HOST'] = conf.get_string("es.host")
    os.environ['ES_PORT'] = conf.get_string("es.port")
    os.environ['ES_INDEX'] = conf.get_string("es.index")


def indexing(key, data):
    es = Elasticsearch([{'host': os.environ.get("ES_HOST"), 'port': int(os.environ.get("ES_PORT"))}])
    es.index(index=os.environ.get("ES_INDEX"), doc_type='_doc', id=key, body=data)
    return True
