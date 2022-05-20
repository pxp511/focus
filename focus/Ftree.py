from treelib import Tree, Node
from queue import Queue
import os
import subprocess
import pickle


number = 0
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
        status,
        id1 = 0,
        id2 = 0,
        type = '',
        path = '',
        time = '',
        author = '',
        message = '',
        file = '',
        is_changed = False,
        is_focued = False
        ):
        self.status = status
        self.id1 = id1
        self.id2 = id2
        self.type = type
        self.path = path
        self.time = time
        self.author = author
        self.message = message
        self.file = file
        self.is_det = is_changed
        self.is_focued = is_focued
        # 0: 未合并
        # 2: 合后并均存在
        # -1: 被删除
        # 1: 新增
        
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

def get_rep_construct():
    global number
    tree = Tree()
    path = os.getcwd()
    number += 1
    root = tree.create_node(path, number, data=Fnode(0))
    pqueue = Queue()
    pqueue.put(root)
    while not pqueue.empty():
        pqueue_temp = Queue()
        while not pqueue.empty():
            pnode = pqueue.get()
            path = pnode.tag
            if os.path.isdir(path):
                for item in sorted(os.listdir(path)):
                    if item[0] == ".":
                        continue
                    number += 1
                    node = tree.create_node(item, number, parent=pnode.identifier, data=Fnode(0))
                    pqueue_temp.put(node)
        pqueue = pqueue_temp
    return tree


def merge_tree_entity(tree1: Tree, tree2: Tree):
    global number
    if tree1 is None:
        tree2.get_node(tree2.root).data = Fnode(1)
        return tree2
    if tree2 is None:
        tree1.get_node(tree1.root).data = Fnode(-1)
        return tree1
    root1: Node = tree1.get_node(tree1.root)
    root2: Node = tree2.get_node(tree2.root)
    assert root1.tag == root2.tag
    new_tree = Tree()
    number += 1
    new_tree.create_node(root1.tag, number)
    if tree1.depth() == 0 and tree2.depth() == 0:
        new_tree.get_node(new_tree.root).data = Fnode(2)
        return new_tree
    children1 = tree1.children(root1.identifier)
    children2 = tree2.children(root2.identifier)
    index1 = 0
    index2 = 0
    length1 = len(children1)
    length2 = len(children2)
    node_list = []
    while index1 < length1 and index2 < length2:
        node1: Node = children1[index1]
        node2: Node = children2[index2]
        number += 1
        if node1.tag == node2.tag:
            node_list.append(Node(node1.tag, number, data=Fnode(2, id1 = node1.identifier, id2 = node2.identifier)))
            index1 += 1
            index2 += 1
        elif node1.tag < node2.tag:
            node_list.append(Node(node1.tag, number, data=Fnode(-1, id1 = node1.identifier)))
            index1 += 1
        elif node1.tag > node2.tag:
            node_list.append(Node(node2.tag, number, data=Fnode(1, id2 = node2.identifier)))
            index2 += 1
    while index1 < length1:
        node1: Node = children1[index1]
        number += 1
        node_list.append(Node(node1.tag, number, data=Fnode(-1, id1 = node1.identifier)))
        index1 += 1
    while index2 < length2:
        node2: Node = children2[index2]
        number += 1
        node_list.append(Node(node2.tag, number, data=Fnode(1, id2 = node2.identifier)))
        index2 += 1
    for node in node_list:
        if node.data.status == -1:
            subtree = tree1.subtree(node.data.id1)
            subtree.get_node(subtree.root).data = Fnode(-1)
        elif node.data.status == 1:
            subtree = tree2.subtree(node.data.id2)
            subtree.get_node(subtree.root).data = Fnode(1)
        elif node.data.status == 2:
            subtree1 = tree1.subtree(node.data.id1)
            subtree2 = tree2.subtree(node.data.id2)
            subtree = merge_tree_entity(subtree1, subtree2)
            subtree.get_node(subtree.root).data = Fnode(2)
        new_tree.paste(new_tree.root, subtree)
    return new_tree


def merge_tree(tree1: Tree, tree2: Tree):
    new_tree = merge_tree_entity(tree1, tree2)
    new_tree.get_node(new_tree.root).data = Fnode(2)
    return new_tree

# with open("/Users/pengxiaopeng/treeobj", 'wb') as f:
#     pickle.dump(new_tree, f)
# with open("/Users/pengxiaopeng/treeobj", 'rb') as f:
#     a_tree = pickle.load(f)
# print(a_tree)