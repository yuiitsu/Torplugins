# -*- coding:utf-8 -*-

import qiniu

strAccessKey = 'zUZ_j6K9_Ey0XStMu8nfsVuKbzvMdUTZuanFskn6'
strSecretKey = 'doKv3u-esXK-gK_yF1Sdp7lt9A3WFG9wv8Q49_cr'
strBucket = 'yidao'

auth = qiniu.Auth(strAccessKey, strSecretKey)

def upload(data, key=None, mime_type='application/octet-stream', bucket = strBucket):
    token = auth.upload_token(bucket, key=key)
    ret, info = qiniu.put_data(token, key, data, mime_type=mime_type)
    return ret
