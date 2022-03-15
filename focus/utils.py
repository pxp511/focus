from tkinter import *


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

def hint(s: str):
    hint = Tk()
    hint.geometry('240x160')
    hint.title('focus')
    hint_label = Label(hint, text=s)
    hint_label.pack()

    