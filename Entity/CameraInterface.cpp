#include "CameraInterface.h"
#include "XSetting.h"

using namespace cv;
using namespace std;

CameraInterface::CameraInterface(QObject *parent) : CameraBase(parent),
    video_capture(nullptr),
    timer_video(nullptr),
    timer_img_grab(nullptr),
    isCameraNotUsed(false)
{
    if (XSetting::isCameraDebug) MyDebug;
    this->_init();
}

CameraInterface::~CameraInterface()
{
    if (XSetting::isCameraDebug) MyDebug;
    this->releaseCamera();
}

void CameraInterface::_init()
{
    if (XSetting::isCameraDebug) MyDebug;
    this->mCameraId = 0;
    this->rate = 30;
    this->timer_video = new QTimer(this);
    this->timer_img_grab = new QTimer(this);
    connect(this->timer_video, SIGNAL(timeout()), this, SLOT(takeVideoSlot()));
    connect(this->timer_img_grab, SIGNAL(timeout()), this, SLOT(timerImgGrab()));

}

void CameraInterface::openCamera()
{
    if (XSetting::isCameraDebug) MyDebug;
    try
    {
        if (this->video_capture == nullptr)
        {
            this->video_capture = new VideoCapture;
            this->video_capture->open(this->mCameraId);
        }
        else
        {
            if (!this->video_capture->isOpened())
            {
                this->video_capture->open(this->mCameraId);
            }

        }

    }
    catch (cv::Exception &e)
    {}

    if (!this->video_capture->isOpened())
    {
        cerr << "ERROR: Could not access the camera!" << endl;
        throw;
    }
    else
    {
        *(this->video_capture) >> this->frame;
        CameraInterface::Mat2QImage(this->frame, this->image);

    }
    cout << "Loaded camera " << this->mCameraId << "." << endl;

    //this->TRANSFOR_TO_QIMAGE = TRANSFOR_TO_QIMAGE;
    timer_img_grab->start(1000.0 / this->rate);


}

///
/// \brief CameraInterface::readFrame
/// \param width_resize
/// \param height_resize
/// \abstract 当width_resize和height_resize都大于0时，image为缩放的图片
void CameraInterface::readFrame(const int &width_resize = -1, const int &height_resize = -1)
{
    if (XSetting::isCameraDebug) MyDebug;
    *(this->video_capture) >> this->frame;
    //flip(frame, frame, 1);
    if (!this->frame.empty())
    {

        if (width_resize > 0 && height_resize > 0)
        {
            Mat tmp;
            resizeImage(tmp, width_resize, height_resize);
            CameraInterface::Mat2QImage(tmp, this->image);
        }
        else
        {
            CameraInterface::Mat2QImage(this->frame, this->image);
        }


    }
}

void CameraInterface::readFrameOnly()
{
    if (XSetting::isCameraDebug) MyDebug;
    mMutex.lock();
    *(this->video_capture) >> this->frame;
    // this->frame.copyTo(frame_copy);
    mMutex.unlock();
    //flip(frame, frame, 1);
}

void CameraInterface::releaseCamera()
{
    if (XSetting::isCameraDebug) MyDebug;
    timer_img_grab->stop();
    timer_video->stop();


}

void CameraInterface::takePictures(const string &dir)
{
    if (XSetting::isCameraDebug) MyDebug;
    //this->readFrame();
    if (!this->frame.empty())
    {
        cv::imwrite(dir, this->frame);
    }
}

void CameraInterface::takeVideo(const string &dir)
{
    if (XSetting::isCameraDebug) MyDebug;
    if (this->video_capture->isOpened())
    {
        //this->video_writer.open(dir, cv::VideoWriter::fourcc('P', 'I', 'M', '1'), this->rate, cv::Size(this->frame.cols, frame.rows), true);
        this->timer_video->start(1000/this->rate);
    }
    else
    {
        qDebug() << "摄像头未开启" << endl;
    }
}

