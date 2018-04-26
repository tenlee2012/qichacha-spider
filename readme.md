
## [企查查](http://www.qichacha.com)爬虫

根据区域抓取全部数据


```
docker-compose build
docker stack deploy -c docker-compose.yml qichacha-spider
```

redis 
```
select 2
lpush qichacha:start_urls 'http://www.qichacha.com'
```
