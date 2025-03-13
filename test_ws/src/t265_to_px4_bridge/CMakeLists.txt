cmake_minimum_required(VERSION 3.8)
project(t265_to_px4_bridge)

# Set C++ standard
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)

# Add compiler flags
add_compile_options(-Wall -Wextra -Wpedantic)

# Create executable
add_executable(t265_to_px4_bridge
  src/t265_to_px4_bridge.cpp
)

# Specify include directories if necessary
# target_include_directories(t265_to_px4_bridge PRIVATE include)

# Link against required libraries and specify dependencies
ament_target_dependencies(t265_to_px4_bridge
  rclcpp
  nav_msgs
  tf2
  tf2_geometry_msgs
)

target_link_libraries(t265_to_px4_bridge
  rclcpp::rclcpp
  tf2::tf2
  tf2_geometry_msgs::tf2_geometry_msgs
)

# Install executable
install(TARGETS t265_to_px4_bridge
  DESTINATION lib/${PROJECT_NAME}
)

# Export package dependencies for downstream packages
ament_export_dependencies(rclcpp nav_msgs tf2 tf2_geometry_msgs)

ament_package()
