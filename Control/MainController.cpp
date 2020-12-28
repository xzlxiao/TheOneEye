#include "MainController.h"

MainController::MainController(QObject *parent) : QObject(parent),
    mMainLoopTimer(this)
{
    initConnect();
}

///
/// \brief 控制器启动入口
///
void MainController::start()
{
    MyDebug;
    mViewController.start();
    mMainLoopTimer.start(50);
}



void MainController::initConnect()
{
    connect(&mMainLoopTimer, SIGNAL(timeout()), this, SLOT(mainLoop()));
}

///
/// \brief 主循环信号槽
///
void MainController::mainLoop()
{

}
