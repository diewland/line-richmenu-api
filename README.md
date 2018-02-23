# LINE Richmenu API
create LINE rich-menu from API

### Example
```python
import os
from pprint import pprint as pp

# init api
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
```
### Reference(s)
https://developers.line.me/en/docs/messaging-api/using-rich-menus/
