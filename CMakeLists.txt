cmake_minimum_required(VERSION 3.2.1 FATAL_ERROR)
add_compile_options(-std=c++11)

project(TheOneEye)

IF (APPLE)
    set(CMAKE_C_COMPILER "/usr/bin/clang")
    set(CMAKE_CXX_COMPILER "/usr/bin/clang++")
    set(Qt5_DIR /Users/xiaozhenlong/Qt/5.15.2/clang_64/lib/cmake/Qt5)
    if(CMAKE_C_COMPILER_ID STREQUAL "Clang")
        set(OpenMP_C_FLAG "-fopenmp=libomp -Wno-unused-command-line-argument")
    endif()
    if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
        set(OpenMP_CXX_FLAG "-fopenmp=libomp -Wno-unused-command-line-argument")
    endif()
ELSE()

ENDIF()

set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_AUTORCC ON)
set(SRC src/cpp/)

set(RESOURCE_DIR resource/resource.qrc)
set(OpenCV_DIR /usr/local/cortexbot/opencv)
find_package(OpenCV REQUIRED)

find_package(Qt5 REQUIRED Widgets Network)

include_directories(${SRC}UserInteraction
    ${SRC}Test
    ${SRC}Algorithm
    ${SRC}Control
    ${SRC}Entity
    ${SRC}Input
    ${SRC}Common
    ${SRC}Views
    ${OpenCV_INCLUDE_DIRS}
    )

# 设置复制到编译目录的文件
set(COPYITEM
    Config.ini)

add_custom_command(OUTPUT  COPY_RES COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/${COPYITEM} ${PROJECT_BINARY_DIR}  )
add_custom_target(CopyTask ALL DEPENDS COPY_RES)

set(ControlSrc
    ${SRC}Control/MainController
    ${SRC}Control/CameraController
    ${SRC}Control/ViewController)

set(AlgorithmSrc
    ${SRC}Algorithm/AlgorithmTest)

set(CommonSrc
    ${SRC}Common/Common
    ${SRC}Common/DebugPrint
    ${SRC}Common/XSetting)

set(EntitySrc
    ${SRC}Entity/EntityTest
    ${SRC}Entity/CameraBase
    ${SRC}Entity/CameraInterface)

set(TestSrc
    ${SRC}Test/Test)

set(ViewsSrc
    ${SRC}Views/MainWindow
    ${SRC}Views/MainWindow.ui
    ${SRC}Views/WinBase
    ${SRC}Views/TestCameraWin
    ${SRC}Views/TestCameraWin.ui
    ${SRC}Views/XLabel
    )

add_executable(TheOneEye
    main.cpp
    Config.ini
    ${ControlSrc}
    ${AlgorithmSrc}
    ${CommonSrc}
    ${EntitySrc}
    ${TestSrc}
    ${ViewsSrc}
    ${RESOURCE_DIR}
    )

target_link_libraries(TheOneEye
    Qt5::Widgets
    Qt5::Network
    ${OpenCV_LIBS}
)
