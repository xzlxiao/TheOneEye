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

Function：Load data

Modules：
pass

(c) 肖镇龙(xzl) 2021

Dependencies：

Updating Records:
2021-01-22 11:21:11 xzl
"""

import torch
import torchvision
import torchvision.transforms as transforms
import torchvision.transforms as T

def get_transform(settings):
    transform = []
    if not settings.isToTensor:
        transforms.append(T.ToTensor())
    if not settings.isRandomHorizontalFlip:
        if not settings.mRandomHorizontalFlip:
            transforms.append(T.RandomHorizontalFlip(settings.mRandomHorizontalFlip))
        else:
            transforms.append(T.RandomHorizontalFlip(0.5))
