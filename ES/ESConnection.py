from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import Config


def getESConnection():
	awsauth = AWS4Auth(Config.es_access_key, Config.es_access_secret, Config.es_region, Config.es_name)
	es = Elasticsearch(
        hosts=[{'host': Config.es_host, 'port': Config.es_port}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
	)
	return es
