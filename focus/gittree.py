from operator import index
import os
import pickle
import shutil
from time import sleep
from focus.Ftree import add_data, merge_tree, pass_data, rep_ast_tree_construct, sh


def fetch_from_origin(debug: bool):
    try:
        # print("Fetching new changes from origin......")
        if not debug:
            sh(f"git fetch")
        # print("Done fetching, you don't need to fetch anymore")
    except Exception as e:
        print(e)
        exit()
    

def get_local() -> str:
    try:
        hashnumber = os.popen(f"git rev-parse HEAD").read()[:-1]
    except Exception as e:
        print(e)
        exit()
    return hashnumber


def get_branch_name() -> str:
    try:
        branch_name = os.popen(f"git rev-parse --abbrev-ref HEAD").read()[:-1]
    except Exception as e:
        print(e)
        exit()
    return branch_name


def get_remote_and_mergebase() -> str:
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


def defalut_tree_construct():
    remote_hashnumber, merge_base = get_remote_and_mergebase()
    tree = get_tree_by_two_hash(merge_base, remote_hashnumber)
    hash_list = os.popen(f"git rev-list  {merge_base}...{remote_hashnumber}").read().splitlines()
    hash_list.append(merge_base)
    hash_list.reverse()
    for index in range(len(hash_list) - 1):
        last_hash = hash_list[index]
        curren_hash = hash_list[index + 1]
        temp_tree = get_tree_by_two_hash(last_hash, curren_hash)
        time = os.popen(f'git log --pretty=format:"%ci" {curren_hash} -1').read()
        time = time[: time.rfind(" ")]
        author = os.popen(f'git log --pretty=format:"%an" {curren_hash} -1').read()
        message = os.popen(f'git log --pretty=format:"%s" {curren_hash} -1').read()
        add_data(temp_tree, time, author, message)
        pass_data(temp_tree, tree, detail=True)
    return tree


def get_tree_by_two_hash(hash1, hash2):
    branch_name = get_branch_name()
    sh(f"git checkout {hash1}")
    last_tree = rep_ast_tree_construct()
    sh(f"git checkout {hash2}")
    current_tree = rep_ast_tree_construct()
    sh(f"git checkout {branch_name}")
    tree = merge_tree(last_tree, current_tree)
    return tree


# class Robot(object):
#     def __init__(
#         self,
#         repository: str,
#         debug: bool,
#         queryinterval: int 
#         ):
#         self._debug = debug
#         self._query_interval = queryinterval
#         self._repository = repository
#         focus_dir = f"{repository}/.git/.focus"
#         self._focus_dir = focus_dir
#         self._tree_obj = f"{focus_dir}/treeobj"
#         self._hash_file = f"{focus_dir}/hash"
#         self._merge_base_file = f"{focus_dir}/merge_base"
#         self._number_file = f"{focus_dir}/number"
#         self._tree: Tree = None
#         self._hash = ''
#         self._merge_base = ''
#         self._change_list = []
#         self._change_list_obj = f"{focus_dir}/change_list_obj"
#         if not os.path.isdir(focus_dir):
#             os.mkdir(focus_dir)
#             tree = defalut_tree_construct()
#             self._tree = tree
#             self.tree_dump()
#         else:
#             with open(self._tree_obj, 'rb') as f:
#                 self._tree = pickle.load(f)

    
#     def is_remote_changed(self):
#         remote_hashnumber, _ = get_remote_and_mergebase()
#         local_hashnumber = get_local()
#         change_content = os.popen(f"git rev-list --left-right {local_hashnumber}...{remote_hashnumber}").read().splitlines()
#         left = 0
#         right = 0
#         for line in change_content:
#             if line[0] == '<':
#                 left += 1
#             elif line[0] == '>':
#                 right += 1
#             else:
#                 print('error: is_remote_changed error')
#         if right != 0:
#             return True
#         else:
#             return False

    
#     def tree_need_change(self):
#         hash_number, merge_base = get_remote_and_mergebase()
#         if self._hash != hash_number or self._merge_base != merge_base:
#             return True
#         return False


