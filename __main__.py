import argparse
from Robot import Robot
import ui
import os
from multiprocessing import Process
from time import sleep

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--repository',
        type=str,
        required=True,
        help=f'repository path',
    )
    args = parser.parse_args()
    repository = args.repository
    focus = f"{repository}/.git/.focus"
    focus_path = f"{focus}/focus.json"
    history_path = f"{focus}/history.json"
    focus_history = f"{focus}/focus_history.json"
    diff_file = f"{focus}/diff.txt"
    hash_path = f"{focus}/hash"
    if os.path.isdir(focus):
        os.system(f"rm -r {focus}")
    os.mkdir(focus)
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