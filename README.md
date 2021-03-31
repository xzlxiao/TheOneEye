# TheOneEye
![](resource/images/EyeOfSauron.jpeg)  
It's designed for machine vison testing tasks.

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

