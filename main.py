import json
import sys
import os
import time
import codecs
from pathlib import Path
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from geopy.geocoders import Nominatim
from instagram_private_api import Client as AppClient
from instagram_private_api import ClientCookieExpiredError, ClientLoginRequiredError, ClientError
import printcolors as pc
import config

class Osintgram:
    api = None
    api2 = None
    geolocator = Nominatim(user_agent="http")
    user_id = None
    target_id = None
    following = False
    target = ""
    writeFile = False
    jsonDump = False
    output_dir = "output"

    def __init__(self, target):
        self.st = time.time()
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 01:', self.elapsed_time, 'seconds')
        
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
        u = config.getUsername()
        p = config.getPassword()
        if True:
          print("\nAttempt to login...")
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 02:', self.elapsed_time, 'seconds')
        
        self.login(u, p)
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 03:', self.elapsed_time, 'seconds')
        
        self.setTarget(target)
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 04:', self.elapsed_time, 'seconds')
        
        self.endpoint = 'users/{user_id!s}/full_detail_info/'.format(**{'user_id': self.target_id})
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 05:', self.elapsed_time, 'seconds')
        
        self.content = self.api._call_api(self.endpoint)
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 06:', self.elapsed_time, 'seconds')
        
        self.data = self.content['user_detail']['user']
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 07:', self.elapsed_time, 'seconds')
        
        self.feed = self.__get_feed__()
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 08:', self.elapsed_time, 'seconds')
        
        self.result = self.api.usertag_feed(self.target_id)
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 09:', self.elapsed_time, 'seconds')
        
        self.rank_token = AppClient.generate_uuid()
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 10:', self.elapsed_time, 'seconds')
        
        self.followers = self.api.user_followers(str(self.target_id), rank_token=self.rank_token)
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 11:', self.elapsed_time, 'seconds')
        
        self.following = self.api.user_following(str(self.target_id), rank_token=self.rank_token)
        self.et = time.time()
        self.elapsed_time = self.et - self.st
        print('Execution time 12:', self.elapsed_time, 'seconds')
        

    def setTarget(self, target):
        self.target = target
        user = self.get_user(target)
        self.target_id = user['id']
        self.__printTargetBanner__()

    def __get_feed__(self):
        data = []

        result = self.api.user_feed(str(self.target_id))
        data.extend(result.get('items', []))

        next_max_id = result.get('next_max_id')
        while next_max_id:
            results = self.api.user_feed(str(self.target_id), max_id=next_max_id)
            data.extend(results.get('items', []))
            next_max_id = results.get('next_max_id')

        return data



    def __printTargetBanner__(self):
        pc.printout("\nLogged as ", pc.GREEN)
        pc.printout(self.api.username, pc.CYAN)
        pc.printout(". Target: ", pc.GREEN)
        pc.printout(str(self.target), pc.CYAN)
        pc.printout(" [" + str(self.target_id) + "]")
        print('\n')

    def get_likes_comments(self):
        comments_counter = 0
        like_counter = 0
        for post in self.feed:
            comments_counter += post['comment_count']
            like_counter += post['like_count']
        return [int(like_counter),int(comments_counter)]

    def get_followers(self):
        _followers = []
        followers = []
        _followers.extend(self.followers.get('users', []))
        for i in range(7):
            u = {
                'id': _followers[i]['pk'],
                'username': _followers[i]['username'],
                'full_name': _followers[i]['full_name']
            }
            followers.append(u)
        # for i in range(0, len(followers) - 6):
        #     followers.pop()
        return [self.extract_fullname(followers), self.extract_username(followers)]

    def get_bestfriends(self):
        _followings = []
        followings = []
        _followings.extend(self.following.get('users', []))
        for i in range(8):
            u = {
                'id': _followings[i]['pk'],
                'username': _followings[i]['username'],
                'full_name': _followings[i]['full_name']
            }
            followings.append(u)
        # for i in range(0, len(followings) - ):
        #     followings.pop()
        return [self.extract_fullname(followings), self.extract_username(followings)]

    def get_user(self, username):
        try:
            content = self.api.username_info(username)
            user = dict()
            user['id'] = content['user']['pk']
            return user
        except ClientError as e:
            print('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response))
            error = json.loads(e.error_response)
            if 'message' in error:
                print(error['message'])
            if 'error_title' in error:
                print(error['error_title'])
            if 'challenge' in error:
                print("Please follow this link to complete the challenge: " + error['challenge']['url'])
            sys.exit(2)

    def login(self, u, p):
        try:
            settings_file = "config/settings.json"
            if not os.path.isfile(settings_file):
                # settings file does not exist
                print(f'Unable to find file: {settings_file!s}')

                # login new
                self.api = AppClient(auto_patch=True, authenticate=True, username=u, password=p,
                                     on_login=lambda x: self.onlogin_callback(x, settings_file))

            else:
                with open(settings_file) as file_data:
                    cached_settings = json.load(file_data, object_hook=self.from_json)
                # print('Reusing settings: {0!s}'.format(settings_file))

                # reuse auth settings
                self.api = AppClient(
                    username=u, password=p,
                    settings=cached_settings,
                    on_login=lambda x: self.onlogin_callback(x, settings_file))

        except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
            print(f'ClientCookieExpiredError/ClientLoginRequiredError: {e!s}')

            # Login expired
            # Do relogin but use default ua, keys and such
            self.api = AppClient(auto_patch=True, authenticate=True, username=u, password=p,
                                 on_login=lambda x: self.onlogin_callback(x, settings_file))

        except ClientError as e:
            pc.printout('ClientError {0!s} (Code: {1:d}, Response: {2!s})'.format(e.msg, e.code, e.error_response), pc.RED)
            error = json.loads(e.error_response)
            pc.printout(error['message'], pc.RED)
            pc.printout(": ", pc.RED)
            pc.printout(e.msg, pc.RED)
            pc.printout("\n")
            if 'challenge' in error:
                print("Please follow this link to complete the challenge: " + error['challenge']['url'])
            exit(9)

    def to_json(self, python_object):
        if isinstance(python_object, bytes):
            return {'__class__': 'bytes',
                    '__value__': codecs.encode(python_object, 'base64').decode()}
        raise TypeError(repr(python_object) + ' is not JSON serializable')

    def from_json(self, json_object):
        if '__class__' in json_object and json_object['__class__'] == 'bytes':
            return codecs.decode(json_object['__value__'].encode(), 'base64')
        return json_object

    def onlogin_callback(self, api, new_settings_file):
        cache_settings = api.settings
        with open(new_settings_file, 'w') as outfile:
            json.dump(cache_settings, outfile, default=self.to_json)

    def people_who_tagged(self):
            posts = []
            posts.extend(self.result.get('items', []))
            next_max_id = self.result.get('next_max_id')
            while next_max_id:
                results = self.api.user_feed(str(self.target_id), max_id=next_max_id)
                posts.extend(results.get('items', []))
                next_max_id = results.get('next_max_id')
            if len(posts) > 0:
                users = []
                for post in posts:
                    if not any(u['username'] == post['user']['username'] for u in users):
                        user = {
                            'username': post['user']['username'],
                            'full_name': post['user']['full_name'],
                            'counter': 1
                        }
                        users.append(user)
                    else:
                        for user in users:
                            if user['username'] == post['user']['username']:
                                user['counter'] += 1
                                break
                ssort = sorted(users, key=lambda value: value['counter'], reverse=True)
                for i in range(0, len(ssort) - 6):
                    ssort.pop()
                return [self.extract_fullname(ssort), self.extract_username(ssort)]
            else:
                return None
   
    def extract_username(self, l):
        username = []
        for ele in l:
            username.append(ele['username'])
        return username
    def extract_fullname(self, l):
        fullname = []
        for ele in l:
            fullname.append(ele['full_name'])
        return fullname
    def extract_count(self, l):
        count = []
        for ele in l:
            count.append(ele['counter'])  
        return count          
        
api = Osintgram(config.getUsername())
data  = api.data
IG_Posts = int(data["media_count"])
IG_Followers = int(data["follower_count"])
IG_Following = int(data["following_count"])
IG_Likes_Comments = api.get_likes_comments()
IG_Likes = IG_Likes_Comments[0]
IG_Comments = IG_Likes_Comments[1]
IG_Tagged = api.people_who_tagged()
IG_Friends = api.get_bestfriends()
IG_Recent_Followers = api.get_followers()



# print(IG_Posts)
# print(IG_Followers)
# print(IG_Following)
# print(IG_Likes)
# print(IG_Comments)
# # print(IG_Tagged)
# # print(IG_Friends[0][0])
# # print(IG_Friends[1][0])
# # print(IG_Friends[0][1])
# # print(IG_Friends[1][1])
# # print(IG_Recent_Followers)