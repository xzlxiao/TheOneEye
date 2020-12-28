#ifndef XSETTING_H
#define XSETTING_H

#include <QObject>
#include <QCoreApplication>
#include <QString>
#include <QSettings>
#include <QDebug>

class XSetting : public QObject
{
    Q_OBJECT
public:
    explicit XSetting(QObject *parent = nullptr);
    static QString mName;
    static bool *isDebug;
public:
    static void print();
    static void setValue(const QString &key, const QString &value);
    static QString getValue(const QString &key);
    static void removeValue(const QString &key);
    static void loadSettingFile();

signals:

public slots:
};

#endif // XSETTING_H
