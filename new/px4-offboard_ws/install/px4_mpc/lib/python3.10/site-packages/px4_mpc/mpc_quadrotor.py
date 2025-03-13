# # #!/usr/bin/env python
# # from px4_mpc.models.multirotor_rate_model import MultirotorRateModel
# # from px4_mpc.controllers.multirotor_rate_mpc import MultirotorRateMPC

# # __author__ = "Jaeyoung Lim"
# # __contact__ = "jalim@ethz.ch"

# # import rclpy
# # import numpy as np
# # from rclpy.node import Node
# # from rclpy.clock import Clock
# # from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy

# # from nav_msgs.msg import Path
# # from geometry_msgs.msg import PoseStamped
# # from visualization_msgs.msg import Marker

# # from px4_msgs.msg import OffboardControlMode
# # from px4_msgs.msg import VehicleStatus
# # from px4_msgs.msg import VehicleAttitude
# # from px4_msgs.msg import VehicleOdometry
# # from px4_msgs.msg import VehicleRatesSetpoint

# # from mpc_msgs.srv import SetPose

# # def vector2PoseMsg(frame_id, position, attitude):
# #     pose_msg = PoseStamped()
# #     # msg.header.stamp = Clock().now().nanoseconds / 1000
# #     pose_msg.header.frame_id=frame_id
# #     pose_msg.pose.orientation.w = attitude[0]
# #     pose_msg.pose.orientation.x = attitude[1]
# #     pose_msg.pose.orientation.y = attitude[2]
# #     pose_msg.pose.orientation.z = attitude[3]
# #     pose_msg.pose.position.x = float(position[0])
# #     pose_msg.pose.position.y = float(position[1])
# #     pose_msg.pose.position.z = float(position[2])
# #     return pose_msg

# # class QuadrotorMPC(Node):

# #     def __init__(self):
# #         super().__init__('minimal_publisher')
# #         qos_profile = QoSProfile(
# #             reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
# #             durability=QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL,
# #             history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
# #             depth=1
# #         )

# #         self.status_sub = self.create_subscription(
# #             VehicleStatus,
# #             '/fmu/out/vehicle_status',
# #             self.vehicle_status_callback,
# #             qos_profile)

# #         self.attitude_sub = self.create_subscription(
# #             VehicleAttitude,
# #             '/fmu/out/vehicle_attitude',
# #             self.vehicle_attitude_callback,
# #             qos_profile)

# #         self.odometry_sub = self.create_subscription(
# #             VehicleOdometry,
# #             '/fmu/out/vehicle_odometry',
# #             self.vehicle_odometry_callback,
# #             qos_profile)

# #         self.set_pose_srv = self.create_service(SetPose, '/set_pose', self.add_set_pos_callback)

# #         self.publisher_offboard_mode = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
# #         self.publisher_rates_setpoint = self.create_publisher(VehicleRatesSetpoint, '/fmu/in/vehicle_rates_setpoint', qos_profile)
# #         self.predicted_path_pub = self.create_publisher(Path, '/px4_mpc/predicted_path', 10)
# #         self.reference_pub = self.create_publisher(Marker, "/px4_mpc/reference", 10)

# #         timer_period = 0.02  # seconds
# #         self.timer = self.create_timer(timer_period, self.cmdloop_callback)

# #         self.nav_state = VehicleStatus.NAVIGATION_STATE_MAX

# #         # Create Quadrotor and controller objects
# #         self.model = MultirotorRateModel()

# #         # Create MPC Solver
# #         MPC_HORIZON = 15

# #         # Spawn Controller
# #         self.mpc = MultirotorRateMPC(self.model)

# #         self.vehicle_attitude = np.array([1.0, 0.0, 0.0, 0.0])
# #         self.vehicle_local_position = np.array([0.0, 0.0, 0.0])
# #         self.vehicle_local_velocity = np.array([0.0, 0.0, 0.0])
# #         self.setpoint_position = np.array([5.0, 4.0, 3.0])

# #     def vehicle_attitude_callback(self, msg):
# #         # TODO: handle NED->ENU transformation 
# #         self.vehicle_attitude[0] = msg.q[0]
# #         self.vehicle_attitude[1] = msg.q[1]
# #         self.vehicle_attitude[2] = -msg.q[2]
# #         self.vehicle_attitude[3] = -msg.q[3]

# #     def vehicle_odometry_callback(self, msg):
# #         # TODO: handle NED->ENU transformation 
# #         self.vehicle_local_position[0] = msg.position[0]
# #         self.vehicle_local_position[1] = -msg.position[1]
# #         self.vehicle_local_position[2] = -msg.position[2]
# #         self.vehicle_local_velocity[0] = msg.velocity[0]
# #         self.vehicle_local_velocity[1] = -msg.velocity[1]
# #         self.vehicle_local_velocity[2] = -msg.velocity[2]

# #     def vehicle_status_callback(self, msg):
# #         self.nav_state = msg.nav_state
    
# #     def publish_reference(self, pub, reference):
# #         msg = Marker()
# #         msg.action = Marker.ADD
# #         msg.header.frame_id = "map"
# #         msg.ns = "arrow"
# #         msg.id = 1
# #         msg.type = Marker.SPHERE
# #         msg.scale.x = 0.5
# #         msg.scale.y = 0.5
# #         msg.scale.z = 0.5
# #         msg.color.r = 1.0
# #         msg.color.g = 0.0
# #         msg.color.b = 0.0
# #         msg.color.a = 1.0
# #         msg.pose.position.x = reference[0]
# #         msg.pose.position.y = reference[1]
# #         msg.pose.position.z = reference[2]
# #         msg.pose.orientation.w = 1.0
# #         msg.pose.orientation.x = 0.0
# #         msg.pose.orientation.y = 0.0
# #         msg.pose.orientation.z = 0.0

