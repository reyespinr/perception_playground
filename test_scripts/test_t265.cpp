#include <librealsense2/rs.hpp>
#include <opencv2/opencv.hpp>

int main() {
    // Create a pipeline to encapsulate the device
    rs2::pipeline pipe;
    rs2::config cfg;
    cfg.enable_device("224622112228");
    cfg.enable_stream(RS2_STREAM_FISHEYE, 1);
    cfg.enable_stream(RS2_STREAM_FISHEYE, 2);
    // Start the pipeline
    pipe.start(cfg);

    // Capture and display the images
    while (true) {
        // Block until a new set of frames is available
        rs2::frameset frameset = pipe.wait_for_frames();

        // Get fisheye frames
        rs2::video_frame fisheye_frame1 = frameset.get_fisheye_frame(1);
        rs2::video_frame fisheye_frame2 = frameset.get_fisheye_frame(2);

        // Convert to OpenCV format
        cv::Mat fisheye_image1(cv::Size(848, 800), CV_8U, (void*)fisheye_frame1.get_data(), cv::Mat::AUTO_STEP);
        cv::Mat fisheye_image2(cv::Size(848, 800), CV_8U, (void*)fisheye_frame2.get_data(), cv::Mat::AUTO_STEP);

        // Display images
        cv::imshow("Fisheye 1", fisheye_image1);
        cv::imshow("Fisheye 2", fisheye_image2);

        // Exit loop if 'esc' key is pressed
        if (cv::waitKey(1) == 27) {
            break;
        }
    }

    return 0;
}
