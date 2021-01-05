#ifndef CAMERAINTERFACE_H
#define CAMERAINTERFACE_H
#include <QObject>
#include <opencv2/opencv.hpp>
#include <QImage>
#include <string>
#include <QDebug>
#include <QTimer>
#include "DebugPrint.h"
#include "CameraBase.h"
#include <QMutex>

class CameraInterface : public CameraBase
{
    Q_OBJECT

public:
    explicit CameraInterface(QObject *parent = nullptr);
    ~CameraInterface();
    void _init();

private:
    cv::VideoCapture *video_capture;
    QTimer *timer_video;
    QTimer *timer_img_grab;
    QMutex mMutex;
    cv::VideoWriter video_writer;   //make a video record

    int display_width=450;
    int display_height=450;
    bool TRANSFOR_TO_QIMAGE;        //是否自动转化QImage

    void readFrame(const int &width_resize, const int &height_resize);       // 读取当前帧信息
    void readFrameOnly();   // 仅读取当前帧，不转换为QImage，并返回读取到的图片的引用

public:
    double rate; //FPS
    cv::Mat frame;          // 原始读取的图片
    QImage image;           // 缩放的图片
    void openCamera();      // 打开摄像头
    bool isCameraNotUsed;    // use it when close the thread
    void releaseCamera();     // 关闭摄像头
    void takePictures(const std::string &dir);    // 拍照
    void takeVideo(const std::string &dir);       // 录像
    void endTakeVideo();    // 停止录像

    void resizeImage(cv::Mat &image_, const int &width_crop, const int &height_crop);
    cv::Rect getShowRect(const cv::Mat &src_image, const int &width_crop, const int &height_crop);
    static void Mat2QImage(const cv::Mat &cvImg, QImage &qImage_out);

    void setDisplaySize(const int &display_width_, const int &display_height_);

signals:
    void gotCvFrameSignal(const cv::Mat &cv_frame);
public slots:
    void slotOpenCamera();
    void slotCloseCamera();
private slots:
    void takeVideoSlot();
    void timerImgGrab();

public:
};

#endif // CAMERAINTERFACE_H
