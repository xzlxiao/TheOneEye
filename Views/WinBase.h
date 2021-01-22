#ifndef WINBASE_H
#define WINBASE_H

#include <QWidget>

namespace Ui {
class WinBase;
}

class WinBase : public QWidget
{
    Q_OBJECT

public:
    explicit WinBase(QWidget *parent = 0);
    ~WinBase();
    virtual void windowLoad(){}

public:
    //Ui::WinBase *ui;
    QString id;     //界面的类名
    QString name;   //界面名

signals:
    void returnSignal();


};

#endif // WINBASE_H
