# from re import M
# import numpy as np

# import rclpy
# from rclpy.node import Node
# from rclpy.clock import Clock
# from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

# from px4_msgs.msg import VehicleAttitude
# from px4_msgs.msg import VehicleOdometry
# from px4_msgs.msg import TrajectorySetpoint
# from geometry_msgs.msg import PoseStamped, Point
# from nav_msgs.msg import Path
# from visualization_msgs.msg import Marker

# def vector2PoseMsg(frame_id, position, attitude):
#     pose_msg = PoseStamped()
#     pose_msg.header.stamp = Clock().now().to_msg()
#     pose_msg.header.frame_id = frame_id
#     pose_msg.pose.orientation.w = attitude[0]
#     pose_msg.pose.orientation.x = attitude[1]
#     pose_msg.pose.orientation.y = attitude[2]
#     pose_msg.pose.orientation.z = attitude[3]
#     pose_msg.pose.position.x = position[0]
#     pose_msg.pose.position.y = position[1]
#     pose_msg.pose.position.z = position[2]
#     return pose_msg

# class PX4Visualizer(Node):
#     def __init__(self):
#         super().__init__("visualizer")

#         qos_profile = QoSProfile(
#             reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
#             history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
#             depth=1,
#         )

#         self.attitude_sub = self.create_subscription(
#             VehicleAttitude,
#             "/fmu/out/vehicle_attitude",
#             self.vehicle_attitude_callback,
#             qos_profile,
#         )
#         self.odom_sub = self.create_subscription(
#             VehicleOdometry,
#             "/fmu/out/vehicle_odometry",
#             self.vehicle_odometry_callback,
#             qos_profile,
#         )
#         self.setpoint_sub = self.create_subscription(
#             TrajectorySetpoint,
#             "/fmu/in/trajectory_setpoint",
#             self.trajectory_setpoint_callback,
#             qos_profile,
#         )

#         self.vehicle_pose_pub = self.create_publisher(
#             PoseStamped, "/px4_visualizer/vehicle_pose", 10
#         )
#         self.vehicle_vel_pub = self.create_publisher(
#             Marker, "/px4_visualizer/vehicle_velocity", 10
#         )
#         self.vehicle_path_pub = self.create_publisher(
#             Path, "/px4_visualizer/vehicle_path", 10
#         )
#         self.setpoint_path_pub = self.create_publisher(
#             Path, "/px4_visualizer/setpoint_path", 10
#         )

#         self.vehicle_attitude = np.array([1.0, 0.0, 0.0, 0.0])
#         self.vehicle_local_position = np.array([0.0, 0.0, 0.0])
#         self.vehicle_local_velocity = np.array([0.0, 0.0, 0.0])
#         self.setpoint_position = np.array([0.0, 0.0, 0.0])
#         self.vehicle_path_msg = Path()
#         self.setpoint_path_msg = Path()

#         self.trail_size = 1000
#         self.last_local_pos_update = 0.0
#         self.declare_parameter("path_clearing_timeout", -1.0)

#         timer_period = 0.02
#         self.timer = self.create_timer(timer_period, self.cmdloop_callback)

#     def vehicle_attitude_callback(self, msg):
#         self.vehicle_attitude[0] = msg.q[0]
#         self.vehicle_attitude[1] = msg.q[1]
#         self.vehicle_attitude[2] = -msg.q[2]
#         self.vehicle_attitude[3] = -msg.q[3]

#     def vehicle_odometry_callback(self, msg):
#         path_clearing_timeout = (
#             self.get_parameter("path_clearing_timeout")
#             .get_parameter_value()
#             .double_value
#         )
#         if path_clearing_timeout >= 0 and (
#             (Clock().now().nanoseconds / 1e9 - self.last_local_pos_update)
#             > path_clearing_timeout
#         ):
#             self.vehicle_path_msg.poses.clear()
#         self.last_local_pos_update = Clock().now().nanoseconds / 1e9

#         self.vehicle_local_position = np.array([msg.y, msg.x, -msg.z])
#         self.vehicle_local_velocity = np.array([msg.vy, msg.vx, -msg.vz])

#     def trajectory_setpoint_callback(self, msg):
#         self.setpoint_position = np.array([msg.position[1], msg.position[0], -msg.position[2]])