# #         pub.publish(msg)

# #     def cmdloop_callback(self):
# #         # Publish offboard control modes
# #         offboard_msg = OffboardControlMode()
# #         offboard_msg.timestamp = int(Clock().now().nanoseconds / 1000)
# #         offboard_msg.position=False
# #         offboard_msg.velocity=False
# #         offboard_msg.acceleration=False
# #         offboard_msg.attitude = False
# #         offboard_msg.body_rate = True
# #         self.publisher_offboard_mode.publish(offboard_msg)

# #         error_position = self.vehicle_local_position - self.setpoint_position
        
# #         print(f"&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&ERROR {error_position}")
# #         x0 = np.array([error_position[0], error_position[1], error_position[2],
# #          self.vehicle_local_velocity[0], self.vehicle_local_velocity[1], self.vehicle_local_velocity[2], 
# #          self.vehicle_attitude[0], self.vehicle_attitude[1], self.vehicle_attitude[2], self.vehicle_attitude[3]]).reshape(10, 1)

# #         u_pred, x_pred = self.mpc.solve(x0)
# #         print(f"U_pred: {u_pred} \n X_pred: {x_pred}")
# #         idx = 0
# #         predicted_path_msg = Path()
# #         for predicted_state in x_pred:
# #             idx = idx + 1
# #             # Publish time history of the vehicle path
# #             predicted_pose_msg = vector2PoseMsg('map', predicted_state[0:3] + self.setpoint_position, np.array([1.0, 0.0, 0.0, 0.0]))
# #             predicted_path_msg.header = predicted_pose_msg.header
# #             predicted_path_msg.poses.append(predicted_pose_msg)
# #         self.predicted_path_pub.publish(predicted_path_msg)
# #         self.publish_reference(self.reference_pub, self.setpoint_position)

# #         thrust_rates = u_pred[0, :]
# #         # Hover thrust = 0.73
# #         thrust_command = -(thrust_rates[0] * 0.07 + 0.0)
# #         if self.nav_state == VehicleStatus.NAVIGATION_STATE_OFFBOARD:
# #             setpoint_msg = VehicleRatesSetpoint()
# #             setpoint_msg.timestamp = int(Clock().now().nanoseconds / 1000)
# #             setpoint_msg.roll = float(thrust_rates[1])
# #             setpoint_msg.pitch = float(-thrust_rates[2])
# #             setpoint_msg.yaw = float(-thrust_rates[3])
# #             setpoint_msg.thrust_body[0] = 0.0
# #             setpoint_msg.thrust_body[1] = 0.0
# #             setpoint_msg.thrust_body[2] = float(thrust_command)
# #             self.publisher_rates_setpoint.publish(setpoint_msg)

# #     def add_set_pos_callback(self, request, response):
# #         self.setpoint_position[0] = 5
# #         self.setpoint_position[1] = 4
# #         self.setpoint_position[2] = request.pose.position.z
# #         print(f"SETPOINT: {self.setpoint_position}")
# #         return response

# # def main(args=None):
# #     rclpy.init(args=args)

# #     quadrotor_mpc = QuadrotorMPC()

# #     rclpy.spin(quadrotor_mpc)

# #     quadrotor_mpc.destroy_node()
# #     rclpy.shutdown()


# # if __name__ == '__main__':
# #     main()
# # ######################################### test code ##################################
# # # #!/usr/bin/env python
# # # import numpy as np
# # # import matplotlib.pyplot as plt
# # # from mpl_toolkits.mplot3d import Axes3D
# # # from px4_mpc.models.multirotor_rate_model import MultirotorRateModel
# # # from px4_mpc.controllers.multirotor_rate_mpc import MultirotorRateMPC

# # # def main():
# # #     # Define the quadrotor model
# # #     model = MultirotorRateModel()

# # #     # Define MPC parameters
# # #     MPC_HORIZON = 15  # MPC prediction horizon

# # #     # Initialize the MPC solver
# # #     mpc = MultirotorRateMPC(model)

# # #     # Initial state [x, y, z, vx, vy, vz, qw, qx, qy, qz]
# # #     x0 = np.array([0.0, 0.0, 0.0,  # Position
# # #                    0.0, 0.0, 0.0,  # Velocity
# # #                    0.6470338106155396, 0.004636550787836313, 
# # #                    -0.008497882634401321, 0.7623999118804932])  # Attitude (quaternion)

# # #     # Desired setpoint position (goal)
# # #     setpoint_position = np.array([0.0, 0.0, 3.0])

# # #     # Compute error between current position and setpoint
# # #     error_position = x0[:3] - setpoint_position

# # #     # Update the initial state with the error
# # #     x0[:3] = error_position

# # #     # Solve the MPC problem
# # #     u_pred, x_pred = mpc.solve(x0.reshape(10, 1))

# # #     # Extract the predicted states for visualization
# # #     predicted_positions = x_pred[:, :3] + setpoint_position  # Add setpoint to get absolute positions

# # #     # Print the results
# # #     print("Predicted Control Inputs (U_pred):")
# # #     print(u_pred)
# # #     print("\nPredicted States (X_pred):")
# # #     print(x_pred)

# # #     # Visualize the predicted path, start, and goal
# # #     visualize_path(predicted_positions, x0[:3], setpoint_position)

# # # def visualize_path(predicted_positions, start_position, goal_position):
# # #     """
# # #     Visualize the predicted path, start position, and goal position in 3D.
# # #     """
# # #     fig = plt.figure()
# # #     ax = fig.add_subplot(111, projection='3d')

# # #     # Plot the predicted path
# # #     ax.plot(predicted_positions[:, 0], predicted_positions[:, 1], predicted_positions[:, 2],
# # #             label="Predicted Path", color="blue", marker="o")

