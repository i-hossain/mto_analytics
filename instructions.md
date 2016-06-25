#Intsall Elasticsearch

wget -qO - https://packages.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

echo "deb http://packages.elastic.co/elasticsearch/2.x/debian stable main" | sudo tee -a /etc/apt/sources.list.d/elasticsearch-2.x.list

sudo apt-get update

sudo apt-get -y install elasticsearch

sudo vi /etc/elasticsearch/elasticsearch.yml
#change:
#network.host: localhost
#cluster.name: loopdetector
#node.name: mto

sudo service elasticsearch restart


#run mto_extract.py to index elasticsearch. Current script will populate for 1 month (full august) with a difference of 1 minute between each timestamps
#you can change mto_extract.py configuration by changing delta_timestamp and polling_rate respectively


#run exit_analytics.py