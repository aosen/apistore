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

###api域名
    http://api.9miao.com

##状态码
<table>
<tbody>
<tr><td><em>err</em></td><td><em>errmsg</em></td><td><em>描述</em></td></tr>
<tr><td>200</td><td>成功</td><td></td></tr>
<tr><td>401</td><td>参数不正确</td><td></td></tr>
<tr><td>402</td><td>验证失败</td><td></td></tr>
<tr><td>403</td><td>缺少sign_method</td><td></td></tr>
<tr><td>404</td><td>缺少sign参数</td><td></td></tr>
<tr><td>405</td><td>非法用户</td><td></td></tr>
<tr><td>406</td><td>不存在</td><td></td></tr>
<tr><td>500</td><td>未知错误</td><td></td></tr>
<tr><td>601</td><td>用户名已经存在</td><td></td></tr>
</tbody>
</table>

##Json返回格式
```
{
"code" : "状态码",
"desc": "描述",
"result": "返回的数据结果"
}
```

##文本搜索引擎
###参数列表
<table>
<tbody>
<tr><td><em>参数名</em></td><td><em>描述</em></td><td><em>默认值</em></td></tr>
<tr><td>appid</td><td>应用ID</td><td>您自己的appid</td></tr>
<tr><td>sign_method</td><td>签名方式</td><td>目前支持MD5</td></tr>
<tr><td>sign</td><td>签名</td><td>MD5加密后结果</td></tr>
<tr><td>text</td><td>搜索内容</td><td>搜索内容, 最大长度:65535</td></tr>
<tr><td>docid</td><td>文档id</td><td>文档id, 用于搜索时返回</td></tr>
<tr><td>docids</td><td>文档id范围</td><td>如: 1-1000, 搜索引擎会在id范围内进行搜索, <em>注</em>: docids的最大取值范围为1 ~ 999999999999</td></tr>
<tr><td>tags</td><td>标签</td><td>如: 搜索-引擎 被打上此标签的搜索内容, 最大长度:65535</td></tr>
<tr><td>timeout</td><td>超时时间</td><td>如果搜索超时,也会有部分内容返回</td></tr>
</tbody>
</table>
###获取搜索结果接口
####接口地址
    /search/
####参数
    text / tags / docids (text与tags至少有一项不为空,docids为必填项) / timeout (可选)
####返回字段
    tokens (关键词列表) / dos (文档列表,已经排序好的) / timeout (是否超时,如果超时也会返回部分结果)
###上传需要被搜索的文档接口
####接口地址
    /index/
####参数
    text / docid / tags
####返回字段
    如果成功返回空 / 失败返回错误信息

##中文分词
###参数列表
<table>
<tbody>
<tr><td><em>参数名</em></td><td><em>描述</em></td><td><em>默认值</em></td></tr>
<tr><td>appid</td><td>应用ID</td><td>您自己的appid</td></tr>
<tr><td>sign_method</td><td>签名方式</td><td>目前支持MD5</td></tr>
<tr><td>sign</td><td>签名</td><td>MD5加密后结果</td></tr>
<tr><td>text</td><td>文本</td><td>要被分词的文本</td></tr>
<tr><td>mode</td><td>模式</td><td>0 普通模式 1 搜索引擎模式</td></tr>
</tbody>
</table>
###获取分词结果接口
####接口地址
    /cut/
####参数
text / mode
####返回字段
text（分词）/ pos（词性）

##新闻WEB API
###参数列表
<table>
<tbody>
<tr><td><em>参数名</em></td><td><em>描述</em></td><td><em>默认值</em></td></tr>
<tr><td>appid</td><td>应用ID</td><td>您自己的appid</td></tr>
<tr><td>sign_method</td><td>签名方式</td><td>目前支持MD5</td></tr>
<tr><td>sign</td><td>签名</td><td>MD5加密后结果</td></tr>
<tr><td>tag</td><td>分类</td><td>分类见下表</td></tr>
<tr><td>limit</td><td>每次请求的条数</td><td>10</td></tr>
<tr><td>page</td><td>页数</td><td>页数</td></tr>
</tbody>
</table>

###获取新闻接口
####接口地址 
    /news/
####参数
    tag / limit / page
#####分类列表
<table>
<tbody>
<tr><td><em>标签</em></td><td>推荐</td><td>热点</td><td>社会</td><td>娱乐</td><td>科技</td><td>汽车</td><td>时尚</td></tr>
<tr><td><em>字段</em></td><td>__all__</td><td>news_hot</td><td>news_society</td><td>news_entertainment</td><td>news_tech</td><td>news_car</td><td>news_fashion</td></tr>
</tbody>
</table>