# # #     # Plot the start position
# # #     ax.scatter(start_position[0], start_position[1], start_position[2],
# # #                label="Start Position", color="green", s=100, marker="o")

# # #     # Plot the goal position (setpoint)
# # #     ax.scatter(goal_position[0], goal_position[1], goal_position[2],
# # #                label="Goal Position", color="red", s=100, marker="x")

# # #     # Set axis labels
# # #     ax.set_xlabel("X (m)")
# # #     ax.set_ylabel("Y (m)")
# # #     ax.set_zlabel("Z (m)")

# # #     # Set title
# # #     ax.set_title("MPC Predicted Path with Start and Goal")

# # #     # Add legend
# # #     ax.legend()

# # #     # Show the plot
# # #     plt.show()

# # # if __name__ == '__main__':
# # #     main()





# ####################################################################################



# #!/usr/bin/env python
# from px4_mpc.models.multirotor_rate_model import MultirotorRateModel
# from px4_mpc.controllers.multirotor_rate_mpc import MultirotorRateMPC

# __author__ = "Jaeyoung Lim"
# __contact__ = "jalim@ethz.ch"

# import rclpy
# import numpy as np
# from rclpy.node import Node
# from rclpy.clock import Clock
# from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy

# from nav_msgs.msg import Path
# from geometry_msgs.msg import PoseStamped
# from visualization_msgs.msg import Marker

# from px4_msgs.msg import OffboardControlMode
# from px4_msgs.msg import VehicleStatus
# from px4_msgs.msg import VehicleAttitude
# from px4_msgs.msg import VehicleOdometry
# from px4_msgs.msg import VehicleRatesSetpoint

# from mpc_msgs.srv import SetPose

# def vector2PoseMsg(frame_id, position, attitude):
#     pose_msg = PoseStamped()
#     pose_msg.header.frame_id = frame_id
#     pose_msg.pose.orientation.w = attitude[0]
#     pose_msg.pose.orientation.x = attitude[1]
#     pose_msg.pose.orientation.y = attitude[2]
#     pose_msg.pose.orientation.z = attitude[3]
#     pose_msg.pose.position.x = float(position[0])
#     pose_msg.pose.position.y = float(position[1])
#     pose_msg.pose.position.z = float(position[2])
#     return pose_msg

# class QuadrotorMPC(Node):

#     def __init__(self):
#         super().__init__('quadrotor_mpc')
#         qos_profile = QoSProfile(
#             reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
#             durability=QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL,
#             history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
#             depth=1
#         )

#         # Subscribers
#         self.status_sub = self.create_subscription(
#             VehicleStatus,
#             '/fmu/out/vehicle_status',
#             self.vehicle_status_callback,
#             qos_profile)

#         self.attitude_sub = self.create_subscription(
#             VehicleAttitude,
#             '/fmu/out/vehicle_attitude',
#             self.vehicle_attitude_callback,
#             qos_profile)

#         self.odometry_sub = self.create_subscription(
#             VehicleOdometry,
#             '/fmu/out/vehicle_odometry',
#             self.vehicle_odometry_callback,
#             qos_profile)

#         # Service for setting pose
#         self.set_pose_srv = self.create_service(SetPose, '/set_pose', self.add_set_pos_callback)

#         # Publishers
#         self.publisher_offboard_mode = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
#         self.publisher_rates_setpoint = self.create_publisher(VehicleRatesSetpoint, '/fmu/in/vehicle_rates_setpoint', qos_profile)
#         self.predicted_path_pub = self.create_publisher(Path, '/px4_mpc/predicted_path', 10)
#         self.reference_pub = self.create_publisher(Marker, "/px4_mpc/reference", 10)

#         # Timer for control loop
#         timer_period = 0.02  # seconds
#         self.timer = self.create_timer(timer_period, self.cmdloop_callback)

#         # Initialize variables
#         self.nav_state = VehicleStatus.NAVIGATION_STATE_MAX
#         self.vehicle_attitude = np.array([1.0, 0.0, 0.0, 0.0])  # Quaternion [qw, qx, qy, qz]
#         self.vehicle_local_position = np.array([0.0, 0.0, 0.0])  # Position [x, y, z]
#         self.vehicle_local_velocity = np.array([0.0, 0.0, 0.0])  # Velocity [vx, vy, vz]
#         self.setpoint_position = np.array([5.0, 4.0, 3.0])  # Desired setpoint [x, y, z]

#         # Create Quadrotor and controller objects
#         self.model = MultirotorRateModel()
#         MPC_HORIZON = 15  # MPC prediction horizon
#         self.mpc = MultirotorRateMPC(self.model)

#     def vehicle_attitude_callback(self, msg):
#         # Handle NED -> ENU transformation
#         self.vehicle_attitude[0] = msg.q[0]
#         self.vehicle_attitude[1] = msg.q[1]
#         self.vehicle_attitude[2] = -msg.q[2]
#         self.vehicle_attitude[3] = -msg.q[3]

#     def vehicle_odometry_callback(self, msg):
#         # Handle NED -> ENU transformation
#         self.vehicle_local_position[0] = msg.position[0]
#         self.vehicle_local_position[1] = -msg.position[1]
#         self.vehicle_local_position[2] = -msg.position[2]
#         self.vehicle_local_velocity[0] = msg.velocity[0]
#         self.vehicle_local_velocity[1] = -msg.velocity[1]
#         self.vehicle_local_velocity[2] = -msg.velocity[2]

#     def vehicle_status_callback(self, msg):
#         self.nav_state = msg.nav_state

