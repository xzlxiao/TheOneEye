# TheOneEye
![](resource/images/EyeOfSauron.jpeg)  
It's designed for machine vision testing tasks.

![](resource/file_res/TOE.gif)

## evironment setup
- sudo apt install libqt5multimedia5-plugins
- sudo apt install libgstreamer-plugins-base1.0-dev libgstreamer1.0-dev
## python compile command
```bash
python3 main.py
```

## C++ compile command
### mac m1 
- the terminal should be set with Rosetta mode
- the opencv shoudl be compile for x86_64
```bash
cmake -DCMAKE_OSX_ARCHITECTURES=x86_64 ..
```

## 备注
- 项目文档正在完善中……

## 项目进度
- 完成图像保存模块
- 解决多处理图像保存时地址错误的问题
- 视频保存模块
  - 使用sk-video替代opencv-python作为视频保存接口

## todo list
- 更多的算法插件
- 解决旋转图像无法保存的问题