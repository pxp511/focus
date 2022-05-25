import os
import subprocess
from queue import Queue
from treelib import Tree, Node
from focus.astutils import ast_parse, get_children, get_name, get_type, get_value

def is_changed_to_status(is_changed):
    if is_changed == True:
        status = 2
    else:
        status = 0
    return status

def sh(command):
    try:
        if isinstance(command, list):
            command = ' '.join(command)
        return subprocess.check_output(
            command, shell=True,
            stderr=subprocess.STDOUT).decode('utf-8').rstrip()
    except Exception as e:
        return None


class Fnode(object):
    def __init__(
        self,
        status = 0,
        type = '',
        path = '',
        time = '',
        author = '',
        message = '',
        is_focused = False,
        value = ""
        ):
        self.is_focused = is_focused
        self.status = status
        self.type = type
        self.value = value
        # 0: 未修改
        # 2: 修改态
        # -1: 删除态
        # 1: 新增态
        self.path = path
        self.time = time
        self.author = author
        self.message = message


# tree = Tree() # 建树
# root = tree.create_node(1, 1)  # 根节点
# node2 = tree.create_node(2, 2, parent=1) # 创建节点
# tree.show() # 展示树
# print(tree.identifier)  # 获取该树的ID
# tree.subtree(3).show()  # 获取子树
# print(tree.nodes)  # 所有节点（dict形式）
# print(tree.all_nodes())  # 所有节点
# print(tree.all_nodes_itr())  # 所有节点的迭代器
# print(tree.get_node(4))  # 获取某节点
# print(tree.parent(4))  # 获取父节点
# print(tree.children(3))  # 获取子节点
# print(tree.siblings(4))  # 获取兄弟节点
# print(tree.leaves())  # 获取所有叶子节点
# print(tree.contains(99))  # 是否包含某ID节点
# print(tree.is_ancestor(3, 4))  # 是否父节点
# print([i for i in tree.rsearch(4)])  # 向根节点遍历
# print(tree.size(2))  # 某一层级的节点数

def get_rep_construct(path = ""):
    tree = Tree()
    if path == "":
        path = os.getcwd()
    root = tree.create_node(path, data=Fnode(0, path=path))
    pqueue = Queue()
    pqueue.put(root)
    while not pqueue.empty():
        pqueue_temp = Queue()
        while not pqueue.empty():
            pnode = pqueue.get()
            path = pnode.data.path
            if os.path.isdir(path):
                pnode.data.type = "dir"
                for item in sorted(os.listdir(path)):
                    if item[0] == "." or item == "__pycache__":
                        continue
                    node = tree.create_node(item, parent=pnode.identifier, data=Fnode(0, path=os.path.join(path, item)))
                    pqueue_temp.put(node)
            else:
                pnode.data.type = "file"
        pqueue = pqueue_temp
    return tree


def merge_tree_entity(tree1: Tree, tree2: Tree):
    assert not(tree1 == None and tree2 == None)
    if tree1 is None:
        tree2.get_node(tree2.root).data.status = 1
        return tree2
    if tree2 is None:
        tree1.get_node(tree1.root).data.status = -1
        return tree1
    root1: Node = tree1.get_node(tree1.root)
    root2: Node = tree2.get_node(tree2.root)
    assert root1.tag == root2.tag
    new_tree = Tree()
    new_tree.create_node(root1.tag)
    if tree1.depth() == 0 and tree2.depth() == 0:
        is_changed = root1.data.value != root2.data.value
        status = is_changed_to_status(is_changed)
        new_tree.get_node(new_tree.root).data = Fnode(status=status,  path=root1.data.path, type=root1.data.type)
        return new_tree
    children1 = tree1.children(root1.identifier)
    children2 = tree2.children(root2.identifier)
    index1 = 0
    index2 = 0
    length1 = len(children1)
    length2 = len(children2)
    while index1 < length1 and index2 < length2:
        node1: Node = children1[index1]
        node2: Node = children2[index2]
        if node1.tag == node2.tag:
            subtree1 = tree1.subtree(node1.identifier)
            subtree2 = tree2.subtree(node2.identifier)
            is_changed = node1.data.value != node2.data.value
            status = is_changed_to_status(is_changed)
            subtree = merge_tree_entity(subtree1, subtree2)
            subtree.get_node(subtree.root).data = Fnode(status=status, path=node1.data.path, type=node1.data.type)
            index1 += 1
            index2 += 1
        elif node1.tag < node2.tag:
            subtree = tree1.subtree(node1.identifier)
            subtree.get_node(subtree.root).data.status = -1
            index1 += 1
        elif node1.tag > node2.tag:
            subtree = tree2.subtree(node2.identifier)
            subtree.get_node(subtree.root).data.status = 1
            index2 += 1
        new_tree.paste(new_tree.root, subtree)
    while index1 < length1:
        node1: Node = children1[index1]
        subtree = tree1.subtree(node1.identifier)
        subtree.get_node(subtree.root).data.status = -1
        new_tree.paste(new_tree.root, subtree)
        index1 += 1
    while index2 < length2:
        node2: Node = children2[index2]
        subtree = tree2.subtree(node2.identifier)
        subtree.get_node(subtree.root).data.status = 1
        new_tree.paste(new_tree.root, subtree)
        index2 += 1
    return new_tree


