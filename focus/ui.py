import os
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


def main(robot: Robot):
    history_count = 5
    length = '1350'
    height = '670'
    type_column = 1
    path_column = 0
    time_column = 5
    author_column = 4
    status_column = 3
    message_column = 6
    file_column = 7
    
    
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


    def find_node(file_path):
        is_find = True
        path_list = path_to_list(file_path)
        tree = robot._tree
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
                is_find = False
        return node, is_find


    def add_focus_file():
        file_path = file_message_entry.get()
        node, is_find = find_node(file_path)
        if is_find:
            node.data.is_focused = True
            hint("find")
            robot.tree_dump()
        else:
            hint("not find")


    def delete_focus_file():
        file_path = file_message_entry.get()
        node, is_find = find_node(file_path)
        if is_find:
            node.data.is_focused = False
            hint("find")
            robot.tree_dump()
        else:
            hint("not find")


    def renew():
        if robot.tree_need_change():
            robot.init()
        print('*'*50 + '\n')
        robot._tree.show()
        robot._tree.show(data_property="is_focused")
        robot._tree.show(data_property="path")
        print('*'*50)
        change_list = robot.get_show_list()
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
        type_label_topline.grid(row=row_number, column=type_column, pady=15, padx=20)
        path_label_topline = Label(history_display_panel, text="path", font=('Arial', 16), bg='white')
        path_label_topline.grid(row=row_number, column=path_column)
        time_label_topline = Label(history_display_panel, text="time", font=('Arial', 16), bg='white')
        time_label_topline.grid(row=row_number, column=time_column)
        author_label_topline = Label(history_display_panel, text="author", font=('Arial', 16), bg='white')
        author_label_topline.grid(row=row_number, column=author_column, padx=20)
        status_label_topline = Label(history_display_panel, text="status", font=('Arial', 16), bg='white')
        status_label_topline.grid(row=row_number, column=status_column, padx=20)
        message_label_topline = Label(history_display_panel, text="message", font=('Arial', 16), bg='white')
        message_label_topline.grid(row=row_number, column=message_column)
        file_label_topline = Label(history_display_panel, text="file", font=('Arial', 16), bg='white')
        file_label_topline.grid(row=row_number, column=file_column)
        for index in range(count_of_history_for_show):
            row_number += 1
            record: dict = change_list[index]
            type_of_record = record["type"]
            if type_of_record == 'directory':
                type_of_record = 'dir'
            path = record["path"]
            status = record["status"]
            time = record["change"]["time"]
            files = record["file"]
            file_content = ""
            for file in files:
                file_content += file + '\n'
            author = record["change"]["author"]
            message = record["change"]["message"]
            type_label = Label(history_display_panel, text=type_of_record, bg='white')
            type_label.grid(row=row_number, column=type_column)
            wraplength = 300
            path_label = Label(history_display_panel, text=path, width=30, height=3, wraplength=wraplength, anchor="center", bg='white')
            path_label.grid(row=row_number, column=path_column)
            time_label = Label(history_display_panel, text=time, width=20, bg='white')
            time_label.grid(row=row_number, column=time_column)
            author_label = Label(history_display_panel, text=author, bg='white')
            author_label.grid(row=row_number, column=author_column)
            status_label = Label(history_display_panel, text=status, bg='white')
            status_label.grid(row=row_number, column=status_column)
            wraplength = 300
            message_label = Label(history_display_panel, text=message, width=30, height=3, wraplength=wraplength, anchor="center", bg='white')
            message_label.grid(row=row_number, column=message_column)
            wraplength = 300
            file_label = Label(history_display_panel, text=file_content, width=30, height=3, wraplength=wraplength, anchor="center", bg='white')
            file_label.grid(row=row_number, column=file_column)
        row_number += 1
        if ellipsis != '':
            ellipsis_label = Label(history_display_panel, text=ellipsis, font=('Arial', 25), bg='white')
            ellipsis_label.grid(row=row_number, column=4)
        history_display_panel.pack()


    def show_all_history():
        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        change_list = robot.get_show_list()
        if change_list == []:
            hint("the change history is empty")
            return
        length = 1350
        height = 670
        content_window = Tk()
        content_window.geometry(f'{length}x{height}')
        content_window.configure(bg="white")
        content_window.title('all focused change')
        canvas = Canvas(content_window, bg='white')
        myscrollbar=Scrollbar(content_window,orient="vertical",command=canvas.yview)
        myscrollbar.place(x=length - 15, y=0, height=height)
        canvas.configure(yscrollcommand=myscrollbar.set)
        canvas.place(x=0, y=0, width=length, height=height)
        content_frame = Frame(canvas, bg='white')
        content_frame.bind("<Configure>",myfunction)
        canvas.create_window((75, 40), window=content_frame,anchor="nw")
        # frame_title = Label(content_frame, text="all focus", font=('Arial', 18), bg='white')
        # frame_title.grid(row=0, column=4, pady=20)
        row_number = 0
        type_label_topline = Label(content_frame, text="type", font=('Arial', 16), bg='white')
        type_label_topline.grid(row=row_number, column=type_column, pady=15, padx=10)
        path_label_topline = Label(content_frame, text="path", font=('Arial', 16), bg='white')
        path_label_topline.grid(row=row_number, column=path_column)
        time_label_topline = Label(content_frame, text="time", font=('Arial', 16), bg='white')
        time_label_topline.grid(row=row_number, column=time_column)
        author_label_topline = Label(content_frame, text="author", font=('Arial', 16), bg='white')
        author_label_topline.grid(row=row_number, column=author_column, padx=5)
        status_label_topline = Label(content_frame, text="status", font=('Arial', 16), bg='white')
        status_label_topline.grid(row=row_number, column=status_column, padx=10)
        message_label_topline = Label(content_frame, text="message", font=('Arial', 16), bg='white')
        message_label_topline.grid(row=row_number, column=message_column)
        file_label_topline = Label(content_frame, text="file", font=('Arial', 16), bg='white')
        file_label_topline.grid(row=row_number, column=file_column)
        for index in range(len(change_list)):
            row_number += 1
            record: dict = change_list[index]
            type_of_record = record["type"]
            if type_of_record == 'directory':
                type_of_record = 'dir'
            path = record["path"]
            time = record["change"]["time"]
            status = record["status"]
            author = record["change"]["author"]
            message = record["change"]["message"]
            files = record["file"]
            file_content = ""
            for file in files:
                file_content += file + '\n'
            type_label = Label(content_frame, text=type_of_record, bg='white')
            type_label.grid(row=row_number, column=type_column)
            wraplength = 300
            path_label = Label(content_frame, text=path, width=30, height=3, wraplength=wraplength, anchor="center", bg='white')
            path_label.grid(row=row_number, column=path_column)
            time_label = Label(content_frame, text=time, width=20, bg='white')
            time_label.grid(row=row_number, column=time_column)
            author_label = Label(content_frame, text=author, bg='white')
            author_label.grid(row=row_number, column=author_column)
            status_label = Label(content_frame, text=status, bg='white')
            status_label.grid(row=row_number, column=status_column, padx=10)
            wraplength = 300
            message_label = Label(content_frame, text=message, width=30, height=3, wraplength=wraplength, anchor="center", bg='white')
            message_label.grid(row=row_number, column=message_column)
            wraplength = 300
            file_label = Label(content_frame, text=file_content, width=30, height=3, wraplength=wraplength, anchor="center", bg='white')
            file_label.grid(row=row_number, column=file_column)
        content_window.mainloop()


    def show_all_focus():
        def myfunction(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        focus_file_list, focus_directory_list = robot.get_focus_list(robot._tree)
        if focus_file_list == [] and focus_directory_list == []:
            hint("your focus is empty")
            return
        length = 440
        height = 500
        content_window = Tk()
        content_window.geometry(f'{length}x{height}')
        content_window.configure(bg="white")
        content_window.title('all focus')
        canvas = Canvas(content_window, bg='white')
        myscrollbar=Scrollbar(content_window,orient="vertical",command=canvas.yview)
        myscrollbar.place(x=length - 15, y=0, height=height)
        canvas.configure(yscrollcommand=myscrollbar.set)
        canvas.place(x=0, y=0, width=length, height=height)
        content_frame = Frame(canvas, bg='white')
        content_frame.bind("<Configure>",myfunction)
        canvas.create_window((65, 50), window=content_frame,anchor="nw")
        # frame_title = Label(content_frame, text="all focus", font=('Arial', 18), bg='white')
        # frame_title.grid(row=0, columnspan=2, pady=20)
        row_number = 0
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
            path_label = Label(content_frame, text=path, width=30, height=3, wraplength=wraplength, anchor="center", bg='white')
            path_label.grid(row=row_number, column=1)
        for item in focus_directory_list:
            row_number += 1
            type_of_record = "dir"
            path = item
            type_label = Label(content_frame, text=type_of_record, bg='white')
            type_label.grid(row=row_number, column=0)
            wraplength = 300
            path_label = Label(content_frame, text=path, width=30, height=3, wraplength=wraplength, anchor="center", bg='white')
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
    file_message_label = Label(add_delete_grid, text="path: ", bg='white', font=('Arial', 15))
    file_message_label.grid(row=0, column=0, pady=0)
    file_message_entry = Entry(add_delete_grid, bg='white')
    file_message_entry.grid(row=0, column=1)
    file_message_add = Button(add_delete_grid, text='add', command=add_focus_file)
    file_message_add.configure(bg="white")
    file_message_add.grid(row=0, column=2)
    file_message_delete = Button(add_delete_grid, text='delete', command=delete_focus_file, bg='black')
    file_message_delete.grid(row=0, column=3)
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