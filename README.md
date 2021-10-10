# EVE_Alarm

EVE预警频道监控

## 依赖

- Python3
- PySide2

## 游戏设置

把【聊天】选项卡下的【把聊天记录保存为文件】选项打开

## 配置文件

配置文件在 `setting.json` 中，如果发生错误，可以尝试删除配置文件，重新运行程序，自动生成新的配置文件。

- log_path: 游戏聊天日志的保存路径，注意目录之间用双斜杠分隔
- channel: 监听的频道名
- listener: 监听的游戏角色
- overtime: 单位秒，超过该时长的预警信息将被忽略
- special_overtime: 单位秒，超过该时长的特殊预警信息将被忽略
- ignore_distance： 超过该距离的预警信息将被忽略

## 环境搭建与使用

需搭建Python3 + PySide2环境

1. 安装Python3

   在 [Python官网](https://www.python.org/downloads/) 下载Python安装包安装即可，注意安装时，把 `Add Python 3.X to PATH`选项勾上。其余设置保持默认即可。

2. 安装PiSide2

   打开命令提示符，输入`pip install pyside2`即可。

3. 运行

   双击运行`run.bat`即可。