#     def tree_update(self):
#         remote_hashnumber, _ = get_remote_and_mergebase()
#         branch_name = os.popen(f"git rev-parse --abbrev-ref HEAD").read()[:-1]
#         number = self.load_number()
#         sh(f"git checkout {remote_hashnumber}")
#         current_tree, number = get_rep_construct(number)
#         sh(f"git checkout {branch_name}")
#         ftree, number = merge_tree(self._tree, current_tree, number)
#         adjust_tree_path(ftree)
#         self.dump_number(number)
#         self._tree = ftree
#         with open(self._hash_file, 'w') as f:
#             f.write(remote_hashnumber)
#         self.tree_dump()


#     def get_last_change_dic(self):
#         remote_hashnumber, merge_base = get_remote_and_mergebase()
#         hash_list = os.popen(f"git rev-list  {merge_base}...{remote_hashnumber}").read().splitlines()
#         hash_list.append(merge_base)
#         last_change_dic = {}
#         for index in range(len(hash_list) - 1):
#             curren_hash = hash_list[index]
#             last_hash = hash_list[index + 1]
#             change_content = os.popen(f'git diff  {curren_hash} {last_hash} --name-only').read().splitlines()
#             for file in change_content:
#                 if last_change_dic.get(file, 0) == 0:
#                     last_change_dic[file] = curren_hash
#         sorted_dic_list = sorted(last_change_dic.items(), key=lambda x:x[0])
#         sorted_dic = {}
#         for item in sorted_dic_list:
#             sorted_dic[item[0]] = item[1]
#         return sorted_dic


#     def last_change_dic_to_change_list(self):
#         dic = self.get_last_change_dic()
#         change_list = []
#         yourself = os.popen('git config user.name').read()[:-1]
#         for file in dic:
#             last_change_hash = dic[file]
#             record = {}
#             record["path"] = f"{file}"
#             record["type"] = "file"
#             time = os.popen(f'git log --pretty=format:"%ci" {last_change_hash} -1').read()
#             time = time[: time.rfind(" ")]
#             record["change"] = {
#                 "time": time,
#                 "author": os.popen(f'git log --pretty=format:"%an" {last_change_hash} -1').read(),
#                 "message": os.popen(f'git log --pretty=format:"%s" {last_change_hash} -1').read(),
#             }
#             # if record["change"]["author"] == yourself:
#             #     continue
#             change_list.append(record)
#         change_list.sort(key=lambda x:x["path"])
#         return change_list


#     def record_leaf_to_root(self, record, node: Node, tree: Tree):
#         node.data.type = "file"
#         node.data.time = record["change"]["time"]
#         node.data.author = record["change"]["author"]
#         node.data.message = record["change"]["message"]
#         node.data.is_changed = True
#         root = tree.get_node(tree.root)
#         dire = tree.parent(node.identifier)
#         while dire != root:
#             dire.data.type = "dir"
#             if dire.data.time == "" or record["change"]["time"] > dire.data.time:
#                 dire.data.time = record["change"]["time"]
#                 dire.data.author = record["change"]["author"]
#                 dire.data.message = record["change"]["message"]
#             if node.data.path not in dire.data.file:
#                 dire.data.file.append(node.data.path)
#             dire.data.is_changed = True
#             dire = tree.parent(dire.identifier)
            
    
#     def get_records_from_leaf(self, node: Node):
#         records = []
#         tree = self._tree
#         root = tree.get_node(tree.root)
#         while node != root:
#             if node.data.is_focused == True:
#                 record = {}
#                 record["path"] = node.data.path
#                 record["type"] = node.data.type
#                 record["status"] = node.data.fstatus
#                 record["file"] = node.data.file
#                 record["change"] = {
#                     "time": node.data.time,
#                     "author": node.data.author,
#                     "message": node.data.message,
#                 }
#                 records.append(record)
#             node = self._tree.parent(node.identifier)
#         return records


#     def adjust_change_list_to_tree(self, change_list: list, tree: Tree):
#         children = tree.leaves()
#         lengthl = len(change_list)
#         indexl = 0
#         indext = 0
#         while indexl < lengthl:
#             record = change_list[indexl]
#             node = children[indext]
#             pathl = record["path"]
#             patht = node.data.path
#             if patht == pathl:
#                 indexl += 1
#                 indext += 1
#                 self.record_leaf_to_root(record, node, tree)
#             elif pathl > patht:
#                 indext += 1
#             elif pathl < patht:
#                 print("error: adjust_change_list_to_tree")
#                 exit()


