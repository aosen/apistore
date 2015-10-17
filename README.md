#WEB API
1. 基于json通信
2. 基于POST方法

##web api 签名验证
###签名方法
调用 API 时需要对请求参数(除sign)进行签名验证，服务器会对该请求参数进行验证是否合法的。方法如下：
根据参数名称（除签名和图片文件）将所有请求参数按照字母先后顺序排序:key + value .... key + value
例如：将foo=1,bar=2,baz=3 排序为bar=2,baz=3,foo=1，参数名和参数值链接后，得到拼装字符串bar2baz3foo1

###系统暂时只支持MD5加密方式：
1. md5：将 appsecret 拼接到参数字符串头、尾进行md5加密，格式是：md5(appsecretkey1value1key2value2...appsecret)
2. 我们需要的是32位的字符串，字母全部小写（如果是md5出来的是大写字母，请转为小写），图片文件不用加入签名中测试。
3. 以下所有api均需要以下参数： appid， sign_method, sign

##新闻WEB API
###参数列表：
<table>
<tbody>
<tr><td><em>参数名</em></td><td><em>描述</em></td><td><em>默认值</em></td></tr>
<tr><td>appid</td><td>应用ID</td><td>您自己的appid</td></tr>
<tr><td>sign_method</td><td>签名方式</td><td>目前支持MD5</td></tr>
<tr><td>sign_method</td><td>签名方式</td><td>目前支持MD5</td></tr>
<tr><td>tag</td><td>分类</td><td>分类见下表</td></tr>
<tr><td>limit</td><td>每次请求的条数</td><td>10</td></tr>
<tr><td>page</td><td>页数</td><td>页数</td></tr>
</tbody>
</table>

###获取新闻接口
####接口地址： 
http://api.doubi.so/news/
####参数：
tag / limit / page
#####分类列表:
<table>
<tbody>
<tr><td><em>标签</em></td><td>推荐</td><td>热点</td><td>社会</td><td>娱乐</td><td>科技</td><td>汽车</td><td>时尚</td></tr>
<tr><td><em>字段</em></td><td>__all__</td><td>news_hot</td><td>news_society</td><td>news_entertainment</td><td>news_tech</td><td>news_car</td><td>news_fashion</td></tr>
</tbody>
</table>

###获取美女图片接口
####接口地址： 
http://api.doubi.so/newsgirlpic/
####参数：
tag / limit / page
#####获取全部美女图片分类: tag为空
#####获取分类下的图片: tag可选参数如下
<table>
<tbody>
<tr><td><em>标签</em></td><td>视觉大片</td><td>八卦</td><td>服饰搭配</td><td>美体瘦身</td><td>彩妆美发</td></tr>
<tr><td><em>字段</em></td><td>photograph_gallery</td><td>gossip</td><td>style</td><td>body</td><td>beauty</td></tr>
</tbody>
</table>

##小说WEB API
###参数列表：
<table>
<tbody>
<tr><td><em>参数名</em></td><td><em>描述</em></td><td><em>默认值</em></td></tr>
<tr><td>appid</td><td>应用ID</td><td>您自己的appid</td></tr>
<tr><td>sign_method</td><td>签名方式</td><td>目前支持MD5</td></tr>
<tr><td>sign_method</td><td>签名方式</td><td>目前支持MD5</td></tr>
<tr><td>first</td><td>一级分类 1：男 0：女</td><td>无</td></tr>
<tr><td>second</td><td>二级分类，按小说内容</td><td>无</td></tr>
<tr><td>novelid</td><td>小说ID</td><td>无</td></tr>
<tr><td>chapterid</td><td>章节ID</td><td>无</td></tr>
</tbody>
</table>
###获取小说分类接口
####接口地址： 
http://api.doubi.so/taglist/
####参数:
first / second
*注：如果获取全部分类目录 无需传first second
####返回字段： 
first  second  name(二级分类名称)

###获取某分类下的小说列表接口
####接口地址： 
http://api.doubi.so/novellist/ 
####参数:
first / second
####返回字段：
title， novelid, author, picture, introduction

###获取小说简介接口
####接口地址： 
http://api.doubi.so/novelintroduction/
####参数说明：
novelid
####返回字段： 
title, novelid, author, picture, introduction

###获取小说的章节列表接口
####接口地址： 
http://api.doubi.so/novelchapter/
####参数说明：
novelid
####返回字段：
title(小说标题), subtitle(小说章节标题)， chapterid(章节id), novelid , author, picture, introduction

###获取章节内容接口
####接口地址： 
http://api.doubi.so/novelcontent/
####参数：
chapterid
####返回字段：
title(小说标题), subtitle(小说章节标题), novelid(小说ID), content(内容)

###小说点击事件上传
####接口地址：
http://api.doubi.so/novelclick/
####接口描述：
上传用户小说点击数，用来记录小说总阅读数
####参数：
novelid
####返回字段：
novelid， novelpv(当前novelid的对应的小说阅读量)

###获取小说排名
####接口地址：
http://api.doubi.so/novelrank/
####接口描述：
获取小说热度排行榜
####参数：
page / limit
####返回字段：
novelid / title / novelpv / picture / author / first / second / rank(排名)
    