#     def publish_reference(self, pub, reference):
#         msg = Marker()
#         msg.action = Marker.ADD
#         msg.header.frame_id = "map"
#         msg.ns = "arrow"
#         msg.id = 1
#         msg.type = Marker.SPHERE
#         msg.scale.x = 0.5
#         msg.scale.y = 0.5
#         msg.scale.z = 0.5
#         msg.color.r = 1.0
#         msg.color.g = 0.0
#         msg.color.b = 0.0
#         msg.color.a = 1.0
#         msg.pose.position.x = reference[0]
#         msg.pose.position.y = reference[1]
#         msg.pose.position.z = reference[2]
#         msg.pose.orientation.w = 1.0
#         msg.pose.orientation.x = 0.0
#         msg.pose.orientation.y = 0.0
#         msg.pose.orientation.z = 0.0
#         pub.publish(msg)

#     def cmdloop_callback(self):
#         # Publish offboard control modes
#         offboard_msg = OffboardControlMode()
#         offboard_msg.timestamp = int(Clock().now().nanoseconds / 1000)
#         offboard_msg.position = False
#         offboard_msg.velocity = False
#         offboard_msg.acceleration = False
#         offboard_msg.attitude = False
#         offboard_msg.body_rate = True
#         self.publisher_offboard_mode.publish(offboard_msg)

#         # Compute error between current position and setpoint
#         error_position = self.vehicle_local_position - self.setpoint_position

#         print(f"ERROR: {error_position}")
#         x0 = np.array([
#             error_position[0], error_position[1], error_position[2],  # Position error
#             self.vehicle_local_velocity[0], self.vehicle_local_velocity[1], self.vehicle_local_velocity[2],  # Velocity
#             self.vehicle_attitude[0], self.vehicle_attitude[1], self.vehicle_attitude[2], self.vehicle_attitude[3]  # Attitude (quaternion)
#         ])

#         # Define reference trajectory and terminal state
#         pos_ref_traj = [self.setpoint_position for _ in range(self.mpc.N)]  # Constant reference for all stages
#         pos_ref_terminal = self.setpoint_position  # Terminal reference

#         # Solve the MPC problem
#         u_pred, x_pred = self.mpc.solve(x0, pos_ref_traj, pos_ref_terminal)

#         # Publish predicted path
#         predicted_path_msg = Path()
#         for predicted_state in x_pred:
#             predicted_pose_msg = vector2PoseMsg('map', predicted_state[:3] + self.setpoint_position, np.array([1.0, 0.0, 0.0, 0.0]))
#             predicted_path_msg.header = predicted_pose_msg.header
#             predicted_path_msg.poses.append(predicted_pose_msg)
#         self.predicted_path_pub.publish(predicted_path_msg)

#         # Publish reference marker
#         self.publish_reference(self.reference_pub, self.setpoint_position)

#         # Extract control inputs
#         thrust_rates = u_pred[0]
#         thrust_command = -(thrust_rates[0] * 0.07 + 0.0)  # Scale thrust command

#         if self.nav_state == VehicleStatus.NAVIGATION_STATE_OFFBOARD:
#             setpoint_msg = VehicleRatesSetpoint()
#             setpoint_msg.timestamp = int(Clock().now().nanoseconds / 1000)
#             setpoint_msg.roll = float(thrust_rates[1])
#             setpoint_msg.pitch = float(-thrust_rates[2])
#             setpoint_msg.yaw = float(-thrust_rates[3])
#             setpoint_msg.thrust_body[0] = 0.0
#             setpoint_msg.thrust_body[1] = 0.0
#             setpoint_msg.thrust_body[2] = float(thrust_command)
#             self.publisher_rates_setpoint.publish(setpoint_msg)

#     def add_set_pos_callback(self, request, response):
#         self.setpoint_position[0] = request.pose.position.x
#         self.setpoint_position[1] = request.pose.position.y
#         self.setpoint_position[2] = request.pose.position.z
#         print(f"SETPOINT: {self.setpoint_position}")
#         return response

# def main(args=None):
#     rclpy.init(args=args)
#     quadrotor_mpc = QuadrotorMPC()
#     rclpy.spin(quadrotor_mpc)
#     quadrotor_mpc.destroy_node()
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()

############################################################################################################################################
############################################################################################################################################

#ChatGPT first

# #!/usr/bin/env python
# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from px4_mpc.models.multirotor_rate_model import MultirotorRateModel
# from px4_mpc.controllers.multirotor_rate_mpc import MultirotorRateMPC

# def main():
#     # Define the quadrotor model
#     model = MultirotorRateModel()

#     # Initialize the MPC solver
#     mpc = MultirotorRateMPC(model)

#     # Initial state [x, y, z, vx, vy, vz, qw, qx, qy, qz]
#     x0 = np.array([0.0, 0.0, 0.0,  # Position
#                    0.0, 0.0, 0.0,  # Velocity
#                    0.647, 0.0046, -0.0085, 0.7624])  # Attitude (quaternion)

#     # Define waypoints and terminal position
#     waypoints = np.array([[1.0, 1.0, 1.0],
#                            [2.0, 1.5, 1.5],
#                            [3.0, 2.0, 2.0],
#                            [4.0, 2.5, 2.5]])
#     terminal_position = np.array([5.0, 3.0, 3.0])

#     # Define reference trajectory
#     N = mpc.N
#     pos_ref_traj = np.linspace(x0[:3], terminal_position, N)
#     pos_ref_terminal = terminal_position

#     # Solve the MPC problem
#     u_pred, x_pred = mpc.solve(x0, pos_ref_traj, pos_ref_terminal, verbose=True)

#     # Extract the predicted positions
#     predicted_positions = x_pred[:, :3]
    
#     #Compute errors for each trajectory step
#     errors = (x_pred[1:, :3] - pos_ref_traj).T  # Shape (3, N)

