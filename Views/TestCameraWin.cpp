#include "TestCameraWin.h"
#include "ui_TestCameraWin.h"

TestCameraWin::TestCameraWin(QWidget *parent) :
    WinBase(parent),
    ui(new Ui::TestCameraWin),
    mCameraShow(nullptr)
{
    ui->setupUi(this);
    mCameraShow = ui->lbCameraShow;
    this->id = QString("TestCameraWin");
    this->name = QString("TestCameraWin");
}

TestCameraWin::~TestCameraWin()
{
    delete ui;
}
