#ifndef __CAMERACONTROLLER_H_
#define __CAMERACONTROLLER_H_
#include <QObject>
#include <map>
#include <QThread>
#include "CameraBase.h"

enum XCameraType{
    X_USB_CAM,
    X_RealsenseD_CAM,
    X_RealsenseT_CAM
};

class CameraController : public QObject
{
    Q_OBJECT

public:
    explicit CameraController(QObject *parent = nullptr);
    ~CameraController(){}
private:    
    std::map<int, QThread * > mCameraList;
    int mCameraNum;

public:
    void run();
    void CamerasDetect();
    void startCamera(int cam_id, XCameraType camera_type);
    void releaseCamera(int cam_id);
signals:

};

#endif //__CAMERACONTROLLER_H_