#     for i in range(errors.shape[1]):  # Iterate over N steps
#         print(f"Step {i}: Error = ({errors[0, i]:.4f}, {errors[1, i]:.4f}, {errors[2, i]:.4f}) m")

#     # Visualize the predicted trajectory
#     visualize_path(predicted_positions, x0[:3], terminal_position, waypoints)

# def visualize_path(predicted_positions, start_position, goal_position, waypoints):
#     """
#     Visualize the predicted path, start position, goal position, and waypoints in 3D.
#     """
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     # Plot the predicted path
#     ax.plot(predicted_positions[:, 0], predicted_positions[:, 1], predicted_positions[:, 2],
#             label="Predicted Path", color="blue", marker="o")

#     # Plot the start position
#     ax.scatter(start_position[0], start_position[1], start_position[2],
#                label="Start Position", color="green", s=100, marker="o")

#     # Plot the goal position (setpoint)
#     ax.scatter(goal_position[0], goal_position[1], goal_position[2],
#                label="Goal Position", color="red", s=100, marker="x")

#     # Plot waypoints
#     for wp in waypoints:
#         ax.scatter(wp[0], wp[1], wp[2], label="Waypoint", color="purple", s=80, marker="^")

#     # Set axis labels
#     ax.set_xlabel("X (m)")
#     ax.set_ylabel("Y (m)")
#     ax.set_zlabel("Z (m)")

#     # Set title
#     ax.set_title("MPC Predicted Path with Waypoints")

#     # Add legend
#     ax.legend()

#     # Show the plot
#     plt.show()

# if __name__ == '__main__':
#     main()


############################################################################################################################################
############################################################################################################################################
############################################ MATPLOTLIB - CORRECT ##############################################
# #!/usr/bin/env 
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
# from px4_mpc.models.multirotor_rate_model import MultirotorRateModel
# from px4_mpc.controllers.multirotor_rate_mpc import MultirotorRateMPC
# import numpy as np

# class MultirotorVisualizer:
#     def __init__(self):
#         self.fig = plt.figure()
#         self.ax = self.fig.add_subplot(111, projection='3d')
#         self.ax.set_xlabel('X [m]')
#         self.ax.set_ylabel('Y [m]')
#         self.ax.set_zlabel('Z [m]')
#         self.ax.set_title('Multirotor Trajectory Tracking')

#         # self.ax1 = self.fig.add_subplot(131, projection='3d')  # Actual trajectory
#         # self.ax2 = self.fig.add_subplot(132, projection='3d')  # Reference trajectory
#         # self.ax3 = self.fig.add_subplot(133, projection='3d')  # Both trajectories
#         # self._setup_axes()
    
#     # def _setup_axes(self):
#     #     """Set up common axis labels and titles for all subplots."""
#     #     for ax, title in zip([self.ax1, self.ax2, self.ax3], 
#     #                          ["Actual Trajectory", "Reference Trajectory", "Both Trajectories"]):
#     #         ax.set_xlabel('X [m]')
#     #         ax.set_ylabel('Y [m]')
#     #         ax.set_zlabel('Z [m]')
#     #         ax.set_title(title)

#     def plot_trajectory(self, reference_trajectory, actual_trajectory):
#         """Plot the reference and actual trajectories."""
#         # Plot reference trajectory
#         self.ax.plot(reference_trajectory[:, 0], reference_trajectory[:, 1], reference_trajectory[:, 2],
#                      'r--', label='Reference Trajectory')
        
#         # Plot actual trajectory
#         self.ax.plot(actual_trajectory[:, 0], actual_trajectory[:, 1], actual_trajectory[:, 2],
#                      'b-', label='Actual Trajectory')
        
#         self.ax.scatter(reference_trajectory[0, 0], reference_trajectory[0, 1], reference_trajectory[0, 2],
#                          color='green', marker='*', s=200, label='Start Point')

#         self.ax.scatter(actual_trajectory[0, 0], actual_trajectory[0, 1], actual_trajectory[0, 2],
#                          color='blue', marker='o', s=50, label='Start Point')

#         print(f"ref = {reference_trajectory[0, 0], reference_trajectory[0, 1], reference_trajectory[0, 2]}::::::::::::actual = ={actual_trajectory[0, 0], actual_trajectory[0, 1], actual_trajectory[0, 2]}")
        
#         # Add legend
#         self.ax.legend()

#         # Show plot
#         plt.show()

#     # def plot_trajectory(self, reference_trajectory, actual_trajectory):
#     #     """Plot the reference and actual trajectories in subplots."""
#     #     # Plot actual trajectory (subplot 1)
#     #     self.ax1.plot(actual_trajectory[:, 0], actual_trajectory[:, 1], actual_trajectory[:, 2],
#     #                 'b-', label='Actual Trajectory')
#     #     self.ax1.scatter(actual_trajectory[0, 0], actual_trajectory[0, 1], actual_trajectory[0, 2],
#     #                 color='blue', marker='o', s=50, label='Start Point (Actual)')
#     #     self.ax1.legend()

#     #     # Plot reference trajectory (subplot 2)
#     #     self.ax2.plot(reference_trajectory[:, 0], reference_trajectory[:, 1], reference_trajectory[:, 2],
#     #                 'r--', label='Reference Trajectory')
#     #     self.ax2.scatter(reference_trajectory[0, 0], reference_trajectory[0, 1], reference_trajectory[0, 2],
#     #                 color='green', marker='*', s=200, label='Start Point (Reference)')
#     #     self.ax2.legend()

