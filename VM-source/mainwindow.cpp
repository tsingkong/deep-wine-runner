/*
 * gfdgd xi
 * 依照 GPLV3 开源
 */
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "buildvbox.h"
#include <QFileDialog>
#include <QDebug>
#include <QNetworkInterface>
#include <QProcess>
#include <QLoggingCategory>
#include <infoutils.h>
#include <QMessageBox>
#include <QTimer>
#include <QJsonParseError>
#include <QJsonValue>
#include <QJsonObject>
#include <QtMath>
#include <QJsonArray>
#include <QDesktopServices>
#include <QMessageBox>
#include <iostream>
#include <QIODevice>
#include <QInputDialog>
#include "qemusetting.h"
#include "vbox.h"
#include "qemu.h"

#include <QInputDialog>

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    //QApplication a(argc, argv);
    ui->tabWidget->setTabPosition(QTabWidget::West);  // 标签靠左
    // 选择最优虚拟机
    if(!system("which qemu-system-x86_64")){
        ui->vmChooser->setCurrentIndex(0);
    }
    if(!system("which vboxmanage")){
        ui->vmChooser->setCurrentIndex(1);
    }
    if(!QFile::exists(QCoreApplication::applicationDirPath() + "/../RunCommandWithTerminal.py")){
        ui->getQemu->setDisabled(true);
    }
    // 允许输出 qDebug 信息
    QLoggingCategory::defaultCategory()->setEnabled(QtDebugMsg, true);
    // 判断是否安装 vbox（无需判断）
    /*if(system("which VBoxManage")){
        if(QMessageBox::question(this, tr("提示"), "检测到您似乎没有安装 VirtualBox，立即安装？") == QMessageBox::Yes){
            system("xdg-open https://www.virtualbox.org/wiki/Linux_Downloads");
        }
    }*/
    // QTimer
    QTimer *cpuGet = new QTimer(this);
    connect(cpuGet, &QTimer::timeout, this, &MainWindow::ShowCPUMessage);
    cpuGet->setInterval(1000);
    cpuGet->start();
    MainWindow::ShowCPUMessage();
    // 读取程序版本号
    // / 版本号文件是否存在
    QFile fileinfo(QCoreApplication::applicationDirPath() + "/../information.json");
    if(!fileinfo.exists()){
        fileinfo.close();
        return;
    }
    fileinfo.open(QIODevice::ReadOnly);
    QJsonParseError error;
    QJsonDocument doc = QJsonDocument::fromJson(fileinfo.readAll(), &error);
    if(error.error != QJsonParseError::NoError){
        QMessageBox::critical(this, "错误", "无法读取版本号！");
        qDebug() << error.errorString();
        fileinfo.close();
        return;
    }
    QJsonObject versionObject = doc.object();
    QJsonValue buildTime = versionObject.value("Time");
    QJsonValue versionValue = versionObject.value("Version");
    QJsonArray thank = versionObject.value("Thank").toArray();
    QString thankText = "";
    for (int i = 0; thank.count() > i; i++) {
        thankText += "<p>" + thank.at(i).toString() + "</p>\n";
        qDebug() << thank.at(i).toString();

    }
    // 设置程序标题
    this->setWindowTitle(tr("Wine 运行器虚拟机安装工具 ") + versionValue.toString());
    // 读取谢明列表
    ui->textBrowser_2->setHtml(tr("<p>程序版本号：") + versionValue.toString() + ", " + GetRunCommand("arch") + tr("</p><p>安装包构建时间：") + buildTime.toString() + tr("</p><p>该组件构建时间：")
                               + __DATE__ + " " + __TIME__ + "</p>" + ui->textBrowser_2->toHtml() +
                               tr("<hr/><h1>谢明列表</h1>") + thankText);
    connect(ui->textBrowser_2, &QTextBrowser::anchorClicked, this, [=](const QUrl &link){
        QDesktopServices::openUrl(link);
    });
    connect(ui->textBrowser, &QTextBrowser::anchorClicked, this, [=](const QUrl &link){
        QDesktopServices::openUrl(link);
    });
    connect(ui->textBrowser_3, &QTextBrowser::anchorClicked, this, [=](const QUrl &link){
        QDesktopServices::openUrl(link);
    });
    // 设置标签栏图标
    ui->tabWidget->setTabIcon(1, QIcon::fromTheme(":/application-vnd.oasis.opendocument.text.svg"));
    // 设置窗口图标
    this->setWindowIcon(QIcon(":/deepin-wine-runner.svg"));

}

