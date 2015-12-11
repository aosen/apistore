# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
参数配置文件
"""

#baseurl = 'http://127.0.0.1:8000'
baseurl = 'http://api.9miao.com'
case = 0
loop=100

#比较慢的url: new,

switch = {
    3: [
        {
            'url': '/test/',
        },
    ],
    2: [
        {
            'url': '/index/',
            'body': {
                'text': 'hello world',
                'docid': '1',
            }
        },
        {
            'url': '/search/',
            'body': {
                'text': 'hello',
                'docids': '0-999',
                }
        }
    ],
        1: [{
            'url': '/novelsearch/',
            'body': {
                'wd':'word',
            }
        }],
        0:[
        {
            'url': '/search/',
            'body': {
                'text': '测试',
                'docids': '0-999',
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
                'limit': '10',
                'page': '1',
                }
            },
        {
            'url': '/newsgirlpic/',
            'body': {
                'tag': 'photograph_gallery',
                'limit': '10',
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
                'url': '/novelintroduction/',
                'body': {
                            'novelid': 10,
                        },
            },
        {
            'url': '/novellist/',
            'body': {
                'first': '1',
                'second': '100',
                }
            },
            {
            'url': '/novelsearch/',
            'body': {
                'wd': '晴天娃娃会下雨'
                },
            },
            {
                'url': '/novelrank/',
            },
        ]
    }

testurl = switch.get(case)
