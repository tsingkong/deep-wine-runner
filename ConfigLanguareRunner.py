#!/usr/bin/env python3
# 使用系统默认的 python3 运行
###########################################################################################
# 作者：gfdgd xi
# 版本：3.0.1
# 更新时间：2022年10月05日
# 感谢：感谢 wine 以及 deepin-wine 团队，提供了 wine 和 deepin-wine 给大家使用，让我能做这个程序
# 基于 Python3 构建
###########################################################################################
import os
import sys
import time
import json
import random
import updatekiller
# 阉割 Android 应用安装功能
#import uengineapi
import platform
import traceback
import webbrowser
import subprocess
import PyQt6.QtWidgets as QtWidgets
# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
information = json.loads(readtxt(f"{programPath}/information.json"))
version = information["Version"]
thankText = ""
helpList = json.loads(readtxt(f"{programPath}/ConfigLanguareRunner-help.json"))
for i in information["Thank"]:
    thankText += f"{i}\n"
programEnv = [
    ["($WINEPREFIX)", f"{os.path.expanduser('~')}/.wine"],
    ["($WINE)", "deepin-wine6-stable"],
    #["($DANGER)", "0"],
    ["($DANGER)", "1"],
    ["($HOME)", os.path.expanduser('~')],
    ["($PROGRAMPATH)", programPath],
    ["($VERSION)", version],
    ["($THANK)", thankText],
    ["($MAKER)", "gfdgd xi"],
    ["($COPYRIGHT)", f"©2020~{time.strftime('%Y')} gfdgd xi"],
    ["($?)", "0"],
    ["($PLATFORM)", platform.system()],
    ["($DEBUG)", "1"]
    #["($DEBUG)", str(int("--debug" in sys.argv))]
]
readOnlyEnv = [
    "($DANGER)",
    "($HOME)",
    "($PROGRAMPATH)",
    "($VERSION)",
    "($THANK)",
    "($MAKER)",
    "($COPYRIGHT)",
    "($?)",
    "($SYSTEM)",
    "($DEBUG)"
]

def FindFile(file, name):
    for i in os.listdir(file):
        path = f"{file}/{i}"
        if os.path.isdir(path):
            returnPath = FindFile(path, name)
            if returnPath != None:
                return returnPath.replace("//", "/")
        if os.path.isfile(path):
            if i == name:
                return path
    return None

def Debug():
    if "--debug" in sys.argv:
        traceback.print_exc()

