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
    ${OpenCV_INCLUDE_DIRS}
    )

set(ControlSrc
    Control/MainController
    Control/CameraController)

set(AlgorithmSrc
    Algorithm/AlgorithmTest)

set(CommonSrc
    Common/Common)

set(EntitySrc
    Entity/EntityTest
    Entity/CameraBase)

set(TestSrc
    Test/Test)

add_executable(TheOneEye
    main.cpp
    ${ControlSrc}
    ${AlgorithmSrc}
    ${CommonSrc}
    ${EntitySrc}
    ${TestSrc}
    )

target_link_libraries(TheOneEye
    Qt5::Widgets
    Qt5::Network
    ${OpenCV_LIBS}
)
