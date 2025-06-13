#!/usr/bin/env python3
# 读取设置单独用一个 py 文件
import os
import sys
import json
import base64
import shutil
import getpass
import datetime
import traceback
import subprocess
import webbrowser
import configparser
import PyQt6.QtGui as QtGui
import PyQt6.QtCore as QtCore
import PyQt6.QtWidgets as QtWidgets

TMPDIR = os.getenv("TMPDIR")
if (TMPDIR == None):
    TMPDIR = ""

# 获取用户主目录
def get_home():
    return os.path.expanduser('~')

# 读取文本文档
def readtxt(path):
    f = open(path, "r") # 设置文件对象
    str = f.read()  # 获取内容
    f.close()  # 关闭文本对象
    return str  # 返回结果

fontSize = 1
'''tempSys = QtWidgets.QApplication(sys.argv)
if tempSys.primaryScreen().availableGeometry().size().width() < 1366 or tempSys.primaryScreen().availableGeometry().size().height() < 768:
    fontSize = 1.1'''

defultProgramList = {
    "Architecture": "Auto",
    "Debug": True,
    "DefultWine": "deepin-wine8-stable",
    "DefultBotton" : get_home() + "/.wine",
    "TerminalOpen": False,
    "WineOption": "",
    "WineBottonDifferent": False,
    "CenterWindow": False,
    "Theme": "",
    "MonoGeckoInstaller": False,
    "AutoWine": True,
    "RuntimeCache": True,
    "MustRead": False,
    "BuildByBottleName": False,
    "AutoPath": False,
    "QemuUnMountHome": False,
    "Chinese": True,
    "FontSize": fontSize
}

programPath = os.path.split(os.path.realpath(__file__))[0]  # 返回 string
iconPath = "{}/deepin-wine-runner.svg".format(programPath)
try:
    information = json.loads(readtxt(f"{programPath}/information.json"))
    setting = json.loads(readtxt(get_home() + "/.config/deepin-wine-runner/WineSetting.json"))
except:
    traceback.print_exc()
    setting = defultProgramList

def SetFont(app):
    defaultFont = app.font()
    size = setting["FontSize"]
    font = QtGui.QFont(defaultFont)
    if size == 1:
        app.setFont(defaultFont)    
        return
    font.setPixelSize(int(defaultFont.pixelSize() / size))
    font.setPointSize(int(defaultFont.pointSize() / size))
    app.setFont(font)

def getFileFolderSize(fileOrFolderPath):
    """get size for file or folder"""
    totalSize = 0
    try:
        if not os.path.exists(fileOrFolderPath):
            return totalSize
        if os.path.isfile(fileOrFolderPath):
            totalSize = os.path.getsize(fileOrFolderPath)  # 5041481
            return totalSize
        if os.path.islink(fileOrFolderPath):
            return 0
        if os.path.isdir(fileOrFolderPath):
            with os.scandir(fileOrFolderPath) as dirEntryList:
                for curSubEntry in dirEntryList:
                    curSubEntryFullPath = os.path.join(fileOrFolderPath, curSubEntry.name)
                    if curSubEntry.is_dir():
                        curSubFolderSize = getFileFolderSize(curSubEntryFullPath)  # 5800007
                        totalSize += curSubFolderSize
                    elif curSubEntry.is_file():
                        curSubFileSize = os.path.getsize(curSubEntryFullPath)  # 1891
                        totalSize += curSubFileSize
                return totalSize
    except:
        return totalSize

def FileToBase64(filePath):
    src = ""
    with open(filePath, "rb") as f:
        base64Byte = base64.b64encode(f.read())
        src += base64Byte.decode("utf-8")
    return src

def SaveLogWindow():
    pass

def OpenUrl(url):
    print(url.url())
    # 判断是否可以使用小窗打开
    webbrowser.open_new_tab(url.url())

def Appreciate():
    global messageAppreciate
    messageAppreciate = QtWidgets.QTextBrowser()
    messageAppreciate.setHtml(f"""<h3>请作者喝杯茶</h3>
    <p>如果您觉得 Wine 运行器对你有帮助，可以请作者喝杯茶 </p>
    <p>
        <img src="{programPath}/Icon/QR/Wechat.png" width="250"  /> 
        <img src="{programPath}/Icon/QR/Alipay.jpg" width="250"  />
        <img src="{programPath}/Icon/QR/QQ.png" width="250" >
    </p>
    <hr/>
    <h3>广告</h3>
    <p>支付宝官方活动，扫描获得支付红包！</p>
    <p><img src="{programPath}/Icon/QR/advertisement0.jpg" width="250" ></p>""")
    messageAppreciate.resize(int(messageAppreciate.frameGeometry().width() * 1.5), int(messageAppreciate.frameGeometry().height() * 1.2))
    messageAppreciate.setWindowTitle("赞赏作者/请作者喝杯茶")
    messageAppreciate.show()

