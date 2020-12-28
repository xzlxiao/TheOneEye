#include "ViewController.h"
#include "DebugPrint.h"
#include <QMovie>

ViewController::ViewController(QObject *parent) : QObject(parent),
    mMainWin(new MainWindow),
    mMainFrame(nullptr),
    mCurrentWin(nullptr),
    mCurrentLayout(nullptr)
{
    MyDebug;
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
/// \brief 界面切换信号槽
/// \param num  切换界面的数字
///
void ViewController::changeWinSlot(uint num)
{
    if (num < this->mFrameList.size())
    {
        ViewController::windowSwitch(mFrameList.at(num));
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
            ViewController::windowSwitch((*iter));
            isFind = true;
        }
    }
    if (!isFind)
    {
        throw "Fail to switch window. The name of win isn't exited, please checking.";
    }
}