class Command():
    # 有风险的命令
    dangerCommand = [
        "bash",
        "bat",
        "download",
        "reg"
    ]
    # 可以被使用的命令
    commandList = [
        "installdll",
        "installfont",
        "installsparkcorefont",
        "installmono",
        "installgecko",
        "installvcpp",
        "installnet",
        "installmsxml",
        "echo",
        "info",
        "error",
        "warning",
        "exit",
        "bash",
        "bat",
        "version",
        "thank",
        "pause",
        "download",
        "installdxvk",
        "createbotton",
        "reg",
        "enabledopengl",
        "disbledopengl",
        "winecfg",
        "winver",
        "changeversion",
        "stopdll",
        "cat",
        "taskmgr",
        "control",
        "killall",
        "killallwineserver",
        "enabledhttpproxy",
        "disbledhttpproxy",
        "enabledwinecrashdialog",
        "disbledwinecrashdialog",
        "disbledWinebottlecreatelink",
        "enabledWinebottlecreatelink",
        "installvb",
        "installother",
        "decompressionbottle",
        "programforum",
        "installmsi",
        "installapk"
    ]

    def __init__(self, commandString: str) -> None:
        self.commandString = commandString

    # 解析器
    # 命令字符串转可供解析的列表
    def GetCommandList(self) -> list:
        shellList = []
        shellFirstShell = self.commandString.split("\n")
        # 转换成可以执行的数组
        for l in range(0, len(shellFirstShell)):
            i = shellFirstShell[l]
            # 判断有没有注释
            if "#" in i:
                # 忽略注释
                i = i[:i.index("#")]
            # 删除前后空格
            i = i.strip()
            # 如果是空行
            if i == "":
                # 忽略此行，此行不做处理
                continue
            # 空格转义
            i = i.replace("\\ ", "@Space@")
            # 解析
            i = i.split()
            # 判断是否为合法的参数，否则提示并忽略
            if not i[0] in self.commandList and i[0][0] != "(":
                print(f"行{l + 1}命令{i[0]}不存在，忽略")
                programEnv[9][1] = "-2"
                continue
            if programEnv[2][1] == "0" and i[0] in self.dangerCommand:
                print(f"行{l + 1}命令{i[0]}目前解析器不允许运行，忽略")
                print("如果需要运行，可以在配置面板开启“允许修改系统”选项（针对GUI用户）")
                print("或添加参数 --system（终端调用运行用户）")
                programEnv[9][1] = "-1"
                continue
            rightList = []
            for k in i:
                # 处理符号转义
                rightList.append(k.replace("@Space@", " ").replace("\\n", "\n").replace("\\r", "\r"))
            shellList.append(rightList)
        return shellList

    # 运行器
    class Run():      
        close = False
        programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
        def Exit(self):
            self.close = True
            return 0

        def InstallDll(self) -> int:
            import InstallDll
            # 如果是数字
            number = False
            try:
                int(self.command[1])
                number = True
            except:
                pass
            if number:
                return InstallDll.Download(self.wineBottonPath, InstallDll.GetNameByNumber(int(self.command[1])), InstallDll.GetUrlByNumber(int(self.command[1])), self.wine)
            return InstallDll.Download(self.wineBottonPath, self.command[1], InstallDll.GetUrlByName(self.command[1]), self.wine)

        def InstallDxvk(self):
            if not os.path.exists(f"{programPath}/dxvk"):
                if os.system(f"7z x \"{programPath}/dxvk.7z\" -o\"{programPath}\""):
                    print("错误：无法解压资源")
                    return 1
                os.remove(f"{programPath}/dxvk.7z")
            return os.system(f"env 'WINE={self.wine}' 'WINE64={self.wine}' 'WINEPREFIX={self.wineBottonPath}' bash '{programPath}/dxvk/auto.sh' install")

        def Thank(self) -> int:
            for i in information["Thank"]:
                print(i)
            return 0

        def InstallFont(self) -> int:
            import InstallFont
            return InstallFont.Download(self.wineBottonPath, int(self.command[1]))
        
        def InstallMono(self) -> int:
            return os.system(f"ENTERNOTSHOW=0 '{self.programPath}/InstallMono.py' '{self.wineBottonPath}' '{self.wine}' mono")

        def InstallGecko(self) -> int:
            return os.system(f"ENTERNOTSHOW=0 '{self.programPath}/InstallMono.py' '{self.wineBottonPath}' '{self.wine}' gecko")

        def InstallVCPP(self) -> int:
            import InstallVisualCPlusPlus
            return InstallVisualCPlusPlus.Download(self.wineBottonPath, int(self.command[1]), self.wine)

        def InstallNet(self) -> int:
            import InstallNetFramework
            return InstallNetFramework.Download(self.wineBottonPath, int(self.command[1]), self.wine)

        def InstallMsxml(self) -> int:
            import InstallMsxml
            return InstallMsxml.Download(self.wineBottonPath, int(self.command[1]), self.wine)

        def Info(self) -> int:
            QtWidgets.QMessageBox.information(None, self.command[1], self.command[2])
            return 0

        def StopDll(self) -> int:
            return os.system(f"WINEPREFIX='{self.wineBottonPath}' '{self.wine}' reg add 'HKEY_CURRENT_USER\\Software\\Wine\\DllOverrides' /v {os.path.splitext(self.command[1])[0]}  /f")

        def CreateBotton(self):
            self.command = ["bat", "exit"]
            self.Bat()
            return 0

        def InstallSparkCoreFont(self):
            if not os.system("which aptss"):
                # 最新版本星火应用商店处理
                os.system("pkexec bash aptss ssupdate")
                return os.system("pkexec bash aptss install ms-core-fonts")
            if not os.system("which ss-apt-fast"):
                # 稍久的版本
                os.system("pkexec ss-apt-fast update")    
                return os.system("pkexec bash ss-apt-fast install ms-core-fonts")
            # 不知道什么版本的处理方法
            if not os.system("which apt-fast"):
                # 稍久的版本
                os.system("pkexec apt-fast update")    
                return os.system("pkexec apt-fast install ms-core-fonts")
            os.system("pkexec apt update")    
            return os.system("pkexec apt install ms-core-fonts")

        def Echo(self) -> int:
            del self.command[0]
            print(" ".join(self.command))
            return 0

        def Warning(self):
            QtWidgets.QMessageBox.warning(None, self.command[1], self.command[2])
            return 0

        def Error(self):
            QtWidgets.QMessageBox.critical(None, self.command[1], self.command[2])
            return 0

        def Bash(self):
            command = ""
            for i in self.command[1:]:
                command += f"'{i}' "
            return os.system(command)

        def Bat(self) -> int:
            # Windows 直接转换为以 cmd 运行
            if platform.system() == "Windows":
                # 直接调用 Bash 函数
                return self.Bash()
            command = ["WINEPREFIX='($WINEPREFIX)'", "($WINE)"]
            for i in programEnv:
                for k in range(len(command)):
                    command[k] = command[k].replace(i[0], i[1])
            for i in self.command[1:]:
                command.append(i)
            commandStr = command[0] + " "
            for i in command[1:]:
                commandStr += f"'{i}' "
            return os.system(commandStr)

        def Version(self):
            print(f"版本：{version}")
            print(f"©2020~{time.strftime('%Y')} gfdgd xi")
            return 0

        def Pause(self) -> int:
            input("按回车键继续……")
            return 0

        def Download(self) -> int:
            command = f"aria2c -x 16 -s 16 -c '{self.command[1]}' "
            try:
                command += f"-d '{self.command[2]}' "
                command += f"-o '{self.command[3]}' "
            except:
                pass
            return os.system(command)

        def Reg(self) -> int:
            self.command = ["bat", "regedit", "/s", self.command[1]]
            return self.Bat()

        def EnabledOpenGl(self) -> int:
            self.command = ["reg", f"z:{programPath}/EnabledOpengl.reg"]
            return self.Reg()

        def DisbledOpenGl(self) -> int:
            self.command = ["reg", f"z:{programPath}/DisabledOpengl.reg"]
            return self.Reg()

        def Winver(self):
            self.command = ["bat", "winver"]
            return self.Bat()

        def Winecfg(self):
            self.command = ["bat", "winecfg"]
            return self.Bat()

        def ChangeVersion(self):
            # 判断是否为正确的版本
            if not os.path.exists(f"{programPath}/ChangeWineBottonVersion/{self.command[1]}.reg"):
                print("错误：您选择的版本错误，目前只支持以下版本")
                for i in os.listdir(f"{programPath}/ChangeWineBottonVersion"):
                    print(i.replace(".reg", ""), end=" ")
                print()
                return 1
            self.command = ["reg", f"z:/{programPath}/ChangeWineBottonVersion/{self.command[1]}.reg"]
            return self.Reg()

        def Cat(self):
            try:
                file = open(self.command[1], "r")
                print(file.read())
                file.close()
                return 0
            except:
                print("文件读取错误")
                Debug()
                return 1

        def Taskmgr(self):
            self.command = ["bat", "taskmgr"]
            return self.Bat()

        def Control(self):
            self.command = ["bat", "control"]
            return self.Bat()

        def Killall(self):
            return os.system(f"killall -9 {self.command[1]}")

        def KillallWineServer(self):
            command = ["WINEPREFIX='($WINEPREFIX)'", "($WINE)", "-k"]
            for i in programEnv:
                for k in range(len(command)):
                    command[k] = command[k].replace(i[0], i[1])
            if "box86" in command[1] or "exagear" in command[1] or "box64" in command[1]:
                print("不支持此 Wine")
                return 1
            if os.path.exists(command[1]):
                # 文件存在
                command[1] = f"{os.path.dirname(command[1])}/wineserver"
            else:
                # 读 which
                command[1] = f"{os.path.dirname(subprocess.getoutput(f'which {command[1]}').strip())}/wineserver" 
            commandStr = command[0] + " "
            for i in command[1:]:
                commandStr += f"'{i}' "
            return os.system(commandStr)
            
        def EnabledWineBottleCreateLink(self):
            self.command = ["bat", "reg", "delete", "HKEY_CURRENT_USER\\Software\\Wine\\DllOverrides", "/v", "winemenubuilder.exe", "/f"]
            return self.Bat()

        def DisbledWineBottleCreateLink(self):
            self.command = ["bat", "reg", "add", "HKEY_CURRENT_USER\\Software\\Wine\\DllOverrides", "/v", "winemenubuilder.exe", "/f"]
            return self.Bat()

        def DisbledWineCrashDialog(self):
            self.command = ["bat", "reg", "add", "HKEY_CURRENT_USER\\Software\\Wine\\WineDbg", "/v", "ShowCrashDialog", "/t", "REG_DWORD", "/d", "00000000", "/f"]
            return self.Bat()

        def EnabledWineCrashDialog(self):
            self.command = ["bat", "reg", "add", "HKEY_CURRENT_USER\\Software\\Wine\\WineDbg", "/v", "ShowCrashDialog", "/t", "REG_DWORD", "/d", "00000001", "/f"]
            return self.Bat()

        def EnabledHttpProxy(self):
            proxyServerAddress = self.command[1]
            port = self.command[2]
            self.command = ["bat", "reg", "add", "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", "/v", "ProxyEnable", "/t", "REG_DWORD", "/d", "00000001", "/f"]
            self.Bat()
            self.command = ["bat", "reg", "add", "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", "/v", "ProxyServer", "/d", f"{proxyServerAddress}:{port}", "/f"]
            return self.Bat()

        def DecompressionBottle(self):
            tempDebDir = f"/tmp/wine-runner-unpack-deb-{random.randint(0, 1000)}"
            if os.system(f"dpkg -x '{self.command[1]}' '{tempDebDir}'"):
                return 1
            zippath = FindFile(tempDebDir, "files.7z")
            if zippath == None:
                return 2
            # 解压文件
            os.system(f"mkdir -p '{self.command[2]}'")
            fi = os.system(f"7z x -y '{zippath}' -o'{self.command[2]}'")
            os.system(f"rm -rfv '{tempDebDir}'")
            return fi
            

        def DisbledHttpProxy(self):
            self.command = ["bat", "reg", "add", "HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings", "/v", "ProxyEnable", "/t", "REG_DWORD", "/d", "00000000", "/f"]
            return self.Bat()

        def InstallVB(self):
            import InstallVisualBasicRuntime
            return InstallVisualBasicRuntime.Download(self.wineBottonPath, int(self.command[1]), self.wine)

        def InstallOther(self):
            import InstallOther
            return InstallOther.Download(self.wineBottonPath, int(self.command[1]), self.wine)

        def ProgramForum(self):
            webbrowser.open_new_tab("https://gfdgdxi.flarum.cloud/")
            return

        def InstallMSI(self):
            self.command = ["bat", "msiexec", "/i", self.command[1]]
            return self.Bat()

        def InstallApk(self):
            if os.system("which uengine > /dev/null"):
                print("未安装 UEngine，无法使用该命令")
                return 1
            apk = uengineapi.APK(self.command[1])
            result = apk.install()
            homePath = os.getenv("HOME")
            if not os.path.exists(f"{homePath}/.local/share/applications/uengine"):
                os.makedirs(f"{homePath}/.local/share/applications/uengine")
            if not os.path.exists(f"{homePath}/.local/share/icons/hicolor/apps"):
                os.makedirs(f"{homePath}/.local/share/icons/hicolor/apps")
            package = apk.packageName()
            apk.saveApkIcon(f"{homePath}/.local/share/icons/hicolor/apps/{package}.png")
            apk.saveDesktopFile(f"{homePath}/.local/share/applications/uengine/{package}.desktop", f"{homePath}/.local/share/icons/hicolor/apps/{package}.png")
            return result

        # 可以运行的命令的映射关系
        # 可以被使用的命令的映射
        commandList = {
            "installdll": InstallDll,
            "installfont": InstallFont,
            "installsparkcorefont": InstallSparkCoreFont,
            "installmono": InstallMono,
            "installgecko": InstallGecko,
            "installvcpp": InstallVCPP,
            "installnet": InstallNet,
            "installmsxml": InstallMsxml,
            "echo": Echo,
            "info": Info,
            "warning": Warning,
            "error": Error,
            "exit": Exit,
            "bash": Bash,
            "bat": Bat,
            "version": Version,
            "thank": Thank,
            "pause": Pause,
            "download": Download,
            "installdxvk": InstallDxvk,
            "createbotton": CreateBotton,
            "reg": Reg,
            "enabledopengl": EnabledOpenGl,
            "disbledopengl": DisbledOpenGl,
            "winecfg": Winecfg,
            "winver": Winver,
            "changeversion": ChangeVersion,
            "stopdll": StopDll,
            "cat": Cat,
            "taskmgr": Taskmgr,
            "control": Control,
            "killallwineserver": KillallWineServer,
            "enabledhttpproxy": EnabledHttpProxy,
            "disbledhttpproxy": DisbledHttpProxy,
            "enabledwinecrashdialog": EnabledWineCrashDialog,
            "disbledwinecrashdialog": DisbledWineCrashDialog,
            "disbledWinebottlecreatelink": DisbledWineBottleCreateLink,
            "enabledWinebottlecreatelink": EnabledWineBottleCreateLink,
            "installvb": InstallVB,
            "installother": InstallOther,
            "decompressionbottle": DecompressionBottle,
            "programforum": ProgramForum,
            "installmsi": InstallMSI,
            "installapk": InstallApk
        }

        # 参数数列表
        commandInfo = {
            "killall": [1],
            "installdll": [1],
            "installfont": [1],
            "installsparkcorefont": [0],
            "installmono": [0],
            "installgecko": [0],
            "installvcpp": [1],
            "installnet": [1],
            "installmsxml": [1],
            "echo": [1],
            "info": [2],
            "warning": [2],
            "error": [2],
            "exit": [0],
            "bash": [1],
            "bat": [1],
            "version": [0],
            "thank": [0],
            "pause": [0],
            "download": [1],
            "installdxvk": [0],
            "createbotton": [0],
            "reg": [1],
            "enabledopengl": [0],
            "disbledopengl": [0],
            "winecfg": [0],
            "winver": [0],
            "changeversion": [1],
            "stopdll": [1],
            "cat": [1],
            "taskmgr": [0],
            "control": [0],
            "killallwineserver": [0],
            "enabledhttpproxy": [2],
            "disbledhttpproxy": [0],
            "enabledwinecrashdialog": [0],
            "disbledwinecrashdialog": [0],
            "disbledWinebottlecreatelink": [0],
            "enabledWinebottlecreatelink": [0],
            "installvb": [1],
            "installother": [1],
            "decompressionbottle": [2],
            "programforum": [0],
            "installmsi": [1],
            "installapk": [1]
        }
        windowsUnrun = [
            "createbotton",
            "installdll",
            "installmono",
            "installgecko",
            "winecfg",
            "stopdll",
            "changeversion",
            "enabledopengl",
            "disbledopengl",
            "installdxvk",
            "installfont",
            "installsparkcorefont",
            "decompressionbottle",
            "installapk"
        ]
        # 解析
        def __init__(self, command: list, wineBottonPath: str, wine: str) -> int:
            self.wineBottonPath = wineBottonPath
            self.wine = wine
            for i in command:
                self.command = i
                # 变量解析
                if self.command[0][0] == "(" and "=" in self.command[0]:
                    env = i[0][: i[0].index("=")]
                    value = i[0][i[0].index("=") + 1:]
                    # 判断是不是只读变量
                    if env in readOnlyEnv:
                        print(f"运行命令{' '.join(self.command)}出现错误")
                        print(f"变量 {env} 只读，无法修改，忽略")
                        continue
                    change = False
                    for k in range(len(programEnv)):
                        # 修改变量
                        if env == programEnv[k][0]:
                            programEnv[k][1] = value
                            change = True
                            break
                    if not change:
                        # 添加变量
                        programEnv.append([f"{env}", value])
                    continue
                # 解析命令是否可以在 Windows 使用（只限在 Windows 系统时）
                if platform.system() == "Windows" and i[0] in self.windowsUnrun:
                    print("此命令不支持在 Windows 上运行")
                    programEnv[9][1] = "-5"
                    continue
                # 获取程序帮助信息
                try:
                    if i[1] == "--help":
                        print(helpList[i[0]].replace("\\n", "\n"))
                        continue
                except:
                    pass
                # 正常命令解析
                if len(i) -1 < self.commandInfo[i[0]][0]:
                    print("参数不足")
                    programEnv[9][1] = "-3"
                    continue
                # 替换环境变量
                for a in range(1, len(i)):
                    for b in programEnv:
                        if b[0] in i[a]:
                            i[a] = i[a].replace(b[0], b[1])
                try:
                    commandReturn = self.commandList[i[0]](self)
                except:
                    traceback.print_exc()
                    commandReturn = 1
                if commandReturn:
                    print(f"运行命令{' '.join(self.command)}出现错误，返回值:", commandReturn)
                programEnv[9][1] = str(commandReturn)
                if self.close: 
                    break

