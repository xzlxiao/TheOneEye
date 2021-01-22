#ifndef DEBUGPRINT_H
#define DEBUGPRINT_H
#include <QDebug>

class DebugPrint
{
public:
    DebugPrint();
    static bool isPrintDebug;
};

#define MyDebug if(DebugPrint::isPrintDebug)qDebug()<<"[FILE:"<<__FILE__<<",LINE"<<__LINE__<<",FUNC"<<__FUNCTION__<<"]"<<endl;

#endif // DEBUGPRINT_H