void MainWindow::ShowCPUMessage(){
    // 获取 CPU 占用率
    long cpuAll = 0;
    long cpuFree = 0;
    infoUtils::cpuRate(cpuAll, cpuFree);
    long cpu = ((cpuAll - m_cpuAll) - (cpuFree - m_cpuFree)) * 100 / (cpuAll - m_cpuAll);
    if(cpu > 100){
        // 处理异常值
        cpu = 100;
    }
    // 获取内存占用率
    long memory = 0;
    long memoryAll = 0;
    long swap = 0;
    long swapAll = 0;

    infoUtils::memoryRate(memory, memoryAll, swap, swapAll);

    // 获取开机时间
    double run,idle;
    infoUtils::uptime(run,idle);
    int time = qFloor(run);
    int ss = time % 60;
    int MM = (time % 3600) / 60;
    int hh = (time % 86400) / 3600;
    int dd = time / 86400;


    QString info = "CPU: " + QString::number(cpu) + "%  内存: " +
            QString::number(memory * 100 / memoryAll) + "% " + QString::number(memory / 1024) + "MB/" + QString::number(memoryAll / 1024) + "MB" +
            " 开机时间: " + QString::number(dd) + "天 " + QString::number(hh) + ":" + QString::number(MM) + ":" + QString::number(ss);
    //qDebug() << cpuAll << "  " << cpuFree;
    if(!stopShowTime){
        ui->CPUValue->showMessage(info, 5000);
    }
    m_cpuAll = cpuAll;
    m_cpuFree = cpuFree;
    //ui->retranslateUi(this);
}

QString MainWindow::GetRunCommand(QString command){
    QProcess process;
    process.start(command);
    process.waitForStarted();
    process.waitForFinished();
    QString re = process.readAllStandardOutput();
    process.close();
    return re;
}


MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_browser_clicked()
{
    // 浏览镜像文件
    QString filePath = QFileDialog::getOpenFileName(this, "选择 ISO 文件", QDir::homePath(), "ISO 镜像文件(*.iso);;所有文件(*.*)");
    if(filePath != ""){
        ui->isoPath->setText(filePath);
    }
}