app = QtWidgets.QApplication(sys.argv)
if os.getenv("WINE") != None:
    programEnv[1][1] = os.getenv("WINE")
if os.getenv("WINEPREFIX") != None:
    programEnv[0][1] = os.getenv("WINEPREFIX")
if __name__ == "__main__":
    optionAll = 0
    if "--debug" in sys.argv:
        optionAll += 1
    if "--system" in sys.argv:
        programEnv[2][1] = "1"
        optionAll += 1
    if len(sys.argv) - optionAll < 2:
        print("Wine 运行器自动配置文件解析器交互环境")
        print(f"版本：{version}")
        print(f"©2020~{time.strftime('%Y')} By gfdgd xi")
        print("--------------------------------------------------------------")
        while True:
            commandLine = input(">")
            if commandLine == "exit":
                break
            com = Command(commandLine)
            com.Run(com.GetCommandList(), programEnv[0][1], programEnv[1][1])
        sys.exit(int(programEnv[9][1]))
    # 读取文件
    try:
        file = open(sys.argv[1], "r")
        com = Command(file.read())
        file.close()
    except:
        print("错误：无法读取该文件，无法继续")
        sys.exit(1)
    print("Wine 运行器自动配置文件解析器")
    print(f"版本：{version}")
    print(f"©2020~{time.strftime('%Y')} gfdgd xi")
    print("--------------------------------------------------------------")
    com.Run(com.GetCommandList(), programEnv[0][1], programEnv[1][1])
    sys.exit(int(programEnv[9][1]))