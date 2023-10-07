#include <librealsense2/rs.hpp>
#include <opencv2/opencv.hpp>

int main()
{
  // Create a pipeline to represent a non-blocking collection of streaming devices
  rs2::pipeline pipeline;
  rs2::config config;

  // Configure all streams for the D435
  config.enable_stream(RS2_STREAM_COLOR, 1280, 720, RS2_FORMAT_BGR8, 30);
  config.enable_stream(RS2_STREAM_DEPTH, 1280, 720, RS2_FORMAT_Z16, 30);
  config.enable_stream(RS2_STREAM_INFRARED, 1, 1280, 720, RS2_FORMAT_Y8, 30);
  config.enable_stream(RS2_STREAM_INFRARED, 2, 1280, 720, RS2_FORMAT_Y8, 30);

  // Start the pipeline
  pipeline.start(config);

  const auto window_name = "Color Feed";
  cv::namedWindow(window_name, cv::WINDOW_AUTOSIZE);

  while (true) {
    rs2::frameset frames = pipeline.wait_for_frames();

    // Get frames
    rs2::frame color_frame = frames.get_color_frame();
    rs2::frame depth_frame = frames.get_depth_frame();
    rs2::frame ir_frame_left = frames.get_infrared_frame(1);
    rs2::frame ir_frame_right = frames.get_infrared_frame(2);

    // Convert to Mat
    cv::Mat color(cv::Size(1280, 720), CV_8UC3, (void *)color_frame.get_data(), cv::Mat::AUTO_STEP);
    cv::Mat depth(
      cv::Size(1280, 720), CV_16UC1, (void *)depth_frame.get_data(), cv::Mat::AUTO_STEP);
    cv::Mat ir_left(
      cv::Size(1280, 720), CV_8UC1, (void *)ir_frame_left.get_data(), cv::Mat::AUTO_STEP);
    cv::Mat ir_right(
      cv::Size(1280, 720), CV_8UC1, (void *)ir_frame_right.get_data(), cv::Mat::AUTO_STEP);

    // Convert depth frame to viewable color frame
    cv::Mat depth_colorized;
    cv::Mat depth_abs;
    cv::convertScaleAbs(depth, depth_abs, 0.03f);
    cv::applyColorMap(depth_abs, depth_colorized, cv::COLORMAP_JET);
    // Display
    cv::imshow("Color Feed", color);
    cv::imshow("Depth Feed", depth_colorized);
    cv::imshow("IR Left", ir_left);
    cv::imshow("IR Right", ir_right);

    // Break the loop when 'esc' key is pressed
    if (cv::waitKey(1) == 27) {
      break;
    }
  }

  cv::destroyAllWindows();

  return 0;
}
