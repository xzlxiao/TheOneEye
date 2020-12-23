#include "XSetting.h"

XSetting::XSetting(QObject *parent) : QObject(parent),
    mConfigFileDir(QCoreApplication::applicationDirPath() + "/Config.ini"),
    mSetting(mConfigFileDir, QSettings::IniFormat)
{

}
