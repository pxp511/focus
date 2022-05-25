import os
import argparse
import pickle
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
        '-q',
        '--queryinterval',
        type=int,
        default=600,
        help=f"query interval setting",
    )
    args = parser.parse_args()
    queryinterval = args.queryinterval
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
        with open(tree_file, 'wb') as f:
            pickle.dump(tree, f)
    else:
        with open(tree_file, 'rb') as f:
            tree = pickle.load(f)
    tree.show(data_property="")
    ui.main(tree, tree_file)

        

if __name__ == '__main__':
    main()