def merge_tree(tree1: Tree, tree2: Tree):
    tree = merge_tree_entity(tree1, tree2)
    tree.get_node(tree.root).data = Fnode(status=0, type="dir", path=tree1.get_node(tree1.root).data.path)
    adjust_status(tree)
    return tree

# status = node.data.status
# if status == 0:
#     node.data.fstatus = 'need merge'
# elif status == 1:
#     node.data.fstatus = 'new'
# elif status == 2:
#     node.data.fstatus = ''
# elif status == -1:
#     node.data.fstatus = 'deleted'
# else:
#     print("error: adjust tree")
def adjust_status(tree: Tree):
    root: Node = tree.get_node(tree.root)
    queue = Queue()
    queue.put(root)
    while not queue.empty():
        pnode: Node = queue.get()
        pstatus = pnode.data.status
        children = tree.children(pnode.identifier)
        for child in children:
            if pstatus in [1, -1]:
                child.data.status = pstatus
            queue.put(child)
    leaves = tree.leaves()
    for leaf in leaves:
        node: Node = leaf
        while node != root:
            pnode = tree.parent(node.identifier)
            if node.data.status in [1, -1, 2] and pnode.data.status == 0:
                pnode.data.status = 2
            node = pnode
    return tree

def is_tag_in_children(tree: Tree, node: Node, tag: str):
    children = tree.children(node.identifier)
    for child in children:
        if tag == child.tag:
            return True
    return False

def get_ast_construct(path):
    ast_root = ast_parse(path)
    tree = Tree()
    root = tree.create_node(get_name(ast_root), data=Fnode(0, path=path))
    ast_queue = Queue()
    ast_queue.put(ast_root)
    queue = Queue()
    queue.put(root)
    while not ast_queue.empty():        
        ast_pnode = ast_queue.get()
        pnode = queue.get()
        ast_children = get_children(ast_pnode)
        for ast_child in ast_children:
            ast_queue.put(ast_child)
            ast_child_name = get_name(ast_child)
            if is_tag_in_children(tree, pnode, ast_child_name):
                node = tree.create_node("", parent=pnode.identifier, data=Fnode(0, path=path))
            else:
                node = tree.create_node(ast_child_name, parent=pnode.identifier, data=Fnode(0, path=os.path.join(pnode.data.path, ast_child_name), type=get_type(ast_child), value=get_value(ast_child)))
            queue.put(node)
    queue = Queue()
    queue.put(tree.get_node(tree.root))
    while not queue.empty():        
        pnode = queue.get()
        if pnode.tag == "":
            tree.remove_node(pnode.identifier)
            continue
        children = tree.children(pnode.identifier)
        for child in children:
            queue.put(child)
    return tree

def rep_ast_tree_construct(path = ""):
    if path == "":
        path = os.getcwd()
    tree = get_rep_construct(path)
    leaves = tree.leaves()
    for node in leaves:
        file_path = node.data.path
        if file_path[-3:] != '.py':
            continue
        ast_tree = get_ast_construct(file_path)
        
        for child in ast_tree.children(ast_tree.root):
            subasttree = ast_tree.subtree(child.identifier)
            tree.paste(node.identifier, subasttree)
    root = tree.get_node(tree.root)
    root.tag = os.path.basename(root.data.path)
    return tree


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


def find_node(tree, file_path):
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
            return None
    return node


def add_focus(tree, file_path):
    node = find_node(tree, file_path)
    if node != None:
        node.data.is_focused = True
        return True
    else:
        return False


