#ifndef __CAMERACONTROLLER_H_
#define __CAMERACONTROLLER_H_
#include <QObject>
#include <vector>
#include "CameraBase.h"

class CameraController : public QObject
{
public:
    explicit CameraController(QObject *parent = nullptr);
    ~CameraController(){}
private:    
    std::<*CameraBase> mCameraList;
    int mCameraNum;

public:
    void run();
    void CamerasDetect();
    void startCamera(int cam_id);
    void releaseCamera(int cam_id);
signals:

};

#endif //__CAMERACONTROLLER_H_
