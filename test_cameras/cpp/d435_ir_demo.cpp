#include <iostream>
#include <librealsense2/rs.hpp>
#include <opencv2/opencv.hpp>

int main()
{
  // Create a RealSense pipeline
  rs2::pipeline pipe;
  rs2::config cfg;

  // Configure the IR streams of the D435
  cfg.enable_stream(RS2_STREAM_INFRARED, 1, 1280, 720, RS2_FORMAT_Y8, 30);  // left IR camera
  cfg.enable_stream(RS2_STREAM_INFRARED, 2, 1280, 720, RS2_FORMAT_Y8, 30);  // right IR camera

  // Start the pipeline
  pipe.start(cfg);

  while (true) {
    // Get the next set of frames from the camera
    rs2::frameset frames = pipe.wait_for_frames();

    // Get both IR frames
    rs2::frame ir_frame_left = frames.get_infrared_frame(1);
    rs2::frame ir_frame_right = frames.get_infrared_frame(2);

    // Convert the IR frames to Mat objects for visualization
    cv::Mat ir_image_left(720, 1280, CV_8U, (void *)ir_frame_left.get_data());
    cv::Mat ir_image_right(720, 1280, CV_8U, (void *)ir_frame_right.get_data());

    // Display the images
    cv::imshow("IR Left", ir_image_left);
    cv::imshow("IR Right", ir_image_right);

    // Break the loop when 'esc' key is pressed
    if (cv::waitKey(1) == 27) {
      break;
    }
  }

  pipe.stop();
  cv::destroyAllWindows();

  return 0;
}
