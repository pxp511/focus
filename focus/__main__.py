import os
import argparse
import focus.ui as ui
from time import sleep
from focus.Robot import Robot
from multiprocessing import Process


def str2bool(s: str) -> bool:
    if s == "False":
        return False
    elif s == "True":
        return True
    else:
        print(f"argument error: debug = s")
        exit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-r',
        '--repository',
        type=str,
        required=True,
        help=f'repository path',
    )
    parser.add_argument(
        '-d',
        '--debug',
        type=str2bool,
        default=False,
        help=f"for debug, ignore this argument",
    )
    parser.add_argument(
        '-q',
        '--queryinterval',
        type=int,
        default=600,
        help=f"for debug, ignore this argument",
    )
    args = parser.parse_args()
    repository = os.path.abspath(args.repository)
    queryinterval = args.queryinterval
    debug = args.debug
    if not os.path.isdir(repository):
        print(f"ERROE: is not a repository")
        exit()
    if not os.path.isdir(os.path.join(repository, '.git')):
        print(f"ERROE: is not a git repository")
        exit()
    os.chdir(f'{repository}')

    robot = Robot(
        repository=repository,
        debug=debug,
        queryinterval=queryinterval
        )

    p1 = Process(target=ui.main, args=(repository,))
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