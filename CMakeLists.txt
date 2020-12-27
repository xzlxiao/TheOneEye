cmake_minimum_required(VERSION 2.8.11 FATAL_ERROR)
add_compile_options(-std=c++11)

project(TheOneEye)

IF (APPLE)
    set(CMAKE_C_COMPILER "/usr/bin/clang")
    set(CMAKE_CXX_COMPILER "/usr/bin/clang++")
    set(Qt5_DIR /Users/xiaozhenlong/Qt/6.0.0/clang_64/lib/cmake/Qt6)
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

set(RESOURCE_DIR resource/resource.qrc)
set(OpenCV_DIR /usr/local/cortexbot/opencv)
find_package(OpenCV REQUIRED)

find_package(Qt5 REQUIRED Widgets Network)

include_directories(UserInteraction
    Test
    Algorithm
    Control
    Entity
    Input
    Common
    Views
    ${OpenCV_INCLUDE_DIRS}
    )

# 设置复制到编译目录的文件
set(COPYITEM
    Config.ini)

add_custom_command(OUTPUT  COPY_RES COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/${COPYITEM} ${PROJECT_BINARY_DIR}  )
add_custom_target(CopyTask ALL DEPENDS COPY_RES)

set(ControlSrc
    Control/MainController
    Control/CameraController
    Control/ViewController)

set(AlgorithmSrc
    Algorithm/AlgorithmTest)

set(CommonSrc
    Common/Common
    Common/DebugPrint
    Common/XSetting)

set(EntitySrc
    Entity/EntityTest
    Entity/CameraBase)

set(TestSrc
    Test/Test)

set(ViewsSrc
    Views/MainWindow
    Views/WinBase
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
    )

target_link_libraries(TheOneEye
    Qt5::Widgets
    Qt5::Network
    ${OpenCV_LIBS}
)