###获取美女图片接口
####接口地址 
    /newsgirlpic/
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
###参数列表
<table>
<tbody>
<tr><td><em>参数名</em></td><td><em>描述</em></td><td><em>默认值</em></td></tr>
<tr><td>appid</td><td>应用ID</td><td>您自己的appid</td></tr>
<tr><td>sign_method</td><td>签名方式</td><td>目前支持MD5</td></tr>
<tr><td>sign</td><td>签名</td><td>MD5加密后结果</td></tr>
<tr><td>first</td><td>一级分类 1：男 0：女</td><td>无</td></tr>
<tr><td>second</td><td>二级分类，按小说内容</td><td>无</td></tr>
<tr><td>novelid</td><td>小说ID</td><td>无</td></tr>
<tr><td>chapterid</td><td>章节ID</td><td>无</td></tr>
<tr><td>wd</td><td>搜索关键词</td><td>无</td></tr>
</tbody>
</table>
###获取小说分类接口
####接口地址
    /taglist/
####参数
first / second
    *注：如果获取全部分类目录 无需传first second
####返回字段 
    first  second  name(二级分类名称)

###获取某分类下的小说列表接口
####接口地址 
    /novellist/ 
####参数
    first / second
####返回字段
    title， novelid, author, picture, introduction

###获取小说简介接口
####接口地址 
    /novelintroduction/
####参数说明
    novelid
####返回字段 
    title, novelid, author, picture, introduction, chapternum

###获取小说的章节列表接口
####接口地址 
    /novelchapter/
####参数说明
    novelid
####返回字段
    title(小说标题), subtitle(小说章节标题)， chapterid(章节id), novelid , author, picture, introduction

###获取章节内容接口
####接口地址 
    /novelcontent/
####参数
    chapterid
####返回字段
    title(小说标题), subtitle(小说章节标题), novelid(小说ID), content(内容), chapterid, prev(上一章节chapterid), next(下一章节chapterid)

###小说点击事件上传
####接口地址
    /novelclick/
####接口描述
    上传用户小说点击数，用来记录小说总阅读数
####参数
    novelid
####返回字段
    novelid， novelpv(当前novelid的对应的小说阅读量)

###获取小说排名
####接口地址
    /novelrank/
####接口描述
    获取小说热度排行榜
####参数
    page / limit
####返回字段
    novelid / title / novelpv / picture / author / first / second / rank(排名)
    
###小说搜索
####接口地址
    /novelsearch/
####接口描述
    获取小说搜索结果
####参数
    wd
####返回字段
    id(即novelid) / title / novelpv / picture(在地址前加 http://api.9miao.com/static/spider/) / author / first / second / introduction
    
###小说下载 
####接口地址
    /noveldownload/
####接口描述
    下载小说
####参数
    novelid
####返回字段
    novelsrc (小说的下载地址)
####小说文件格式
    Json格式, 格式如下:
    {
        "title" : "XXXXXXXXXXX", //小说标题
        "chaptercontent": [
            {
                "chapterid": 123,
                "subtitle": "XXXXXXX",
                "content": "XXXXXXXXXXXXXX",
            },           
        ]
    }
    
##用户认证接口
###参数列表
<table>
<tbody>
<tr><td><em>参数名</em></td><td><em>描述</em></td><td><em>默认值</em></td></tr>
<tr><td>appid</td><td>应用ID</td><td>您自己的appid</td></tr>
<tr><td>sign_method</td><td>签名方式</td><td>目前支持MD5</td></tr>
<tr><td>sign</td><td>签名</td><td>MD5加密后结果</td></tr>
<tr><td>username</td><td>用户名</td><td>无</td></tr>
<tr><td>password</td><td>密码</td><td>无</td></tr>
</tbody>
</table>
###用户注册
####接口地址
    /register/
####接口描述
    用于开发者的用户注册
####参数
    username / password
####返回字段
    如果成功 code: 200 失败 code为相应错误码
    
###亲加通讯云的用户登录验证
    登录的用户名格式 account-appid-method-sign
    将account,appid,method进行字典排序后md5加密
    sign = md5(appsecretkey1value1key2value2...appsecret)

###验证用户是否存在
####接口地址
    /checkuserexist/
####接口描述
    验证用户是否已经存在
####参数
    username
####返回字段
    存在code: 601 不存在 code: 602

##开发计划
* 2015-12-18 将数据库中的小说转化为json,并形成txt文件,开发响应脚本,脚本名称 novelfile ***done***
* 2015-12-14 提供小说文件下载接口  ***done***
* 2015-12-14 将数据库中的小说文本转化为txt文件 ***done***
* 2015-12-9 增加redis缓存
