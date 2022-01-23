from ast import Return
from email import message
from tkinter import messagebox
import cmd_manager
from tkinter import *
import json
import utils
from Robot import Robot
import os
    

def main(robot: Robot):
    # maximum of changes for show 
    history_count = 3
    focus_history_path = robot._focus_history_file
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
    message_label_block = Label(message_panel_block, text="block name:")
    message_entry_block = Entry(message_panel_block)
    
    def add():
        nonlocal message_entry_file
        nonlocal message_entry_block
        file_path = message_entry_file.get()
        block_name = message_entry_block.get()
        if not utils.is_file(file_path):
            utils.hint("no such file")
            return 0
        if block_name == "":
            utils.hint("successfully add a focus file")
            cmd_manager.add_focus(file_path, block_name, False, robot)
        elif block_name != "":
            if not utils.is_block(block_name):
                utils.hint("no such block")
                return 0
            else:
                utils.hint("successfully add a focus block")
                cmd_manager.add_focus(file_path, block_name, True, robot)
            
    def delete():
        nonlocal message_entry_file
        nonlocal message_entry_block
        file_path = message_entry_file.get()
        block_name = message_entry_block.get()
        if not utils.is_file(file_path):
            utils.hint("no such file")
            return 0
        if block_name == "":
            utils.hint("successfully delete a focus file")
            cmd_manager.delete_focus(file_path, block_name, False)
        elif block_name != "":
            if not utils.is_block(block_name):
                utils.hint("no such block")
                return 0
            else:
                utils.hint("successfully delete a focus block")
                cmd_manager.delete_focus(file_path, block_name, True)
    
    def renew():
        focus_history_json = {}
        focus_history_json["change_list"] = []
        if os.path.isfile(focus_history_path):
            with open(focus_history_path, 'r') as f:
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
            file_path = record["file_path"]
            time = record["change"]["time"]
            block_name = record["block_name"]
            if type_of_record == "file":
                text = f"file: {file_path} time: {time}"
            elif type_of_record == "block":
                text = f"file: {file_path} block:{block_name}time: {time}"
            var_list[i].set(text)
            
    
    bottom_panel = Frame(root)
    add = Button(bottom_panel, text='add', command=add)
    delet = Button(bottom_panel, text='delete', command=delete)
    renew = Button(bottom_panel, text='renew', command=renew)
    
    message_label_file.pack(side=LEFT)
    message_entry_file.pack(side=RIGHT)
    message_label_block.pack(side=LEFT)
    message_entry_block.pack(side=RIGHT)
    message_panel_file.pack()
    message_panel_block.pack()
    add.pack()
    delet.pack()
    renew.pack()
    bottom_panel.pack()
    for label in label_list:
        label.pack()
    mainloop()
        
        

if __name__ == '__main__':
    main()
