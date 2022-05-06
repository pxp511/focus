import os
import json
from time import sleep


def fetch_from_origin():
    print("Fetching new changes from origin......")
    os.system(f"git fetch")
    print("Done fetching.")
    
    
def get_remote_head_hashnumber(debug: bool) -> str:
    if debug == True:
        hashnumber = os.popen(f"git rev-parse HEAD").read()[:-1]
    else:
        branch_name = os.popen(f"git rev-parse --abbrev-ref HEAD").read()
        hashnumber = os.popen(f"git rev-parse origin/{branch_name}").read()[:-1]
    return hashnumber


class Robot(object):

    def __init__(
        self,
        repository: str,
        debug: bool,
        queryinterval: int 
        ):
        self._debug = debug
        self._query_interval = queryinterval
        self._repository = repository
        focus_dir = f"{repository}/.git/.focus"
        self._focus_file = f"{focus_dir}/focus.json"
        self._change_file = f"{focus_dir}/change.json"
        self._history_file = f"{focus_dir}/history.json"
        self._diff_file = f"{focus_dir}/diff"
        self._hashnumber = ""   # hashnumber of last time
        self._hash_path = f"{focus_dir}/hash"
        if not self._debug:
            fetch_from_origin()
        if os.path.isdir(focus_dir):
            with open(self._hash_path, 'r') as f:
                self._hashnumber = f.readline()
        else:
            os.mkdir(focus_dir)
            hashnumber = get_remote_head_hashnumber(self._debug)
            with open(self._hash_path, 'w') as f:
                f.write(hashnumber)
            focus_json = {}
            focus_json["focus_file_list"] = []
            focus_json["focus_directory_list"] = []
            with open(self._focus_file, 'w') as f:
                json.dump(focus_json, f, indent=4)


    def get_local_head_hashnumber(self) -> str:
        with open(self._hash_path, 'r') as f:
            hashnumber = f.readline()
        return hashnumber


    def renew_hashnumber(self):
        hash_path = self._hash_path
        hashnumber_current = get_remote_head_hashnumber(self._debug)
        self._hashnumber = hashnumber_current
        with open(f'{hash_path}', 'w') as f:
            f.write(hashnumber_current)


    def is_change_happend(self):
        hashnumber = get_remote_head_hashnumber(self._debug)
        return hashnumber != self._hashnumber


    def change2diff(self):
        hashnumber_last = self._hashnumber
        hashnumber_current = get_remote_head_hashnumber(self._debug)
        diff_path = self._diff_file
        change = os.popen(f"git diff {hashnumber_last} {hashnumber_current}").read()
        with open(f'{diff_path}', 'w') as f:
            f.write(change)


    def get_change_list(self) -> list: 
        # get changed files
        hashnumber_last = self._hashnumber
        hashnumber_current = get_remote_head_hashnumber(self._debug)
        change_content = os.popen(f'git diff  {hashnumber_last} {hashnumber_current} --name-only').read().splitlines()
        change_list = []
        for file in change_content:
            record = {}
            if not os.path.isfile(os.path.abspath(file)):
                record["type"] = "file"
                record["stat"] = "deleted"
                record["path"] = f"{file}"
                record["change"] = {
                    "time": "",
                    "author": "",
                    "message": "",
                    "detail": ""
                }
            else:
                s = os.popen(f"git log --pretty=oneline -1 {file}").read()
                commit_id = s[0:s.find(' ')]
                record["type"] = "file"
                record["stat"] = "exist"
                record["path"] = f"{file}"
                record["change"] = {
                    "time": os.popen(f'git log --pretty=format:"%cd" {commit_id} -1').read(),
                    "author": os.popen(f'git log --pretty=format:"%an" {commit_id} -1').read(),
                    "message": os.popen(f'git log --pretty=format:"%s" {commit_id} -1').read(),
                    "detail": ""
                }
            change_list.append(record)
        return change_list


    def get_focus_change_file_list(self, change_list, focus_file_list):
        focus_change_file_list = []
        for change in change_list:
            for focus_file in focus_file_list:
                if change["path"] == focus_file:
                    focus_change_file_list.append(change)
                    break
        return focus_change_file_list


    def get_focus_change_directory_list(self, change_list, focus_directory_list):
        focus_change_directory_list = []
        for change in change_list:
            change_dir = os.path.dirname(change["path"])
            while change_dir != "":
                for focus_directory in focus_directory_list:
                    if change_dir == focus_directory:
                        directory_change_item = {}
                        directory_change_item["type"] = "directory"
                        directory_change_item["stat"] = "exist"
                        directory_change_item["path"] = focus_directory
                        directory_change_item["file"] = change["path"]
                        directory_change_item["change"] = {
                            "time": change["change"]["time"],
                            "author": change["change"]["author"],
                            "message": change["change"]["message"],
                            "detail": ""
                        }
                        focus_change_directory_list.append(directory_change_item)
                        break
                change_dir = os.path.dirname(change_dir)
        return focus_change_directory_list


    def get_focus_change_list(self, change_list: list) -> list:
        # change files to focus files and directories
        fucos_file = self._focus_file
        focus = {}
        if os.path.isfile(fucos_file):
            with open(fucos_file, 'r') as f:
                focus = json.load(f)
        focus_file_list = focus["focus_file_list"]
        focus_directory_list = focus["focus_directory_list"]
        focus_change_list = []
        focus_change_list += self.get_focus_change_file_list(change_list, focus_file_list)
        focus_change_list += self.get_focus_change_directory_list(change_list, focus_directory_list)
        return focus_change_list


    def renew_change(self, focus_change_list: list):
        change_json = {}
        change_json["change_list"] = focus_change_list
        with open(f"{self._change_file}", 'w') as f:
            json.dump(change_json, f, indent=4)


    def renew_history(self, focus_change_list: list):
        history_file = self._history_file
        history = {}
        history["change_list"] = []
        if os.path.isfile(history_file):
            with open(history_file, 'r') as f:
                    history = json.load(f)
        history["change_list"] += focus_change_list
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=4)


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
            else:
                change_list = self.get_change_list()
                focus_change_list = self.get_focus_change_list(change_list)
                self.renew_change(focus_change_list)
                self.renew_history(focus_change_list)
                self.renew_hashnumber()
                sleep(self.query_interval)
            if not self._debug:
                fetch_from_origin()
        # check if the remote repository has changed by query_interval