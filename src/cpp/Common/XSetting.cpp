#include "XSetting.h"
#include "DebugPrint.h"
QString XSetting::mName = "None";
bool *XSetting::isDebug = &DebugPrint::isPrintDebug;
bool XSetting::isShowBorder = false;
bool XSetting::isCameraDebug = false;

XSetting::XSetting(QObject *parent) : QObject(parent)
{
    MyDebug;
}

void XSetting::print()
{
    MyDebug;
    qDebug() << "【XSetting test】";
    qDebug() << "Test/Name: " << XSetting::mName << endl;
}

void XSetting::setValue(const QString &key, const QString &value)
{
    MyDebug;
    QString ConfigFileDir = QCoreApplication::applicationDirPath() + "/Config.ini";
    QSettings my_setting(ConfigFileDir, QSettings::IniFormat);
    my_setting.setValue(key, value);

}


QString XSetting::getValue(const QString &key)
{
    MyDebug;
    QString ConfigFileDir = QCoreApplication::applicationDirPath() + "/Config.ini";
    QSettings my_setting(ConfigFileDir, QSettings::IniFormat);
    return my_setting.value(key, "Fail").toString();
}

void XSetting::removeValue(const QString &key)
{
    MyDebug;
    QString ConfigFileDir = QCoreApplication::applicationDirPath() + "/Config.ini";
    QSettings my_setting(ConfigFileDir, QSettings::IniFormat);
    my_setting.remove(key);
}

void XSetting::loadSettingFile()
{
    MyDebug;
    QString ConfigFileDir = QCoreApplication::applicationDirPath() + "/Config.ini";
    QSettings my_setting(ConfigFileDir, QSettings::IniFormat);
    mName = my_setting.value("Test/Name", "Fail").toString();
    DebugPrint::isPrintDebug = my_setting.value("Debug/isDebug", false).toBool();
    isShowBorder = my_setting.value("Debug/isShowBorder", false).toBool();
    isCameraDebug = my_setting.value("Debug/isCameraDebug", false).toBool();
}
