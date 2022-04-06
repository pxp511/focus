# focus

TODO: 适配远程开发
todo: 先获取修改的文件，再根据文件查看最后一次commit id，再根据commit id寻找time，author，commit message
# git log --pretty=oneline -1 README.md
# git log README.md
# git log --pretty=format:"%cd" HEAD -1 time
# git log --pretty=format:"%an" HEAD -1 author
# git log --pretty=format:"%s" HEAD -1 commit message
# git log --pretty=format:"%cd" -1 README.md
# git diff  HEAD^^ HEAD~3 --stat 两次commit所改动的文件概况
环境要求:
    python3

库要求：
    tkinter
    multiprocessing

下载:
    python3 -m pip install focus-xp -U

使用:
    python3 -m focus -r GIT_REPOSITORY