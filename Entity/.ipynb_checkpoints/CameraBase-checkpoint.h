#ifndef __CAMERABASE_H_
#define __CAMERABASE_H_
#include <QObject>

class CameraBase : public QObject
{
public:
    explicit CameraBase(QObject *parent = nullptr);
    
    int mCameraId;
    virtual openCamera() const {throw "未实现该成员方法"; }
    virtual releaseCamera() const {throw "未实现该成员方法"; }
signals:

};

#endif // __CAMERABASE_H_