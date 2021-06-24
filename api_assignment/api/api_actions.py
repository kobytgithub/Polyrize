import json
import requests


class ApiActions(object):
    server = "http://0.0.0.0:8000"
    auth = {}
    headers = None
    dict_obj = {"data": [{"key": "key1", "val": "val1", "valType": "str"}]}

    def __init__(self):
        super(ApiActions, self).__init__()

    def authenticate(self, username=None, password=None):
        if username:
            self.auth["username"] = username
        else:
            self.auth["username"] = "test"
        if password:
            self.auth["password"] = password
        else:
            self.auth["password"] = "1234"

        try:
            print(f"Will authenticate with these creds: [{self.auth}]")
            res = requests.post(f"{self.server}/api/auth", json=self.auth)
            res_json = res.json()
            if "access_token" in res_json:
                token = res_json["access_token"]
            else:
                print(res_json)
                print("No access_token in response")
                return False
            self.headers = {"Content-Type": "application/json",
                            "Authorization": f"Bearer {token}"}
            print(f"Got token: [{token}]")
            return True

        except Exception as e:
            print(f"Failed to authenticate: [{e}]")
            return False

    def get_object_list(self):
        try:
            print("Will get object list")
            res = requests.get(f"{self.server}/api/poly", headers=self.headers)
            res_json = res.json()
            if res.status_code == 200 and type(res_json) == type([]):
                print("Got object list")
            else:
                print("No object list")
                return False
            return res_json

        except Exception as e:
            print(f"Failed getting all objects: [{e}]")
            return False

    def get_object(self, obj_id):
        try:
            print(f"Getting object by id: [{obj_id}]")
            res = requests.get(f"{self.server}/api/poly/{obj_id}", headers=self.headers)
            res_json = res.json()
            if "error" in res_json:
                print(f"Error getting object: [{res_json['error']}]")
                return False
            print(f"Got object: [{res_json}]")
            return res_json

        except Exception as e:
            print(f"Failed getting object by id: [{e}]")
            return False

    def create_object(self, dict_obj=None):
        if dict_obj:
            self.dict_obj = dict_obj
        try:
            print(f"Will Create object: [{self.dict_obj}]")
            res = requests.post(f"{self.server}/api/poly", headers=self.headers, data=json.dumps(self.dict_obj))
            res_json = res.json()
            if "error" in res_json:
                print(f"Error creating object: [{res_json['error']}][{res_json['message']}]")
                return False
            print(f"Created object, object id: [{res_json['id']}]")
            return res_json

        except Exception as e:
            print(f"Failed getting all objects: [{e}]")
            return False

    def delete_object(self, obj_id):
        try:
            print(f"Deleting object by id: [{obj_id}]")
            res = requests.delete(f"{self.server}/api/poly/{obj_id}", headers=self.headers)
            if res.status_code == 200:
                return True
            else:
                return False

        except Exception as e:
            print(f"Failed deleting object by id: [{e}]")
            return False
