import os
import argparse
import pickle
from focus.Ftree import add_focus, delete_focus, get_changed_focus
import focus.ui as ui
from time import sleep
from focus.gittree import defalut_tree_construct
from multiprocessing import Process


def str2bool(s: str) -> bool:
    if s in ["False", 'false', 'f', '0']:
        return False
    elif s in ["True", 'true', 't', '1']:
        return True
    else:
        print(f"argument error: debug = s")
        exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--add',
        type=str,
        default=[],
        nargs="+",
        help=f"mark one or more concerns",
    )
    parser.add_argument(
        '-d',
        '--delete',
        type=str,
        default=[],
        nargs="+",
        help=f"delete one or more concerns",
    )
    parser.add_argument(
        '-u',
        '--ui',
        action="store_true",
        help=f"user interface",
    )
    parser.add_argument(
        '--show',
        action="store_true",
        help=f"show all concerns that changed briefly",
    )
    parser.add_argument(
        '--show_detail',
        action="store_true",
        help=f"show all concerns that changed in detail",
    )
    args = parser.parse_args()
    concerns_for_add = args.add
    concerns_for_delete = args.delete
    is_ui = args.ui
    show = args.show
    show_detail = args.show_detail
    pwd = os.getcwd()
    if not os.path.isdir(pwd):
        print(f"ERROE: is not a repository")
        exit()
    if not os.path.isdir(os.path.join(pwd, '.git')):
        print(f"ERROE: is not a git repository")
        exit()
    # print(f"Now monitoring directory: {repository}")
    
    focus_dir = f"{pwd}/.git/.focus"
    tree_file = f"{focus_dir}/tree_obj"
    if not os.path.isdir(focus_dir):
        os.mkdir(focus_dir)
        tree = defalut_tree_construct()
    else:
        with open(tree_file, 'rb') as f:
            tree = pickle.load(f)
    tree.show(data_property="")
    for concern_for_add in concerns_for_add:
        add_focus(tree, concern_for_add)
    for concern_for_delete in concerns_for_delete:
        delete_focus(tree, concern_for_delete)
    with open(tree_file, 'wb') as f:
        pickle.dump(tree, f)
    if is_ui:
        ui.main(tree, tree_file)
    if show:
        change_list = get_changed_focus(tree)
        for item in change_list:
            print(f"{item['status']:<8} {item['type']:>11}: {item['path']}")
    if show_detail:
        change_list = get_changed_focus(tree)
        print(change_list)


if __name__ == '__main__':
    main()