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
#include "CameraController.h"
#include "ViewController.h"

class MainController : public QObject
{
    Q_OBJECT

public:
    MainController(QObject *parent = nullptr);

private:    // 组件
    QTimer mMainLoopTimer;

    CameraController mCameraController;
    ViewController mViewController;

public:     // 方法
    void start();
    void initConnect();

public slots:
    void mainLoop();
};

#endif // MAINCONTROLLER_H
