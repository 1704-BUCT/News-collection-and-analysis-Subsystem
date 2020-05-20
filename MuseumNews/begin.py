from scrapy import cmdline

cmdline.execute(['scrapy', 'crawl', 'autospd',"-a","kword=博物馆","-a","timee=365"])