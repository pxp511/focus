import os
import json
from time import sleep

DEBUG_MODEL = False

def get_remote_head_hashnumber() -> str:
    if DEBUG_MODEL == True:
        hashnumber = os.popen(f"git rev-parse HEAD").read()[:-1]
    else:
        branch_name = os.popen(f"git rev-parse --abbrev-ref HEAD").read()
        hashnumber = os.popen(f"git rev-parse origin/{branch_name}").read()[:-1]
    return hashnumber
    

def get_change_from_diff_file(diff_file: str):
    lines = open(diff_file, 'r').readlines()
    fpath = ''
    result = []
    detail = ''
    for line in lines:
        record = {}
        if is_file_line(line):
            fpath = get_filename_by_diff_line(line)
            record["type"] = "file"
            record["file_path"] = f"{fpath}"
            record["block_name"] =  ""
            record["change"] = {
                "time": "",
                "detail": f"{detail}"
            }
            result.append(record)
            detail = ''
        elif is_block_line(line):
            block = get_block_by_diff_line(line)
            record["type"] = "block"
            record["file_path"] = f"{fpath}"
            record["block_name"] =  f"{block}"
            record["change"] = {
                "time": "",
                "detail": f"{detail}"
            }
            result.append(record)
            detail = ''
        else:
            detail += line
    return result


def is_file_line(s: str):
    # whether this line indicate a file
    return s[: 10] == 'diff --git'

def is_block_line(s: str):
    # whether this line indicate a code block
    result = True
    result = result and s[:2] == '@@'
    index = s.rfind('@@')
    res_of_blank_line = index + 2 != len(s) - 1
    result = result and res_of_blank_line
    return result

def get_filename_by_diff_line(s: str):
    # get file path from this line
    index = s.find(' b/')
    fpath = s[13:index]
    return fpath

def get_block_by_diff_line(s: str):
    # get code block name from this line
    index = s.rfind('@@')
    block = s[index + 3:-1]
    return block

def is_block(s: str):
    # whether is a valid block
    return True

def is_file(s: str):
    # whether is a valid file
    return True


class Robot(object):

    def __init__(
        self,
        repository: str,
        ):
        self._query_interval = 10
        self._repository = repository
        focus_dir = f"{repository}/.git/.focus"
        self._focus_file = f"{focus_dir}/focus.json"
        self._change_file = f"{focus_dir}/change.json"
        self._history_file = f"{focus_dir}/history.json"
        self._diff_file = f"{focus_dir}/diff"
        self._hashnumber = ""   # hashnumber of last time
        self._hash_path = f"{focus_dir}/hash"
        if DEBUG_MODEL == False:
            print("Fetching new changes from origin......")
            os.system(f"git fetch")
        if os.path.isdir(focus_dir):
            with open(self._hash_path, 'r') as f:
                self._hashnumber = f.readline()
        else:
            os.mkdir(focus_dir)
            hashnumber = get_remote_head_hashnumber()
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
        hashnumber_current = get_remote_head_hashnumber()
        self._hashnumber = hashnumber_current
        with open(f'{hash_path}', 'w') as f:
            f.write(hashnumber_current)


    def is_change_happend(self):
        hashnumber = get_remote_head_hashnumber()
        print(hashnumber, self._hashnumber)
        return hashnumber != self._hashnumber


    def change2diff(self):
        hashnumber_last = self._hashnumber
        hashnumber_current = get_remote_head_hashnumber()
        diff_path = self._diff_file
        change = os.popen(f"git diff {hashnumber_last} {hashnumber_current}").read()
        with open(f'{diff_path}', 'w') as f:
            f.write(change)


    def get_change_list(self) -> list: 
        # get changed files
        hashnumber_last = self._hashnumber
        hashnumber_current = get_remote_head_hashnumber()
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


    def diff2history(self):
        # get the change from the remote repository and add to history file
        diff_path = self._diff_file
        history_file = self._history_file
        
        history = {}
        history["change_list"] = []
        if os.path.isfile(history_file):
            with open(history_file, 'r') as f:
                    history = json.load(f)
                    
        result = get_change_from_diff_file(diff_path)
        
        history["change_list"] += result
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=4) 


    def change2focus_history(self):
        # cross-compare history.json and focus.json, then add the changes which user concerns to focus_history.json
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
        if os.path.isfile(self._change_file):
            with open(self._change_file, 'r') as f:
                history_json = json.load(f)
        history = history_json["change_list"]
        result = []
        for record in history:
            if record["type"] == "file":
                for file_path in focus_file:
                    if record["path"] == file_path:
                        result.append(record)
                        break
            elif record["type"] == "block":
                for block in focus_block:
                    if record["path"] == block["path"] and record["block_name"] == block["block_name"]:
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
        # check if the remote repository has changed by query_interval
    