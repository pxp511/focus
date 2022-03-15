import os
import argparse
import focus.ui as ui
from time import sleep
from focus.Robot import Robot
from multiprocessing import Process


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r',
        '--repository',
        type=str,
        required=True,
        help=f'repository path',
    )
    args = parser.parse_args()
    repository = os.path.abspath(args.repository)
    if not os.path.isdir(os.path.join(repository, '.git')):
        print(f"ERROE: is not a git repository")
        exit()
    focus = f"{repository}/.git/.focus"
    focus_path = f"{focus}/focus.json"
    history_path = f"{focus}/history.json"
    focus_history = f"{focus}/focus_history.json"
    diff_file = f"{focus}/diff.txt"
    hash_path = f"{focus}/hash"
    if os.path.isdir(focus):
        os.system(f"rm -r {focus}")
    os.mkdir(focus)
    os.system(f'cd {repository}')
    os.system(f"git rev-parse HEAD > {hash_path}")
    with open(hash_path, 'r') as f:
        hashnumber = f.readline()[:-1]
        
    robot = Robot(
        query_interval=10,
        repository=repository,
        focus_file=focus_path,
        history_file=history_path,
        focus_history_file=focus_history,
        diff_file=diff_file,
        hashnumber=hashnumber,
        hash_path=hash_path,
        is_changed=False
        )
    # robot.store_change_to_diff_file()
    # robot.repository_query()
    # robot.change_focus_history()
    p1 = Process(target=ui.main, args=(robot,))
    p1.start()
    p2 = Process(target=robot.run)
    p2.start()
    while True:
        sleep(1)
        if not p1.is_alive():
            p2.terminate()
            break
        

if __name__ == '__main__':
    main()