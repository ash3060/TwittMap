from elasticsearch import Elasticsearch, RequestsHttpConnection
from elasticsearch.helpers import bulk
from requests_aws4auth import AWS4Auth
import json, Config, sys

reload(sys)
sys.setdefaultencoding('utf-8')

tweet_mapping = \
    {'properties':
        {
            'timestamp_ms': {'type': 'date'},
            'text': {'type': 'string'},
            'coordinates': {'type': 'geo_point'},
            'username': {'type': 'string'}
        }
    }

index = 't1'
type = 'tweet'
mapping = {type: tweet_mapping}
bulk_chunk_size = Config.es_bulk_chunk_size


def parseTweet(doc):
    tweet = {}
    tweet['coordinates'] = doc['coordinates']['coordinates']
    tweet['timestamp_ms'] = doc['timestamp_ms']
    tweet['text'] = doc['text'].decode('utf-8')
    tweet['username'] = doc['user']['name'].decode('utf-8')
    # tweet['mentions'] = re.findall(r'@\w*', doc['text'])
    return tweet


def create_index(es, index, mapping):
    es.indices.create(index, body={'mappings': mapping})


def addTweets(data):
    awsauth = AWS4Auth(Config.es_access_key, Config.es_access_secret, Config.es_region, Config.es_name)

    es = Elasticsearch(
        hosts=[{'host': Config.es_host, 'port': Config.es_port}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    if not es.indices.exists(index):
        create_index(es, index, mapping)

    docs = json.loads('[' + data + ']')
    counter = 0
    bulk_data = []
    list_size = len(docs)
    for doc in docs:
        tweet = parseTweet(doc)
        bulk_doc = {
            "_index": index,
            "_type": type,
            "_source": tweet
        }
        bulk_data.append(bulk_doc)
        counter += 1

        if counter % bulk_chunk_size == 0 or counter == list_size:
            print "ElasticSearch bulk index (index: {INDEX}, type: {TYPE})...".format(INDEX=index, TYPE=type)
            success, _ = bulk(es, bulk_data)
            print 'ElasticSearch indexed %d documents' % success
            bulk_data = []
