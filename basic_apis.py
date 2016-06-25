import json, requests
from elasticsearch import Elasticsearch
import time
from pprint import pprint

es=Elasticsearch()

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'loopdetector'
TYPE_NAME = 'mto'

es=Elasticsearch(hosts=[ES_HOST])


def apis(time1=None, time2=None, size=10):
	#print"entered API module"
	if not time2:
		query ={
			"query": {
			    "bool": {
			      "must": [
			        { "match": { "timestamp": time1 }}
			      ]
			    }
			  }
			}

	elif time2:
		query={
		    "query": {"filtered": {
		       "filter": {"range": {
		          "timestamp": {
		             "from": time1,
		             "to": time2
		          }
		       }}
	    	}}
			}

	res = es.search(index=INDEX_NAME, body=query, size=size)
	total_entries=res["hits"]["total"]

	result=[]
	for i in res["hits"]["hits"]:
		result.append(i["_source"])


	return json.dumps(result)
