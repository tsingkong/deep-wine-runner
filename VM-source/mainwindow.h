/*
 * gfdgd xi
 * 依照 GPLV3 开源
 */
#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void ShowCPUMessage();
    void on_browser_clicked();
    QString GetRunCommand(QString command);
    void on_install_clicked();


    void on_getvbox_clicked();

    void on_getQemu_clicked();

    void on_vmChooser_currentIndexChanged(int index);

    void on_qemuSetting_clicked();

    void on_addQemuDisk_triggered();

    void on_delQemuDisk_triggered();

    void on_addQemuDiskButton_clicked();

    void on_saveQemuDiskButton_clicked();

    void on_delQemuDiskButton_clicked();

    void on_kvmTest_clicked();

    void on_actionVMLog_triggered();

    void on_actionVMRunlLog_triggered();

    void on_actionVMTest_triggered();

    void on_actionVMInstallLog_triggered();

    void on_action_StopVirtualBox_triggered();

    void on_action_StopQemu_triggered();

    void on_actionQemuDiskAddSpace_triggered();

    void on_getDCLC_triggered();

private:
    bool stopShowTime = 0;
    Ui::MainWindow *ui;
    long m_cpuAll;
    long m_cpuFree;
};

#endif // MAINWINDOW_H
