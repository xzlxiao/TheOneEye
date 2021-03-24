#include "MainController.h"
#include <QImage>
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

MainController::MainController(QObject *parent) : QObject(parent),
    mMainLoopTimer(this)
{
    MyDebug;
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

    mViewController.navigateTo("TestCameraWin");
    mCameraController.startCamera(0, X_USB_CAM);
}



void MainController::initConnect()
{
    MyDebug;
    connect(&mMainLoopTimer, SIGNAL(timeout()), this, SLOT(mainLoop()));
}

///
/// \brief 主循环信号槽
///
void MainController::mainLoop()
{
    MyDebug;
    Mat cam_frame;
    mCameraController.gotFrame(0, cam_frame);
    mViewController.displayImageInQLabel(cam_frame, mViewController.mTestMovieShow);
    mViewController.mTestMovieShow->update();
}
