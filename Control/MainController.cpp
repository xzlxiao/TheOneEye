#include "MainController.h"

MainController::MainController(QObject *parent) : QObject(parent),
    mMainWin(new MainWindow),
    mMainFrame(nullptr),
    mCurrentWin(nullptr),
    mCurrentLayout(nullptr),
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
    mMainWin->show();
    mMainLoopTimer.start(50);
}

///
/// \brief 窗口切换器
/// \param win
///
void MainController::windowSwitch(QWidget *win)
{
    if (mCurrentWin != nullptr)
    {
        delete mCurrentLayout;
    }
    if (mCurrentWin != nullptr)
    {
        mCurrentWin->hide();
    }
    mCurrentLayout = new QGridLayout();
    mCurrentLayout->addWidget(win);
    mMainFrame->setLayout(mCurrentLayout);
    mCurrentWin = win;
    mCurrentWin->show();
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
