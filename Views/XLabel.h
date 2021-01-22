#ifndef __XLABEL_H_
#define __XLABEL_H_
#include <QLabel>
#include <QImage>


class XLabel : public QLabel
{
    Q_OBJECT

public:
    explicit XLabel(QWidget *parent = 0);
    ~XLabel(){};

public:
    QImage mImage;

   void paintEvent(QPaintEvent *event);


};

#endif // __XLABEL_H_