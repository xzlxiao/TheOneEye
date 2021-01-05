#include "XLabel.h"
#include <QPainter>

XLabel::XLabel(QWidget *parent) :
    QLabel(parent)
{

}

void XLabel::paintEvent(QPaintEvent *event)
{
    Q_UNUSED(event);

    QPainter painter(this);

    // 反走样
    painter.setRenderHint(QPainter::Antialiasing, true);

    // 绘制图标
    painter.drawPixmap(rect(), QPixmap::fromImage(mImage));
}