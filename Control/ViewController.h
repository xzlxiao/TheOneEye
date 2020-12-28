#ifndef VIEWCONTROLLER_H
#define VIEWCONTROLLER_H

#include <QObject>
#include "MainWindow.h"
#include "WinBase.h"
#include <QFrame>
#include <QGridLayout>

class ViewController : public QObject
{
    Q_OBJECT
public:
    explicit ViewController(QObject *parent = nullptr);

public:     // 窗口
    MainWindow *mMainWin;
    QFrame *mMainFrame;
    QWidget *mCurrentWin;
    QGridLayout *mCurrentLayout;
    std::vector<WinBase * > mFrameList;

public:     // 方法
    void start();
    void windowSwitch(QWidget *win);

public slots:
    void changeWinSlot(uint num);
    void changeWinSlot(QString win_name);
signals:

};

#endif // VIEWCONTROLLER_H
