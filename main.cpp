#include <QApplication>
#include <iostream>
#include <QDebug>
#include <QString>
#include <string>
#include "Control/MainController.h"
using namespace std;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    cout << "test" << endl;
    MainController main_controller;
    main_controller.start();
    return a.exec();
}


