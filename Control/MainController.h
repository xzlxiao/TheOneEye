#ifndef MAINCONTROLLER_H
#define MAINCONTROLLER_H

#include <QObject>
#include <QWidget>
#include <QFrame>
#include <QTimer>
#include <QGridLayout>
#include <vector>
#include "MainWindow.h"
#include "DebugPrint.h"

class MainController : public QObject
{
    Q_OBJECT

public:
    MainController(QObject *parent = nullptr);

public:     // 窗口
    MainWindow *mMainWin;
    QFrame *mMainFrame;
    QWidget *mCurrentWin;
    QGridLayout *mCurrentLayout;
    std::vector<QWidget * > mFrameList;

private:    // 组件
    QTimer mMainLoopTimer;

public:     // 方法
    void start();
    void windowSwitch(QWidget *win);
    void initConnect();

public slots:
    void mainLoop();
};

#endif // MAINCONTROLLER_H
