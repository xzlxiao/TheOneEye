#include "ViewController.h"
#include "DebugPrint.h"
#include "TestCameraWin.h"
#include "XSetting.h"
#include <QMovie>
#include <QResizeEvent>
#include "Common.h"
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

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
    mTestMovieShow = test_camera_win->mCameraShow;
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

cv::Rect ViewController::getShowRect(const cv::Mat &src_image, const int &width_crop, const int &height_crop)
{
    double gui_wh_ratio, img_wh_ratio;
    cv::Rect ret;
    gui_wh_ratio = (double)width_crop / (double)height_crop;
    img_wh_ratio = (double)src_image.size().width / (double)src_image.size().height;
    if (gui_wh_ratio > img_wh_ratio)
    {
        ret.width = src_image.size().width;
        ret.height = (double)(((double)ret.width / (double)width_crop) * (double)height_crop);
        ret.x = 0;
        ret.y = (int)floor(((double)src_image.size().height - (double)ret.height) / 2.0);
    }
    else
    {
        ret.height = src_image.size().height;
        ret.width = (int)(((double)ret.height / (double)height_crop) * (double)width_crop);

        ret.x = (int)floor(((double)src_image.size().width - (double)ret.width) / 2.0);
        ret.y = 0;
    }
    return ret;
}

void ViewController::resizeImage(cv::Mat &image_, const int &width_crop, const int &height_crop)
{
    image_ = image_(getShowRect(image_, width_crop,height_crop));
    cv::resize(image_,image_, cv::Size(width_crop, height_crop));
}

void ViewController::displayImageInQLabel(const cv::Mat &image, XLabel *label)
{
    cv::Mat image_tmp;
    QImage q_rgb;
    if (!image.empty())
    {
        image.copyTo(image_tmp);
        resizeImage(image_tmp, label->width(), label->height());
        Common::Mat2QImage(image_tmp, label->mImage);
    }
    else
    {
        //const_cast<QLabel &>(label).clear();
    }
}
