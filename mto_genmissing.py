#iterator is number of seconds it goes back from the original
#epochTime, it goes back numTimes
from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np
import time
import json
import sys

#findMissingData(1441065600,20, 1000, 'loopdetector', 'QEWDN0060DNS')
def findMissingDataGenIndex(epochTime, iterator, numTimes, INDEX, contractID):
        es=Elasticsearch()
        lane1=[];
        lane2=[];
        count = 0;
        epochTimeI = epochTime;
        while count < numTimes:
                query={
                "query": {
                "bool": {
                        "must": [
                                                { "match": { "timestamp":  str(epochTimeI) }},
                                                { "match": { "contractId": contractID   }}
                                        ]
                                }
                                }
                        }
                res = es.search(index=INDEX, body=query);
                if not res['hits']['hits']:
                        print "List is empty"
                        lane1.append(None);
                        lane2.append(None);
                else:
                        print res['hits']['hits'][0]['_source']['laneData']
                        lane1.append(res['hits']['hits'][0]['_source']['laneData'][0]['laneVol']);
                        lane2.append(res['hits']['hits'][0]['_source']['laneData'][1]['laneVol']);
                epochTimeI = epochTimeI - iterator;
                count=count+1;
        #print the original lane volumes (20 second interval gap between each element) plus missing data
        print lane1;
        print lane2;
        numpy.set_printoptions(threshold='nan')
        #print the original lane volumes plus predict data
        genlane1 = pd.Series(lane1).interpolate(method='linear').tolist();
        genlane2 = pd.Series(lane2).interpolate(method='linear').tolist();
        print genlane1;
        print genlane2;
        query={
        "query": {
                "bool": {
                "must": [
                                { "match": { "timestamp":  str(epochTime) }},
                                { "match": { "contractId": contractID }}
                        ]
                        }
                }
        }
        epochTimeJ = epochTime;
        res = es.search(index=INDEX, body=query);
        #what we use as a bases to input data into our new index
        #TODO: predict lane speed and occupancy
        template = res['hits']['hits'][0]['_source']
        count=0;
        while count < numTimes:
                template['timestamp']=epochTimeJ;
                template['laneData'][0]['laneVol']=str(genlane1[count])
                template['laneData'][1]['laneVol']=str(genlane2[count])
                print(count)
                template['vol'] = str(genlane1[count] + genlane2[count])
                es.index(index=INDEX + '_gen',body=template,doc_type='genrecord', id=epochTimeJ)
                epochTimeJ = epochTimeJ - iterator;
                count=count+1;

def printData(epochTime, iterator, numTimes, INDEX, contractID):
        es=Elasticsearch()
        count = 0;
        epochTimeI = epochTime;
        while count < numTimes:
                query={
                "query": {
                "bool": {
                        "must": [
                                                { "match": { "timestamp":  str(epochTimeI) }},
                                                { "match": { "contractId": contractID  }}
                                        ]
                                }
                                }
                        }
                res = es.search(index=INDEX, body=query);
                if not res['hits']['hits']:
                        print "List is empty"
                else:
                        print res['hits']['hits'][0]['_source']['laneData']
                epochTimeI = epochTimeI - iterator;
                count=count+1;

#awk -F '\\n' '{cnt=cnt+1} { printf "<option value=\"%d\">"$1"</option>\n", cnt}' listofstreets
#getDataFullNoContract(1441065600,20, 1000, 'loopdetector')
def getDataFullNoContract(epochTime, iterator, numTimes, INDEX):
        es=Elasticsearch()
        count = 0;
	ress = [];
        epochTimeI = epochTime;
        while count < numTimes:
                query={
                "query": {
                "bool": {
                        "must": [
                                                { "match": { "timestamp":  str(epochTimeI) }},
                                        ]
                                }
                                }
                        }
                res = es.search(index=INDEX, body=query);
                if not res['hits']['hits']:
                        #print "List is empty"
			ress.append(None);
                else:
                        #print res['hits']['hits'][0]['_source']
			ress.append(res['hits']['hits'][0]['_source']);
                epochTimeI = epochTimeI - iterator;
                count=count+1;
 	return ress;

#takes in a list of elasticsearch results(the one returned from getDataFullNoContract)
#outputs to stdout
#produces a list of loopdetectorname, contractid
def genLoopdetectorList(ress):
        for x in ress:
            if(x!=None):
                if(x['description'] != None and x['contractId'] != None):
                    print x['description'], ',', x['contractId'];


