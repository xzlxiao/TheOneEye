#include "Test.h"
#include "XSetting.h"
#include <assert.h>

void UnitTest()
{
    testSettings();
}

void testSettings()
{
    XSetting::print();
    assert(XSetting::getValue("Test/Name")==QString("Configuration"));
    XSetting::setValue("Test/Name2", "123");
    assert(XSetting::getValue("Test/Name2").toInt()==123);
    XSetting::removeValue("Test/Name2");
    assert(XSetting::getValue("Test/Name2")=="Fail");
}


