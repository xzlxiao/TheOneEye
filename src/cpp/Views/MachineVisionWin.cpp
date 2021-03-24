#include "MachineVisionWin.h"
#include "ui_MachineVisionWin.h"

MachineVisionWin::MachineVisionWin(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::MachineVisionWin)
{
    ui->setupUi(this);
}

MachineVisionWin::~MachineVisionWin()
{
    delete ui;
}