# 显示“关于这个程序”窗口
def about_this_program()->"显示“关于这个程序”窗口":
    global about
    global title
    global iconPath
    global clickIconTime
    clickIconTime = 0
    QT.message = QtWidgets.QMainWindow()  
    QT.message.setWindowIcon(QtGui.QIcon(iconPath))
    messageWidget = QtWidgets.QWidget()
    messageWidget.setObjectName("messageWidget")
    messageWidget.setStyleSheet(f"QWidget#messageWidget {{background: url({programPath}/Icon/Program/about-background.png) no-repeat;background-position: left bottom;}}")
    QT.message.setWindowTitle(f"关于 {title}")
    messageLayout = QtWidgets.QGridLayout()
    iconShow = QtWidgets.QLabel(f"<a href='https://www.gfdgdxi.top'><img width=256 src='{iconPath}'></a>")
    def ChangeIcon():
        global clickIconTime
        if clickIconTime >= 0:
            clickIconTime = clickIconTime + 1
        if clickIconTime > 0:
            clickIconTime = -1
            for k in ["", "Function", "Program"]:
                try:
                    for i in os.listdir(f"{programPath}/Icon/{k}"):
                        if i[-4:] == ".svg" or i[-4:] == ".png":
                            iconPathList.append(f"{programPath}/Icon/{k}/{i}")
                except:
                    traceback.print_exec()
        randomNumber = random.randint(0, len(iconPathList) - 1)
        iconShow.setText(f"<a href='https://www.gfdgdxi.top'><img width=256 src='{iconPathList[randomNumber]}'></a><p align='center'>{randomNumber + 1}/{len(iconPathList)}</p>")
    iconShow.linkActivated.connect(ChangeIcon)
    messageLayout.addWidget(iconShow, 0, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignTop)
    aboutInfo = QtWidgets.QTextBrowser(messageWidget)
    aboutInfo.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
    #aboutInfo.copyAvailable.connect(lambda: print("b"))
    aboutInfo.anchorClicked.connect(OpenUrl)
    aboutInfo.setOpenLinks(False)
    aboutInfo.setHtml(about)
    aboutInfo.setOpenExternalLinks(False)
    messageLayout.addWidget(aboutInfo, 0, 1, 1, 1)
    ok = QtWidgets.QPushButton(QtCore.QCoreApplication.translate("U", "确定"))
    ok.clicked.connect(QT.message.close)
    messageLayout.addWidget(ok, 1, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignBottom | QtCore.Qt.AlignmentFlag.AlignRight)
    messageWidget.setLayout(messageLayout)
    
    QT.message.setCentralWidget(messageWidget)
    QT.message.resize(int(messageWidget.frameGeometry().width() * 1.5), int(messageWidget.frameGeometry().height() * 1.5))
    QT.message.show()

