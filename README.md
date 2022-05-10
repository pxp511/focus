# focus

干了什么:
    自动将当前HEAD所在分支所跟踪的远程代码fetch到本地，并与当前HEAD比较，得出你所关心的差异

todo:
    文字无法对齐，怀疑是tkinter的显示问题，图形界面使用可滑动的grid而不是label
    目录变化的话加上文件

环境要求:
    python 3.10

库要求:
    tkinter
    multiprocessing

下载:
    python3 -m pip install focus-xp -U

使用:
    python3 -m focus -r GIT_REPOSITORY

!!!注意事项:
    增加或删除关注点的时候请填写完整路径
    十分钟自动fetch一次，也可以自己手动点击fetch
    添加或删除关注点后点击renew展示窗口就会随之更新
    renew不会自动fetch
    HEAD默认位于当前分支最后一个提交位置，如果HEAD分离将得出奇怪的结果或程序崩溃。