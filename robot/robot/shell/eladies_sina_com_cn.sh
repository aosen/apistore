#!/bin/bash
PATH=$PATH:/usr/local/bin
export PATH
cd /home/zhen/apistore/robot/robot/news
scrapy crawl eladies_sina_com_cn
