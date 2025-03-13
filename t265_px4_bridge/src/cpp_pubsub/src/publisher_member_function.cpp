#include <rclcpp/rclcpp.hpp>
#include <nav_msgs/msg/odometry.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <px4_msgs/msg/vehicle_odometry.hpp>

class OdomBridge : public rclcpp::Node
{
public:
  OdomBridge() : Node("t265_to_px4_bridge")
  {
    publisher_ = this->create_publisher<px4_msgs::msg::VehicleOdometry>(
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
    px4_msgs::msg::VehicleOdometry px4_odom;

    // Convert timestamp to PX4 format (microseconds)
    px4_odom.timestamp = static_cast<uint64_t>(msg->header.stamp.sec) * 1000000 + 
                        msg->header.stamp.nanosec / 1000;

    // Position transformation (ENU → NED)
    px4_odom.position[0] = msg->pose.pose.position.x;   // ENU Y to NED X
    px4_odom.position[1] = -msg->pose.pose.position.y;   // ENU X to NED Y
    px4_odom.position[2] = -msg->pose.pose.position.z;  // ENU Z to NED Z Down

    // Orientation transformation
    tf2::Quaternion q_orig, q_rot, q_new;
    tf2::fromMsg(msg->pose.pose.orientation, q_orig);

    // Rotation: 180-degree roll (X) then -90-degree yaw (Z)
    q_rot.setRPY(M_PI, 0.0, -M_PI/2);
    q_new = q_rot * q_orig;
    q_new.normalize();
    px4_odom.q[0] = q_orig.x();
    px4_odom.q[1] = q_orig.y();
    px4_odom.q[2] = -q_orig.z();
    px4_odom.q[3] = -q_orig.w();

    // Frame specifications (using PX4 constants)
    px4_odom.pose_frame = px4_msgs::msg::VehicleOdometry::POSE_FRAME_NED;
    px4_odom.velocity_frame = px4_msgs::msg::VehicleOdometry::VELOCITY_FRAME_NED;

    // Position covariance (ENU to NED mapping)
    px4_odom.position_variance[0] = msg->pose.covariance[0];  // Y → X
    px4_odom.position_variance[1] = msg->pose.covariance[4];  // X → Y
    px4_odom.position_variance[2] = msg->pose.covariance[5];  // Z variance

    // Orientation covariance
    px4_odom.orientation_variance[0] = msg->pose.covariance[21];  // rotX
    px4_odom.orientation_variance[1] = msg->pose.covariance[28];  // rotY
    px4_odom.orientation_variance[2] = msg->pose.covariance[35];  // rotZ

    // Velocity transformation (ENU → NED)
    px4_odom.velocity[0] = msg->twist.twist.linear.x;   // ENU Y to NED X
    px4_odom.velocity[1] = -msg->twist.twist.linear.y;   // ENU X to NED Y
    px4_odom.velocity[2] = -msg->twist.twist.linear.z;  // ENU Z to NED Z Down

    // Velocity covariance
    px4_odom.velocity_variance[0] = msg->twist.covariance[0];  // Y → X
    px4_odom.velocity_variance[1] = msg->twist.covariance[4];  // X → Y
    px4_odom.velocity_variance[2] = msg->twist.covariance[5];  // Z variance

    px4_odom.quality = 90;
    publisher_->publish(px4_odom);
  }

  rclcpp::Publisher<px4_msgs::msg::VehicleOdometry>::SharedPtr publisher_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr subscription_;
};

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<OdomBridge>());
  rclcpp::shutdown();
  return 0;
}