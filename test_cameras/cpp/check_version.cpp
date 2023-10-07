#include <iostream>
#include <librealsense2/rs.hpp>

int main()
{
  std::cout << "RealSense Version: " << RS2_API_VERSION_STR << std::endl;
  return 0;
}
