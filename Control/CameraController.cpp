#include "CameraController.h"
#include "CameraInterface.h"
#include "Common.h"
using namespace std;
CameraController::CameraController(QObject *parent) : QObject(parent)
{
    MyDebug;
    qRegisterMetaType<cv::Mat *>("cv::Mat *");
    // qRegisterMetaType<cv::Mat &>("cv::Mat &");
    qRegisterMetaType<cv::Mat>("cv::Mat");
}

void CameraController::startCamera(int cam_id, XCameraType camera_type)
{
    MyDebug;
    QThread *thread1 = new QThread();
    if (camera_type == X_USB_CAM)
    {
        CameraInterface *camera = new CameraInterface();
        CameraSwitcher *camera_switcher = new CameraSwitcher();
        camera->setCameraID(cam_id);
        connect(camera_switcher, SIGNAL(signalStopCamera()), camera, SLOT(slotCloseCamera()));
        connect(camera_switcher, SIGNAL(signalOpenCamera()), camera, SLOT(slotOpenCamera()));
        connect(camera, SIGNAL(gotCvFrameSignal(cv::Mat)), camera_switcher, SLOT(slotGotCvFrame(cv::Mat)));
        // connect(camera_switcher, &QThread::finished, camera, &QObject::deleteLater);
        camera->moveToThread(thread1);
        this->mCameraList.insert(pair<int, QThread * >(cam_id, thread1));
        this->mCameraSwitherList.insert( pair<int, CameraSwitcher *>(cam_id, camera_switcher));
        thread1->start();
        camera_switcher->openCamera();
    }
    else
    {

    }

}

void CameraController::releaseCamera(int cam_id)
{
    MyDebug;
    mCameraSwitherList[cam_id]->releaseCamera();
    mCameraSwitherList.erase(cam_id);
    mCameraList.at(cam_id)->quit();
    mCameraList.at(cam_id)->wait();
    mCameraList.erase(cam_id);
}

void CameraController::gotFrame(int cam_id, cv::Mat &image)
{
    MyDebug;
    image = mCameraSwitherList[cam_id]->mCvImage;
}

CameraSwitcher::CameraSwitcher(QObject *parent) : QObject(parent)
{
    MyDebug;
}

void CameraSwitcher::releaseCamera()
{
    MyDebug;
    emit this->signalStopCamera();
}

void CameraSwitcher::openCamera()
{
    MyDebug;
    emit this->signalOpenCamera();
}

void CameraSwitcher::slotGotCvFrame(const cv::Mat &cv_frame)
{
    MyDebug;
    mMutex.lock();
    cv_frame.copyTo(mCvImage);
    mMutex.unlock();
}
