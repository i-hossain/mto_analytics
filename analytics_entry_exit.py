import json, requests
from elasticsearch import Elasticsearch
import time
import pprint

time1 = 1440806400
time2 = 1441065600
delta_hour = 3600
delta_day = 86400
delta_week = delta_day*7
delta_month = delta_day*30

exit_name = ["401DE0200DWC","401DE0190DWC"]


def query(iterations, start_time, exit, delta):
	end_time = start_time + delta

	i = 0
	res=[]
	y_axis = []

	while i < iterations:
		query={
		   "query": {
		      "filtered": {
		         "query": {
		            "match": {
		               "contractId": exit
		            }
		         },
		         "filter": {
		            "range": {
		               "timestamp": {
		                  "gte": start_time,
		                  "lte": end_time
		               }
		            }
		         }
		      }
		   },
		   "aggs":{
		       # "avg_vol":{"avg":{"field":"vol"}},
		       "sum_vol":{"sum" : { "field" : "vol" } }
		   }
		}
		res = es.search(index=INDEX_NAME, body=query)
		y_axis.append(res['aggregations']['sum_vol']['value'])
		# print res['aggregations']['sum_vol']['value']

		start_time = end_time + 1
		end_time = start_time + delta
		i += 1

	return [res,y_axis]




def entry_exit_analytics(time1,time2, exit_name, delta):
    num_iterations=(time2-time1)/delta
    print 'numdays: ', num_iterations
    exit1 = exit_name[0] #"401DE0040DNF"
    exit2 = exit_name[1] #"404DN0010DNC"


    before = query(num_iterations, time1, exit1, delta)
    after = query(num_iterations, time1, exit2, delta)

    if before[0] or after[0]:
		#print res1[0]['aggregations']['sum_vol']['value']
		#print res2[0]['aggregations']['sum_vol']['value']
        print "not exception"
    else:
        print "exception"

    x_axis_epoch= range(time1, time2, delta)
	#print 'x_axis_epoch',x_axis_epoch
    x_axis_human=[]
    difference = [i[0] - i[1] for i in zip(before[1], after[1])]

	#write_data_to_file(x_axis_epoch, y_axis)
	#strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
	#'Thu, 28 Jun 2001 14:17:15 +0000'
    for epoch in x_axis_epoch:
        x_axis_human.append(time.strftime("%b %d %Y %H:%M:%S", time.localtime(epoch)))

    #print "Time", x_axis_human

    #print "Before exit:", before[1]
    #print "After exit:", after[1]
    #print "Volume Difference", difference

   

    result = json.dumps([{'date': date, 'before': before, 'after': after, 'difference': difference} for date, before, after, difference in zip(x_axis_human, before[1],after[1],difference)])
    #pprint.pprint(result)

    return result
'''
def exit_weekly(time1,time2, exit_name):
	num_weeks=(time2-time1)/delta_week
	print 'numweeks: ', num_weeks
	exit1 = exit_name[0]
	exit2 = exit_name[1]


	res1 = query(num_weeks, time1, exit1, delta_week)
	res2 = query(num_weeks, time1, exit2, delta_week)

	if res1[0] or res2[0]:
		print res1[0]['aggregations']['sum_vol']['value']
		print res2[0]['aggregations']['sum_vol']['value']

	else:
		print "exception"

	x_axis= range(time1, time2, delta_week)

	y_axis = [i[0] - i[1] for i in zip(res1[1], res2[1])]

	write_data_to_file(x_axis, y_axis)

	for epoch in x_axis:
		print time.strftime("%Y-%m-%d", time.localtime(epoch))

	json.dumps([{'date': date, 'value': value} for date, value in zip(x_axis, y_axis)])

def exit_monthly(time1,time2, exit_name):
	num_months=(time2-time1)/delta_month
	print 'numdays: ', num_months
	exit1 = exit_name[0]
	exit2 = exit_name[1]


	res1 = query(num_months, time1, exit1, delta_month)
	res2 = query(num_months, time1, exit2, delta_month)

	if res1[0] or res2[0]:
		print res1[0]['aggregations']['sum_vol']['value']
		print res2[0]['aggregations']['sum_vol']['value']

	else:
		print "exception"


	y_axis = [i[0] - i[1] for i in zip(res1[1], res2[1])]

	write_data_to_file(x_axis, y_axis)

	for epoch in x_axis:
		print time.strftime("%Y-%m-%d", time.localtime(epoch))

	json.dumps([{'date': date, 'value': value} for date, value in zip(x_axis, y_axis)])
'''

es=Elasticsearch()

ES_HOST = {"host" : "localhost", "port" : 9200}
INDEX_NAME = 'loopdetector'
TYPE_NAME = 'mto'

es=Elasticsearch(hosts=[ES_HOST])

#exit_analytics(time1, time2, exit_name, delta_day)


# query={
#    "query": {
#       "filtered": {
#          "query": {
#             "match": {
#                "contractId": "404DN0010DNC"  #401DE0040DNF
#             }
#          },
#          "filter": {
#             "range": {
#                "timestamp": {
#                   "gte": 1441059600,
#                   "lte": 1441065600
#                }
#             }
#          }
#       }
#    },
#    "aggs":{
#        "avg_vol":{"avg":{"field":"vol"}},
#        "sum_vol":{"sum" : { "field" : "vol" } }
#    }
# }
# res = es.search(index=INDEX_NAME, body=query)
# print res['aggregations']['sum_vol']['value']

