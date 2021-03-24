#ifndef COMMON_H
#define COMMON_H

#include <QObject>
#include <opencv2/core.hpp>
#include <opencv2/opencv.hpp>
#include <QImage>
#include <time.h>
#include <string>
#include "DebugPrint.h"
#include <QString>
#include <QDateTime>
#include <iostream>
#include <fstream>
#include <stdio.h>
#include <sstream>
#include <vector>
#include <initializer_list>


class Common
{
public:
    Common();
    static std::string getTime();
    static QString qGetTime();
    template <typename T> static std::string toString(T t);
    template <typename T> static T fromString(std::string t);
    static double getSimilarity(const cv::Mat &A, const cv::Mat &B);
    static std::vector<std::string> MODE_NAME;
    static void Mat2QImage(const cv::Mat &cvImg, QImage &qImage_out);
};


#endif // COMMON_H
