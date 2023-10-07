#include <librealsense2/rs.hpp>
#include <opencv2/opencv.hpp>

int main()
{
  // Setup D435
  rs2::pipeline d435_pipeline;
  rs2::config d435_config;
  d435_config.enable_device("018322070175");
  d435_config.enable_stream(RS2_STREAM_COLOR, 640, 480, RS2_FORMAT_BGR8, 30);
  d435_config.enable_stream(RS2_STREAM_DEPTH, 640, 480, RS2_FORMAT_Z16, 30);
  d435_pipeline.start(d435_config);

  // Setup T265
  rs2::pipeline t265_pipeline;
  rs2::config t265_config;
  t265_config.enable_device("224622112228");
  t265_config.enable_stream(RS2_STREAM_FISHEYE, 1, 848, 800, RS2_FORMAT_Y8, 30);
  t265_config.enable_stream(RS2_STREAM_FISHEYE, 2, 848, 800, RS2_FORMAT_Y8, 30);
  t265_pipeline.start(t265_config);

  const auto window_name_d435_color = "Color Feed";
  const auto window_name_d435_depth = "Depth Feed";
  const auto window_name_t265_fisheye1 = "Fisheye1 Feed";
  const auto window_name_t265_fisheye2 = "Fisheye2 Feed";
  cv::namedWindow(window_name_d435_color, cv::WINDOW_AUTOSIZE);
  cv::namedWindow(window_name_d435_depth, cv::WINDOW_AUTOSIZE);
  cv::namedWindow(window_name_t265_fisheye1, cv::WINDOW_AUTOSIZE);
  cv::namedWindow(window_name_t265_fisheye2, cv::WINDOW_AUTOSIZE);

  while (true) {
    rs2::frameset d435_frames = d435_pipeline.wait_for_frames();
    rs2::frame color_frame = d435_frames.get_color_frame();
    rs2::frame depth_frame = d435_frames.get_depth_frame();

    rs2::frameset t265_frames = t265_pipeline.wait_for_frames();
    rs2::frame fisheye1_frame = t265_frames.get_fisheye_frame(1);
    rs2::frame fisheye2_frame = t265_frames.get_fisheye_frame(2);

    cv::Mat color_img(
      cv::Size(640, 480), CV_8UC3, (void *)color_frame.get_data(), cv::Mat::AUTO_STEP);
    cv::Mat depth_img(
      cv::Size(640, 480), CV_16U, (void *)depth_frame.get_data(), cv::Mat::AUTO_STEP);
    cv::Mat depth_colormap;
    cv::Mat depth_abs;
    cv::convertScaleAbs(depth_img, depth_abs, 0.03f);
    cv::applyColorMap(depth_abs, depth_colormap, cv::COLORMAP_JET);

    cv::Mat fisheye1_img(
      cv::Size(848, 800), CV_8UC1, (void *)fisheye1_frame.get_data(), cv::Mat::AUTO_STEP);
    cv::Mat fisheye2_img(
      cv::Size(848, 800), CV_8UC1, (void *)fisheye2_frame.get_data(), cv::Mat::AUTO_STEP);

    cv::imshow(window_name_d435_color, color_img);
    cv::imshow(window_name_d435_depth, depth_colormap);
    cv::imshow(window_name_t265_fisheye1, fisheye1_img);
    cv::imshow(window_name_t265_fisheye2, fisheye2_img);

    if (cv::waitKey(1) == 27) {  // 'esc' key
      break;
    }
  }

  d435_pipeline.stop();
  t265_pipeline.stop();
  cv::destroyAllWindows();
  return 0;
}
