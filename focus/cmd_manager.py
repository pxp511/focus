import os
import json
from focus.Robot import Robot

def add_focus(
    file_name: str,
    block_name: str,
    use_block: bool,
    robot: Robot
    ):
    # add a record to the focus_file
    # block_name indicates whether focus-point is a block
    # if block_name == True: add record by block
    focus_path = robot._focus_file
    focus_json = {}
    focus_json["focus_file_list"] = []
    focus_json["focus_block_list"] = []
    if os.path.isfile(focus_path):
        with open(focus_path, 'r') as f:
            focus_json = json.load(f)
            
    if use_block == False:
        focus_json["focus_file_list"].append(file_name)
    elif use_block == True:
        record = {}
        record["file_path"] = file_name
        record["block_name"] = block_name
        focus_json["focus_block_list"].append(record)
    with open(focus_path, 'w') as f:
        json.dump(focus_json, f, indent=4)
        
def delete_focus(
    file_name: str,
    block_name: str,
    use_block: bool
    ):
    # delete a record from the focus_record_file
    # # block_name indicates whether focus-point is a block
    # if block_name == True: add record by block
    return

def get_history(display: bool):
    # get the focus_change_history_file
    # if display == True: display focus_change_history_file in terminal
    return

def do_merge():
    # os.system("git merge")
    return

def get_focus():
    # display focus-points from focus.json
    return

def cmd_parse(cmd: str):
    # get command line from ternimal and parse the arguments
    # call contigent function according to the result
    if 1:
        add_focus(file_name, block_name, use_block)
    elif 2:
        delete_focus(file_name, block_name, use_block)
    elif 3:
        get_history()
    elif 4:
        do_merge()
    elif 5:
        get_focus()        
