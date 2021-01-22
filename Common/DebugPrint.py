"""
       .==.        .==.
      //`^\\      //^`\\
     // ^ ^\(\__/)/^ ^^\\
    //^ ^^ ^/+  0\ ^^ ^ \\
   //^ ^^ ^/( >< )\^ ^ ^ \\
  // ^^ ^/\| v''v |/\^ ^ ^\\
 // ^^/\/ /  `~~`  \ \/\^ ^\\
 ----------------------------
BE CAREFULL! THERE IS A DRAGON.

Function：For debug function

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：

Updating Records:
2021-01-22 09:38:15 xzl
"""
import inspect
import sys
sys.path.append("../")


class DebugPrint:
    isPrintDebug = False

    def __init__(self):
        pass


def get_current_function_name():
    return inspect.stack()[1][3]


def myDebug(class_name, function_name):
    if DebugPrint.isPrintDebug:
        print("%s.%s invoked" % (class_name, function_name))
