#WEB API
基于json通信
基于POST方法

##web api 签名验证(仅供测试)
1. appid: 10000
2. appsecret: c174cb1fda3491285be953998bb867a0

###签名方法
调用 API 时需要对请求参数进行签名验证，服务器会对该请求参数进行验证是否合法的。方法如下：
根据参数名称（除签名和图片文件）将所有请求参数按照字母先后顺序排序:key + value .... key + value
例如：将foo=1,bar=2,baz=3 排序为bar=2,baz=3,foo=1，参数名和参数值链接后，得到拼装字符串bar2baz3foo1

###系统暂时只支持MD5加密方式：
1. md5：将 appsecret 拼接到参数字符串头、尾进行md5加密，格式是：md5(appsecretkey1value1key2value2...appsecret)
2. 注：我们需要的是32位的字符串，字母全部小写（如果是md5出来的是大写字母，请转为小写），图片文件不用加入签名中测试。

###签名认证的测试连接：
####地址：http://api.doubi.so/taglist/
####参数：
<table>
<tbody>
<tr><td><em>Year</em></td><td><em>Temperature (low)</em></td><td><em>Temperature (high)</em></td></tr>
<tr><td>1900</td><td>-10</td><td>25</td></tr>
<tr><td>1910</td><td>-15</td><td>30</td></tr>
<tr><td>1920</td><td>-10</td><td>32</td></tr>
</tbody>
</table>
|| *参数名* || *必填* || *描述* || *默认值* ||
|| appid || yes || 应用ID || 您自己的appid ||
||sign_method || yes || 签名方式 || 目前支持md5 ||
|| sign || yes || 签名 || 加密后得到的签名 ||

#新闻WEB API
##参数列表：
    appid, sign, sign_method, tag，limit，page

##获取新闻接口，前三条为置顶新闻
###接口地址： http://api.doubi.so/news/
###参数说明：
    tag：分类，page: 第几页，limit:每页最多显示的条数
####分类列表:
    [
    //推荐
    '__all__',
    //热门
    'news_hot',
    //社会
    'news_society',
    //娱乐
    'news_entertainment',
    //科技
    'news_tech',
    //汽车
    'news_car',
    //时尚
    'news_fashion',
    ]
###举例：
    http://api.doubi.so/news/
    tag=__all__
    page=1
    limit=20
    appid:10000
    sign_method:md5
    sign=*****************************


##获取美女图片接口
###接口地址： http://api.doubi.so/newsgirlpic/
###参数说明：
####获取全部美女图片分类: tag为空
####获取分类下的没图片: tag可选参数如下
    [
    // 视觉大片
    'photograph_gallery',
    // 八卦
    'gossip',
    // 服饰搭配
    'style',
    // 美体瘦身
    'body',
    // 彩妆美发
    'beauty',
    ]
###举例:
    http://api.soubi.so/newsgirlpic/
    tag=gossip
    page=1
    limt=10
    appid:10000
    sign_method:md5
    sign=*****************************



#小说WEB API
##参数列表：
    一级分类： first （男／女）
    二级分类： second
    小说ID: novelid
    章节ID: chapterid
    应用ID：appid
    签名ID：sign
    签名方法：sign_method

##获取小说分类接口
###接口地址： http://api.doubi.so/taglist/
###参数说明:
    获取全部小说分类: first 为空 second 为空 
    举例： 
    http://api.doubi.so/taglist/
appid:10000
sign_method:md5
sign=*****************************
###返回字段： 
first  second  name(二级分类名称)

##获取某分类下的小说列表接口
###接口地址： http://api.doubi.so/novellist/ 
###参数说明:
    根据分类列表获取的first  second查询
    举例：
    http://api.doubi.so/
    first=1
    second=1
    appid:10000
    sign_method:md5
    sign=*****************************
###返回字段：title， novelid, author, picture, introduction

##获取小说简介接口
###接口地址： http://api.doubi.so/novelintroduction/
###参数说明：
    根据分类下的小说列表中返回的novelid获取小说简介
    举例： 
    http://api.doubi.so/
    novelid=1
    appid:10000
    sign_method:md5
    sign=*****************************
####返回字典： 
    title, novelid, author, picture, introduction

##获取小说的章节列表接口
###接口地址： 
    http://api.doubi.so/novelchapter/
###参数说明：
    根据某分类下的小说列表中返回的novelid字段获取相应小说章节列表
    举例：
    http://api.doubi.so/
    novelid=10
    appid:10000
    sign_method:md5
    sign=*****************************
###返回字段：
    \title(小说标题), subtitle(小说章节标题)， chapterid(章节id), novelid , author, picture, introduction

##获取章节内容接口
###接口地址： 
    http://api.doubi.so/novelcontent/
###参数说明：
    根据小说章节列表中返回的chapterid 获取章节内容
    举例： 
    http://api.doubi.so/
    chapterid=10
    appid:10000
    sign_method:md5
    sign=*****************************
###返回字段：
title(小说标题), subtitle(小说章节标题), novelid(小说ID), content(内容)

