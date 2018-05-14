# -*- coding: utf-8 -*-
import requests
import ssl
import re

ssl._create_default_https_context= ssl._create_unverified_context

session = requests.Session()

#登录地址
url_init = "https://cas.bjut.edu.cn/login?service=https%3A%2F%2Fmy1.bjut.edu.cn%2Fc%2Fportal%2Flogin"

# 第一次初始化时的header
urlheader = {
    'Host':	'cas.bjut.edu.cn',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                 'Chrome/66.0.3359.139 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'gscu_1159939665=03670946ik4o2912; CASPRIVACY=""; TGC=""; JSESSIONID=C0294166AA915C42321760E452157098-n1'
}

# 第二次 登录header
loginHeader = {
    'Host': 'cas.bjut.edu.cn',
    'Connection': 'keep-alive',
    'Content-Length': '5623',
    'Cache-Control': 'max-age=0',
    'Origin': 'https://cas.bjut.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.139 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'https://cas.bjut.edu.cn/login?service=https%3A%2F%2Fmy1.bjut.edu.cn%2Fc%2Fportal%2Flogin',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '_gscu_1159939665=03670946ik4o2912; CASPRIVACY=""; TGC=""; JSESSIONID=937C86E286BE9898C41955D16C309540-n1'
}

# 第三次访问 请求数据时的header
urlheader_new = {
    'Host':	'my1.bjut.edu.cn',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/66.0.3359.139 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '_gscu_1159939665=03670946ik4o2912; COOKIE_SUPPORT=true; GUEST_LANGUAGE_ID=zh_CN; '
              'JSESSIONID=DAEC0F514C2B5628C34B494DBE26F1FF.a; LFR_SESSION_STATE_217891=1526288234272'
}



def getHtml():
    # 1、初始化 访问页面 生成execution以及lt校验值
    initHtml(url_init)


def initHtml(url):
    r = session.get(url, headers=urlheader, verify=False)
    data = r.content.decode('utf-8')

    # 获取execution
    execution_pattern = "execution.*value=\"(.*)\" "

    re.compile(execution_pattern)

    execution = re.findall(execution_pattern, data)
    execution_str = execution[0]
    print(execution_str)

    # 获取lt
    lt_pattern = "lt.*value=\"(.*)\" "
    re.compile(lt_pattern)
    ltlst = re.findall(lt_pattern, data)
    ltlst_str = ltlst[0]

    postHtml(url, execution_str, ltlst_str)


def postHtml(url, execution, lt):
    # 表单数据
    formdata = {
        'username': 'S201761441',
        'password': '812727',
        'lt': lt,
        'execution': execution,
        '_eventId': 'submit',
        'submit': ''
    }
    rlogin = session.post(url, data=formdata, headers=loginHeader, verify=False)

    loginHtml(lt)

def loginHtml(lt):
    url_group = "https://my1.bjut.edu.cn/group/graduate?ticket=" + lt
    print("new url:" + url_group)
    resp_new = session.get(url_group, headers=urlheader_new, verify=False)
    resp_data_new = resp_new.content.decode('utf-8')
    print(resp_data_new)
    saveHtml(resp_data_new)


# 保存到本地
def saveHtml(data):
    f = open("/Users/xupeng/PycharmProjects/school_login.html", "wb")
    f.write(data.encode('utf-8'))
    f.close()


if __name__ == '__main__':
    getHtml()