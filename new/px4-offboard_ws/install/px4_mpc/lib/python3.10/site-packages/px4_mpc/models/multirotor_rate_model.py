from acados_template import AcadosModel
import casadi as cs

class MultirotorRateModel():
    def __init__(self):
        self.name = 'multirotor_rate_model'

        # constants
        self.mass = 1.
        print('8888888888888888888888888888888888888888888888888888888888888888888888888888888888mass',self.mass)
        hover_thrust = 0.5
        self.max_thrust = self.mass * 9.81/hover_thrust
        self.max_rate = 0.5

    def get_acados_model(self) -> AcadosModel:
        def skew_symmetric(v):
            return cs.vertcat(cs.horzcat(0, -v[0], -v[1], -v[2]),
                cs.horzcat(v[0], 0, v[2], -v[1]),
                cs.horzcat(v[1], -v[2], 0, v[0]),
                cs.horzcat(v[2], v[1], -v[0], 0))

        def q_to_rot_mat(q):
            qw, qx, qy, qz = q[0], q[1], q[2], q[3]

            rot_mat = cs.vertcat(
                cs.horzcat(1 - 2 * (qy ** 2 + qz ** 2), 2 * (qx * qy - qw * qz), 2 * (qx * qz + qw * qy)),
                cs.horzcat(2 * (qx * qy + qw * qz), 1 - 2 * (qx ** 2 + qz ** 2), 2 * (qy * qz - qw * qx)),
                cs.horzcat(2 * (qx * qz - qw * qy), 2 * (qy * qz + qw * qx), 1 - 2 * (qx ** 2 + qy ** 2)))

            return rot_mat

        def v_dot_q(v, q):
            rot_mat = q_to_rot_mat(q)

            return cs.mtimes(rot_mat, v)

        model = AcadosModel()

        # set up states & controls
        p      = cs.MX.sym('p', 3)
        v      = cs.MX.sym('v', 3)
        q = cs.MX.sym('q', 4)

        x = cs.vertcat(p, v, q)

        F = cs.MX.sym('F')
        w = cs.MX.sym('w', 3)
        u = cs.vertcat(F, w)

        # xdot
        p_dot      = cs.MX.sym('p_dot', 3)
        v_dot      = cs.MX.sym('v_dot', 3)
        q_dot      = cs.MX.sym('q_dot', 4)

        xdot = cs.vertcat(p_dot, v_dot, q_dot)
        g = cs.vertcat(0.0, 0.0, -9.81) # gravity constant [m/s^2]
        
        force = cs.vertcat(0.0, 0.0, F)

        a_thrust = v_dot_q(force, q)/self.mass
        
        # dynamics
        f_expl = cs.vertcat(v,
                        a_thrust + g,
                        1 / 2 * cs.mtimes(skew_symmetric(w), q)
                        )

        f_impl = xdot - f_expl


        model.f_impl_expr = f_impl
        model.f_expl_expr = f_expl
        model.x = x
        model.xdot = xdot
        model.u = u
        model.name = self.name

        return model


#################################################################################################

# from acados_template import AcadosModel
# import casadi as cs

# class MultirotorRateModel():
#     def __init__(self):
#         self.name = 'multirotor_rate_model'
#         # Constants
#         self.mass = 1.0  # Mass of the multirotor (kg)
#         hover_thrust = 0.5  # Fraction of max thrust used for hovering
#         self.max_thrust = self.mass * 9.81 / hover_thrust  # Maximum thrust
#         self.max_rate = 0.5  # Maximum angular rate (rad/s)

#     def get_acados_model(self) -> AcadosModel:
#         """
#         Define the multirotor dynamics and return an AcadosModel object.
#         """
#         # Helper functions
#         def skew_symmetric(v):
#             """Create a skew-symmetric matrix from a 3D vector."""
#             return cs.vertcat(
#                 cs.horzcat(0, -v[2], v[1]),
#                 cs.horzcat(v[2], 0, -v[0]),
#                 cs.horzcat(-v[1], v[0], 0)
#             )

#         def q_to_rot_mat(q):
#             """Convert a quaternion to a rotation matrix."""
#             qw, qx, qy, qz = q[0], q[1], q[2], q[3]
#             rot_mat = cs.vertcat(
#                 cs.horzcat(1 - 2 * (qy ** 2 + qz ** 2), 2 * (qx * qy - qw * qz), 2 * (qx * qz + qw * qy)),
#                 cs.horzcat(2 * (qx * qy + qw * qz), 1 - 2 * (qx ** 2 + qz ** 2), 2 * (qy * qz - qw * qx)),
#                 cs.horzcat(2 * (qx * qz - qw * qy), 2 * (qy * qz + qw * qx), 1 - 2 * (qx ** 2 + qy ** 2))
#             )
#             return rot_mat
#         def omega_matrix(w):
#             """Create the 4x4 Omega matrix from a 3D angular velocity vector."""
#             wx, wy, wz = w[0], w[1], w[2]
#             return cs.vertcat(
#                 cs.horzcat(0, -wx, -wy, -wz),
#                 cs.horzcat(wx, 0, wz, -wy),
#                 cs.horzcat(wy, -wz, 0, wx),
#                 cs.horzcat(wz, wy, -wx, 0)
#             )

#         def v_dot_q(v, q):
#             """Rotate a vector `v` by a quaternion `q`."""
#             rot_mat = q_to_rot_mat(q)
#             return cs.mtimes(rot_mat, v)

#         # Define states
#         p = cs.MX.sym('p', 3)  # Position [x, y, z]
#         v = cs.MX.sym('v', 3)  # Velocity [vx, vy, vz]
#         q = cs.MX.sym('q', 4)  # Quaternion [qw, qx, qy, qz]

#         # Concatenate states into a single vector
#         x = cs.vertcat(p, v, q)

#         # Define controls
#         F = cs.MX.sym('F')  # Thrust force
#         w = cs.MX.sym('w', 3)  # Angular rates [wx, wy, wz]

#         # Concatenate controls into a single vector
#         u = cs.vertcat(F, w)

#         # Define state derivatives
#         p_dot = cs.MX.sym('p_dot', 3)  # Derivative of position
#         v_dot = cs.MX.sym('v_dot', 3)  # Derivative of velocity
#         q_dot = cs.MX.sym('q_dot', 4)  # Derivative of quaternion

#         # Concatenate state derivatives into a single vector
#         xdot = cs.vertcat(p_dot, v_dot, q_dot)

#         # Define gravity vector
#         g = cs.vertcat(0.0, 0.0, -9.81)  # Gravity constant [m/s^2]

#         # Define thrust force vector
#         force = cs.vertcat(0.0, 0.0, F)

#         # Compute acceleration due to thrust
#         a_thrust = v_dot_q(force, q) / self.mass

#         # Dynamics equations
#         f_expl = cs.vertcat(
#             v,  # Position derivative
#             a_thrust + g,  # Velocity derivative
#             #0.5 * cs.mtimes(skew_symmetric(w), q)  # Quaternion derivative
#             0.5 * cs.mtimes(omega_matrix(w), q)
#         )

#         # Implicit dynamics formulation
#         f_impl = xdot - f_expl

#         # Create AcadosModel object
#         model = AcadosModel()
#         model.f_impl_expr = f_impl  # Implicit dynamics
#         model.f_expl_expr = f_expl  # Explicit dynamics
#         model.x = x  # States
#         model.xdot = xdot  # State derivatives
#         model.u = u  # Controls
#         model.name = self.name  # Model name

#         return model


