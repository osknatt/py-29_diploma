import json
import requests
import time

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        try:
            self.friends = self.get_friends(self.user_id)
            self.groups = self.get_groups(self.user_id)
        except:
            # Реакция на недоступных пользователей
            self.friends = {}
            self.groups = {}

    def get_friends(self, user_id):
        friends = requests.get(
            'https://api.vk.com/method/friends.get',
            params={
                'access_token': TOKEN,
                'v': '5.52',
                'user_id': user_id
            }
        )
        friends = friends.json()
        return set(friends['response']['items'])

    def get_groups(self, user_id):
        groups = requests.get(
            'https://api.vk.com/method/groups.get',
            params={
                'access_token': TOKEN,
                'v': '5.52',
                'user_id': user_id
            }
        )
        groups = groups.json()
        return set(groups['response']['items'])


user_of_interest = User('171691064')
unique_groups = []
for group in user_of_interest.groups:
    time.sleep(1)
    print('.', end='')
    members = requests.get(
        'https://api.vk.com/method/groups.getMembers',
        params={
            'access_token': TOKEN,
            'v': '5.52',
            'group_id': group
        }
    )
    members = members.json()
    members = set(members['response']['items'])
    if len(user_of_interest.friends & members) == 0:
        try:
            group = requests.get(
                'https://api.vk.com/method/groups.getById',
                params={
                    'access_token': TOKEN,
                    'v': '5.52',
                    'group_id': group,
                    'fields': 'members_count'
                }
            )
            group = group.json()
            group = group['response'][0]
            unique_groups.append({
                'name': group['name'],
                'gid': group['id'],
                'members_count': group['members_count']
            })
        except:
            pass

with open('groups.json', 'w') as outfile:
    json.dump(unique_groups, outfile, indent=2, ensure_ascii=False)

print('Done!')
