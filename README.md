# SumaToolBox
SingUMA Group Lyric Tool &amp; ffmpeg tool


# 如何使用  
先将FFmpeg解压到lib目录下，运行需要Python3环境和安装相应的支持库（见Requirements.txt），或使用“一键安装需求”功能。  
点击“点我运行.bat”，或者使用cmd运行  
> python main.py  
进入命令行交互式界面，执行相应的操作。  

# 主要功能
程序的主要逻辑可以读入lrc文件并且转换为竖行，带卡拉OK功能的ass（特效字幕）文件。在此基础之上整合了相关的压制功能和歌词的下载功能。本程序适合对原理已经有相关基础的用户使用。  
使用的效果可以在我们的官方账户：https://space.bilibili.com/1844255459/ 中看到，欢迎关注。  

# 进阶使用
您可以对main.py中的功能进行二次开发，实现不同的特效模式、对齐和遮罩效果。  
主要的修改部分在变量ass_header的样式部分和函数convert_suma_to_ass的定位点、行高部分。  

# 已知的问题
1.生成的ass文件无法被aegisub正常解析  
解决方法：使用potplayer打开，使用快捷键ctrl+alt+s将字幕另存为即可。  

# 项目依赖
本项目的压制功能依赖于ffmpeg（ https://github.com/FFmpeg/FFmpeg ）感谢开源社区的贡献人员。  
本项目的lrc解析取自163MusicApi，仅作学习和交流使用，请勿滥用。  
