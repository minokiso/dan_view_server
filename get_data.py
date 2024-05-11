import datetime
import hashlib
import traceback
import pytz

import requests
import threading
import os
import django
from django.forms import model_to_dict

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dan_view.settings')
django.setup()

from output.models import RealOEEDay, LastDayOutPut, EVR1, EVR2

tz_Beijing = pytz.timezone('Asia/Shanghai')


def get_token():
    now = datetime.datetime.utcnow()
    seconds = (now - datetime.datetime(1970, 1, 1)).total_seconds()
    time_initial = int(seconds)
    timevalue = "%s000" % time_initial
    uid = "f5bf08858626428f9f6912f866fdf818"
    sid = "a816661f1db74d3398a108b1ae50ca92"
    random = "dan123"
    timestamp = timevalue
    content_to_encrypt = uid + sid + random + timestamp
    md5_hash = hashlib.md5()
    md5_hash.update(content_to_encrypt.encode('utf-8'))
    encrypted_hash = md5_hash.hexdigest().upper()

    url = "https://hcloud.huceen.com/api/v1/token/initToken"
    data = {'uid': 'f5bf08858626428f9f6912f866fdf818', 'sid': 'a816661f1db74d3398a108b1ae50ca92',
            'random': 'dan123',
            'timestamp': timevalue, 'signature': encrypted_hash}
    response = requests.post(url, data=data)
    token = response.json().get("data", {}).get("token", None)
    return token


def get_t2():
    url = "https://hcloud.huceen.com/api/v1/data/realtimeDatas"
    token = get_token()
    data = {'token': token, 'variantIds': '178f106f09214924b3c80f3987c0361f(:0);'
                                          '178f106f09214924b3c80f3987c0361f(:1);'
                                          '178f106f09214924b3c80f3987c0361f(:2);'
                                          '178f106f09214924b3c80f3987c0361f(:4);'
                                          '178f106f09214924b3c80f3987c0361f(:5)'}
    response = requests.post(url, data=data)
    daily_line_oee = None
    lastday_output = None
    datetime_utc = datetime.datetime.now(pytz.utc)
    today = datetime_utc.astimezone(tz_Beijing)

    for d in response.json().get("data", []):
        if d.get("id") == "178f106f09214924b3c80f3987c0361f:5":
            daily_line_oee = d.get("value")
        if d.get("id") == "178f106f09214924b3c80f3987c0361f:1":
            lastday_output = d.get("value")
    r_obj, r_created = RealOEEDay.objects.update_or_create(
        time__date=today.date(),
        defaults={
            "value": daily_line_oee if daily_line_oee else 0,
            "time": today
        })
    print("RealOEEDay 创建成功", today, model_to_dict(r_obj), r_created)
    l_obj, l_created = LastDayOutPut.objects.update_or_create(
        time__date=today.date(),
        defaults={
            "value": lastday_output if lastday_output else 0,
            "time": today
        })
    print("LastDayOutPut 创建成功", today, model_to_dict(l_obj), l_created)


def get_evr():
    url = "https://hcloud.huceen.com/api/v1/data/realtimeDatas"
    token = get_token()
    data = {'token': token, 'variantIds': '4e29f69bb02a4761b91f7cb7fa8cea35(:3);'
                                          '4e29f69bb02a4761b91f7cb7fa8cea35(:8)'}
    response = requests.post(url, data=data)
    evr1 = None
    evr2 = None
    datetime_utc = datetime.datetime.now(pytz.utc)
    today = datetime_utc.astimezone(tz_Beijing)
    for d in response.json().get("data", []):
        if d.get("id") == "4e29f69bb02a4761b91f7cb7fa8cea35:3":
            evr1 = d.get("value")
        if d.get("id") == "4e29f69bb02a4761b91f7cb7fa8cea35:8":
            evr2 = d.get("value")
    evr1, evr1_created = EVR1.objects.update_or_create(
        time__date=today.date(),
        defaults={
            "value": evr1 if evr1 else 0,
            "time": today
        })
    print("EVR1 创建成功", today, model_to_dict(evr1), evr1_created)
    evr2_obj, evr2_created = EVR2.objects.update_or_create(
        time__date=today.date(),
        defaults={
            "value": evr2 if evr2 else 0,
            "time": today
        })
    print("EVR2 创建成功", today, model_to_dict(evr2_obj), evr2_created)


def get_data_thread():
    try:
        get_t2()
        get_evr()
    except Exception as e:
        traceback.print_exc()
    finally:
        print("--------------------------------")
        threading.Timer(3600, get_data_thread).start()


if __name__ == '__main__':
    get_data_thread()
