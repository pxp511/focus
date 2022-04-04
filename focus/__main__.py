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
    if not os.path.isdir(repository):
        print(f"ERROE: is not a repository")
        exit()
    if not os.path.isdir(os.path.join(repository, '.git')):
        print(f"ERROE: is not a git repository")
        exit()
    os.chdir(f'{repository}')

    focus_dir = f"{repository}/.git/.focus"
    hash_path = f"{focus_dir}/hash"
    diff_file = f"{focus_dir}/diff"
    focus_path = f"{focus_dir}/focus.json"
    history_path = f"{focus_dir}/history.json"
    focus_history = f"{focus_dir}/focus_history.json"

    hashnumber = ""
    if os.path.isdir(focus_dir):
        with open(hash_path, 'r') as f:
            hashnumber = f.readline()
    else:
        os.mkdir(focus_dir)
        hashnumber = os.popen(f"git rev-parse HEAD").read()[:-1]
        with open(hash_path, 'w') as f:
            f.write(hashnumber)        

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