import ast
import os
import queue

path = os.path.join(os.path.abspath("."), "zzzz.py")

def get_type(node):
    return type(node).__name__

def assign_attr_parse(node):
    node = node.targets[0]
    ret = ""
    while get_type(node) == "Attribute":
        name = node.attr
        ret = '.' + name + ret
        node = node.value
    ret = node.id + ret
    return ret

def annassign_attr_parse(node):
    node = node.target
    ret = ""
    while get_type(node) == "Attribute":
        name = node.attr
        ret = '.' + name + ret
        node = node.value
    ret = node.id + ret
    return ret

def assign_tuple_parse(node):
    ret = []
    for son in node.targets[0].elts:
        ret.append(son.id)
    return ret
    
def get_children(node):
    type_name = get_type(node)
    if type_name in ["Module", "FunctionDef", "ClassDef", "Try"]:
        ret = []
        for item in node.body:
            if type(item).__name__ in ["FunctionDef", "Assign", "ClassDef", "AnnAssign", "Try"]:
                ret.append(item)
        return ret
    if type_name in ["Assign", "AnnAssign"]:
        return []
    
def get_name(node):
    type_name = get_type(node)
    if type_name == "Module":
        return "Module"
    if type_name == "FunctionDef":
        return node.name
    if type_name == "Assign":
        assign_type = get_type(node.targets[0])
        if assign_type == "Name":
            return node.targets[0].id
        if assign_type == "Attribute":
            return assign_attr_parse(node)
        if assign_type == "Tuple":
            return assign_tuple_parse(node)
    if type_name == "AnnAssign":
        annassign_type = get_type(node.target)
        if annassign_type == "Name":
            return node.target.id
        if annassign_type == "Attribute":
            return annassign_attr_parse(node)
        if annassign_type == "Tuple":
            return assign_tuple_parse(node)
    if type_name == "ClassDef":
        return node.name
    if type_name == "Try":
        return ""

def get_value(node):
    type_name = get_type(node)
    if type_name == "Module":
        return "Module"
    if type_name in ["FunctionDef", "Assign", "AnnAssign", "ClassDef", "Try"]:
        return ast.dump(node)


with open(path, 'r') as f:
    tree = ast.parse(f.read())


queue = queue.Queue()
queue.put(tree)
while not queue.empty():
    node = queue.get()
    # if get_name(node) == "Module":
    #     print(ast.dump(node))
    #     exit()
    print(get_name(node))
    # print(ast.dump(node))
    children = get_children(node)
    for child in children:
        queue.put(child)