#     def create_arrow_marker(self, id, tail, vector):
#         msg = Marker()
#         msg.action = Marker.ADD
#         msg.header.frame_id = "map"
#         # msg.header.stamp = Clock().now().nanoseconds / 1000
#         msg.ns = "arrow"
#         msg.id = id
#         msg.type = Marker.ARROW
#         msg.scale.x = 0.1
#         msg.scale.y = 0.2
#         msg.scale.z = 0.0
#         msg.color.r = 0.5
#         msg.color.g = 0.5
#         msg.color.b = 0.0
#         msg.color.a = 1.0
#         dt = 0.3
#         tail_point = Point()
#         tail_point.x = tail[0]
#         tail_point.y = tail[1]
#         tail_point.z = tail[2]
#         head_point = Point()
#         head_point.x = tail[0] + dt * vector[0]
#         head_point.y = tail[1] + dt * vector[1]
#         head_point.z = tail[2] + dt * vector[2]
#         msg.points = [tail_point, head_point]
#         return msg

#     def append_vehicle_path(self, msg):
#         self.vehicle_path_msg.poses.append(msg)
#         if len(self.vehicle_path_msg.poses) > self.trail_size:
#             del self.vehicle_path_msg.poses[0]

#     def append_setpoint_path(self, msg):
#         self.setpoint_path_msg.poses.append(msg)
#         if len(self.setpoint_path_msg.poses) > self.trail_size:
#             del self.setpoint_path_msg.poses[0]


#     def cmdloop_callback(self):
#         vehicle_pose_msg = vector2PoseMsg("map", self.vehicle_local_position, self.vehicle_attitude)
#         self.vehicle_pose_pub.publish(vehicle_pose_msg)

#         self.vehicle_path_msg.header = vehicle_pose_msg.header
#         self.vehicle_path_msg.poses.append(vehicle_pose_msg)
#         if len(self.vehicle_path_msg.poses) > self.trail_size:
#             del self.vehicle_path_msg.poses[0]
#         self.vehicle_path_pub.publish(self.vehicle_path_msg)

#         setpoint_pose_msg = vector2PoseMsg("map", self.setpoint_position, self.vehicle_attitude)
#         self.setpoint_path_msg.header = setpoint_pose_msg.header
#         self.setpoint_path_msg.poses.append(setpoint_pose_msg)
#         if len(self.setpoint_path_msg.poses) > self.trail_size:
#             del self.setpoint_path_msg.poses[0]
#         self.setpoint_path_pub.publish(self.setpoint_path_msg)

# def main(args=None):
#     rclpy.init(args=args)
#     px4_visualizer = PX4Visualizer()
#     rclpy.spin(px4_visualizer)
#     px4_visualizer.destroy_node()
#     rclpy.shutdown()

# if __name__ == "__main__":
#     main()




#########################################################################################################################################################################





from re import M
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.clock import Clock
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from px4_msgs.msg import VehicleAttitude
from px4_msgs.msg import VehicleLocalPosition
from px4_msgs.msg import TrajectorySetpoint
from geometry_msgs.msg import PoseStamped, Point
from nav_msgs.msg import Path
from visualization_msgs.msg import Marker

def vector2PoseMsg(frame_id, position, attitude):
    pose_msg = PoseStamped()
    pose_msg.header.stamp = Clock().now().to_msg()
    pose_msg.header.frame_id = frame_id
    pose_msg.pose.orientation.w = attitude[0]
    pose_msg.pose.orientation.x = attitude[1]
    pose_msg.pose.orientation.y = attitude[2]
    pose_msg.pose.orientation.z = attitude[3]
    pose_msg.pose.position.x = position[0]
    pose_msg.pose.position.y = position[1]
    pose_msg.pose.position.z = position[2]
    return pose_msg

