import os
import json
from tkinter import *
    

focus_file = ""


def add_focus_file(
    file_path: str,
    ):
    global focus_file
    if not os.path.isfile(os.path.abspath(file_path)):
        hint("no such file")
        return
    with open(focus_file, 'r') as f:
        focus_json = json.load(f)
    for file in focus_json["focus_file_list"]:
        if file_path == file:
            hint("file already been focused")
            return
    focus_json["focus_file_list"].append(file_path)
    with open(focus_file, 'w') as f:
        json.dump(focus_json, f, indent=4)
    hint("successfully add a focus file")


def add_focus_directory(
    directory_path: str,
    ):
    global focus_file
    if not os.path.isdir(os.path.abspath(directory_path)):
        hint("no such directory")
        return
    with open(focus_file, 'r') as f:
        focus_json = json.load(f)
    for directory in focus_json["focus_directory_list"]:
        if directory_path == directory:
            hint("directory already been focused")
            return
    focus_json["focus_directory_list"].append(directory_path)
    with open(focus_file, 'w') as f:
        json.dump(focus_json, f, indent=4)
    hint("successfully add a focus directory")


def delete_focus_file(
    file_path: str,
    ):
    global focus_file
    with open(focus_file, 'r') as f:
        focus_json = json.load(f)
    for file in focus_json["focus_file_list"]:
        if file_path == file:
            focus_json["focus_file_list"].remove(file_path)
            with open(focus_file, 'w') as f:
                json.dump(focus_json, f, indent=4)
            hint("successfully delete a focus file")
            return
    hint("no such focus file")


def delete_focus_directory(
    directory_path: str,
    ):
    global focus_file
    with open(focus_file, 'r') as f:
        focus_json = json.load(f)
    for directory in focus_json["focus_directory_list"]:
        if directory_path == directory:
            focus_json["focus_directory_list"].remove(directory_path)
            with open(focus_file, 'w') as f:
                json.dump(focus_json, f, indent=4)
            hint("successfully delete a focus directory")
            return
    hint("no such focus directory")


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

def hint(s: str):
    hint = Tk()
    hint.geometry('240x160')
    hint.title('focus')
    hint_label = Label(hint, text=s)
    hint_label.pack()
    

def is_block(s: str):
    # whether is a valid block
    return True


def is_file(s: str):
    # whether is a valid file
    return True


def main(repository):
    # maximum of changes for show 
    focus_dir = f"{repository}/.git/.focus"
    global focus_file
    focus_file = f"{focus_dir}/focus.json"
    change_file = f"{focus_dir}/change.json"
    history_file = f"{focus_dir}/history.json"
    history_count = 3
    history_path = history_file
    root = Tk()
    root.geometry('480x320')
    root.title('focus')
    
    var_list = []
    label_list = []
    for i in range(history_count):
        var=StringVar()
        var.set("")
        label = Label(root, textvariable=var)
        var_list.append(var)
        label_list.append(label)
        
    message_panel_file = Frame(root)
    message_label_file = Label(message_panel_file, text="file path:")
    message_entry_file = Entry(message_panel_file)
    message_panel_block = Frame(root)
    message_label_block = Label(message_panel_block, text="directory path:")
    message_entry_block = Entry(message_panel_block)
    
    def add():
        nonlocal message_entry_file
        nonlocal message_entry_block
        file_path = message_entry_file.get()
        directory_path = message_entry_block.get()
        if file_path != "":
            add_focus_file(file_path)
        if directory_path != "":
            add_focus_directory(directory_path)
        
            
    def delete():
        nonlocal message_entry_file
        nonlocal message_entry_block
        file_path = message_entry_file.get()
        directory_path = message_entry_block.get()
        if file_path != "":
            delete_focus_file(file_path)
        if directory_path != "":
            delete_focus_directory(directory_path)
    
    def renew():
        focus_history_json = {}
        focus_history_json["change_list"] = []
        if os.path.isfile(history_path):
            with open(history_path, 'r') as f:
                focus_history_json = json.load(f)
        # if len(focus_history_json["change_list"]) != 0:
        #     print(focus_history_json["change_list"])
        if len(focus_history_json["change_list"]) > history_count:
            count_of_history_for_show = history_count
        else:
            count_of_history_for_show = len(focus_history_json["change_list"])
        for i in range(count_of_history_for_show):
            record = focus_history_json["change_list"][- (i + 1)]
            type_of_record = record["type"]
            stat = record["stat"]
            path = record["path"]
            time = record["change"]["time"]
            time = time[time.find(" "): time.rfind(" ")]
            author = record["change"]["author"]
            message = record["change"]["message"]
            # 这里没有对关注点是文件还是目录分类讨论
            text = f"{type_of_record}: {path}   {time}   {author}   {stat}"
            var_list[i].set(text)

    
    bottom_panel = Frame(root)
    add_button = Button(bottom_panel, text='add', command=add)
    delet_button = Button(bottom_panel, text='delete', command=delete)
    renew_button = Button(bottom_panel, text='renew', command=renew)
    
    message_label_file.pack(side=LEFT)
    message_entry_file.pack(side=RIGHT)
    message_label_block.pack(side=LEFT)
    message_entry_block.pack(side=RIGHT)
    message_panel_file.pack()
    message_panel_block.pack()
    add_button.pack()
    delet_button.pack()
    renew_button.pack()
    bottom_panel.pack()
    for label in label_list:
        label.pack()
    renew()
    mainloop()


if __name__ == '__main__':
    main()
