# API

### 可以通过以下接口远程控制部署在服务器上的爬虫项目

#### 开启爬虫服务
    curl http://39.98.107.127:6800/schedule.json -d project=MuseumNews -d spider=autospd -d kword=[想爬取的特定博物馆名称] -d timee=[想获取新闻的特定时间范围]

#### 停止爬虫
    curl http://39.98.107.127:6800/cancel.json -d project=MuseumNews -d job=[job_id]

#### 列出爬虫
    curl http://39.98.107.127:6800/listspiders.json?project=MuseumNews

#### 列出job
    curl http://39.98.107.127:6800/listjobs.json?project=MuseumNews

#### 删除项目
    curl http://39.98.107.127:6800/delproject.json -d project=MuseumNews