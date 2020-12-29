#include "ViewController.h"
#include "DebugPrint.h"
#include "TestCameraWin.h"
#include "XSetting.h"
#include <QMovie>
#include <QResizeEvent>

ViewController::ViewController(QObject *parent) : QObject(parent),
    mMainWin(new MainWindow),
    mMainFrame(new QFrame(mMainWin)),
    mCurrentWin(nullptr),
    mCurrentLayout(nullptr)
{
    MyDebug;
    windowLoad();

}

void ViewController::windowLoad()
{
    mMainFrame->setGeometry(0, 0, mMainWin->mCentralWidget->height(), mMainWin->mCentralWidget->width());
    if (XSetting::isShowBorder)
        mMainFrame->setStyleSheet("border:2px solid rgba(255, 0, 0, 1);");
    mMainFrame->show();
    eventFilterInstall();
    TestCameraWin *test_camera_win = new TestCameraWin(mMainFrame);
    mFrameList.push_back(test_camera_win);
}

void ViewController::eventFilterInstall()
{
    mMainWin->installEventFilter(this);
}

void ViewController::start()
{
    MyDebug;
    mMainWin->show();
    QMovie *movie = new QMovie(":/images/background001.gif");
    for (auto iter = mMainWin->mlbBackgroundList.begin(); iter != mMainWin->mlbBackgroundList.end(); ++iter)
    {
        (*iter)->setMovie(movie);
        (*iter)->setScaledContents(true);
    }
    movie->start();
}

///
/// \brief ViewController::navigateTo
/// \param win_name
///
void ViewController::navigateTo(QString win_name)
{
    bool isFind = false;
    for (auto iter = mFrameList.begin(); iter != mFrameList.end(); ++iter)
    {
        if (win_name.trimmed()==(*iter)->name)
        {
            windowSwitch((*iter));
            isFind = true;
        }
    }
    if (!isFind)
    {
        throw "Fail to switch window. The name of win isn't exited, please checking.";
    }
}


///
/// \brief 窗口切换器
/// \param win
///
void ViewController::windowSwitch(QWidget *win)
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

///
/// \brief ViewController::eventFilter 事件过滤器
/// \abstract 进入事件过滤器的组件需要使用installEventFilter接口加载
/// \param watched
/// \param event
/// \return
///
bool ViewController::eventFilter(QObject *watched, QEvent *event)
{
    if (watched==mMainWin)
    {
        if (event->type()==QResizeEvent::Resize)
        {
            mMainFrame->resize(mMainWin->mCentralWidget->width(), mMainWin->mCentralWidget->height());
        }
    }
}

///
/// \brief 界面切换信号槽
/// \param num  切换界面的数字
///
void ViewController::changeWinSlot(uint num)
{
    if (num < this->mFrameList.size())
    {
        windowSwitch(mFrameList.at(num));
    }
    else
    {
        throw "Fail to switch window. The No. of win isn't exited, please checking.";
    }
}

void ViewController::changeWinSlot(QString win_name)
{
    bool isFind = false;
    for (auto iter = mFrameList.begin(); iter != mFrameList.end(); ++iter)
    {
        if (win_name.trimmed()==(*iter)->name)
        {
            windowSwitch((*iter));
            isFind = true;
        }
    }
    if (!isFind)
    {
        throw "Fail to switch window. The name of win isn't exited, please checking.";
    }
}
