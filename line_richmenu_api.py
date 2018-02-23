import requests
import magic
import json

class LINERichmenuAPI(object):

    def __init__(self, access_token):
        self.access_token = access_token
        self.headers      = { 'Authorization': 'Bearer %s' % self.access_token }

    ########## API(s) ##########

    def create_menu_config(self, config):
        headers = dict(self.headers)
        headers['Content-Type'] = 'application/json'
        url = "https://api.line.me/v2/bot/richmenu"
        return requests.post(url, headers=headers, data=json.dumps(config)).json()

    def upload_menu_image(self, rich_menu_id, img_path):
        mime = magic.Magic(mime=True)
        headers = dict(self.headers)
        headers['Content-Type'] = mime.from_file(img_path)
        url = "https://api.line.me/v2/bot/richmenu/%s/content" % rich_menu_id
        data = open(img_path,'rb')
        return requests.post(url, headers=headers, data=data).json()

    def link_user_menu(self, user_id, rich_menu_id):
        url = "https://api.line.me/v2/bot/user/%s/richmenu/%s" % ( user_id, rich_menu_id )
        return requests.post(url, headers=self.headers).json()

    def unlink_user_menu(self, user_id):
        url = "https://api.line.me/v2/bot/user/%s/richmenu" % user_id
        return requests.delete(url, headers=self.headers).json()

    def list_menus(self):
        url = "https://api.line.me/v2/bot/richmenu/list"
        return requests.get(url, headers=self.headers).json()

    def remove_menu(self, rich_menu_id):
        url = "https://api.line.me/v2/bot/richmenu/%s" % rich_menu_id
        return requests.delete(url, headers=self.headers).json()

    ########## UTILITIES ##########

    def create_menu(self, config, img_path):
        resp = self.create_menu_config(config)
        menu_id = resp['richMenuId']
        resp = self.upload_menu_image(menu_id, img_path)
        return { 'richMenuId': menu_id }

    def remove_all_menus(self, confirm=False):
        if not confirm:
            return
        menus = self.list_menus()['richmenus']
        for menu in menus:
            self.remove_menu(menu['richMenuId'])

if __name__ == "__main__":

    import os
    from pprint import pprint as pp

    access_token = os.environ.get('LINE_ACCESS_TOKEN')
    api = LINERichmenuAPI(access_token)

    # sample user_id, menu config
    user_id = '-----<LINE-USER-ID>-----'
    config = {
        "size": {
          "width": 2500,
          "height": 1686
        },
        "selected": False,
        "name": "Nice richmenu",
        "chatBarText": "Tap here",
        "areas": [
          {
            "bounds": {
              "x": 0,
              "y": 0,
              "width": 2500,
              "height": 1686
            },
            "action": {
              "type":"message",
              "text":"Welcome rich-menu!"
            }
          }
        ]
    }

    # setup menu 1 time only
    print('remove all menus')
    api.remove_all_menus(True)

    print('create new rich-menu')
    resp = api.create_menu(config, './sample.png')
    menu_id = resp['richMenuId']

    # link/unlink menu (per user) as much as you want
    print('link menu to user')
    api.unlink_user_menu(user_id)
    api.link_user_menu(user_id, menu_id)

    # view script result
    print('list menu(s)')
    pp(api.list_menus())