void MainWindow::on_install_clicked()
{
    switch (ui->vmChooser->currentIndex()) {
    case 0:
        if(system("which qemu-system-x86_64")){
            if(QMessageBox::question(this, tr("提示"), tr("您似乎没有安装 Qemu，是否继续创建虚拟机？")) == QMessageBox::No){
                return;
            }
        }
        break;
    case 1:
        if(system("which vboxmanage")){
            if(QMessageBox::question(this, tr("提示"), tr("您似乎没有安装 VBox，是否继续创建虚拟机？")) == QMessageBox::No){
                return;
            }
        }
        break;
     case 8:
        if(system("which qemu-system-arm")){
            if(QMessageBox::question(this, tr("提示"), tr("无法检测到 qemu-system-arm，是否继续创建虚拟机？")) == QMessageBox::No){
                return;
            }
        }
        break;
     case 9:
       if(system("which qemu-system-aarch64")){
           if(QMessageBox::question(this, tr("提示"), tr("无法检测到 qemu-system-aarch64，是否继续创建虚拟机？")) == QMessageBox::No){
               return;
           }
       }
       break;
    }
    QFile file(QDir::homePath() + "/.config/deepin-wine-runner/QEMU-EFI");
    QFile archFile(QDir::homePath() + "/.config/deepin-wine-runner/QEMU-ARCH");
    QDir dir(QDir::homePath() + "/.config/deepin-wine-runner");
    archFile.open(QIODevice::WriteOnly);
    archFile.write("amd64");
    archFile.close();
    switch (ui->systemVersion->currentIndex()) {
        case 0:
            if(!QFile::exists(QCoreApplication::applicationDirPath() + "/Windows7X86Auto.iso")){
                if(QMessageBox::question(this, tr("提示"), tr("似乎无法找到 Windows7X86Auto.iso，是否继续创建虚拟机？\n缺少该文件可能会导致虚拟机无法正常启动，尝试重新安装 Wine 运行器再试试？")) == QMessageBox::No){
                    return;
                }
            }
            break;
        case 1:
            if(!QFile::exists(QCoreApplication::applicationDirPath() + "/Windows7X64Auto.iso")){
                if(QMessageBox::question(this, tr("提示"), tr("似乎无法找到 Windows7X64Auto.iso，是否继续创建虚拟机？\n缺少该文件可能会导致虚拟机无法正常启动，尝试重新安装 Wine 运行器再试试？")) == QMessageBox::No){
                    return;
                }
            }
            break;
        case 3:
            if(!QFile::exists("/usr/share/qemu/OVMF.fd") && !QFile::exists(QCoreApplication::applicationDirPath() + "/OVMF.fd") && ui->vmChooser->currentIndex() == 0){
                if(QMessageBox::question(this, tr("提示"), tr("似乎无法找到 UEFI 固件，是否继续创建虚拟机？\nQemu 固件可以在“安装 Qemu”处安装")) == QMessageBox::No){
                    return;
                }
            }
            if(!dir.exists()){
                dir.mkpath(QDir::homePath() + "/.config/deepin-wine-runner");
            }
            if(!QFile::exists(QDir::homePath() + "/.config/deepin-wine-runner/QEMU-EFI")){
                // 写入用于识别的空文件
                file.open(QIODevice::WriteOnly);
                file.write("1");
                file.close();
            }
            break;
        case 4:
        case 5:
        case 6:
        case 7:
            if(ui->vmChooser->currentIndex() == 0){
                QMessageBox::warning(this, tr("提示"), tr("Qemu 不支持该选项！"));
                return;
            }
            break;
        case 8:
            if(ui->vmChooser->currentIndex() == 1){
                QMessageBox::warning(this, tr("提示"), tr("VirtualBox 不支持该选项！"));
                return;
            }
            archFile.open(QIODevice::WriteOnly);
            archFile.write("armhf");
            archFile.close();
            break;
        case 9:
            if(ui->vmChooser->currentIndex() == 1){
                QMessageBox::warning(this, tr("提示"), tr("VirtualBox 不支持该选项！"));
                return;
            }
            archFile.open(QIODevice::WriteOnly);
            archFile.write("aarch64");
            archFile.close();
            break;
        default:
            if(ui->vmChooser->currentIndex() == 0 && QFile::exists(QDir::homePath() + "/.config/deepin-wine-runner/QEMU-EFI")){
                QFile::remove(QDir::homePath() + "/.config/deepin-wine-runner/QEMU-EFI");
            }
    }
    buildvbox(ui->isoPath->text(), ui->systemVersion->currentIndex(), ui->vmChooser->currentIndex());
    ui->tabWidget->setCurrentIndex(1);
    stopShowTime = 1;
    ui->CPUValue->showMessage(tr("提示：目前已经尝试开启虚拟机，如果在一段时间后依旧还没看到虚拟机窗口开启，请在菜单栏查看虚拟机日志"), 10000);
    return;
}

void MainWindow::on_getvbox_clicked()
{
    QDesktopServices::openUrl(QUrl("https://www.virtualbox.org/wiki/Linux_Downloads"));
}

void MainWindow::on_getQemu_clicked()
{
    system(("python3 '" + QCoreApplication::applicationDirPath() + "/../RunCommandWithTerminal.py' pkexec '" + QCoreApplication::applicationDirPath() + "/../QemuSystemInstall.sh'").toLatin1());
}

