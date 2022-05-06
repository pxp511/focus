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


def hint(s: str):
    hint = Tk()
    hint.geometry('240x160')
    hint.title('focus')
    hint_label = Label(hint, text=s)
    hint_label.pack()


def main(repository):
    focus_dir = f"{repository}/.git/.focus"
    global focus_file
    focus_file = f"{focus_dir}/focus.json"
    change_file = f"{focus_dir}/change.json"
    history_file = f"{focus_dir}/history.json"
    history_count = 5
    history_path = history_file
    length = '480'
    height = '320'
    root = Tk()
    root.geometry(f'{length}x{height}')
    root.title('focus')
    
    def add():
        nonlocal file_message_entry
        nonlocal dir_message_entry
        file_path = file_message_entry.get()
        directory_path = dir_message_entry.get()
        if file_path != "":
            add_focus_file(file_path)
        if directory_path != "":
            add_focus_directory(directory_path)
        
            
    def delete():
        nonlocal file_message_entry
        nonlocal dir_message_entry
        file_path = file_message_entry.get()
        directory_path = dir_message_entry.get()
        if file_path != "":
            delete_focus_file(file_path)
        if directory_path != "":
            delete_focus_directory(directory_path)


    def renew():
        if os.path.isfile(history_path):
            with open(history_path, 'r') as f:
                history_json = json.load(f)
        change_list: list = history_json['change_list']
        if len(change_list) > history_count:
            count_of_history_for_show = history_count
            ellipsis = '\n......'
        else:
            count_of_history_for_show = len(change_list)
            ellipsis = ''
        content = ''
        for index in range(len(change_list) - 1, len(change_list) - count_of_history_for_show - 1, -1):
            record: dict = change_list[index]
            type_of_record = record["type"]
            if type_of_record == 'directory':
                type_of_record = 'dir'
            stat = record["stat"]
            path = record["path"]
            time = record["change"]["time"]
            time = time[time.find(" "): time.rfind(" ")]
            author = record["change"]["author"]
            message = record["change"]["message"]
            text = f"{type_of_record:^5}   {time:^25}   {author:^10}   {stat:^10}   {path}"
            content += text + '\n'
        content = content[:-1] + ellipsis
        history_var.set(content)


    def show_all_history():
        if os.path.isfile(history_path):
            with open(history_path, 'r') as f:
                history_json = json.load(f)
        change_list: list = history_json['change_list']
        if change_list == []:
            return
        content = ''
        for index in range(len(change_list) - 1, -1, -1):
            record: dict = change_list[index]
            type_of_record = record["type"]
            if type_of_record == 'directory':
                type_of_record = 'dir'
            stat = record["stat"]
            path = record["path"]
            time = record["change"]["time"]
            time = time[time.find(" "): time.rfind(" ")]
            author = record["change"]["author"]
            message = record["change"]["message"]
            text = f"{type_of_record:^4}   {time:^25}   {author:^10}   {stat:^10}   {path}"
            content += text + '\n'
        content_window = Tk()
        content_window.geometry(f'{length}x{height}')
        content_window.title('all history')
        title_line = f"{'':^4}   {'time':^25}   {'author':^10}   {'status':^10}   {'path'}"
        content_title_line = Label(content_window, text=title_line, fg='grey')
        content_title_line.pack()
        content_label = Label(content_window, text=content)
        content_label.pack()


    history_var = StringVar()
    history_var.set("")
    history_label = Label(root, textvariable=history_var)

    message_panel = Frame(root)
    file_message_panel = Frame(message_panel)
    file_message_label = Label(file_message_panel, text="file path:")
    file_message_entry = Entry(file_message_panel)
    file_message_label.pack(side=LEFT)
    file_message_entry.pack(side=RIGHT)
    file_message_panel.pack()
    dir_message_panel = Frame(message_panel)
    dir_message_label = Label(dir_message_panel, text="dir path:")
    dir_message_entry = Entry(dir_message_panel)
    dir_message_label.pack(side=LEFT)
    dir_message_entry.pack(side=RIGHT)
    dir_message_panel.pack()
    button_message_panel = Frame(message_panel)
    button_add = Button(button_message_panel, text='add', command=add)
    button_delete = Button(button_message_panel, text='delete', command=delete)
    button_add.pack(side=LEFT)
    button_delete.pack(side=RIGHT)
    button_message_panel.pack()
    
    renew_button = Button(root, text='show all history', command=show_all_history)
    
    message_panel.pack()
    blank_label = Label(root, text="\n")
    blank_label.pack()
    recent_change_label = Label(root, text="recent change", fg='grey', font=('Arial', 18))
    recent_change_label.pack()
    history_label.pack()
    renew_button.pack()
    renew()
    mainloop()


if __name__ == '__main__':
    main()
