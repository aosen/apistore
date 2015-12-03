#aosencloud项目说明
为crossapp应用搭建统一服务，包括内容采集系统，运营后台，web api

#选型
##测试系统
ubuntu 12.04
##线上系统
CentOS release 6.7 (Final)
##web api 
由tornado做后端，版本为 4.2.0， 安装方法：
```bash
pip install tornado==4.2.0
```
nginx做前端
##运营后台
由django搭建，版本 1.8.4, 安装方法：
```bash
pip install django==1.8.4
```
##信息采集
使用scrapy，版本 1.0.3, 安装方法：
```bash
pip install scrapy==1.0.3
```
##orm torndb
```bash
pip install torndb==0.3
```
##memcached
```bash
yum install memcached
wget https://launchpad.net/libmemcached/1.0/1.0.16/+download/libmemcached-1.0.16.tar.gz
./configure
make
sudo make
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
pip install pylibmc
```
##其他依赖的软件包
```bash
pip install gevent
pip install Pillow
#每天定时将最新需要搜索的内容更新至redis
pip install redis
#从redis中进行搜索
pip install tornado-redis
yum install redis
pip install pandas
```

##Golang源码
###分词包
github.com/aosen/cut
###搜索包
github.com/aosen/search
###搜索服务器
github.com/aosen/searchserver

#技术关键点
##web api调用认证
##信息采集
1 动态载入代理IP from memcached
2 动态载入user-agent from settings
3 代理ip可用性检测脚本
##小说检索算法
参见Golang源码
