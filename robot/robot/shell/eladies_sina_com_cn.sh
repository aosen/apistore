#! /bin/bash
cd /home/zhen/apistore/robot/robot
nohup scrapy crawl eladies_sina_com_cn >>/home/zhen/apistore/robot/robot/log/eladies_sina_com_cn.log&