void MainWindow::on_vmChooser_currentIndexChanged(int index)
{
    ui->qemuSetting->setDisabled(index);
}

void MainWindow::on_qemuSetting_clicked()
{
    QemuSetting *show = new QemuSetting();
    show->show();

}

void MainWindow::on_addQemuDisk_triggered()
{
    if(QFile::exists(QDir::homePath() + "/Qemu/Windows/Windows.qcow2")){
        if(QMessageBox::question(this, tr("提示"), tr("磁盘文件已存在，是否覆盖？\n覆盖后将无法恢复！")) == QMessageBox::No){
            return;
        }
    }
    QString path = QFileDialog::getOpenFileName(this, tr("选择 Qemu 镜像"), QDir::homePath(), tr("Qemu镜像(*.qcow2 *.img *.raw *.qcow *.qed *.vdi *.vhdx *.vmdk);;所有文件(*.*)"));
    qDebug() << path;
    if(path == ""){
        return;
    }
    QDir dir(QDir::homePath() + "/Qemu/Windows");
    if(!dir.exists()){
        dir.mkpath(QDir::homePath() + "/Qemu/Windows");
    }
    if(QFile::exists(QDir::homePath() + "/Qemu/Windows/Windows.qcow2")){
        if(!QFile::remove(QDir::homePath() + "/Qemu/Windows/Windows.qcow2") | !QFile::copy(path, QDir::homePath() + "/Qemu/Windows/Windows.qcow2")){
            QMessageBox::critical(this, tr("提示"), tr("添加错误！"));
            return;
        }
    }
    else{
        if(!QFile::copy(path, QDir::homePath() + "/Qemu/Windows/Windows.qcow2")){
            QMessageBox::critical(this, tr("提示"), tr("添加错误！"));
            return;
        }
    }
    QMessageBox::information(this, tr("提示"), tr("添加完成！"));
}

void MainWindow::on_delQemuDisk_triggered()
{
    if(!QFile::exists(QDir::homePath() + "/Qemu/Windows/Windows.qcow2")){
        QMessageBox::information(this, tr("提示"), tr("不存在磁盘文件，无法导出"));
        return;
    }
    std::system(("xdg-open \"" + QDir::homePath() + "/Qemu/Windows/\"").toUtf8());
}

void MainWindow::on_addQemuDiskButton_clicked()
{
    MainWindow::on_addQemuDisk_triggered();
}

void MainWindow::on_saveQemuDiskButton_clicked()
{
    MainWindow::on_delQemuDisk_triggered();
}

void MainWindow::on_delQemuDiskButton_clicked()
{
    if(!QFile::exists(QDir::homePath() + "/Qemu/Windows/Windows.qcow2")){
        QMessageBox::information(this, tr("提示"), tr("不存在磁盘文件，无法移除"));
        return;
    }
    if(QMessageBox::question(this, tr("提示"), tr("是否删除？\n删除后将无法恢复！")) == QMessageBox::No){
        return;
    }
    if(!QFile::remove(QDir::homePath() + "/Qemu/Windows/Windows.qcow2")){
        QMessageBox::critical(this, tr("提示"), tr("移除失败"));
        return;
    }
    QMessageBox::information(this, tr("提示"), tr("移除成功"));
}

void MainWindow::on_kvmTest_clicked()
{
    if(system("which kvm-ok")&& !QFile::exists(QCoreApplication::applicationDirPath() + "/kvm-ok")){
        QMessageBox::critical(this, tr("错误"), tr("未识别到命令 kvm-ok\n可以使用命令 sudo apt install cpu-checker 安装"));
        return;
    }
    QString kvm_ok_path = "kvm-ok";
    if(!system("which kvm-ok")){
        kvm_ok_path = "kvm-ok";
    }
    else if(QFile::exists(QCoreApplication::applicationDirPath() + "/kvm-ok")){
        kvm_ok_path = QCoreApplication::applicationDirPath() + "/kvm-ok";
    }
    qDebug() << tr("使用") << kvm_ok_path;
    QProcess process;
    process.start(kvm_ok_path);
    process.waitForStarted();
    process.waitForFinished();
    if(process.exitCode()){
        QMessageBox::critical(this, tr("错误"), tr("您的系统不支持使用 kvm：\n") + process.readAll());
        return;
    }
    QMessageBox::information(this, tr("提示"), tr("您的系统支持使用 kvm：\n") + process.readAll());

}


