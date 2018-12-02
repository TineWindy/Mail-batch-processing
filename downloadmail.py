

# author: WHU CS Chris Huang
# time: 2018-11

import poplib
import datetime
import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.header import Header
 
 
 
# 输入邮件地址, 口令和POP3服务器地址:
user = '1670142089@qq.com'
password = 'vxlcknjcsflrdaac'
pop3_server = 'pop.qq.com'

# 输入存储文件地址:
direction =  '/Users/Visionary/Desktop/homework/'

# 设置筛选时间区间
starttime = '19990501'
endtime = '20181204'

 
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
 
def getFile(mail, path):
    '''
    下载附件
    '''
    
    for annex in mail.walk():
        # 获取附件名
       	fileName = annex.get_filename()
        # print(annex)
        
        if fileName: 
            # 编码附件名
            name = decode_header(Header(fileName))
            filename = name[0][0]
            if name[0][1]:
                filename = decode_str(str(filename,name[0][1]))
            print(filename)

            # 获取附件二进制
            data = annex.get_payload(decode=True)
            
            # 保存到本地路径
            out = open(path + filename, 'wb')
            print(filename)
            out.write(data)
            out.close()

def filterEmail(mail):
    '''
    此函数可根据自定义条件筛选邮件
    paras:
    email Message Object
    return bool
    '''

    # 设置时间条件
    # 设置需要的邮件的时间区间。可根据需求更改，格式为8位长度
    date = time.strptime(mail.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S') 
    date = time.strftime("%Y%m%d", date)   
    if (date<starttime) or (date>endtime):
        return False

    # 还可以设置很多条件，如有无附件、发件者筛选等
    # 有能力的朋友可以自行添加
    # 不熟悉python相关包使用的同学也可以发issue由作者来添加相关功能

    return True

def getMails(popServer):
    '''
    从pop object中获取所有邮件信息
    '''

    mailList = []

    response, emails, counts = popServer.list()
    # print("All emails: " + emails)

    print(emails)

    for i in range(len(emails), 0, -1):
        #倒序遍历邮件
        response, msgLines, counts = server.retr(i)
        # print(msgLines)
        try:
            # msgLines以数组形式存储信息，转换为字符串
            msgContent = b'\r\n'.join(msgLines).decode('utf-8')
        except:
            print(str(i) + " is empty")
            continue

        # 解析邮件字符串信息为message object
        mail = Parser().parsestr(msgContent)
        
        # 筛选邮件
        if not filterEmail(mail):
            continue

        mailList.append(mail)

    return mailList


def connectServer(user, password, host):
    '''
    获取成功登录上pop服务器的pop3 object
    '''
    # 链接服务器。qq邮箱需要ssl加密
    server = poplib.POP3_SSL(host)

    # 根据需要设置调试优先级
    server.set_debuglevel(1)

    # 登录
    server.user(user)
    server.pass_(password)

    return server
 
        
            
if __name__ == '__main__':
    server = connectServer(user, password, pop3_server)
    mails = getMails(server)
    for i in mails:
        getFile(i, direction)
