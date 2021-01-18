#include "ContentsNavWin.h"
#include "ui_ContentsNavWin.h"

ContentsNavWin::ContentsNavWin(QWidget *parent) :
    QWidget(parent),
    ui(new Ui::ContentsNavWin)
{
    ui->setupUi(this);
}

ContentsNavWin::~ContentsNavWin()
{
    delete ui;
}