class SaveLogReport():
    userName = getpass.getuser()
    time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    kernelVersion = subprocess.getoutput("uname -a")
    wineRunnerVersion = information["Version"]
    architecture = subprocess.getoutput("arch")
    cpuInfo = subprocess.getoutput("lscpu")
    lsmod = subprocess.getoutput("lsmod")
    lshw = subprocess.getoutput("lshw")
    cpu = subprocess.getoutput("cat /proc/cpuinfo | grep 'model name' | head -n 1 | awk -F: '{print $2}'")
    gpu = subprocess.getoutput("lspci | grep -i 'VGA\|3D\|2D'")

    def __init__(self, chooseWineName, chooseWineCommand, runCommand, binPath, logOut, description="无", imgPath=[]) -> None:
        self.chooseWineName = chooseWineName
        self.chooseWineCommand = chooseWineCommand
        self.runCommand = runCommand
        self.binPath = binPath
        self.logOut = logOut
        self.description = description
        self.imgPath = imgPath
        # 读取可执行文件信息
        if os.path.exists(binPath):
            try:
                self.binSize = f"{str(int(getFileFolderSize(binPath) / 1024 / 1024))}MB"
            except:
                self.binSize = "Error"
                traceback.print_exc()
            os.system(f"'{programPath}/wrestool' '{binPath}' -x -t 14 > '/tmp/wine-runner-log-icon.png'")
            # 如果提取成功
            if os.path.exists(TMPDIR + "/tmp/wine-runner-log-icon.png"):
                # 转换成 base64 编码
                self.binIcon = "data:image/jpg;base64," + FileToBase64(TMPDIR + "/tmp/wine-runner-log-icon.png")
                self.binIconPath = "/tmp/wine-runner-log-icon.png"
            else:
                self.binIcon = "Not Found"
                self.binIconPath = "Not Found"
        else:
            self.binSize = "Not Found"
            self.binIcon = "Not Found"
            self.binIconPath = "Not Found"
        try:
            self.memoryInfo = readtxt("/proc/meminfo")
        except:
            traceback.print_exc()
            self.memoryInfo = traceback.format_exc()
        # 读取系统信息
        try:
            with open("/etc/os-release", "r") as file:
                text = "[Default]\n" + file.read()
            conf = configparser.ConfigParser()
            conf.read_string(text)
            self.systemVersion = conf.get("Default", "PRETTY_NAME")
        except:
            traceback.print_exc()
            self.systemVersion = subprocess.getoutput("lsb_release -a")

    def SetWindow(self):
        def AddImageToListClicked():
            choose = QtWidgets.QFileDialog.getOpenFileNames(messagebox, "选择图像", get_home(), "图片文件(*.png *.jpg *.bmp *.gif *.svg);;所有文件(*.*)")
            print(choose)
            for i in choose[0]:
                if i in imageList:
                    continue
                imageList.append(i)
            nmodel = QtGui.QStandardItemModel(messagebox)
            for i in imageList:
                item = QtGui.QStandardItem(i)
                nmodel.appendRow(item)
            imageListView.setModel(nmodel)

        def DeleteImageToListClicked():
            index = imageListView.currentIndex().row()
            if index < 0:
                QtWidgets.QMessageBox.information(messagebox, "提示", "您未选择任何项")
                return
            del imageList[index]
            nmodel = QtGui.QStandardItemModel(messagebox)
            for i in imageList:
                item = QtGui.QStandardItem(i)
                nmodel.appendRow(item)
            imageListView.setModel(nmodel)
            # 选择第一项
            imageListView.setCurrentIndex(nmodel.index(0, 0))

        def OkClicked():
            self.description = description.toPlainText()
            self.imgPath = imageList
            path = QtWidgets.QFileDialog.getSaveFileName(messagebox, "保存日志报告", get_home(), "7z 文件(*.7z);;所有文件(*.*)")
            print(path)
            if path[0] != "":
                try:
                    self.To7z(path[0])
                except:
                    traceback.print_exc()
                    QtWidgets.QMessageBox.critical(messagebox, "错误", traceback.format_exc())
                    return
                messagebox.close()
                QtWidgets.QMessageBox.information(messagebox, "提示", "生成完成！\n建议将报告与可执行文件一并提交以便排除错误")

        def CancelClicked():
            messagebox.close()

        # 权重
        size = QtWidgets.QSizePolicy()
        size.setHorizontalPolicy(QtWidgets.QSizePolicy.Policy.Fixed)
        imageList = []
        messagebox = QtWidgets.QDialog()
        layout = QtWidgets.QGridLayout()
        description = QtWidgets.QTextEdit()
        imageListView = QtWidgets.QListView()
        addImageToList = QtWidgets.QPushButton("+")
        deleteImageToList = QtWidgets.QPushButton("-")
        controlLayout = QtWidgets.QHBoxLayout()
        ok = QtWidgets.QPushButton("保存")
        cancel = QtWidgets.QPushButton("取消")
        description.setPlaceholderText("可以填写故障的现象、复现步骤以及其他有关的信息，同时也可以填写联系方式")
        addImageToList.clicked.connect(AddImageToListClicked)
        deleteImageToList.clicked.connect(DeleteImageToListClicked)
        ok.clicked.connect(OkClicked)
        cancel.clicked.connect(CancelClicked)
        addImageToList.setSizePolicy(size)
        deleteImageToList.setSizePolicy(size)
        ok.setSizePolicy(size)
        cancel.setSizePolicy(size)
        layout.addWidget(QtWidgets.QLabel("<h2>描述（建议填写）</h2>"), 0, 0)
        layout.addWidget(description, 1, 0, 1, 3)
        layout.addWidget(QtWidgets.QLabel("<hr>"), 2, 0, 1, 4)
        layout.addWidget(QtWidgets.QLabel("<h2>截图（建议选择）</h2>"), 3, 0)
        layout.addWidget(imageListView, 4, 0, 4, 3)
        layout.addWidget(addImageToList, 5, 3)
        layout.addWidget(deleteImageToList, 6, 3)
        layout.addLayout(controlLayout, 8, 2, 1, 2)
        controlLayout.addWidget(cancel)
        controlLayout.addWidget(ok)
        messagebox.setLayout(layout)
        messagebox.exec()

    def To7z(self, savePath):
        os.system("rm -rfv $TMPDIR/tmp/wine-runner-log")
        os.system("mkdir -v $TMPDIR/tmp/wine-runner-log")
        self.ToHtml(TMPDIR + "/tmp/wine-runner-log/index.html", toZip=True)
        if os.path.exists(self.binIconPath):
            shutil.copy(self.binIconPath, f"/tmp/wine-runner-log/{os.path.basename(self.binIconPath)}")
        lists = ["wine-runner-log-icon.png", "index.html"]
        for i in self.imgPath:
            name = os.path.basename(i)
            if os.path.basename(i) in lists:
                while name in lists:
                    name = os.path.splitext(name)[0] + "-copy" + os.path.splitext(name)[1]
                lists.append(name)
            else:
                lists.append(name)
            shutil.copy(i, f"/tmp/wine-runner-log/{name}")
        os.system(f"7z a '{savePath}' $TMPDIR/tmp/wine-runner-log")


    def ToHtml(self, savePath, toZip=False):
        print(self.userName, self.time)
        # 对文本进行处理
        description = ""
        logOut = ""
        cpuInfo = ""
        memoryInfo = ""
        imgPath = ""
        lsmod = ""
        lshw = ""
        charReplaceMap = {
            "<": "&lt;",
            ">": "&gt;",
            "&": "&amp;",
            '"': "&quot;"
        }
        for i in self.description.splitlines():
            for k in charReplaceMap:
                i = i.replace(k, charReplaceMap[k])
            description += f'<span class="line code">{i}</span>\n'
        for i in self.logOut.splitlines():
            for k in charReplaceMap:
                i = i.replace(k, charReplaceMap[k])
            logOut += f'<span class="line code">{i}</span>\n'
        for i in self.cpuInfo.splitlines():
            for k in charReplaceMap:
                i = i.replace(k, charReplaceMap[k])
            cpuInfo += f'<span class="line code">{i}</span>\n'
        for i in self.memoryInfo.splitlines():
            for k in charReplaceMap:
                i = i.replace(k, charReplaceMap[k])
            memoryInfo += f'<span class="line code">{i}</span>\n'
        for i in self.lsmod.splitlines():
            for k in charReplaceMap:
                i = i.replace(k, charReplaceMap[k])
            lsmod += f'<span class="line code">{i}</span>\n'
        for i in self.lshw.splitlines():
            for k in charReplaceMap:
                i = i.replace(k, charReplaceMap[k])
            lshw += f'<span class="line code">{i}</span>\n'
        text = readtxt(f"{programPath}/Resources/LogTemplate/template.html")
        if toZip:
            binIcon = os.path.basename(self.binIconPath)
            # 重名排除
            lists = ["wine-runner-log-icon.png", "index.html"]
            for i in self.imgPath:
                name = os.path.basename(i)
                if os.path.basename(i) in lists:
                    while name in lists:
                        name = os.path.splitext(name)[0] + "-copy" + os.path.splitext(name)[1]
                    lists.append(name)
                else:
                    lists.append(name)
                imgPath += f'<p align="center"><img src="{name}" class="imgShow"></p>\n'
        else:
            binIcon = self.binIcon
            for i in self.imgPath:
                try:
                    path = "data:image/jpg;base64," + FileToBase64(i)
                except:
                    traceback.print_exc()
                    path = "Error"
                imgPath += f'   <p align="center"><img src="{path}" class="imgShow"></p>\n'

        replaceMap = {
            "%UserName%": self.userName,
            "%Time%": self.time,
            "%KernelVersion": self.kernelVersion,
            "%ChooseWineName%": self.chooseWineName,
            "%ChooseWineCommand%": self.chooseWineCommand,
            "%RunCommand%": self.runCommand,
            "%BinPath%": self.binPath,
            "%WineRunnerVersion%": self.wineRunnerVersion,
            "%BinSize%": self.binSize,
            "%BinIcon%": binIcon,
            "%CPUInfo%": cpuInfo,
            "%Architecture%": self.architecture,
            "%MemoryInfo%": memoryInfo,
            "%LogOut%": logOut,
            "%Description%": description,
            "%ImgPath%": imgPath,
            "%Lsmod%": lsmod,
            "%Lshw%": lshw,
            "%CPU%": self.cpu,
            "%GPU%": self.gpu,
            "%SystemVersion%": self.systemVersion
        }
        for i in replaceMap.keys():
            text = text.replace(i, replaceMap[i])
        with open(savePath, "w") as file:
            file.write(text)

