import os
import json
from tkinter import *
from focus.Robot import Robot, fetch_from_origin


def hint(s: str):
    hint = Tk()
    hint.geometry('360x120')
    hint.title('focus')
    hint.configure(bg='white')
    hint_label = Label(hint, text=s, bg='white')
    hint_label.pack(pady=40)


def warnning(s: str):
    warnning = Tk()
    warnning.geometry('360x120')
    warnning.title('focus')
    warnning.configure(bg='white')
    warnning_label = Label(warnning, text='\nWANNING', bg='white', fg='red')
    warnning_label.pack()
    warnning_content = Label(warnning, text=s, bg='white')
    warnning_content.pack()


def get_pos(chars: str, wraplength: int):
    char_number = wraplength / 7
    if len(chars) > char_number:
        pos = 'w'
    else:
        pos = 'center'
    return pos

def main(robot: Robot):
    repository = robot._repository
    focus_dir = f"{repository}/.git/.focus"
    global focus_file
    focus_file = f"{focus_dir}/focus.json"
    change_file = f"{focus_dir}/change.json"
    history_count = 5
    length = '1300'
    height = '670'
    
    
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
            warnning("the file doesn't exist, but added anyway.\n i can't do correction for you, \n so make sure your path is right")
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
            warnning("the directory doesn't exist, but added anyway.\n i can't do correction for you, \n so make sure your path is right")
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
        delete_ok = False
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
        delete_ok = False
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
        for widget in history_display_panel.winfo_children():
            widget.destroy()
        row_number = 0
        type_label_topline = Label(history_display_panel, text="type", font=('Arial', 16), bg='white')
        type_label_topline.grid(row=row_number, column=0, pady=15)
        path_label_topline = Label(history_display_panel, text="path", font=('Arial', 16), bg='white')
        path_label_topline.grid(row=row_number, column=1)
        stat_label_topline = Label(history_display_panel, text="status", font=('Arial', 16), bg='white')
        stat_label_topline.grid(row=row_number, column=2)
        time_label_topline = Label(history_display_panel, text="time", font=('Arial', 16), bg='white')
        time_label_topline.grid(row=row_number, column=3)
        author_label_topline = Label(history_display_panel, text="author", font=('Arial', 16), bg='white')
        author_label_topline.grid(row=row_number, column=4)
        message_label_topline = Label(history_display_panel, text="message", font=('Arial', 16), bg='white')
        message_label_topline.grid(row=row_number, column=5)
        file_label_topline = Label(history_display_panel, text="file", font=('Arial', 16), bg='white')
        file_label_topline.grid(row=row_number, column=6)
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
            type_label = Label(history_display_panel, text=type_of_record, bg='white')
            type_label.grid(row=row_number, column=0)
            wraplength = 300
            pos = get_pos(path, wraplength)
            path_label = Label(history_display_panel, text=path, width=30, height=3, wraplength=wraplength, anchor=pos, bg='white')
            path_label.grid(row=row_number, column=1)
            stat_label = Label(history_display_panel, text=stat, bg='white')
            stat_label.grid(row=row_number, column=2)
            time_label = Label(history_display_panel, text=time, width=20, bg='white')
            time_label.grid(row=row_number, column=3)
            author_label = Label(history_display_panel, text=author, bg='white')
            author_label.grid(row=row_number, column=4)
            wraplength = 300
            pos = get_pos(message, wraplength)
            message_label = Label(history_display_panel, text=message, width=30, height=3, wraplength=wraplength, anchor=pos, bg='white')
            message_label.grid(row=row_number, column=5)
            wraplength = 300
            pos = get_pos(file, wraplength)
            file_label = Label(history_display_panel, text=file, width=30, height=3, wraplength=wraplength, anchor=pos, bg='white')
            file_label.grid(row=row_number, column=6)
        row_number += 1
        if ellipsis != '':
            ellipsis_label = Label(history_display_panel, text=ellipsis, font=('Arial', 25), bg='white')
            ellipsis_label.grid(row=row_number, column=4)
        history_display_panel.pack()


    def show_all_history():
        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        if os.path.isfile(change_file):
            with open(change_file, 'r') as f:
                history_json = json.load(f)
        change_list: list = history_json['change_list']
        if change_list == []:
            hint("the change history is empty")
            return
        width = 1300
        height = 670
        content_window = Tk()
        content_window.geometry(f'{width}x{height}')
        content_window.configure(bg="white")
        content_window.title('focus')
        canvas = Canvas(content_window, bg='white')
        myscrollbar=Scrollbar(content_window,orient="vertical",command=canvas.yview)
        myscrollbar.place(x=width - 15, y=0, height=height)
        canvas.configure(yscrollcommand=myscrollbar.set)
        canvas.place(x=0, y=0, width=width, height=height)
        content_frame = Frame(canvas, bg='white')
        content_frame.bind("<Configure>",myfunction)
        canvas.create_window((65, 50), window=content_frame,anchor="nw")
        frame_title = Label(content_frame, text="all focus", font=('Arial', 18), bg='white')
        frame_title.grid(row=0, column=4, pady=20)
        row_number = 1
        type_label_topline = Label(content_frame, text="type", font=('Arial', 16), bg='white')
        type_label_topline.grid(row=row_number, column=0, pady=15)
        path_label_topline = Label(content_frame, text="path", font=('Arial', 16), bg='white')
        path_label_topline.grid(row=row_number, column=1)
        stat_label_topline = Label(content_frame, text="status", font=('Arial', 16), bg='white')
        stat_label_topline.grid(row=row_number, column=2)
        time_label_topline = Label(content_frame, text="time", font=('Arial', 16), bg='white')
        time_label_topline.grid(row=row_number, column=3)
        author_label_topline = Label(content_frame, text="author", font=('Arial', 16), bg='white')
        author_label_topline.grid(row=row_number, column=4)
        message_label_topline = Label(content_frame, text="message", font=('Arial', 16), bg='white')
        message_label_topline.grid(row=row_number, column=5)
        file_label_topline = Label(content_frame, text="file", font=('Arial', 16), bg='white')
        file_label_topline.grid(row=row_number, column=6)
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
            type_label = Label(content_frame, text=type_of_record, bg='white')
            type_label.grid(row=row_number, column=0)
            wraplength = 300
            pos = get_pos(path, wraplength)
            path_label = Label(content_frame, text=path, width=30, height=3, wraplength=wraplength, anchor=pos, bg='white')
            path_label.grid(row=row_number, column=1)
            stat_label = Label(content_frame, text=stat, bg='white')
            stat_label.grid(row=row_number, column=2)
            time_label = Label(content_frame, text=time, width=20, bg='white')
            time_label.grid(row=row_number, column=3)
            author_label = Label(content_frame, text=author, bg='white')
            author_label.grid(row=row_number, column=4)
            wraplength = 300
            pos = get_pos(message, wraplength)
            message_label = Label(content_frame, text=message, width=30, height=3, wraplength=wraplength, anchor=pos, bg='white')
            message_label.grid(row=row_number, column=5)
            wraplength = 300
            pos = get_pos(file, wraplength)
            file_label = Label(content_frame, text=file, width=30, height=3, wraplength=wraplength, anchor=pos, bg='white')
            file_label.grid(row=row_number, column=6)
        content_window.mainloop()


    def show_all_focus():
        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        if os.path.isfile(focus_file):
            with open(focus_file, 'r') as f:
                focus_json = json.load(f)
        focus_file_list: list = focus_json['focus_file_list']
        focus_directory_list: list = focus_json['focus_directory_list']
        if focus_file_list == [] and focus_directory_list == []:
            hint("your focus is empty")
            return
        width = 440
        height = 500
        content_window = Tk()
        content_window.geometry(f'{width}x{height}')
        content_window.configure(bg="white")
        content_window.title('focus')
        canvas = Canvas(content_window, bg='white')
        myscrollbar=Scrollbar(content_window,orient="vertical",command=canvas.yview)
        myscrollbar.place(x=width - 15, y=0, height=height)
        canvas.configure(yscrollcommand=myscrollbar.set)
        canvas.place(x=0, y=0, width=width, height=height)
        content_frame = Frame(canvas, bg='white')
        content_frame.bind("<Configure>",myfunction)
        canvas.create_window((65, 50), window=content_frame,anchor="nw")
        frame_title = Label(content_frame, text="all focus", font=('Arial', 18), bg='white')
        frame_title.grid(row=0, columnspan=2, pady=20)
        row_number = 1
        type_label_topline = Label(content_frame, text="type", font=('Arial', 16), bg='white')
        type_label_topline.grid(row=row_number, column=0, pady=15)
        path_label_topline = Label(content_frame, text="path", font=('Arial', 16), bg='white')
        path_label_topline.grid(row=row_number, column=1)
        for item in focus_file_list:
            row_number += 1
            type_of_record = "file"
            path = item
            type_label = Label(content_frame, text=type_of_record, bg='white')
            type_label.grid(row=row_number, column=0)
            wraplength = 300
            pos = get_pos(path, wraplength)
            path_label = Label(content_frame, text=path, width=30, height=3, wraplength=wraplength, anchor=pos, bg='white')
            path_label.grid(row=row_number, column=1)
        for item in focus_directory_list:
            row_number += 1
            type_of_record = "dir"
            path = item
            type_label = Label(content_frame, text=type_of_record, bg='white')
            type_label.grid(row=row_number, column=0)
            wraplength = 300
            pos = get_pos(path, wraplength)
            path_label = Label(content_frame, text=path, width=30, height=3, wraplength=wraplength, anchor=pos, bg='white')
            path_label.grid(row=row_number, column=1)
        content_window.mainloop()



    def fetch():
        fetch_from_origin(robot._debug)
        hint("Done fetching.")

    root = Tk()
    root.geometry(f'{length}x{height}')
    root.title('focus')
    root.configure(bg='white')
    
    blank_line = Label(root, text=" ", bg='white')
    blank_line.pack(pady=10)
    add_delete_grid = Frame(root, bg='white')
    file_message_label = Label(add_delete_grid, text="file path:", bg='white')
    file_message_label.grid(row=0, column=0, pady=0)
    file_message_entry = Entry(add_delete_grid, bg='white')
    file_message_entry.grid(row=0, column=1)
    file_message_add = Button(add_delete_grid, text='add', command=add_focus_file)
    file_message_add.configure(bg="white")
    file_message_add.grid(row=0, column=2)
    file_message_delete = Button(add_delete_grid, text='delete', command=delete_focus_file, bg='black')
    file_message_delete.grid(row=0, column=3)
    dir_message_label = Label(add_delete_grid, text="directory path:", bg='white')
    dir_message_label.grid(row=1, column=0, pady=12)
    dir_message_entry = Entry(add_delete_grid, bg='white')
    dir_message_entry.grid(row=1, column=1)
    dir_message_add = Button(add_delete_grid, text='add', command=add_focus_directory, bg='white')
    dir_message_add.grid(row=1, column=2)
    dir_message_delete = Button(add_delete_grid, text='delete', command=delete_focus_directory, bg='white')
    dir_message_delete.grid(row=1, column=3)
    add_delete_grid.pack()
    recent_change_label = Label(root, text="\nyour focus change", fg='black', font=('Arial', 18), bg='white')
    recent_change_label.pack(pady=10)
    history_display_panel = Frame(root, bg='white')
    renew()
    blank_line = Label(root, text="", bg='white')
    blank_line.pack(pady=10)
    renew_history_fetch_button_panel = Frame(root)
    renew_button = Button(renew_history_fetch_button_panel, text='renew', width=10, height=2, command=renew, bg='white')
    renew_button.pack(side="left")
    history_button = Button(renew_history_fetch_button_panel, text='show all change', width=10, height=2, command=show_all_history, bg='white')
    history_button.pack(side="left")
    focus_button = Button(renew_history_fetch_button_panel, text='show all focus', width=10, height=2, command=show_all_focus, bg='white')
    focus_button.pack(side="left")
    fetch_button = Button(renew_history_fetch_button_panel, text='fetch', width=10, height=2, command=fetch, bg='white')
    fetch_button.pack(side="left")
    renew_history_fetch_button_panel.pack()
    mainloop()