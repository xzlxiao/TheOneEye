#ifndef __CAMERACONTROLLER_H_
#define __CAMERACONTROLLER_H_
#include <QObject>
#include <QImage>
#include <map>
#include <QThread>
#include "CameraBase.h"
#include <QMetaType>
#include <QLabel>
#include <opencv2/opencv.hpp>
#include <QMutex>

enum XCameraType{
    X_USB_CAM,
    X_RealsenseD_CAM,
    X_RealsenseT_CAM
};

class CameraSwitcher : public QObject
{
    Q_OBJECT

public:
    explicit CameraSwitcher(QObject *parent = nullptr);
    ~CameraSwitcher(){}
    cv::Mat mCvImage;
    QMutex mMutex;
public:
    void releaseCamera();
    void openCamera();
    static cv::Rect getShowRect(const cv::Mat &src_image, const int &width_crop, const int &height_crop);
    static void resizeImage(cv::Mat &image_, const int &width_crop, const int &height_crop);
    static void displayImageInQLabel(const cv::Mat &image, const QLabel &label);
signals:
    void signalStopCamera();
    void signalOpenCamera();
public slots:
    void slotGotCvFrame(const cv::Mat &cv_frame);
};

class CameraController : public QObject
{
    Q_OBJECT

public:
    explicit CameraController(QObject *parent = nullptr);
    ~CameraController(){}
private:    
    std::map<int, QThread * > mCameraList;
    std::map<int, CameraSwitcher *> mCameraSwitherList;
    int mCameraNum;

public:
    void run();
    void CamerasDetect();
    void startCamera(int cam_id, XCameraType camera_type);
    void releaseCamera(int cam_id);
    void gotFrame(int cam_id, cv::Mat &image);
signals:

};

#endif //__CAMERACONTROLLER_H_
