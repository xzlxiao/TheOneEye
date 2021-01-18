#ifndef CONTENTSNAVWIN_H
#define CONTENTSNAVWIN_H

#include <QWidget>

namespace Ui {
class ContentsNavWin;
}

class ContentsNavWin : public QWidget
{
    Q_OBJECT

public:
    explicit ContentsNavWin(QWidget *parent = nullptr);
    ~ContentsNavWin();

private:
    Ui::ContentsNavWin *ui;
};

#endif // CONTENTSNAVWIN_H
