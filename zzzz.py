from operator import index
import os
import pickle
import shutil
from time import sleep
from focus.Ftree import *


def fetch_from_origin(debug: bool):
    try:
        # print("Fetching new changes from origin......")
        if not debug:
            sh(f"git fetch")
        # print("Done fetching, you don't need to fetch anymore")
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
        merge_base = os.popen(f"git merge-base {branch_name} {remote_name}").read()[:-1]
    except Exception as e:
        print(e)
        exit()
    return hashnumber, merge_base


def path_to_list(path):
    l = []
    dname = os.path.dirname(path)
    bname = os.path.basename(path)
    while dname != "":
        l.append(os.path.basename(dname))
        dname = os.path.dirname(dname)
    l.reverse()
    l.append(bname)
    return l


def find_node(file_path, tree):
    is_find = True
    path_list = path_to_list(file_path)
    node = tree.get_node(tree.root)
    for path in path_list:
        children = tree.children(node.identifier)
        is_exist = False
        for child in children:
            if child.tag == path:
                node = child
                is_exist = True
                break
        if not is_exist:
            is_find = False
    return node, is_find


def add_focus_file(file_path, tree):
    node, is_find = find_node(file_path, tree)
    if is_find:
        node.data.is_focused = True


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
        self._focus_dir = focus_dir
        self._tree_obj = f"{focus_dir}/treeobj"
        self._hash_file = f"{focus_dir}/hash"
        self._merge_base_file = f"{focus_dir}/merge_base"
        self._number_file = f"{focus_dir}/number"
        self._tree: Tree = None
        self._hash = ''
        self._merge_base = ''
        self._change_list = []
        self._change_list_obj = f"{focus_dir}/change_list_obj"
        fetch_from_origin(self._debug)
        if not os.path.isdir(focus_dir):
            self.init()
        else:
            with open(self._tree_obj, 'rb') as f:
                self._tree = pickle.load(f)
            with open(self._change_list_obj, 'rb') as f:
                self._change_list = pickle.load(f)
            with open(self._hash_file, 'r') as f:
                self._hash = f.readline()
            with open(self._merge_base_file, 'r') as f:
                self._merge_base = f.readline()


    def is_remote_changed(self):
        remote_hashnumber, _ = get_remote_head_hashnumber()
        local_hashnumber = get_local_head_hashnumber()
        change_content = os.popen(f"git rev-list --left-right {local_hashnumber}...{remote_hashnumber}").read().splitlines()
        # left = 0
        # right = 0
        # for line in change_content:
        #     if line[0] == '<':
        #         left += 1
        #     elif line[0] == '>':
        #         right += 1
        #     else:
        #         print('error: is_remote_changed error')
        # if right != 0:
        #     return True
        # else:
        #     return False



            
