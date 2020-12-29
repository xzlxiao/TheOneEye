#include "CameraController.h"
#include "CameraInterface.h"
CameraController::CameraController(QObject *parent) : QObject(parent)
{
    
}

void CameraController::startCamera(int cam_id, XCameraType camera_type)
{
    switch (camera_type) {
    case X_USB_CAM:
        CameraInterface *camera = new CameraInterface();
        QThread *thread1 = new QThread();
        camera->setCameraID(cam_id);
        camera->moveToThread(thread1);
        this->mCameraList.insert(pair<int, QThread * >(cam_id, thread1));
        break;
    default:
        break;
    }
}