void MainWindow::on_actionVMLog_triggered(){}


void MainWindow::on_actionVMRunlLog_triggered()
{
    QFile file("/tmp/windows-virtual-machine-installer-for-wine-runner-run.log");
    if(!file.exists()){
        QMessageBox::information(this, tr("提示"), tr("没有日志文件"));
        return;
    }
    file.open(QIODevice::ReadOnly);
    QInputDialog::getMultiLineText(this, tr("运行日志"), tr("虚拟机运行日志"), file.readAll());
    file.close();
}


void MainWindow::on_actionVMTest_triggered()
{
    // 运行 Demo
    if(QFile::exists(QCoreApplication::applicationDirPath() + "/test.qcow2")){
        // 优先使用本地的磁盘
        system(("qemu-system-i386 --hda '" + QCoreApplication::applicationDirPath() + "/test.qcow2' -rtc base=localtime > /tmp/windows-virtual-machine-installer-for-wine-runner-run.log 2>&1").toUtf8());
        return;
    }
    // 写入 disk 文件
    QFile file(":/TestDisk/test.qcow2");
    // 计算随机数
    QFile writeFile("/tmp/indows-virtual-machine-installer-for-wine-runner-test-disk.qcow2");
    file.open(QIODevice::ReadOnly);
    writeFile.open(QIODevice::WriteOnly);
    writeFile.write(file.readAll());
    file.close();
    writeFile.close();
    system("qemu-system-i386 --hda /tmp/indows-virtual-machine-installer-for-wine-runner-test-disk.qcow2 -rtc base=localtime > /tmp/windows-virtual-machine-installer-for-wine-runner-run.log 2>&1");
}


void MainWindow::on_actionVMInstallLog_triggered()
{
    QFile file("/tmp/windows-virtual-machine-installer-for-wine-runner-install.log");
    if(!file.exists()){
        QMessageBox::information(this, tr("提示"), tr("没有日志文件"));
        return;
    }
    file.open(QIODevice::ReadOnly);
    QInputDialog::getMultiLineText(this, tr("安装日志"), tr("虚拟机安装日志"),file.readAll());
    file.close();
}


void MainWindow::on_action_StopVirtualBox_triggered()
{
    vbox vmControl("");
    vmControl.Stop();
}


void MainWindow::on_action_StopQemu_triggered()
{
    qemu vmControl("");
    vmControl.Stop();
}


void MainWindow::on_actionQemuDiskAddSpace_triggered()
{
    double data = QInputDialog::getDouble(this, tr("磁盘扩容"), "输入扩容多少GB\n注：1、扩容所需要的时间较长，程序可能会出现假死的情况，请不要关闭否则会导致虚拟磁盘损坏\n2、扩展后需要自行在虚拟机使用 Deepin Community Live CD、Live CD、Windows PE\n等工具调整系统分区大小才能使用");
    if(data <= 0) {
        return;
    }
    // 开始扩容
    int result = qemu("").AddDiskSpace(QDir::homePath() + "/Qemu/Windows/Windows.qcow2", data);
    qDebug() << "Exit Code: " << result;
    if(result) {
        QMessageBox::critical(this, tr("错误"), tr("扩容失败！"));
        return;
    }
    QMessageBox::information(this, tr("提示"), tr("扩容完成！"));
}


void MainWindow::on_getDCLC_triggered()
{
    QDesktopServices::openUrl(QUrl("https://github.com/gfdgd-xi/deepin-community-live-cd/"));
}