#     #     # Plot both trajectories (subplot 3)
#     #     self.ax3.plot(reference_trajectory[:, 0], reference_trajectory[:, 1], reference_trajectory[:, 2],
#     #                 'r--', label='Reference Trajectory')
#     #     self.ax3.plot(actual_trajectory[:, 0], actual_trajectory[:, 1], actual_trajectory[:, 2],
#     #                 'b-', label='Actual Trajectory')
#     #     self.ax3.scatter(reference_trajectory[0, 0], reference_trajectory[0, 1], reference_trajectory[0, 2],
#     #                 color='green', marker='*', s=200, label='Start Point (Reference)')
#     #     self.ax3.scatter(actual_trajectory[0, 0], actual_trajectory[0, 1], actual_trajectory[0, 2],
#     #                 color='blue', marker='o', s=50, label='Start Point (Actual)')
#     #     self.ax3.legend()

#     #     # Show plot
#     #     plt.tight_layout()  # Adjust layout to prevent overlap
#     #     plt.show()

# # Example usage
# def main():
#     # Define a reference trajectory function (example: circular trajectory)
#     def reference_trajectory(t):
#         radius = 2.0
        
#         omega = 2 * np.pi / 100
#         #omega = 0  # 10 seconds per full circle
#         x = radius * np.cos(omega * t)
#         y = radius * np.sin(omega * t)
#         z = 1.0  # Constant altitude
#         return np.array([x, y, z])
    
#     # Initialize the MPC and visualizer
#     model = MultirotorRateModel()  # Replace with your model initialization
    
#     initial_position = reference_trajectory(0)  # Evaluate reference trajectory at t = 0
#     x0 = np.array([*initial_position, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])  # Append orientation and velocities
#     mpc = MultirotorRateMPC(model, x0 = x0)
#     #mpc.Tf = 2
#     #mpc.N = 20

#     visualizer = MultirotorVisualizer()

#     # Simulate for a few steps and collect trajectories
#     num_steps = 50
#     reference_trajectory_points = []
#     actual_trajectory_points = []

#     for _ in range(num_steps):
#         # Solve MPC step
#         simU, simX = mpc.solve_step(reference_trajectory)
        
#         # Store reference and actual points
#         t_k = mpc.current_time
#         reference_trajectory_points.append(reference_trajectory(t_k))
#         actual_trajectory_points.append(simX[0, 0:3])  # First 3 states are position

#         reference = reference_trajectory(t_k)
#         actual = simX[0, 0:3]
#         error = reference - actual
#         # print(f"ERROR: {error}")
#         # print(f"ref_traj = {reference}")
        

#     # Convert to numpy arrays
#     reference_trajectory_points = np.array(reference_trajectory_points)
#     actual_trajectory_points = np.array(actual_trajectory_points)
    
#     # Visualize
#     visualizer.plot_trajectory(reference_trajectory_points, actual_trajectory_points)
    

############################################################################################################################################
############################################################################################################################################

#!/usr/bin/env python3
from px4_mpc.models.multirotor_rate_model import MultirotorRateModel
from px4_mpc.controllers.multirotor_rate_mpc import MultirotorRateMPC

import time
import rclpy
import numpy as np
import tf2_ros
import pdb
from rclpy.node import Node
from rclpy.clock import Clock
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy, QoSDurabilityPolicy

from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker
from geometry_msgs.msg import TransformStamped

from px4_msgs.msg import OffboardControlMode
from px4_msgs.msg import VehicleStatus
from px4_msgs.msg import VehicleAttitude
from px4_msgs.msg import VehicleLocalPosition
from px4_msgs.msg import VehicleRatesSetpoint

from px4_msgs.msg import VehicleOdometry

def vector2PoseMsg(frame_id, position, attitude):
    pose_msg = PoseStamped()
    pose_msg.header.frame_id = frame_id
    pose_msg.pose.orientation.w = attitude[0]
    pose_msg.pose.orientation.x = attitude[1]
    pose_msg.pose.orientation.y = attitude[2]
    pose_msg.pose.orientation.z = attitude[3]
    pose_msg.pose.position.x = float(position[0])
    pose_msg.pose.position.y = float(position[1])
    pose_msg.pose.position.z = float(position[2])
    return pose_msg