#takes in a filename that contains a sorted list of loopdetectorname,contractid
#and collapses the entries to loopdetecotrname,contractid1,contractid2, ..., contractidn
#outputs to stdout
#"400: Exit 25 S":["400DN0080DSS","400DN0070DSS"],
def collapseLoopdetectorList(filename):
     f = open(filename,'r');
     current = '_'
     list=[];
     for line in f:
         x = line.split(',');
         x[0] = x[0].replace("\n","");
         x[1] = x[1].replace("\n","");
         if(x[0].lower()==current.lower()):
             list.append(x[1]);
         else:
             sys.stdout.write(current);
             sys.stdout.write(',');
             for i,g in enumerate(list):
                 sys.stdout.write(g);
                 if((i+1)<len(list)):
                     sys.stdout.write(',');
             current = x[0];
             list = [];
             list.append(x[1]);
             sys.stdout.write('\n');

#like previous function but outputs python dictionary code
#"400: Exit 25 S":["400DN0080DSS","400DN0070DSS"],
def collapseListPythonDicOut(filename):
     f = open(filename,'r');
     current = '_'
     list=[];
     for line in f:
         x = line.split(',');
         x[0] = x[0].replace("\n","");
         x[1] = x[1].replace("\n","");
         if(x[0].lower()==current.lower()):
             list.append(x[1]);
         else:
             sys.stdout.write('"');
             sys.stdout.write(current);
             sys.stdout.write('":[');
             for i,g in enumerate(list):
                 sys.stdout.write('"');
                 sys.stdout.write(g);
                 sys.stdout.write('"');
                 if((i+1)<len(list)):
                     sys.stdout.write(',');
             current = x[0];
             list = [];
             list.append(x[1]);
             sys.stdout.write('],\n');


def printDataFull(epochTime, iterator, numTimes, INDEX, contractID):
        es=Elasticsearch()
        count = 0;
        epochTimeI = epochTime;
        while count < numTimes:
                query={
                "query": {
                "bool": {
                        "must": [
                                                { "match": { "timestamp":  str(epochTimeI) }},
                                                { "match": { "contractId": contractID   }}
                                        ]
                                }
                                }
                        }
                res = es.search(index=INDEX, body=query);
                if not res['hits']['hits']:
                        print "List is empty"
                else:
                        print res['hits']['hits'][0]['_source']
                epochTimeI = epochTimeI - iterator;
                count=count+1;


def findMissingData(epochTime, iterator, numTimes, INDEX, contractID):
        es=Elasticsearch()
        lane1=[];
        lane2=[];
        count = 0;
        epochTimeI = epochTime;
        while count < numTimes:
                query={
                "query": {
                "bool": {
                        "must": [
                                                { "match": { "timestamp":  str(epochTimeI) }},
                                                { "match": { "contractId": contractID   }}
                                        ]
                                }
                                }
                        }
                res = es.search(index=INDEX, body=query);
                if not res['hits']['hits']:
                        print "List is empty"
                        lane1.append(None);
                        lane2.append(None);
                else:
                        print res['hits']['hits'][0]['_source']['laneData']
                        lane1.append(res['hits']['hits'][0]['_source']['laneData'][0]['laneVol']);
                        lane2.append(res['hits']['hits'][0]['_source']['laneData'][1]['laneVol']);
                epochTimeI = epochTimeI - iterator;
                count=count+1;
        #print the original lane volumes (20 second interval gap between each element) plus missing data
        print lane1;
        print lane2;
        numpy.set_printoptions(threshold='nan')
        #print the original lane volumes plus predict data
        genlane1 = pd.Series(lane1).interpolate(method='linear').tolist();
        genlane2 = pd.Series(lane2).interpolate(method='linear').tolist();
        print genlane1;
        print genlane2;

#query4= { "query":{  "bool": { "must": [
#                                       {"match":{ "contractId": "QEWDN0060DNS" }},
#                                       { "range":{ "timestamp":{"lte":1441065600, "gte": 1441064600}}}
#                                       ] 
#        }         }          }
#query={
#"query": {
#"bool": {
#        "must": [
#                { "match": { "timestamp":  str(epochTimeI) }},
#                { "match": { "contractId": contractID   }}
#        ]
#         }
#        }
#}
#from mto_genmissing import genmissing_analytics
#genmissing_analytics(1441055600, 1441065600 , 'QEWDN0060DNS', 'loopdetector', 20);
def checkAnalyticsPossible(time1,time2, contractID, INDEX):
    if(time2<=time1):
        return 4
    es=Elasticsearch();
    query= { "query":{  "bool": { "must": [
                                       {"match":{ "contractId": contractID }},
                                       { "range":{ "timestamp":{"lte":time2, "gte": time1}}}
                                       ] 
        }         }          }
    res = es.search(index=INDEX, body=query, size=1000);
    total = res['hits']['total']
    print "total is ", total
    #for rec in res['hits']['hits']:
    #    if rec['_source'
    if (total < 1 ):
        return -1
    elif (total > 1000):
        return 1
    else:
        return 0

