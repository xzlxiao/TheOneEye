#include <QApplication>
#include <iostream>
#include <QDebug>
#include <QString>
#include <string>
#include "MainController.h"
#include "Test.h"
#include "XSetting.h"

using namespace std;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    XSetting::loadSettingFile();
    if (*XSetting::isDebug) UnitTest();

    MainController main_controller;
    main_controller.start();
    return a.exec();
}


