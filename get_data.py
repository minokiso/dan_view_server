import datetime
import hashlib
import traceback

import requests
import threading
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dan_view.settings')
django.setup()

from output.models import RealOEEDay, LastDayOutPut


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


def get_data():
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

    for d in response.json().get("data", []):
        if d.get("id") == "178f106f09214924b3c80f3987c0361f:5":
            daily_line_oee = d
        if d.get("id") == "178f106f09214924b3c80f3987c0361f:1":
            lastday_output = d
    if not daily_line_oee:
        RealOEEDay.objects.get_or_create(time=datetime.datetime.now(), value=0)
    else:
        RealOEEDay.objects.get_or_create(time=datetime.datetime.fromtimestamp(daily_line_oee.get("time")),
                                         value=daily_line_oee.get("value"))
    if not lastday_output:
        LastDayOutPut.objects.get_or_create(time=datetime.datetime.now(), value=0)
    else:
        LastDayOutPut.objects.get_or_create(time=datetime.datetime.fromtimestamp(lastday_output.get("time")),
                                            value=lastday_output.get("value"))


def get_data_thread():
    try:
        get_data()
    except Exception as e:
        traceback.print_exc()
    finally:
        threading.Timer(30, get_data_thread).start()


if __name__ == '__main__':
    get_data_thread()
