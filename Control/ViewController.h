#ifndef VIEWCONTROLLER_H
#define VIEWCONTROLLER_H

#include <QObject>
#include "MainWindow.h"
#include "WinBase.h"
#include <QFrame>
#include <QGridLayout>
#include <QLabel>
#include <opencv2/opencv.hpp>
#include "XLabel.h"

class ViewController : public QObject
{
    Q_OBJECT
public:
    explicit ViewController(QObject *parent = nullptr);

public:     // 窗口
    MainWindow *mMainWin;
    QFrame *mMainFrame;
    QWidget *mCurrentWin;
    QGridLayout *mCurrentLayout;
    std::vector<WinBase * > mFrameList;

    XLabel *mTestMovieShow;

public:     // 方法
    void windowLoad();
    void eventFilterInstall();
    void start();
    void navigateTo(QString win_name);
    void windowSwitch(QWidget *win);
    cv::Rect getShowRect(const cv::Mat &src_image, const int &width_crop, const int &height_crop);
    void resizeImage(cv::Mat &image_, const int &width_crop, const int &height_crop);
    void displayImageInQLabel(const cv::Mat &image, XLabel *label);

public:     // 事件
    bool eventFilter(QObject *watched, QEvent *event);

public slots:
    void changeWinSlot(uint num);
    void changeWinSlot(QString win_name);
signals:

};

#endif // VIEWCONTROLLER_H
