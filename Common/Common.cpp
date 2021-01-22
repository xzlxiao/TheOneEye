#include "Common.h"
using namespace std;
using namespace cv;

Common::Common()
{

}
std::vector<std::string> Common::MODE_NAME = { "Startup", "Detection", "Collect Faces", "Training", "Recognition", "Delete All", "ERROR!" };

string Common::getTime()
{
    MyDebug;
    time_t tt = time(NULL);//这句返回的只是一个时间cuo
    tm* t= localtime(&tt);
    char tmp[64];
    strftime(tmp, sizeof(tmp), "%Y-%m-%d_%H-%M-%S", t);
    string time = tmp;
    return time;
}

QString Common::qGetTime()
{
    QDateTime current_date_time =QDateTime::currentDateTime();
    QString current_date = current_date_time.toString("yyyy-MM-dd_hh-mm-ss");
    return current_date;
}

// Compare two images by getting the L2 error (square-root of sum of squared error).
///
/// \brief Common::getSimilarity 比较两图片的差异
/// \param A
/// \param B
/// \return 数值越大，差异越大
///
double Common::getSimilarity(const Mat &A, const Mat &B)
{
    if (A.rows > 0 && A.rows == B.rows && A.cols > 0 && A.cols == B.cols)
    {
        // Calculate the L2 relative error between the 2 images.
        double errorL2 = norm(A, B, NORM_L2);
        // Convert to a reasonable scale, since L2 error is summed across all pixels of the image.
        double similarity = errorL2 / (double)(A.rows * A.cols);
        return similarity;
    }
    else
    {
        //cout << "WARNING: Images have a different size in 'getSimilarity()'." << endl;
        return 100000000.0;  // Return a bad value
    }
}

void Common::Mat2QImage(const Mat &cvImg, QImage &qImage_out)
{
    //MyDebug;
    Mat invert_img;
    if(cvImg.channels()==3)                             //3 channels color image
    {

        cv::cvtColor(cvImg,invert_img,COLOR_BGR2RGB);
        qImage_out =QImage((const unsigned char*)(invert_img.data),
                           invert_img.cols, invert_img.rows,
                           invert_img.cols*invert_img.channels(),
                           QImage::Format_RGB888);
    }
    else if(cvImg.channels()==1)                    //grayscale image
    {
        qImage_out =QImage((const unsigned char*)(cvImg.data),
                           cvImg.cols,cvImg.rows,
                           cvImg.cols*cvImg.channels(),
                           QImage::Format_Indexed8);
    }
    else
    {
        qImage_out =QImage((const unsigned char*)(cvImg.data),
                           cvImg.cols,cvImg.rows,
                           cvImg.cols*cvImg.channels(),
                           QImage::Format_RGB888);
    }
}
