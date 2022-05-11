import os
import json
from tkinter import *
from focus.Robot import Robot, fetch_from_origin

focus_file = ""

def add_focus_file(
    file_path: str,
    ):
    global focus_file
    with open(focus_file, 'r') as f:
        focus_json = json.load(f)
    for file in focus_json["focus_file_list"]:
        if file_path == file:
            hint("file already been focused")
            return
    if os.path.isfile(os.path.abspath(file_path)):
        hint("successfully add a focus file")
    else:
        hint("WARNNING \n the file doesn't exist, but added anyway.\n i can't do correction for you, \n so make sure your path is right")
    focus_json["focus_file_list"].append(file_path)
    with open(focus_file, 'w') as f:
        json.dump(focus_json, f, indent=4)


def add_focus_directory(
    directory_path: str,
    ):
    global focus_file
    with open(focus_file, 'r') as f:
        focus_json = json.load(f)
    for directory in focus_json["focus_directory_list"]:
        if directory_path == directory:
            hint("directory already been focused")
            return
    if os.path.isdir(os.path.abspath(directory_path)):
        hint("successfully add a focus directory")
    else:
        hint("WARNNING \n the directory doesn't exist, but added anyway.\n i can't do correction for you, \n so make sure your path is right")
    focus_json["focus_directory_list"].append(directory_path)
    with open(focus_file, 'w') as f:
        json.dump(focus_json, f, indent=4)


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
    hint.geometry('360x100')
    hint.title('focus')
    hint_label = Label(hint, text=s)
    hint_label.pack()


def main(robot: Robot):
    repository = robot._repository
    focus_dir = f"{repository}/.git/.focus"
    global focus_file
    focus_file = f"{focus_dir}/focus.json"
    change_file = f"{focus_dir}/change.json"
    history_file = f"{focus_dir}/history.json"
    history_count = 3
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
        if robot.is_remote_changed():
            robot.change_parse()
        if os.path.isfile(change_file):
            with open(change_file, 'r') as f:
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
        if os.path.isfile(change_file):
            with open(change_file, 'r') as f:
                history_json = json.load(f)
        change_list: list = history_json['change_list']
        if change_list == []:
            return
        content_window = Tk()
        content_window.geometry(f'600x400')
        content_window.title('all history')
        type_label_topline = Label(content_window, text="type")
        type_label_topline.grid(row=0, column=0)
        path_label_topline = Label(content_window, text="path")
        path_label_topline.grid(row=0, column=1)
        stat_label_topline = Label(content_window, text="status")
        stat_label_topline.grid(row=0, column=2)
        time_label_topline = Label(content_window, text="time")
        time_label_topline.grid(row=0, column=3)
        author_label_topline = Label(content_window, text="author")
        author_label_topline.grid(row=0, column=4)
        message_label_topline = Label(content_window, text="message")
        message_label_topline.grid(row=0, column=5)
        file_label_topline = Label(content_window, text="file")
        file_label_topline.grid(row=0, column=6)
        row_number = 0
        for index in range(len(change_list) - 1, -1, -1):
            row_number += 1
            record: dict = change_list[index]
            type_of_record = record["type"]
            if type_of_record == 'directory':
                type_of_record = 'dir'
            path = record["path"]
            stat = record["stat"]
            time = record["change"]["time"]
            time = time[time.find(" "): time.rfind(" ")]
            author = record["change"]["author"]
            message = record["change"]["message"]
            file = record.get("file", "")
            type_label = Label(content_window, text=type_of_record)
            type_label.grid(row=row_number, column=0)
            path_label = Label(content_window, text=path)
            path_label.grid(row=row_number, column=1)
            stat_label = Label(content_window, text=stat)
            stat_label.grid(row=row_number, column=2)
            time_label = Label(content_window, text=time)
            time_label.grid(row=row_number, column=3)
            author_label = Label(content_window, text=author)
            author_label.grid(row=row_number, column=4)
            message_label = Label(content_window, text=message)
            message_label.grid(row=row_number, column=5)
            file_label = Label(content_window, text=file)
            file_label.grid(row=row_number, column=6)
        content_window.mainloop()


    def fetch():
        fetch_from_origin(robot._debug)
        hint("Done fetching.")


    add_delete_panel = Frame(root)
    file_message_panel = Frame(add_delete_panel)
    file_message_label = Label(file_message_panel, text="file path:")
    file_message_entry = Entry(file_message_panel)
    file_message_label.pack(side=LEFT)
    file_message_entry.pack(side=RIGHT)
    file_message_panel.pack()
    dir_message_panel = Frame(add_delete_panel)
    dir_message_label = Label(dir_message_panel, text="dir path:")
    dir_message_entry = Entry(dir_message_panel)
    dir_message_label.pack(side=LEFT)
    dir_message_entry.pack(side=RIGHT)
    dir_message_panel.pack()
    button_message_panel = Frame(add_delete_panel)
    button_add = Button(button_message_panel, text='add', command=add)
    button_delete = Button(button_message_panel, text='delete', command=delete)
    button_add.pack(side=LEFT)
    button_delete.pack(side=RIGHT)
    button_message_panel.pack()
    add_delete_panel.pack()
    
    renew_history_display_panel = Frame(root)
    blank_label = Label(renew_history_display_panel, text="\n")
    blank_label.pack()
    recent_change_label = Label(renew_history_display_panel, text="your focus change", fg='black', font=('Arial', 18))
    recent_change_label.pack()
    title_line = f"{'':^4}   {'time':^25}   {'author':^10}   {'status':^10}   {'path'}"
    content_title_line = Label(renew_history_display_panel, text=title_line, fg='grey')
    content_title_line.pack()
    history_var = StringVar()
    history_var.set("")
    history_label = Label(renew_history_display_panel, textvariable=history_var)
    history_label.pack()
    renew_history_panel = Frame(renew_history_display_panel)
    renew_button = Button(renew_history_panel, text='renew', command=renew)
    renew_button.pack(side=LEFT)
    history_button = Button(renew_history_panel, text='show all', command=show_all_history)
    history_button.pack(side=LEFT)
    fetch_button = Button(renew_history_panel, text='fetch', command=fetch)
    fetch_button.pack(side=LEFT)
    renew_history_panel.pack()
    renew_history_display_panel.pack()

    renew()
    mainloop()


if __name__ == '__main__':
    main()