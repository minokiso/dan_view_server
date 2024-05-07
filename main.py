# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# 时间戳转换
import datetime
# from mysql.connector import MySQLConnection
# from mysql.connector.fabric import MySQLFabricConnection
# #from requests import Response
import urllib.request
now = datetime.datetime.utcnow()
seconds = (now - datetime.datetime(1970, 1, 1)).total_seconds()
timeinitial = int(seconds)  # print("%s000"%timeinitial)
timevalue = "%s000" % timeinitial
print(timevalue)  # 1


### md5加密
import hashlib
uid = "f5bf08858626428f9f6912f866fdf818"
sid = "a816661f1db74d3398a108b1ae50ca92"
random = "dan123"
timestamp = timevalue
content_to_encrypt = uid + sid + random + timestamp
md5_hash = hashlib.md5()
md5_hash.update(content_to_encrypt.encode('utf-8'))
# print((md5_hash.hexdigest()).upper())
encrypted_hash = md5_hash.hexdigest().upper()
# 输出加密后的MD5哈希值
print(encrypted_hash)  # 2
### 获取token数据
import requests  # 获取token函数
import json
url = "https://hcloud.huceen.com/api/v1/token/initToken"
data = {'uid': 'f5bf08858626428f9f6912f866fdf818', 'sid': 'a816661f1db74d3398a108b1ae50ca92', 'random': 'dan123',
        'timestamp': timevalue, 'signature': encrypted_hash}
# r = requests.post(url, data=data)
#  return (r.json()["data.data.token"])
# 将获取的token返回
# print(r)
response = requests.post(url, data=data)  # 发送post请求
# print(response.text)
response_data: object = json.loads(response.text)
# 将数据拆分为不同的部分
part1 = response_data['data']['token']
# 打印token数据
print(part1)  # 3
# 获取T2数据
import requests
url = "https://hcloud.huceen.com/api/v1/data/realtimeDatas"
data = {'token': part1, 'variantIds': '4e29f69bb02a4761b91f7cb7fa8cea35(:3);'
                                      '4e29f69bb02a4761b91f7cb7fa8cea35(:8)'}
response = requests.post(url, data=data)  # 发送post请求
responsecode = requests.get('https://hcloud.huceen.com/api/v1/data/realtimeDatas')
print(responsecode.status_code)# 4
print(response.text)  # 5
# 解析JSON响应
response_data = json.loads(response.text)
# 将数据拆分为不同的部分
# 打印每个部分的数据
# 分析内容
repositories = response_data['data']

from datetime import datetime, timedelta
def get_morning_time():
    # 获取今天的日期
    today = datetime.now().date()
    # 创建一个时间对象，时间设置为早上7点
    morning_time = datetime.combine(today, datetime.min.time()) + timedelta(hours=7)
    # 设置秒和微秒为0
    morning_time = morning_time.replace(second=0, microsecond=0)
    # 返回格式化后的时间字符串
    return morning_time.strftime("%Y-%m-%d 07:00:00")
# 打印结果
print(get_morning_time())




def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
