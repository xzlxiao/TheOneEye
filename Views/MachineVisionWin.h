#ifndef MACHINEVISIONWIN_H
#define MACHINEVISIONWIN_H

#include <QWidget>

namespace Ui {
class MachineVisionWin;
}

class MachineVisionWin : public QWidget
{
    Q_OBJECT

public:
    explicit MachineVisionWin(QWidget *parent = nullptr);
    ~MachineVisionWin();

private:
    Ui::MachineVisionWin *ui;
};

#endif // MACHINEVISIONWIN_H
