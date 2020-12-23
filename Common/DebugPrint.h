#ifndef DEBUGPRINT_H
#define DEBUGPRINT_H
#include <QDebug>

class DebugPrint
{
public:
    DebugPrint();
};

const bool isPrintDebug = 0;
#define MyDebug if(isPrintDebug)qDebug()<<"[FILE:"<<__FILE__<<",LINE"<<__LINE__<<",FUNC"<<__FUNCTION__<<"]"<<endl;

#endif // DEBUGPRINT_H
