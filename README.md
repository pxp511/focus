# focus

干了什么:
    自动将当前HEAD所在分支所跟踪的远程代码fetch到本地, 并与当前HEAD比较, 得出你所关心的差异

涉及文件:
    会在.git目录下生成一个.focus文件夹, 里面会有三个文件: focus.json, change.json, history.json, 可以直接通过编辑focus.json增加或者删除关注点, hange.json里存放的是所关注的文件或目录的远程变化

环境要求:
    python 3.10+
    git 1.7+

库要求:
    tkinter
    multiprocessing

下载:
    python3 -m pip install focus-xp -U

使用:
    python3 -m focus -r GIT_REPOSITORY

!!!注意事项:
    仅适用于git作为项目管理工具的仓库;
    仓库需要在本机存在(仅适用于本地开发);
    增加或删除关注点的时候请填写完整路径;
    如果所添加的关注文件或目录本地不存在但远程仓库存在, 请自行确保路径正确性;
    十分钟自动fetch一次, 也可以自己手动点击fetch;
    添加或删除关注点后展示窗口就会随之更新;
    HEAD默认位于当前分支, 如果HEAD分离将得出奇怪的结果或程序崩溃。