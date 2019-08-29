
## [企查查](http://www.qichacha.com)爬虫

根据区域抓取全部数据


```
docker-compose build
docker stack deploy -c docker-compose.yml qichacha-spider
```

kafka
```
./bin/kafka-topics.sh --create --zookeeper localhost:2181 --partitions 3 --replication-factor 1 --topic qichacha-start_urls
./bin/kafka-topics.sh --create --zookeeper localhost:2181 --partitions 3 --replication-factor 1 --topic qichacha-requests
./bin/kafka-console-producer.sh --broker-list localhost:9092 --topic demo-start_urls
>http://www.qichacha.com
```
