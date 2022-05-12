import os
import json
from tkinter import *
from focus.Robot import Robot, fetch_from_origin


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
    history_count = 5
    length = '600'
    height = '400'


    def add_focus_file():
        file_path = file_message_entry.get()
        if file_path == "":
            hint("file path input is empty")
            return
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
        renew()


    def add_focus_directory():
        directory_path = dir_message_entry.get()
        if directory_path == "":
            hint("directory path input is empty")
            return
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
        renew()


    def delete_focus_file():
        file_path = file_message_entry.get()
        if file_path == "":
            hint("file path input is empty")
            return
        with open(focus_file, 'r') as f:
            focus_json = json.load(f)
        for file in focus_json["focus_file_list"]:
            if file_path == file:
                focus_json["focus_file_list"].remove(file_path)
                with open(focus_file, 'w') as f:
                    json.dump(focus_json, f, indent=4)
                hint("successfully delete a focus file")
                delete_ok = True
                break
        if delete_ok != True:
            hint("no such focus file")
        renew()


    def delete_focus_directory():
        directory_path = dir_message_entry.get()
        if directory_path == "":
            hint("directory path input is empty")
            return
        with open(focus_file, 'r') as f:
            focus_json = json.load(f)
        for directory in focus_json["focus_directory_list"]:
            if directory_path == directory:
                focus_json["focus_directory_list"].remove(directory_path)
                with open(focus_file, 'w') as f:
                    json.dump(focus_json, f, indent=4)
                hint("successfully delete a focus directory")
                delete_ok = True
                break
        if delete_ok != True:
            hint("no such focus directory")
        renew()


    def renew():
        if robot.is_remote_changed():
            robot.change_parse()
        if os.path.isfile(change_file):
            with open(change_file, 'r') as f:
                history_json = json.load(f)
        change_list: list = history_json['change_list']
        if len(change_list) > history_count:
            count_of_history_for_show = history_count
            ellipsis = '......'
        else:
            count_of_history_for_show = len(change_list)
            ellipsis = ''
        for widget in renew_history_display_panel.winfo_children():
            widget.destroy()
        blank_label = Label(renew_history_display_panel, text="\n")
        blank_label.grid(row=0, column=0, columnspan=6)
        recent_change_label = Label(renew_history_display_panel, text="your focus change", fg='black', font=('Arial', 18))
        recent_change_label.grid(row=1, columnspan=6)
        type_label_topline = Label(renew_history_display_panel, text="type")
        type_label_topline.grid(row=2, column=0)
        path_label_topline = Label(renew_history_display_panel, text="path")
        path_label_topline.grid(row=2, column=1)
        stat_label_topline = Label(renew_history_display_panel, text="status")
        stat_label_topline.grid(row=2, column=2)
        time_label_topline = Label(renew_history_display_panel, text="time")
        time_label_topline.grid(row=2, column=3)
        author_label_topline = Label(renew_history_display_panel, text="author")
        author_label_topline.grid(row=2, column=4)
        message_label_topline = Label(renew_history_display_panel, text="message")
        message_label_topline.grid(row=2, column=5)
        file_label_topline = Label(renew_history_display_panel, text="file")
        file_label_topline.grid(row=2, column=6)
        row_number = 2
        for index in range(len(change_list) - 1, len(change_list) - count_of_history_for_show - 1, -1):
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
            type_label = Label(renew_history_display_panel, text=type_of_record)
            type_label.grid(row=row_number, column=0)
            path_label = Label(renew_history_display_panel, text=path)
            path_label.grid(row=row_number, column=1)
            stat_label = Label(renew_history_display_panel, text=stat)
            stat_label.grid(row=row_number, column=2)
            time_label = Label(renew_history_display_panel, text=time)
            time_label.grid(row=row_number, column=3)
            author_label = Label(renew_history_display_panel, text=author)
            author_label.grid(row=row_number, column=4)
            message_label = Label(renew_history_display_panel, text=message)
            message_label.grid(row=row_number, column=5)
            file_label = Label(renew_history_display_panel, text=file)
            file_label.grid(row=row_number, column=6)
        row_number += 1
        if ellipsis != '':
            ellipsis_label = Label(renew_history_display_panel, text=ellipsis)
            ellipsis_label.grid(row=row_number, column=0, columnspan=6)
            row_number += 1
        renew_button = Button(renew_history_display_panel, text='renew', command=renew)
        renew_button.grid(row=row_number, column=1)
        history_button = Button(renew_history_display_panel, text='show all', command=show_all_history)
        history_button.grid(row=row_number, column=3)
        fetch_button = Button(renew_history_display_panel, text='fetch', command=fetch)
        fetch_button.grid(row=row_number, column=5)
        renew_history_display_panel.pack()


    def show_all_history():
        if os.path.isfile(change_file):
            with open(change_file, 'r') as f:
                history_json = json.load(f)
        change_list: list = history_json['change_list']
        if change_list == []:
            return
        content_window = Tk()
        content_window.geometry(f'{length}x{height}')
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

    root = Tk()
    root.geometry(f'{length}x{height}')
    root.title('focus')
    add_delete_grid = Frame(root)
    span = 2
    file_message_label = Label(add_delete_grid, text="file path:")
    file_message_label.grid(row=0, column=0)
    file_message_entry = Entry(add_delete_grid)
    file_message_entry.grid(row=0, column=1, columnspan=span)
    file_message_add = Button(add_delete_grid, text='add', command=add_focus_file)
    file_message_add.grid(row=0, column=(span + 1))
    file_message_delete = Button(add_delete_grid, text='delete', command=delete_focus_file)
    file_message_delete.grid(row=0, column=(span + 2))
    dir_message_label = Label(add_delete_grid, text="directory path:")
    dir_message_label.grid(row=1, column=0)
    dir_message_entry = Entry(add_delete_grid)
    dir_message_entry.grid(row=1, column=1, columnspan=span)
    dir_message_add = Button(add_delete_grid, text='add', command=add_focus_directory)
    dir_message_add.grid(row=1, column=(span + 1))
    dir_message_delete = Button(add_delete_grid, text='delete', command=delete_focus_directory)
    dir_message_delete.grid(row=1, column=(span + 2))
    add_delete_grid.pack()
    renew_history_display_panel = Frame(root)
    renew()
    mainloop()


if __name__ == '__main__':
    main()