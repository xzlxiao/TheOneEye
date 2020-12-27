#ifndef VIEWCONTROLLER_H
#define VIEWCONTROLLER_H

#include <QObject>

class ViewController : public QObject
{
    Q_OBJECT
public:
    explicit ViewController(QObject *parent = nullptr);

signals:

};

#endif // VIEWCONTROLLER_H
