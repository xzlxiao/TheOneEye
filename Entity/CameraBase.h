#ifndef __CAMERABASE_H_
#define __CAMERABASE_H_
#include <QObject>

class CameraBase : public QObject
{
    Q_OBJECT

public:
    explicit CameraBase(QObject *parent = nullptr);
    
    int mCameraId;
    virtual void openCamera() const {throw "未实现该成员方法"; }
    virtual void releaseCamera() const {throw "未实现该成员方法"; }
    void setCameraID(int id);
signals:

};

#endif // __CAMERABASE_H_