class PX4Visualizer(Node):
    def __init__(self):
        super().__init__("visualizer")

        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1,
        )

        self.attitude_sub = self.create_subscription(
            VehicleAttitude,
            "/fmu/out/vehicle_attitude",
            self.vehicle_attitude_callback,
            qos_profile,
        )
        self.odom_sub = self.create_subscription(
            VehicleLocalPosition,
            "/fmu/out/vehicle_local_position",
            self.vehicle_local_position_callback,
            qos_profile,
        )
        self.setpoint_sub = self.create_subscription(
            TrajectorySetpoint,
            "/fmu/in/trajectory_setpoint",
            self.trajectory_setpoint_callback,
            qos_profile,
        )

        self.vehicle_pose_pub = self.create_publisher(
            PoseStamped, "/px4_visualizer/vehicle_pose", 10
        )
        self.vehicle_vel_pub = self.create_publisher(
            Marker, "/px4_visualizer/vehicle_velocity", 10
        )
        self.vehicle_path_pub = self.create_publisher(
            Path, "/px4_visualizer/vehicle_path", 10
        )
        self.setpoint_path_pub = self.create_publisher(
            Path, "/px4_visualizer/setpoint_path", 10
        )

        self.vehicle_attitude = np.array([1.0, 0.0, 0.0, 0.0])
        self.vehicle_local_position = np.array([0.0, 0.0, 0.0])
        self.vehicle_local_velocity = np.array([0.0, 0.0, 0.0])
        self.setpoint_position = np.array([0.0, 0.0, 0.0])
        self.vehicle_path_msg = Path()
        self.setpoint_path_msg = Path()

        self.trail_size = 1000
        self.last_local_pos_update = 0.0
        self.declare_parameter("path_clearing_timeout", -1.0)

        timer_period = 0.02
        self.timer = self.create_timer(timer_period, self.cmdloop_callback)

    def vehicle_attitude_callback(self, msg):
        self.vehicle_attitude[0] = msg.q[0]
        self.vehicle_attitude[1] = msg.q[1]
        self.vehicle_attitude[2] = -msg.q[2]
        self.vehicle_attitude[3] = -msg.q[3]

    def vehicle_local_position_callback(self, msg):
        path_clearing_timeout = (
            self.get_parameter("path_clearing_timeout")
            .get_parameter_value()
            .double_value
        )
        if path_clearing_timeout >= 0 and (
            (Clock().now().nanoseconds / 1e9 - self.last_local_pos_update)
            > path_clearing_timeout
        ):
            self.vehicle_path_msg.poses.clear()
        self.last_local_pos_update = Clock().now().nanoseconds / 1e9

        self.vehicle_local_position = np.array([msg.y, msg.x, -msg.z])
        self.vehicle_local_velocity = np.array([msg.vy, msg.vx, -msg.vz])

    def trajectory_setpoint_callback(self, msg):
        self.setpoint_position = np.array([msg.position[1], msg.position[0], -msg.position[2]])

    def create_arrow_marker(self, id, tail, vector):
        msg = Marker()
        msg.action = Marker.ADD
        msg.header.frame_id = "map"
        # msg.header.stamp = Clock().now().nanoseconds / 1000
        msg.ns = "arrow"
        msg.id = id
        msg.type = Marker.ARROW
        msg.scale.x = 0.1
        msg.scale.y = 0.2
        msg.scale.z = 0.0
        msg.color.r = 0.5
        msg.color.g = 0.5
        msg.color.b = 0.0
        msg.color.a = 1.0
        dt = 0.3
        tail_point = Point()
        tail_point.x = tail[0]
        tail_point.y = tail[1]
        tail_point.z = tail[2]
        head_point = Point()
        head_point.x = tail[0] + dt * vector[0]
        head_point.y = tail[1] + dt * vector[1]
        head_point.z = tail[2] + dt * vector[2]
        msg.points = [tail_point, head_point]
        return msg

    def append_vehicle_path(self, msg):
        self.vehicle_path_msg.poses.append(msg)
        if len(self.vehicle_path_msg.poses) > self.trail_size:
            del self.vehicle_path_msg.poses[0]

    def append_setpoint_path(self, msg):
        self.setpoint_path_msg.poses.append(msg)
        if len(self.setpoint_path_msg.poses) > self.trail_size:
            del self.setpoint_path_msg.poses[0]


    def cmdloop_callback(self):
        vehicle_pose_msg = vector2PoseMsg("map", self.vehicle_local_position, self.vehicle_attitude)
        self.vehicle_pose_pub.publish(vehicle_pose_msg)

        self.vehicle_path_msg.header = vehicle_pose_msg.header
        self.vehicle_path_msg.poses.append(vehicle_pose_msg)
        if len(self.vehicle_path_msg.poses) > self.trail_size:
            del self.vehicle_path_msg.poses[0]
        self.vehicle_path_pub.publish(self.vehicle_path_msg)

        setpoint_pose_msg = vector2PoseMsg("map", self.setpoint_position, self.vehicle_attitude)
        self.setpoint_path_msg.header = setpoint_pose_msg.header
        self.setpoint_path_msg.poses.append(setpoint_pose_msg)
        if len(self.setpoint_path_msg.poses) > self.trail_size:
            del self.setpoint_path_msg.poses[0]
        self.setpoint_path_pub.publish(self.setpoint_path_msg)

def main(args=None):
    rclpy.init(args=args)
    px4_visualizer = PX4Visualizer()
    rclpy.spin(px4_visualizer)
    px4_visualizer.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