def delete_focus(tree, file_path):
    node = find_node(tree, file_path)
    if node != None:
        node.data.is_focused = False
        return True
    else:
        return False


def add_data(tree, time="", author="", message=""):
    root: Node = tree.get_node(tree.root)
    queue = Queue()
    queue.put(root)
    while not queue.empty():
        node: Node = queue.get()
        if node.data.status != 0:
            node.data.time = time
            node.data.author = author
            node.data.message = message
        children = tree.children(node.identifier)
        for child in children:
            queue.put(child)
    

# self.is_focused = is_focused
# self.status = status
# self.type = type
# self.value = value
# # 0: 未修改
# # 2: 修改态
# # -1: 删除态
# # 1: 新增态
# self.path = path
# self.time = time
# self.author = author
# self.message = message
def pass_data(tree1: Tree, tree2: Tree, is_focused=False, detail=False):
    root1: Node = tree1.get_node(tree1.root)
    root2: Node = tree2.get_node(tree2.root)
    assert root1.tag == root2.tag
    queue1 = Queue()
    queue2 = Queue()
    queue1.put(root1)
    queue2.put(root2)
    while not (queue1.empty() and queue2.empty()):
        list1 = []
        list2 = []
        queue1_t = Queue()
        queue2_t = Queue()
        while not queue1.empty():
            node: Node = queue1.get()
            children = tree1.children(node.identifier)
            for child in children:
                queue1_t.put(child)
            list1.append(node)
        while not queue2.empty():
            node: Node = queue2.get()
            children = tree2.children(node.identifier)
            for child in children:
                queue2_t.put(child)
            list2.append(node)
        queue1 = queue1_t
        queue2 = queue2_t
        index1 = 0
        index2 = 0
        length1 = len(list1)
        length2 = len(list2)
        while index1 < length1 and index2 < length2:
            node1 = list1[index1]
            node2 = list2[index2]
            path1 = node1.data.path
            path2 = node2.data.path
            if path1 == path2:
                if is_focused == True:
                    if node1.data.is_focused == True:
                        node2.data.is_focused = node1.data.is_focused
                if detail == True:
                    if node1.data.time != "":
                        node2.data.time = node1.data.time
                    if node1.data.author != "":
                        node2.data.author = node1.data.author
                    if node1.data.message != "":
                        node2.data.message = node1.data.message
                index1 += 1
                index2 += 1
            elif path1 < path2:
                index1 += 1
            elif path1 > path2:
                index2 += 1


def get_focus(tree):
    focus_list = []
    root: Node = tree.get_node(tree.root)
    queue = Queue()
    queue.put(root)
    while not queue.empty():
        node: Node = queue.get()
        children = tree.children(node.identifier)
        for child in children:
            if child.data.is_focused == True:
                focus_list.append((child.data.type, child.data.path))
            queue.put(child)
    return focus_list

def get_changed_focus(tree):
    changed_focus_list = []
    root: Node = tree.get_node(tree.root)
    queue = Queue()
    queue.put(root)
    while not queue.empty():
        node: Node = queue.get()
        children = tree.children(node.identifier)
        for child in children:
            if child.data.is_focused == True and child.data.status != 0:
                status = child.data.status
                if status == 0:
                    fstatus = 'untouched'
                elif status == 1:
                    fstatus = 'new'
                elif status == 2:
                    fstatus = 'modified'
                elif status == -1:
                    fstatus = 'deleted'
                else:
                    print("error: adjust tree")
                item = {
                    "type": child.data.type,
                    "path": child.data.path,
                    "status": fstatus,
                    "time": child.data.time,
                    "author": child.data.author,
                    "message": child.data.message
                }
                changed_focus_list.append(item)
            queue.put(child)
    return changed_focus_list

if __name__ == "__main__":
    print()
    
    path = "/Users/pengxiaopeng/test"
    os.chdir(path)
    sh(f"git checkout origin/main")
    current_tree = rep_ast_tree_construct(path)
    
    sh(f"git checkout main")
    last_tree = rep_ast_tree_construct(path)
    
    tree = merge_tree(last_tree, current_tree)
    # add_data(tree, "time", "author", "message")
    # last_tree.show(data_property="type")
    # current_tree.show(data_property="type")
    # tree.show(data_property="message")
    # add_focus(tree, "focus/ui.py")
    # add_focus(tree, "adir/bdir/file1")
    # tree.show(data_property="is_focused")

    # print(get_changed_focus(tree))