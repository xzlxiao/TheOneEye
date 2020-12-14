cmake_minimum_required(VERSION 2.8.11 FATAL_ERROR)
add_compile_options(-std=c++11)

project(TheOneEye)
set(Qt5_DIR /Users/xiaozhenlong/Qt/5.15.2/wasm_32/lib/cmake/Qt5)

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
    Control/MainController)

set(AlgorithmSrc
    Algorithm/AlgorithmTest)

set(CommonSrc
    Common/Common)

set(EntitySrc
    Entity/EntityTest)

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