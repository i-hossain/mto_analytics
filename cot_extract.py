import json, requests
from elasticsearch import Elasticsearch

es=Elasticsearch()

prefix = 'http://portal.cvst.ca/api/0.1/loop_detector/latest/cot?timestamp='
initial_timestamp = 1459468800 #April 1 2016
final_timestamp = 1388534400 #Jan 1 2014
polling_rate = 20 #2 seconds
delta_timestamp = initial_timestamp - final_timestamp
# url_mto = 'http://portal.cvst.ca/api/0.1/loop_detector/latest/mto?timestamp=1441065600'
# url_cot = 'http://portal.cvst.ca/api/0.1/loop_detector/latest/cot?timestamp=1441065600'
# url_mto = prefix + str(timestamp)

head={"index":{"_index":"loopdetector","_type":"cot"}}
bulk_data=[]

timestamp=initial_timestamp


# create ES client, create index
ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'loopdetector'
TYPE_NAME = 'cot'

es=Elasticsearch(hosts=[ES_HOST])
'''
if es.indices.exists(INDEX_NAME):
    print("deleting '%s' index..." % (INDEX_NAME))
    res = es.indices.delete(index = INDEX_NAME)
    print(" response: '%s'" % (res))

# since we are running locally, use one shard and no replicas
request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}

print("creating '%s' index..." % (INDEX_NAME))
res = es.indices.create(index = INDEX_NAME, body = request_body)
print(" response: '%s'" % (res))
'''

curr_time=0
prev_time=0
j = 0
while timestamp >= final_timestamp:
    resp = requests.get(url=prefix + str(timestamp))
    data = json.loads(resp.content)
    if not data:
        j += 1
        continue
    curr_time = data[0]['timestamp']
    if curr_time == prev_time:
    	timestamp -= polling_rate
    	j += 1
    	continue

    for i in range(len(data)):
        bulk_data.append(head)
        bulk_data.append(data[i])


    # bulk index the data
    print("bulk indexing...")
    res = es.bulk(index = INDEX_NAME, body = bulk_data, refresh = True)

    #empty the bulk set
    bulk_data=[]

    #proceed to the next timestamp
    timestamp -= polling_rate

    j += 1

    print "Timestamp: ", timestamp
    print "Iteration number: ", j, ", Out of ", delta_timestamp/polling_rate
    print "Percentage done: ", (j/(delta_timestamp/polling_rate))*100
    print "-----------------------------"

    prev_time=curr_time
 
# sanity check
# res = es.search(index=INDEX_NAME, q='contractId:"403DN0030DWR"')
# print res
'''
bulk=[]

resp = requests.get(url=prefix + str(1440353840))
data = json.loads(resp.content)
for cot in data:
    bulk.append([cot['lat'],cot['longit'],cot['Id']])

text_file = open("Output.txt", "w")
for i in range(len(bulk)):
    text_file.write("%s, %s {%s}\n" %(bulk[i][0], bulk[i][1], bulk[i][2]))
text_file.close()
'''