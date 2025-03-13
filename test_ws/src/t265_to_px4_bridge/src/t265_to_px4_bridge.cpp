#include <rclcpp/rclcpp.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

class OdomBridge : public rclcpp::Node
{
public:
  OdomBridge() : Node("t265_to_px4_bridge")
  {
    publisher_ = this->create_publisher<nav_msgs::msg::Odometry>(
      "/fmu/in/vehicle_visual_odometry", 
      10
    );

    subscription_ = this->create_subscription<nav_msgs::msg::Odometry>(
      "/camera/odom/sample", 
      10,
      std::bind(&OdomBridge::odomCallback, this, std::placeholders::_1)
    );
  }

private:
  void odomCallback(const nav_msgs::msg::Odometry::SharedPtr msg)
  {
    // Create modified message
    nav_msgs::msg::Odometry px4_odom = *msg;

    // Position transformation (ENU/FLU → NED)
    const double x_orig = msg->pose.pose.position.x;
    const double y_orig = msg->pose.pose.position.y;
    const double z_orig = msg->pose.pose.position.z;
    
    px4_odom.pose.pose.position.x = y_orig;  // East → North
    px4_odom.pose.pose.position.y = x_orig;  // North → East
    px4_odom.pose.pose.position.z = -z_orig; // Up → Down

    // Orientation transformation
    tf2::Quaternion q_orig, q_rot, q_new;
    tf2::fromMsg(msg->pose.pose.orientation, q_orig);

    // Rotation: FLU (camera frame) to NED (PX4 frame)
    // 90-degree rotation around Z (PI/2) then 180 around X (PI)
    q_rot.setRPY(M_PI, 0.0, M_PI/2);
    q_new = q_rot * q_orig;
    q_new.normalize();
    px4_odom.pose.pose.orientation = tf2::toMsg(q_new);

    // Covariance transformation (6x6 matrix, XYZRPY order)
    // Position covariance
    px4_odom.pose.covariance[0] = msg->pose.covariance[4];   // Y → X
    px4_odom.pose.covariance[1] = msg->pose.covariance[3];   // XY → YX
    px4_odom.pose.covariance[4] = msg->pose.covariance[0];   // X → Y
    px4_odom.pose.covariance[5] = -msg->pose.covariance[5];  // Z → -Z

    // Orientation covariance
    px4_odom.pose.covariance[21] = msg->pose.covariance[21];  // Rot X
    px4_odom.pose.covariance[28] = msg->pose.covariance[28];  // Rot Y
    px4_odom.pose.covariance[35] = msg->pose.covariance[35];  // Rot Z

    // Frame ID updates
    px4_odom.header.frame_id = "odom_ned";
    px4_odom.child_frame_id = "base_link_ned";

    // Publish transformed odometry
    publisher_->publish(px4_odom);
  }

  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr publisher_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<OdomBridge>());
  rclcpp::shutdown();
  return 0;
}