class QuadrotorMPC(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        qos_profile = QoSProfile(
            reliability=QoSReliabilityPolicy.RMW_QOS_POLICY_RELIABILITY_BEST_EFFORT,
            durability=QoSDurabilityPolicy.RMW_QOS_POLICY_DURABILITY_TRANSIENT_LOCAL,
            history=QoSHistoryPolicy.RMW_QOS_POLICY_HISTORY_KEEP_LAST,
            depth=1
        )

        self.tf_broadcaster = tf2_ros.StaticTransformBroadcaster(self)
        self.publish_map_frame()

        self.status_sub = self.create_subscription(
            VehicleStatus,
            '/fmu/out/vehicle_status',
            self.vehicle_status_callback,
            qos_profile)

        self.attitude_sub = self.create_subscription(
            VehicleAttitude,
            '/fmu/out/vehicle_attitude',
            self.vehicle_attitude_callback,
            qos_profile)

        self.local_position_sub = self.create_subscription(
            VehicleLocalPosition,
            '/fmu/out/vehicle_local_position',
            self.vehicle_local_position_callback,
            qos_profile)

        self.publisher_offboard_mode = self.create_publisher(OffboardControlMode, '/fmu/in/offboard_control_mode', qos_profile)
        self.publisher_rates_setpoint = self.create_publisher(VehicleRatesSetpoint, '/fmu/in/vehicle_rates_setpoint', qos_profile)

        # predicted path
        self.predicted_path_pub = self.create_publisher(Path, '/px4_mpc/predicted_path', 10)

        # reference path
        self.reference_path_pub = self.create_publisher(Path, "/px4_mpc/reference_path", 10)
        self.reference_path_msg = Path()
        self.reference_path_msg.header.frame_id = "map"

        # reference marker
        self.reference_pub = self.create_publisher(Marker, "/px4_mpc/reference", 10)

        timer_period = 0.02  # seconds
        self.timer = self.create_timer(timer_period, self.cmd_callback)

        self.vehicle_attitude = np.array([1.0, 0.0, 0.0, 0.0])
        self.vehicle_local_position = np.array([0.0, 0.0, 0.0])
        self.vehicle_local_velocity = np.array([0.0, 0.0, 0.0])
#
        self.total_duration = 12.0  
        self.sample_interval = 0.5
        self.reference_samples = self.generate_circular_samples(
            radius=10.0,
            z_height=3.0,
            num_samples=25,
            total_duration=12.0
        )

        self.nav_state = VehicleStatus.NAVIGATION_STATE_MAX
        self.initial_position = self.reference_trajectory(0)  # Evaluate reference trajectory at t = 0
        
        # Create Quadrotor and controller objects
        self.model = MultirotorRateModel()

        self.x0 = np.array([*self.initial_position, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
        
        # Create MPC Solver
        self.mpc = MultirotorRateMPC(self.model, self.x0)
        self.prediction_horizon = int(self.mpc.Tf * self.mpc.N)

    def generate_circular_samples(self, radius, z_height, num_samples, total_duration):
        """Generate pre-computed circular trajectory samples"""
        omega = 2 * np.pi / total_duration
        samples = []
        for t in np.linspace(0, total_duration, num_samples):
            x = radius * np.cos(omega * t)
            y = radius * np.sin(omega * t)
            samples.append(np.array([x, y, z_height]))
        return samples

    def reference_trajectory(self, t):
        """Get reference position using pre-sampled points with linear interpolation"""
        t_mod = t % self.total_duration
        exact_index = t_mod / self.sample_interval
        
        # Handle wrap-around for circular trajectory
        index_floor = int(np.floor(exact_index))
        index_ceil = (index_floor + 1) % len(self.reference_samples)
        
        # Linear interpolation between samples
        alpha = exact_index - index_floor
        pos_floor = self.reference_samples[index_floor]
        pos_ceil = self.reference_samples[index_ceil]
        
        return (1 - alpha) * pos_floor + alpha * pos_ceil

    def vehicle_status_callback(self, msg):
        if msg.nav_state == VehicleStatus.NAVIGATION_STATE_OFFBOARD:
            self.get_logger().info("Switched to OFFBOARD mode")
        self.nav_state = msg.nav_state

    def vehicle_attitude_callback(self, msg):
        # TODO: handle NED->ENU transformation 
        self.vehicle_attitude[0] = msg.q[0]
        self.vehicle_attitude[1] = msg.q[1]
        self.vehicle_attitude[2] = -msg.q[2]
        self.vehicle_attitude[3] = -msg.q[3]

    def vehicle_local_position_callback(self, msg):
        # TODO: handle NED->ENU transformation 
        self.vehicle_local_position[0] = msg.x
        self.vehicle_local_position[1] = -msg.y
        self.vehicle_local_position[2] = -msg.z
        self.vehicle_local_velocity[0] = msg.vx
        self.vehicle_local_velocity[1] = -msg.vy
        self.vehicle_local_velocity[2] = -msg.vz

    def publish_reference(self, pub, reference):
        msg = Marker()
        msg.action = Marker.ADD
        msg.header.frame_id = "map"
        msg.ns = "arrow"
        msg.id = 1
        msg.type = Marker.SPHERE
        msg.scale.x = 0.5
        msg.scale.y = 0.5
        msg.scale.z = 0.5
        msg.color.r = 1.0
        msg.color.g = 0.0
        msg.color.b = 0.0                                                  # what is this?
        msg.color.a = 1.0
        msg.pose.position.x = reference[0]
        msg.pose.position.y = reference[1]
        msg.pose.position.z = reference[2]
        msg.pose.orientation.w = 1.0
        msg.pose.orientation.x = 0.0
        msg.pose.orientation.y = 0.0
        msg.pose.orientation.z = 0.0

        pub.publish(msg)

    def publish_map_frame(self):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "world"  # Parent frame (can be "odom" or "base_link" if needed)
        t.child_frame_id = "map"      # The frame we are creating

        # Identity transform (no translation or rotation)
        t.transform.translation.x = 0.0
        t.transform.translation.y = 0.0
        t.transform.translation.z = 0.0
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        self.tf_broadcaster.sendTransform(t)
        self.get_logger().info("Published static map frame")

    def cmd_callback(self):
        # Publish offboard control modes
        offboard_msg = OffboardControlMode()
        offboard_msg.timestamp = int(Clock().now().nanoseconds / 1000)
        offboard_msg.position = False
        offboard_msg.velocity = False
        offboard_msg.acceleration = False
        offboard_msg.attitude = False  
        offboard_msg.body_rate = True                                             
        self.publisher_offboard_mode.publish(offboard_msg)
        print(f"Offboard message sent!!!")

        # Update current state
        x0 = np.array([
            self.vehicle_local_position[0],
            self.vehicle_local_position[1],
            self.vehicle_local_position[2],
            self.vehicle_local_velocity[0],
            self.vehicle_local_velocity[1],
            self.vehicle_local_velocity[2],
            self.vehicle_attitude[0],
            self.vehicle_attitude[1],
            self.vehicle_attitude[2],                                 
            self.vehicle_attitude[3]
        ]).reshape(-1,1)
        x_pos = x0[0:3]
        # Get current time
        t_k = self.get_clock().now().nanoseconds / 1e9  
        horizon_refs = []
        dt = self.mpc.Tf / self.mpc.N 
        for k in range(self.mpc.N):
            t = t_k + k * dt
            horizon_refs.append(self.reference_trajectory(t))                             
        # print(f" Time : {t_k}")
        # Solve MPC step with current reference
        start_time = time.perf_counter()
        # u_pred, x_pred = self.mpc.solve_step(x0, horizon_refs-x_pos.T)    
        u_pred, x_pred = self.mpc.solve_step(x0, horizon_refs) 
        solve_time = time.perf_counter() - start_time                         
        # print(f"u_pred : {u_pred} time : {t_k}")
        # self.get_logger().info(f"MPC solve time: {solve_time*1000:.2f} ms")
        # Publish predicted path
        predicted_path_msg = Path()
        predicted_path_msg.header.frame_id = "map"
        predicted_path_msg.header.stamp = self.get_clock().now().to_msg()
        for state in x_pred.T:  # Assuming x_pred is (state_dim, prediction_horizon)
            position = state[:3]
            attitude = state[6:10]
            pose_msg = vector2PoseMsg("map", position, attitude)
            predicted_path_msg.poses.append(pose_msg)
        self.predicted_path_pub.publish(predicted_path_msg)
        # pdb.set_trace()

        # #### Update and publish reference trajectory
        # reference_pos = self.reference_trajectory(t_k)
        # reference_pose = vector2PoseMsg("map", self.reference_trajectory(t_k), [1.0, 0.0, 0.0, 0.0])
        # self.reference_path_msg.poses.append(reference_pose)
        # if len(self.reference_path_msg.poses) > 1000:
        #     del self.reference_path_msg.poses[0]
        # self.reference_path_msg.header.stamp = self.get_clock().now().to_msg()
        # self.reference_path_pub.publish(self.reference_path_msg)
        # # Publish current reference point as Marker
        # self.publish_reference(self.reference_pub, reference_pos) 

        #### Update and publish reference trajectory
        reference_pos = self.reference_trajectory(t_k)
        # uncomment to get the complete path
        # if not hasattr(self, 'full_trajectory_published'):
        #     full_traj_marker = Marker()
        #     full_traj_marker.header.frame_id = "map"
        #     full_traj_marker.header.stamp = self.get_clock().now().to_msg()
        #     full_traj_marker.type = Marker.LINE_STRIP
        #     full_traj_marker.action = Marker.ADD
        #     full_traj_marker.scale.x = 0.1  # Line width
        #     full_traj_marker.color.a = 1.0   # Alpha
        #     full_traj_marker.color.b = 1.0   # Blue color
        #     full_traj_marker.id = 0
        #     full_traj_marker.ns = "full_trajectory"

        #     # Add all sample points
        #     for sample in self.reference_samples:
        #         point = Point()
        #         point.x = float(sample[0])
        #         point.y = float(sample[1])
        #         point.z = float(sample[2])
        #         full_traj_marker.points.append(point)
            
        #     self.reference_pub.publish(full_traj_marker)
        #     self.full_trajectory_published = True
        self.publish_reference(self.reference_pub, reference_pos)
        
        self.reference_path_msg = Path()  # Reset instead of clearing
        self.reference_path_msg.header.frame_id = "map"
        self.reference_path_msg.header.stamp = self.get_clock().now().to_msg()
        for pos in horizon_refs:
            pose = vector2PoseMsg("map", pos, [1.0, 0.0, 0.0, 0.0])
            self.reference_path_msg.poses.append(pose)
        self.reference_path_pub.publish(self.reference_path_msg)

        current_position = x0[:3, 0]  # Extract x,y,z from initial state
        error_vector = current_position - reference_pos
        error_magnitude = np.linalg.norm(error_vector)
        
        # Log error information
        # self.get_logger().info(f"Position error: {error_magnitude:.2f} m")
        # print(f"Error components [X: {error_vector[0]:.2f}, Y: {error_vector[1]:.2f}, Z: {error_vector[2]:.2f}]")


        ##### Extract control inputs (assuming u_pred is (control_dim, prediction_horizon))
        if u_pred.size > 0:
            thrust_rate = u_pred[0, 0]
            roll_rate = u_pred[1, 0]
            pitch_rate = -(u_pred[2, 0])
            yaw_rate = -(u_pred[3, 0])

            # Convert thrust to PX4's expected format (assuming mapping is needed)
            # This conversion may require tuning based on your platform
            # thrust_command = (thrust_rate + 1.0) / 2.0  # Example mapping
            thrust_command = -(thrust_rate * 0.07 + 0.0)

            # Publish rates setpoint if in OFFBOARD mode
            if self.nav_state == VehicleStatus.NAVIGATION_STATE_OFFBOARD:
                setpoint_msg = VehicleRatesSetpoint()
                setpoint_msg.timestamp = int(Clock().now().nanoseconds / 1000)
                setpoint_msg.roll = float(roll_rate)
                setpoint_msg.pitch = float(-pitch_rate)
                setpoint_msg.yaw = float(-yaw_rate)
                setpoint_msg.thrust_body[2] = float(thrust_command)  # Z-component in NED
                self.publisher_rates_setpoint.publish(setpoint_msg)
                # print(f"CONTROL INPUT : {setpoint_msg}")
            '''
                px4_msgs::msg::VehicleRatesSetpoint

        The following input combination is supported:
            roll, pitch, yaw and thrust_body.

        All the values are in the drone body FRD frame. The rates are in [rad/s] while thrust_body is normalized in [-1, 1].

            '''
def main(args=None):
    rclpy.init(args=args)
    quadrotor_mpc = QuadrotorMPC()
    rclpy.spin(quadrotor_mpc)
    quadrotor_mpc.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()


# /goal_pose
# /initialpose
# /parameter_events
# /px4_mpc/predicted_path
# /px4_mpc/reference
# /px4_mpc/reference_array
# /px4_visualizer/vehicle_path
# /px4_visualizer/vehicle_pose
# /rviz_target_pose_marker/feedback
# /rviz_target_pose_marker/update



