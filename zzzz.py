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

class Robot(object):

    def __init__(
        self,
        repository: str,
        debug: bool,
        queryinterval: int 
        ):
        self._debug = debug

            