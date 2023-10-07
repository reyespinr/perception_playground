cmake_minimum_required(VERSION 3.10)
project(PerceptionPlayground)

# Add C++11 support
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED TRUE)

# Find required packages
find_package(realsense2 REQUIRED)
find_package(OpenCV REQUIRED)

# Set the include directories
include_directories(
    ${realsense2_INCLUDE_DIR}
    ${OpenCV_INCLUDE_DIRS}

    # Add other include directories if needed
)

# Macro to easily add executables for different tests
macro(add_camera_test test_name)
    add_executable(${test_name} test_cameras/cpp/${test_name}.cpp)
    target_link_libraries(${test_name}
        ${realsense2_LIBRARY}
        ${OpenCV_LIBS}

        # Add other required libraries here
    )
endmacro()

# Add the executables
add_camera_test(t265_demo)
add_camera_test(check_version)

# Add other tests using the macro as you create them
