#include "MainWindow.h"
#include "ui_MainWindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    mCentralWidget(nullptr)
{
    ui->setupUi(this);
    mCentralWidget = ui->centralwidget;
    mlbBackgroundList.push_back(ui->lbBackground1);
    mlbBackgroundList.push_back(ui->lbBackground2);
    mlbBackgroundList.push_back(ui->lbBackground3);
    mlbBackgroundList.push_back(ui->lbBackground4);
    mlbBackgroundList.push_back(ui->lbBackground5);
    mlbBackgroundList.push_back(ui->lbBackground6);
    mlbBackgroundList.push_back(ui->lbBackground7);
    mlbBackgroundList.push_back(ui->lbBackground8);
    mlbBackgroundList.push_back(ui->lbBackground9);
//    QMovie *movie = new QMovie(":/images/background001.gif");
//    ui->lbBackground->setMovie(movie);
//    movie->start();

}

MainWindow::~MainWindow()
{
    delete ui;
}