def genmissing_analytics(time1,time2, contractID, INDEX, delta):
    print (str(time1) + ' ' + str(time2) + ' ' + contractID + ' ' + INDEX + ' ' + str(delta)); 
    num_iterations=(time2-time1)/delta
    print 'numdays: ', num_iterations
    es=Elasticsearch()
    total=[];
    count = 0;
    epochTimeI = time1;
    emptyCount=0;
    while count < num_iterations:
        query={
        "query": {
        "bool": {
                "must": [
                        { "match": { "timestamp":  str(epochTimeI) }},
                        { "match": { "contractId": contractID   }}
                        ]
                 }
                }
              }
        res = es.search(index=INDEX, body=query);
        if not res['hits']['hits']:
            print "List is empty"
            total.append(None);
            emptyCount+=1;
        else:
            #TODO: consider all lanes
            if(len(res['hits']['hits'][0]['_source']['laneData']) > 1):
                total.append(res['hits']['hits'][0]['_source']['laneData'][0]['laneVol']+ res['hits']['hits'][0]['_source']['laneData'][1]['laneVol']);
            else:
                total.append(res['hits']['hits'][0]['_source']['laneData'][0]['laneVol'])
            #print res['hits']['hits'][0]['_source']['laneData'][0]['laneVol']+ res['hits']['hits'][0]['_source']['laneData'][1]['laneVol'];
        epochTimeI = epochTimeI + delta;
        count=count+1;
    #print the original lane volumes (20 second interval gap between each element) plus missing data

    noNones = [];
    for i in total:
        if (i!=None):
            noNones.append(i);
    print "empty count is ", emptyCount, " num_iterations is ", num_iterations
    if(num_iterations-emptyCount < num_iterations/20):
        print "miss rate is more than 95% for the given input";
        result = json.dumps({'error': "3", 'message': "miss rate is more than 95% for the given input" })
        print result
        return result

    maxOcc=max(noNones);
    print "the maximum occupancy is ", maxOcc
    if(maxOcc==0):
        result = json.dumps({'error': "2", 'message': "street is empty for the given time period" })
        print result
        return result

    print total;
    #print the original lane volumes plus predict data
    gentotal = pd.Series(total).interpolate(method='polynomial', order=3, limit_direction='both', limit=20).interpolate(method='linear').bfill().ffill().tolist(); 
    print gentotal; 

    firstreal=0;
    lastreal=len(total)-1;

    while (total[firstreal]==None):
        firstreal=firstreal+1;
    while (total[lastreal]==None):
        lastreal=lastreal-1;

    for data,data2 in zip(total,gentotal):
        print (data);
        print (data2);

    j=firstreal;
    i=firstreal+1;
    while(j<lastreal):
        while(total[i]==None and i < lastreal):
            i=i+1;

        print("we're from ", total[j], " to ",total[i]);
        x=j+1;
        avg = (total[i]+total[j])/2;
        y = x;
        div=1;
        while (y<i):
            if(gentotal[x]<min(total[i],total[j])):
                 if(min(total[i],total[j])-gentotal[x] > 5):
                     div=7;
            elif (gentotal[x]>max(total[i],total[j])):
                 if(gentotal[x]-max(total[i],total[j]) > 5):
                     div=7;
            y=y+1;
        while(x<i):
            print("gentotal[x] = ", gentotal[x]);
            if(gentotal[x]<min(total[i],total[j])):
                newdiff = (avg-gentotal[x])/3;
                newdiff = newdiff/div;
                gentotal[x]= min(total[i],total[j])-newdiff;
                print("new gentotal[x] = ", gentotal[x]);
                if(gentotal[x]<0):
                    gentotal[x]=0;
            elif (gentotal[x]>max(total[i],total[j])):
                newdiff = (gentotal[x]-avg)/3;
                newdiff = newdiff/div;
                gentotal[x]=max(total[i],total[j])+newdiff;
                print("new gentotal[x] = ", gentotal[x]);
            x=x+1;
        j=i; i=i+1;
        

    print ("first real = ", firstreal, "value = ", total[firstreal], "last real = ", lastreal, "value = ", total[lastreal]);

    x_axis_epoch= range(time1, time2, delta)
    x_axis_human=[]
    y_axis = zip(total, gentotal);


    for epoch in x_axis_epoch:
        x_axis_human.append(time.strftime("%b %d %Y %H:%M:%S", time.localtime(epoch)))

#    print "x_axis_human", x_axis_human[0]

    result = json.dumps([{'date': date, 'before': b, 'after': a } for date, b,a in zip(x_axis_human, total, gentotal)])
    print result
    return result
