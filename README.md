# News-collection-and-analysis-Subsystem
新闻采集分析子系统

#### 通过程序能从主要的新闻网站上爬取博物馆相关的新闻信息，进行加工处理。主要包括以下功能：
* 数据获取：爬取主要的新闻网站中的博物馆相关新闻（如百度新闻）。可以支持爬取指定时间范围内的新闻，如1年内的新闻，半年内的新闻等。
* 数据加工：对于爬取的信息进行过滤和加工，抽取需要的内容。例如，抽取新闻的发布时间、新闻的标题、新闻的内容、新闻涉及的博物馆等。
* 数据分析：对于加工好的新闻，分析是正面新闻还是负面信息。可采用已有的可直接调用的服务和代码实现。
* 数据定制服务：可以根据指定的某一家博物馆，获取该博物馆的指定时间的新闻，并进行加工分析，得到该博物馆指定时间内的主要新闻，正面新闻和负面新闻。
  
#### 项目结构
* 见MuseumNews/list.txt

#### 常用接口
##### 开启爬虫服务
    curl http://39.98.107.127:6800/schedule.json -d project=MuseumNews -d spider=autospd -d kword=[想爬取的特定博物馆名称] -d timee=[想获取新闻的特定时间范围]

##### 停止爬虫
    curl http://39.98.107.127:6800/cancel.json -d project=MuseumNews -d job=[job_id]

##### 列出爬虫
    curl http://39.98.107.127:6800/listspiders.json?project=MuseumNews

##### 列出job
    curl http://39.98.107.127:6800/listjobs.json?project=MuseumNews

##### 删除项目
    curl http://39.98.107.127:6800/delproject.json -d project=MuseumNews