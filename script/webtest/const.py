# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
参数配置文件
"""

#baseurl = 'http://127.0.0.1:8000'
baseurl = 'http://api.9miao.com'
"""
testurl = [
    {
        'url': '/cut/',
        'body': {
            'text': '测试测试',
            'mode': 1,
        }
    },
]
"""

testurl = [
    {
        'url': '/search/',
        'body': {
            'text': '测试',
            'docids': '99999999998-99999999999',
        }
    },
    {
        'url': '/index/',
        'body': {
            'text': '测试',
            'docid': '99999999999',
        }
    },
    {
        'url': '/cut/',
        'body': {
            'text': '测试测试',
            'mode': 1,
        }
    },
    {
        'url': '/news/',
        'body': {
            'tag': '__all__',
            'limit': '100',
            'page': '1',
        }
    },
    {
        'url': '/newsgirlpic/',
        'body': {
            'tag': 'photograph_gallery',
            'limit': '100',
            'page': '1',
        }
    },
    {
        'url': '/novelcontent/',
        'body': {
            'chapterid': 100,
        }
    },
    {
        'url': '/taglist/',
    },
    {
        'url': '/novellist/',
        'body': {
            'first': '1',
            'second': '100',
        }
    }
]