void CameraInterface::endTakeVideo()
{
    if (XSetting::isCameraDebug) MyDebug;
    this->timer_video->stop();
    this->video_writer.release();
}

void CameraInterface::resizeImage(cv::Mat &image_, const int &width_crop, const int &height_crop)
{
    if (XSetting::isCameraDebug) MyDebug;
    image_ = this->frame(getShowRect(this->frame, width_crop,height_crop));
    cv::resize(image_,image_, Size(width_crop, height_crop));
}

Rect CameraInterface::getShowRect(const Mat &src_image, const int &width_crop, const int &height_crop)
{
    if (XSetting::isCameraDebug) MyDebug;
    double gui_wh_ratio, img_wh_ratio;
    Rect ret;
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

void CameraInterface::Mat2QImage(const Mat &cvImg, QImage &qImage_out)
{
    if (XSetting::isCameraDebug) MyDebug;
    Mat invert_img;
    if(cvImg.channels()==3)                             //3 channels color image
    {

        cv::cvtColor(cvImg,invert_img,COLOR_BGR2RGB);
        qImage_out =QImage((const unsigned char*)(invert_img.data),
                           invert_img.cols, invert_img.rows,
                           invert_img.cols*invert_img.channels(),
                           QImage::Format_RGB888);
    }
    else if(cvImg.channels()==1)                    //grayscale image
    {
        qImage_out =QImage((const unsigned char*)(cvImg.data),
                           cvImg.cols,cvImg.rows,
                           cvImg.cols*cvImg.channels(),
                           QImage::Format_Indexed8);
    }
    else
    {
        qImage_out =QImage((const unsigned char*)(cvImg.data),
                           cvImg.cols,cvImg.rows,
                           cvImg.cols*cvImg.channels(),
                           QImage::Format_RGB888);
    }

}

void CameraInterface::setDisplaySize(const int &display_width_, const int &display_height_)
{
    if (XSetting::isCameraDebug) MyDebug;
    this->display_width = display_width_;
    this->display_height = display_height_;
}

void CameraInterface::slotOpenCamera()
{
    if (XSetting::isCameraDebug) MyDebug;
    while(!isCameraNotUsed)
    {
        try
        {
            if (this->video_capture == nullptr)
            {
                this->video_capture = new VideoCapture;
                this->video_capture->open(this->mCameraId);
                if (!this->video_capture->isOpened())
                    continue;
            }
            else
            {
                if (!this->video_capture->isOpened())
                {
                    this->video_capture->open(this->mCameraId);
                }
                if (!this->video_capture->isOpened())
                    continue;
            }
            break;

        }
        catch (cv::Exception &e)
        {}
    }


    if (!isCameraNotUsed)
    {
        if (!this->video_capture->isOpened())
        {
            cerr << "ERROR: Could not access the camera!" << endl;
            throw;
        }
        else
        {
            *(this->video_capture) >> this->frame;
//            CameraInterface::Mat2QImage(this->frame, this->image);
            emit gotCvFrameSignal(this->frame);
        }
        cout << "Loaded camera " << this->mCameraId << "." << endl;

        //this->TRANSFOR_TO_QIMAGE = TRANSFOR_TO_QIMAGE;
        timer_img_grab->start(1000.0 / this->rate);
    }
}

void CameraInterface::slotCloseCamera()
{
    if (XSetting::isCameraDebug) MyDebug;
    isCameraNotUsed = true;
    releaseCamera();
}

void CameraInterface::takeVideoSlot()
{
    if (XSetting::isCameraDebug) MyDebug;
    this->video_writer.write(this->frame);
}

void CameraInterface::timerImgGrab()
{
    if (XSetting::isCameraDebug) MyDebug;
    if (!isCameraNotUsed)
    {
        this->readFrameOnly();
        emit gotCvFrameSignal(this->frame);
    }
    else
    {
        timer_img_grab->stop();
    }

}
