#ifndef ENTITYTEST_H
#define ENTITYTEST_H

#include <QObject>

class EntityTest : public CameraBase
{
    Q_OBJECT

public:
    explicit EntityTest(QObject *parent = nullptr);

signals:

};

#endif // ENTITYTEST_H
