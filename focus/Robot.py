import os
import json
from time import sleep
import focus.utils as utils



class Robot(object):

    def __init__(
        self,
        query_interval: int,
        repository: str,
        focus_file: str,
        history_file: str,
        focus_history_file: str,
        diff_file: str,
        hashnumber: str,
        hash_path: str,
        is_changed: bool
        ):
        self._query_interval = query_interval
        self._repository = repository
        self._focus_file = focus_file
        self._history_file = history_file
        self._focus_history_file = focus_history_file
        self._diff_file = diff_file
        self._hashnumber = hashnumber   # hashnumber of last time
        self._hash_path = hash_path
        self._is_changed = is_changed


    def get_remote_head_hashnumber(self) -> str:
        hashnumber = os.popen(f"git rev-parse HEAD").read()[:-1]
        return hashnumber


    def get_local_head_hashnumber(self) -> str:
        with open(self._hash_path, 'r') as f:
            hashnumber = f.readline()
        return hashnumber


    def renew_hashnumber(self):
        hash_path = self._hash_path
        hashnumber_current = self.get_remote_head_hashnumber()
        self._hashnumber = hashnumber_current
        with open(f'{hash_path}', 'w') as f:
            f.write(hashnumber_current)


    def is_change_happend(self):
        hashnumber = self.get_remote_head_hashnumber()
        return hashnumber != self._hashnumber


    def change2diff(self):
        hashnumber_last = self._hashnumber
        hashnumber_current = self.get_remote_head_hashnumber()
        diff_path = self._diff_file
        change = os.popen(f"git diff {hashnumber_last} {hashnumber_current}").read()
        with open(f'{diff_path}', 'w') as f:
            f.write(change)


    def diff2history(self):
        # get the change from the remote repository and add to history file
        diff_path = self._diff_file
        history_file = self._history_file
        
        history = {}
        history["change_list"] = []
        if os.path.isfile(history_file):
            with open(history_file, 'r') as f:
                    history = json.load(f)
                    
        result = utils.get_change_from_diff_file(diff_path)
        
        history["change_list"] += result
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=4) 


    def history2focus_history(self):
        # cross-compare history.json and focus.json, then add the changes which user concerns to focus_history.json
        ##空文件还没有处理
        focus_json = {}
        focus_json["focus_file_list"] = []
        focus_json["focus_block_list"] = []
        if os.path.isfile(self._focus_file):
            with open(self._focus_file, 'r') as f:
                focus_json = json.load(f)
        focus_file = focus_json["focus_file_list"]
        focus_block = focus_json["focus_block_list"]
        
        history_json = {}
        history_json["change_list"] = []
        if os.path.isfile(self._history_file):
            with open(self._history_file, 'r') as f:
                history_json = json.load(f)
        history = history_json["change_list"]
        result = []
        for record in history:
            if record["type"] == "file":
                for file_path in focus_file:
                    if record["file_path"] == file_path:
                        result.append(record)
                        break
            elif record["type"] == "block":
                for block in focus_block:
                    if record["file_path"] == block["file_path"] and record["block_name"] == block["block_name"]:
                        result.append(record)
                        break
        focus_history = {}
        focus_history["change_list"] = []
        if os.path.isfile(self._focus_history_file):
            with open(self._focus_history_file, 'r') as f:
                focus_history = json.load(f)
        focus_history["change_list"].extend(result)
        with open(self._focus_history_file, 'w') as f:
            json.dump(focus_history, f, indent=4)
            
#    "focus_file_list":[
#         "file_path"
#     ],
#     "focus_block_list":[
#         {
#             "file_path": "file_path",
#             "block_name": "block_name"
#         }
#     ]                 
        
# "change_list":[
#         {
#             "type": "",
#             "file_path": "",
#             "block_name": "",
#             "change":{
#                 "time": "",
#                 "detail": ""
#             }
#         }
#     ]
    @property
    def query_interval(self):
        return self._query_interval

    @query_interval.setter
    def query_interval(self, query_interval):
        self._query_interval = query_interval
    
    def run(self):
        while True:
            if not self.is_change_happend():
                sleep(self.query_interval)
                continue
            else:       
                self.change2diff()
                self.diff2history()
                self.history2focus_history()
                self.renew_hashnumber()
                sleep(self.query_interval)
        # check if the remote repository has changed by query_interval
    