#     def get_show_list(self):
#         focus_list = []
#         root: Node = tree.get_node(tree.root)
#         queue = Queue()
#         queue.put(root)
#         while not queue.empty():
#             node: Node = queue.get()
#             children = tree.children(node.identifier)
#             for child in children:
#                 if child.data.is_focused == True and child.data.status != 0:
#                     focus_list.append((node.data.type, node.data.path))
#                 queue.put(node)
#         return focus_list





#     def focus_inherit(self, dead_tree, tree):
#         focus_file_list, focus_directory_list = self.get_focus_list(dead_tree)
#         focus_list = focus_file_list + focus_directory_list
#         for item in focus_list:
#             add_focus_file(item, tree)


#     @property
#     def query_interval(self):
#         return self._query_interval

#     @query_interval.setter
#     def query_interval(self, query_interval):
#         self._query_interval = query_interval


#     def init(self):
#         dead_tree = None
#         if os.path.isfile(self._tree_obj):
#             dead_tree = self.tree_load()
#         if os.path.isdir(self._focus_dir):
#             self.rm_focus()
#         os.mkdir(self._focus_dir)
#         self.dump_number(0)
#         hash_number, merge_base = get_remote_and_mergebase()
#         with open(self._hash_file, 'w') as f:
#             f.write(hash_number)
#         self._hash = hash_number
#         with open(self._merge_base_file, 'w') as f:
#             f.write(merge_base)
#         self._merge_base = merge_base
#         branch_name = os.popen(f"git rev-parse --abbrev-ref HEAD").read()[:-1]
#         number = self.load_number()
#         sh(f"git checkout {merge_base}")
#         last_tree, number = get_rep_construct(number)
#         sh(f"git checkout {hash_number}")
#         current_tree, number = get_rep_construct(number)
#         sh(f"git checkout {branch_name}")
#         ftree, number = merge_tree(last_tree, current_tree, number)        
#         self.dump_number(number)
#         adjust_tree_path(ftree)
#         change_list = self.last_change_dic_to_change_list()
#         with open(self._change_list_obj, 'wb') as f:
#             pickle.dump(change_list, f)
#         self._change_list = change_list
#         self.adjust_change_list_to_tree(change_list, ftree)
#         if dead_tree != None:
#             self.pass_focus(dead_tree, ftree)
#         self._tree = ftree
#         self.tree_dump()


#     def tree_dump(self):
#         with open(self._tree_obj, 'wb') as f:
#             pickle.dump(self._tree, f)


#     def tree_load(self):
#         with open(self._tree_obj, 'rb') as f:
#             tree = pickle.load(f)
#         return tree


#     def rm_focus(self):
#         shutil.rmtree(self._focus_dir)


#     def run(self):
#         # self.test()
#         # exit()
#         self._tree.show()
#         self._tree.show(data_property="is_focused")
#         self._tree.show(data_property="path")
#         # self._tree.show(data_property="file")
#         # self._tree.show(data_property="author")
#         while True:
#             sleep(self.query_interval)
#             fetch_from_origin(self._debug)
#             if self.tree_need_change():
#                 self.init()
#         # check if the remote repository has changed by query_interval

#     def test(self):
#         hash_number, merge_base = get_remote_and_mergebase()
#         branch_name = os.popen(f"git rev-parse --abbrev-ref HEAD").read()[:-1]
#         number = self.load_number()
#         sh(f"git checkout {merge_base}")
#         last_tree, number = get_rep_construct(number)
#         sh(f"git checkout {hash_number}")
#         current_tree, number = get_rep_construct(number)
#         sh(f"git checkout {branch_name}")
#         ftree, number = merge_tree(last_tree, current_tree, number)
#         adjust_tree_path(ftree)
#         self.dump_number(number)
#         self._tree.show(data_property="is_focused")
#         ftree.show(data_property="is_focused")
#         self.pass_focus(self._tree, ftree)
#         ftree.show(data_property="is_focused")