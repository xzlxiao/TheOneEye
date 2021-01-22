#include "CameraBase.h"

CameraBase::CameraBase(QObject *parent) : QObject(parent)
{

}

void CameraBase::setCameraID(int id)
{
    mCameraId = id;
}
