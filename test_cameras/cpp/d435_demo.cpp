#include <iostream>
#include <librealsense2/rs.hpp>
#include <opencv2/opencv.hpp>

int main()
{
  // Initialize RealSense pipeline
  rs2::pipeline pipeline;
  rs2::config config;

  // Configure and start the stream (color & depth)
  config.enable_stream(RS2_STREAM_COLOR, 640, 480, RS2_FORMAT_BGR8, 30);
  config.enable_stream(RS2_STREAM_DEPTH, 640, 480, RS2_FORMAT_Z16, 30);
  pipeline.start(config);

  const auto window_name_color = "Color Feed";
  const auto window_name_depth = "Depth Feed";
  cv::namedWindow(window_name_color, cv::WINDOW_AUTOSIZE);
  cv::namedWindow(window_name_depth, cv::WINDOW_AUTOSIZE);

  while (cv::waitKey(1) < 0) {
    // Get frames
    rs2::frameset frames = pipeline.wait_for_frames();
    rs2::video_frame color_frame = frames.get_color_frame();
    rs2::depth_frame depth_frame = frames.get_depth_frame();

    // Convert frames to OpenCV images
    cv::Mat color_image(
      cv::Size(640, 480), CV_8UC3, (void *)color_frame.get_data(), cv::Mat::AUTO_STEP);
    cv::Mat depth_image(
      cv::Size(640, 480), CV_16U, (void *)depth_frame.get_data(), cv::Mat::AUTO_STEP);

    // Apply colormap on depth image
    depth_image.convertTo(depth_image, CV_8UC1, 0.03);
    cv::Mat depth_colormap;
    cv::applyColorMap(depth_image, depth_colormap, cv::COLORMAP_JET);

    // Display both images
    cv::imshow(window_name_color, color_image);
    cv::imshow(window_name_depth, depth_colormap);

    // Break the loop when 'esc' key is pressed
    if (cv::waitKey(1) == 27) {
      break;
    }
  }

  pipeline.stop();
  cv::destroyAllWindows();

  return 0;
}
