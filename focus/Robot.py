import os
import json
import pickle
from time import sleep
from focus.Ftree import *


def fetch_from_origin(debug: bool):
    try:
        print("Fetching new changes from origin......")
        if not debug:
            sh(f"git fetch")
        print("Done fetching, you don't need to fetch anymore")
    except Exception as e:
        print(e)
        exit()
    

def get_local_head_hashnumber() -> str:
    try:
        hashnumber = os.popen(f"git rev-parse HEAD").read()[:-1]
    except Exception as e:
        print(e)
        exit()
    return hashnumber


def get_remote_head_hashnumber() -> str:
    try:
        branch_name = os.popen(f"git rev-parse --abbrev-ref HEAD").read()[:-1]
        upstream = '{upstream}'
        remote_name = os.popen(f"git rev-parse --abbrev-ref {branch_name}@{upstream}").read()[:-1]
        hashnumber = os.popen(f"git rev-parse {remote_name}").read()[:-1]
    except Exception as e:
        print(e)
        exit()
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
        self._tree_obj = f"{focus_dir}/treeobj"
        self._hash_file = f"{focus_dir}/hash"
        self._number_file = f"{focus_dir}/number"
        self._tree: Tree = None
        self._hash = ''
        self._change_list = []
        fetch_from_origin(self._debug)
        if not os.path.isdir(focus_dir):
            os.mkdir(focus_dir)
            focus_json = {}
            focus_json["focus_file_list"] = []
            focus_json["focus_directory_list"] = []
            with open(self._focus_file, 'w') as f:
                json.dump(focus_json, f, indent=4)
            self.dump_number(0)
            hash_number = get_remote_head_hashnumber()
            with open(self._hash_file, 'w') as f:
                f.write(hash_number)
            self._hash = hash_number
            self.ftree_init()
        else:
            with open(self._tree_obj, 'rb') as f:
                self._tree = pickle.load(f)
            with open(self._hash_file, 'r') as f:
                self._hash = f.readline()
        history_json = {}
        history_json["change_list"] = []
        with open(self._history_file, 'w') as f:
            json.dump(history_json, f, indent=4)
        change_json = {}
        change_json["change_list"] = []
        with open(self._change_file, 'w') as f:
            json.dump(change_json, f, indent=4)


    def is_remote_changed(self):
        if self.tree_need_change():
            self.tree_update()
        history_json = {}
        history_json["change_list"] = []
        with open(self._history_file, 'w') as f:
            json.dump(history_json, f, indent=4)
        change_json = {}
        change_json["change_list"] = []
        with open(self._change_file, 'w') as f:
            json.dump(change_json, f, indent=4)
        remote_hashnumber = get_remote_head_hashnumber()
        local_hashnumber = get_local_head_hashnumber()
        change_content = os.popen(f"git rev-list --left-right {local_hashnumber}...{remote_hashnumber}").read().splitlines()
        left = 0
        right = 0
        for line in change_content:
            if line[0] == '<':
                left += 1
            elif line[0] == '>':
                right += 1
            else:
                print('error: is_remote_changed error')
        if right != 0:
            return True
        else:
            return False

    
    def tree_need_change(self):
        hash_number = get_remote_head_hashnumber()
        return self._hash != hash_number


    def tree_update(self):
        remote_hashnumber = get_remote_head_hashnumber()
        branch_name = os.popen(f"git rev-parse --abbrev-ref HEAD").read()[:-1]
        number = self.load_number()
        sh(f"git checkout {remote_hashnumber}")
        current_tree, number = get_rep_construct(number)
        sh(f"git checkout {branch_name}")
        ftree, number = merge_tree(self._tree, current_tree, number)
        adjust_tree_path(ftree)
        self.dump_number(number)
        self._tree = ftree
        with open(self._hash_file, 'w') as f:
            f.write(remote_hashnumber)
        self.tree_dump()


    def get_last_change_dic(self):
        remote_hashnumber = get_remote_head_hashnumber()
        local_hashnumber = get_local_head_hashnumber()
        merge_base = os.popen(f"git merge-base {remote_hashnumber} {local_hashnumber}").read()[:-1]
        hash_list = os.popen(f"git rev-list  {merge_base}...{remote_hashnumber}").read().splitlines()
        hash_list.append(merge_base)
        last_change_dic = {}
        for index in range(len(hash_list) - 1):
            curren_hash = hash_list[index]
            last_hash = hash_list[index + 1]
            change_content = os.popen(f'git diff  {curren_hash} {last_hash} --name-only').read().splitlines()
            for file in change_content:
                if last_change_dic.get(file, 0) == 0:
                    last_change_dic[file] = curren_hash
        sorted_dic_list = sorted(last_change_dic.items(), key=lambda x:x[0])
        sorted_dic = {}
        for item in sorted_dic_list:
            sorted_dic[item[0]] = item[1]
        return sorted_dic


    def last_change_dic_to_change_list(self, dic: dict):
        change_list = []
        yourself = os.popen('git config user.name').read()[:-1]
        for file in dic:
            last_change_hash = dic[file]
            record = {}
            record["path"] = f"{file}"
            record["type"] = "file"
            time = os.popen(f'git log --pretty=format:"%ci" {last_change_hash} -1').read()
            time = time[: time.rfind(" ")]
            record["change"] = {
                "time": time,
                "author": os.popen(f'git log --pretty=format:"%an" {last_change_hash} -1').read(),
                "message": os.popen(f'git log --pretty=format:"%s" {last_change_hash} -1').read(),
            }
            # if record["change"]["author"] == yourself:
            #     continue
            change_list.append(record)
        change_list.sort(key=lambda x:x["path"])
        return change_list


    def record_leaf_to_root(self, record, node: Node):
        node.data.type = "file"
        node.data.time = record["change"]["time"]
        node.data.author = record["change"]["author"]
        node.data.message = record["change"]["message"]
        node.data.is_changed = True
        tree = self._tree
        root = tree.get_node(tree.root)
        dire = tree.parent(node.identifier)
        while dire != root:
            dire.data.type = "dir"
            if dire.data.time == "" or record["change"]["time"] > dire.data.time:
                dire.data.time = record["change"]["time"]
            dire.data.author = record["change"]["author"]
            dire.data.message = record["change"]["message"]
            if node.data.path not in dire.data.file:
                dire.data.file.append(node.data.path)
            dire.data.is_changed = True
            dire = self._tree.parent(dire.identifier)
            
    
    def get_records_from_leaf(self, node: Node):
        records = []
        tree = self._tree
        root = tree.get_node(tree.root)
        while node != root:
            if node.data.is_focused == True:
                record = {}
                record["path"] = node.data.path
                record["type"] = node.data.type
                record["status"] = node.data.fstatus
                record["file"] = node.data.file
                record["change"] = {
                    "time": node.data.time,
                    "author": node.data.author,
                    "message": node.data.message,
                }
                records.append(record)
            node = self._tree.parent(node.identifier)
        return records


    def adjust_change_list_to_tree(self, change_list: list):
        children = self._tree.leaves()
        lengthl = len(change_list)
        indexl = 0
        indext = 0
        while indexl < lengthl:
            record = change_list[indexl]
            node = children[indext]
            pathl = record["path"]
            patht = node.data.path
            if patht == pathl:
                indexl += 1
                indext += 1
                self.record_leaf_to_root(record, node)
            elif pathl > patht:
                indext += 1
            elif pathl < patht:
                print("error: adjust_change_list_to_tree")
        
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
                        directory_change_item["path"] = focus_directory
                        directory_change_item["file"] = change["path"]
                        directory_change_item["change"] = {
                            "time": change["change"]["time"],
                            "author": change["change"]["author"],
                            "message": change["change"]["message"],
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
        with open(self._change_file, 'w') as f:
            json.dump(change_json, f, indent=4)


    def renew_history(self, change_list: list):
        history_json = {}
        history_json["change_list"] = change_list
        with open(self._history_file, 'w') as f:
            json.dump(history_json, f, indent=4)


    def get_show_list(self):
        show_list = []
        change_list = self._change_list
        children = self._tree.leaves()
        lengthl = len(change_list)
        indexl = 0
        indext = 0
        while indexl < lengthl:
            record = change_list[indexl]
            node = children[indext]
            pathl = record["path"]
            patht = node.data.path
            if patht == pathl:
                indexl += 1
                indext += 1
                records = self.get_records_from_leaf(node)
                for one in records:
                    if one not in show_list:
                        show_list.append(one)
            elif pathl > patht:
                indext += 1
            elif pathl < patht:
                print("error: adjust_change_list_to_tree")
        return show_list


    def get_focus_list(self):
        focus_file_list = []
        focus_directory_list = []
        tree = self._tree
        root: Node = tree.get_node(tree.root)
        pqueue = Queue()
        pqueue.put(root)
        while not pqueue.empty():
            pqueue_temp = Queue()
            while not pqueue.empty():
                pnode: Node = pqueue.get()
                children = tree.children(pnode.identifier)
                for node in children:
                    if node.data.is_focused == True:
                        if node.data.type == "dir":
                            focus_directory_list.append(node.data.path)
                        if node.data.type == "file":
                            focus_file_list.append(node.data.path)
                    pqueue_temp.put(node)
            pqueue = pqueue_temp
        return focus_file_list, focus_directory_list


    @property
    def query_interval(self):
        return self._query_interval

    @query_interval.setter
    def query_interval(self, query_interval):
        self._query_interval = query_interval
    
    def change_parse(self):
        # self._tree.show()
        # self._tree.show(data_property="is_focused")
        # self._tree.show(data_property="path")
        # self._tree.show(data_property="file")
        last_change_dic = self.get_last_change_dic()
        change_list = self.last_change_dic_to_change_list(last_change_dic)
        self._change_list = change_list
        self.adjust_change_list_to_tree(change_list)
        self.tree_dump()
        focus_change_list = self.get_focus_change_list(change_list)
        self.renew_history(change_list)
        self.renew_change(focus_change_list)
        

    
    def ftree_init(self):
        remote_hashnumber = get_remote_head_hashnumber()
        local_hashnumber = get_local_head_hashnumber()
        merge_base = os.popen(f"git merge-base {remote_hashnumber} {local_hashnumber}").read()[:-1]
        branch_name = os.popen(f"git rev-parse --abbrev-ref HEAD").read()[:-1]
        sh(f"git checkout {merge_base}")
        number = self.load_number()
        last_tree, number = get_rep_construct(number)
        sh(f"git checkout {remote_hashnumber}")
        current_tree, number = get_rep_construct(number)
        sh(f"git checkout {branch_name}")
        ftree, number = merge_tree(last_tree, current_tree, number)
        adjust_tree_path(ftree)
        self.dump_number(number)
        self._tree = ftree
        self.tree_dump()
    
    
    def tree_dump(self):
        with open(self._tree_obj, 'wb') as f:
            pickle.dump(self._tree, f)
    
    
    def tree_load(self):
        with open(self._tree_obj, 'rb') as f:
            tree = pickle.load(f)
        return tree


    def load_number(self):
        with open(self._number_file, 'r') as f:
            number = f.readline()
        return int(number)


    def dump_number(self, number):
        with open(self._number_file, 'w') as f:
            f.write(str(number))


    def run(self):
        while True:
            sleep(self.query_interval)
            fetch_from_origin(self._debug)
            if self.is_remote_changed():
                self.change_parse()
        # check if the remote repository has changed by query_interval