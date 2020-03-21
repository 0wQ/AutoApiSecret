import requests as req
import json
import sys
import time

path = sys.path[0] + r'/1.txt'

def gettoken(refresh_token):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': id,
        'client_secret': secret,
        'redirect_uri': 'http://localhost:53682/'
    }
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token', data=data, headers=headers)
    jsontxt = json.loads(html.text)
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    with open(path, 'w+') as f:
        f.write(refresh_token)
    return access_token


def main():
    fo = open(path, "r+")
    refresh_token = fo.read()
    fo.close()
    num = 0
    localtime = time.asctime(time.localtime(time.time()))
    access_token = gettoken(refresh_token)
    headers = {
        'Authorization': access_token,
        'Content-Type': 'application/json'
    }
    try:
        urls = {
            'https://graph.microsoft.com/v1.0/me/drive/root',
            'https://graph.microsoft.com/v1.0/me/drive',
            'https://graph.microsoft.com/v1.0/drive/root',
            'https://graph.microsoft.com/v1.0/users',
            'https://graph.microsoft.com/v1.0/me/messages',
            'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
            'https://graph.microsoft.com/v1.0/me/drive/root/children',
            'https://api.powerbi.com/v1.0/myorg/apps',
            'https://graph.microsoft.com/v1.0/me/mailFolders',
            'https://graph.microsoft.com/v1.0/me/outlook/masterCategories',
        }
        for url in urls:
            if req.get(url, headers=headers).status_code == 200:
                num += 1
                print(str(num) + ' - ' + 'Success, ' + url)
        
        data_1 = req.get("https://graph.microsoft.com/beta/me/drive/root/search(q='test')?select=name", headers=headers)
        if data_1.status_code == 200:
            num += 1
            print(str(num) + ' - ' + '自定义_搜索文件')
            # print(', '.join(str(a['name']) for a in data_1.json()['value']))
        
        data_2 = req.get("https://graph.microsoft.com/beta/me/drive/recent", headers=headers)
        if data_2.status_code == 200:
            num += 1
            print(str(num) + ' - ' + '自定义_最近文件 ' + ', '.join(str(a['name']) for a in data_2.json()['value']))
        
        print('此次运行结束:', localtime)
    except:
        print("Pass...")
        pass


for _ in range(5):
    main()
