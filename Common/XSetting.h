#ifndef XSETTING_H
#define XSETTING_H

#include <QObject>
#include <QCoreApplication>
#include <QString>
#include <QSettings>

class XSetting : public QObject
{
    Q_OBJECT
public:
    explicit XSetting(QObject *parent = nullptr);
private:
    QString mConfigFileDir;
    QSettings mSetting;
public:


signals:

public slots:
};

#endif // XSETTING_H
