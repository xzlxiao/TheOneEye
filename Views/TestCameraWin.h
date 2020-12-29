#ifndef TESTCAMERAWIN_H
#define TESTCAMERAWIN_H

#include "WinBase.h"
#include <QLabel>

namespace Ui {
class TestCameraWin;
}

class TestCameraWin : public WinBase
{
    Q_OBJECT

public:
    explicit TestCameraWin(QWidget *parent = 0);
    ~TestCameraWin();

private:
    Ui::TestCameraWin *ui;

public:
    QLabel *mCameraShow;
};

#endif // TESTCAMERAWIN_H
