# from acados_template import AcadosOcp, AcadosOcpSolver, AcadosSimSolver
# import numpy as np
# import scipy.linalg
# import casadi as cs

# class MultirotorRateMPC():
#     def __init__(self, model):
#         self.model = model
#         self.Tf = 1.0
#         self.N = 50

#         self.x0 = np.array([0.01, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0])

#         self.ocp_solver, self.integrator = self.setup(self.x0, self.N , self.Tf)

#     def setup(self, x0, N_horizon, Tf):
#         # create ocp object to formulate the OCP
#         ocp = AcadosOcp()

#         # set model
#         model = self.model.get_acados_model()
#         Fmax = self.model.max_thrust
#         wmax = self.model.max_rate

#         ocp.model = model

#         nx = model.x.size()[0]
#         nu = model.u.size()[0]
#         ny = nx + nu
#         ny_e = nx

#         # set dimensions
#         ocp.dims.N = N_horizon

#         # set cost
#         Q_mat = 2*np.diag([1e1, 1e1, 1e1, 1e1, 1e1, 1e1, 0.0, 0.1, 0.1, 0.1])
#         Q_e = 2*np.diag([3e2, 3e2, 3e2, 1e2, 1e2, 1e2, 0.0, 0.0, 0.0, 0.0])
#         R_mat = 2*np.diag([1e1, 5e2, 5e2, 5e2])

#         # TODO: How do you add terminal costs?

#         # the 'EXTERNAL' cost type can be used to define general cost terms
#         # NOTE: This leads to additional (exact) hessian contributions when using GAUSS_NEWTON hessian.
#         # ocp.cost.cost_type = 'EXTERNAL'
#         # ocp.cost.cost_type_e = 'EXTERNAL'
#         # ocp.model.cost_expr_ext_cost = model.x.T @ Q_mat @ model.x + model.u.T @ R_mat @ model.u
#         # ocp.model.cost_expr_ext_cost_e = model.x.T @ Q_e @ model.x

#         ocp.cost.cost_type = 'NONLINEAR_LS'
#         ocp.cost.cost_type_e = 'NONLINEAR_LS'
#         ocp.cost.W = scipy.linalg.block_diag(Q_mat, R_mat)
#         ocp.cost.W_e = scipy.linalg.block_diag(Q_e)


#         ocp.model.cost_y_expr = cs.vertcat(model.x, model.u)
#         ocp.model.cost_y_expr_e = model.x
#         ocp.cost.yref  = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
#         ocp.cost.yref_e = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])

#         # set constraints
#         ocp.constraints.lbu = np.array([0.0, -wmax, -wmax, -0.5*wmax])
#         ocp.constraints.ubu = np.array([+Fmax,  wmax, wmax, 0.5*wmax])
#         ocp.constraints.idxbu = np.array([0, 1, 2, 3])

#         ocp.constraints.x0 = x0

#         # set options
#         ocp.solver_options.qp_solver = 'PARTIAL_CONDENSING_HPIPM' # FULL_CONDENSING_QPOASES
#         # PARTIAL_CONDENSING_HPIPM, FULL_CONDENSING_QPOASES, FULL_CONDENSING_HPIPM,
#         # PARTIAL_CONDENSING_QPDUNES, PARTIAL_CONDENSING_OSQP, FULL_CONDENSING_DAQP
#         ocp.solver_options.hessian_approx = 'GAUSS_NEWTON' # 'GAUSS_NEWTON', 'EXACT'
#         ocp.solver_options.integrator_type = 'ERK'
#         # ocp.solver_options.print_level = 1
#         use_RTI=True
#         if use_RTI:
#             ocp.solver_options.nlp_solver_type = 'SQP_RTI' # SQP_RTI, SQP
#             ocp.solver_options.sim_method_num_stages = 4
#             ocp.solver_options.sim_method_num_steps = 3
#         else:
#             ocp.solver_options.nlp_solver_type = 'SQP' # SQP_RTI, SQP

#         ocp.solver_options.qp_solver_cond_N = N_horizon

#         # set prediction horizon
#         ocp.solver_options.tf = Tf

#         ocp_solver = AcadosOcpSolver(ocp, json_file = 'acados_ocp.json')
#         # create an integrator with the same settings as used in the OCP solver.
#         acados_integrator = AcadosSimSolver(ocp, json_file = 'acados_ocp.json')

#         return ocp_solver, acados_integrator
#     def solve(self, x0, verbose=False):

#         # preparation phase
#         ocp_solver = self.ocp_solver

#         # set initial state
#         ocp_solver.set(0, "lbx", x0)
#         ocp_solver.set(0, "ubx", x0)

#         status = ocp_solver.solve()
#         if verbose:
#             self.ocp_solver.print_statistics() # encapsulates: stat = ocp_solver.get_stats("statistics")

#         if status != 0:
#             raise Exception(f'acados returned status {status}.')

#         N = self.N
#         nx = self.model.get_acados_model().x.size()[0]
#         nu = self.model.get_acados_model().u.size()[0]

#         simX = np.ndarray((N+1, nx))
#         simU = np.ndarray((N, nu))

#         # get solution
#         for i in range(N):
#             simX[i,:] = self.ocp_solver.get(i, "x")
#             simU[i,:] = self.ocp_solver.get(i, "u")
#         simX[N,:] = self.ocp_solver.get(N, "x")

#         return simU, simX

# #######################################################################################################

# from acados_template import AcadosOcp, AcadosOcpSolver, AcadosSimSolver
# import numpy as np
# import scipy.linalg
# import casadi as cs

# class MultirotorRateMPC():
#     def __init__(self, model, waypoints, Tf=1.0, N=50):
#         self.model = model
#         self.Tf = Tf
#         self.N = N
#         self.waypoints = waypoints
#         self.dt = Tf / N
#         self.x0 = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])  # Initial state
#         self.ocp_solver, self.integrator = self.setup(self.x0, N, Tf)

#     def setup(self, x0, N_horizon, Tf):
#         # Create OCP object
#         ocp = AcadosOcp()
#         model = self.model.get_acados_model()
#         Fmax = self.model.max_thrust
#         wmax = self.model.max_rate
#         ocp.model = model
#         nx = model.x.size()[0]
#         nu = model.u.size()[0]
#         ny = nx + nu
#         ny_e = nx

#         # Set dimensions
#         ocp.dims.N = N_horizon

#         # Set cost
#         Q_mat = 2 * np.diag([1e1, 1e1, 1e1, 1e1, 1e1, 1e1, 0.0, 0.1, 0.1, 0.1])
#         Q_e = 2 * np.diag([3e2, 3e2, 3e2, 1e2, 1e2, 1e2, 0.0, 0.0, 0.0, 0.0])
#         R_mat = 2 * np.diag([1e1, 5e2, 5e2, 5e2])
#         ocp.cost.cost_type = 'NONLINEAR_LS'
#         ocp.cost.cost_type_e = 'NONLINEAR_LS'
#         ocp.cost.W = scipy.linalg.block_diag(Q_mat, R_mat)
#         ocp.cost.W_e = scipy.linalg.block_diag(Q_e)

#         ocp.model.cost_y_expr = cs.vertcat(model.x, model.u)
#         ocp.model.cost_y_expr_e = model.x

#         # Set constraints
#         ocp.constraints.lbu = np.array([0.0, -wmax, -wmax, -0.5 * wmax])
#         ocp.constraints.ubu = np.array([+Fmax, wmax, wmax, 0.5 * wmax])
#         ocp.constraints.idxbu = np.array([0, 1, 2, 3])
#         ocp.constraints.x0 = x0

#         # Set options
#         ocp.solver_options.qp_solver = 'PARTIAL_CONDENSING_HPIPM'
#         ocp.solver_options.hessian_approx = 'GAUSS_NEWTON'
#         ocp.solver_options.integrator_type = 'ERK'
#         ocp.solver_options.nlp_solver_type = 'SQP_RTI'
#         ocp.solver_options.sim_method_num_stages = 4
#         ocp.solver_options.sim_method_num_steps = 3
#         ocp.solver_options.qp_solver_cond_N = N_horizon

#         # Set prediction horizon
#         ocp.solver_options.tf = Tf

#         # Create solver and integrator
#         ocp_solver = AcadosOcpSolver(ocp, json_file='acados_ocp.json')
#         acados_integrator = AcadosSimSolver(ocp, json_file='acados_ocp.json')
#         return ocp_solver, acados_integrator

#     def update_references(self, current_time):
#         """Update reference trajectory for the MPC."""
#         dt = self.dt
#         N = self.N
#         waypoints = self.waypoints
#         num_waypoints = len(waypoints)

#         # Interpolate waypoints to generate smooth trajectory
#         t_ref = np.linspace(0, num_waypoints - 1, int(num_waypoints / dt))
#         x_ref = np.interp(t_ref, np.arange(num_waypoints), waypoints[:, 0])
#         y_ref = np.interp(t_ref, np.arange(num_waypoints), waypoints[:, 1])
#         z_ref = np.interp(t_ref, np.arange(num_waypoints), waypoints[:, 2])

#         # Extract references for the prediction horizon
#         idx_start = int(current_time / dt)
#         idx_end = idx_start + N
#         if idx_end > len(t_ref):
#             idx_end = len(t_ref)
#             x_ref = np.pad(x_ref, (0, N), 'edge')
#             y_ref = np.pad(y_ref, (0, N), 'edge')
#             z_ref = np.pad(z_ref, (0, N), 'edge')

#         ref_traj = np.vstack((x_ref[idx_start:idx_end],
#                               y_ref[idx_start:idx_end],
#                               z_ref[idx_start:idx_end])).T
#         return ref_traj

#     def solve(self, x0, current_time):
#         """Solve the MPC problem."""
#         ocp_solver = self.ocp_solver
#         ref_traj = self.update_references(current_time)

#         # Set initial state
#         ocp_solver.set(0, "lbx", x0)
#         ocp_solver.set(0, "ubx", x0)

#         # Set reference trajectory
#         for i in range(self.N):
#             ocp_solver.set(i, "yref", np.hstack((ref_traj[i], np.zeros(4))))
#         ocp_solver.set(self.N, "yref", np.hstack((ref_traj[-1], np.zeros(4))))

#         # Solve OCP
#         status = ocp_solver.solve()
#         if status != 0:
#             raise Exception(f'acados returned status {status}.')

#         # Get solution
#         simX = np.zeros((self.N + 1, self.model.get_acados_model().x.size()[0]))
#         simU = np.zeros((self.N, self.model.get_acados_model().u.size()[0]))
#         for i in range(self.N):
#             simX[i, :] = ocp_solver.get(i, "x")
#             simU[i, :] = ocp_solver.get(i, "u")
#         simX[self.N, :] = ocp_solver.get(self.N, "x")

#         return simU, simX




#######################################################################################################


# from acados_template import AcadosOcp, AcadosOcpSolver, AcadosSimSolver
# import numpy as np
# import scipy.linalg
# import casadi as cs

# class MultirotorRateMPC():
#     def __init__(self, model):
#         self.model = model
#         self.Tf = 1.0  # prediction horizon time (seconds)
#         self.N = 50    # number of discretization steps

#         # Initial state: assumed to be 10-dimensional where the first 3 entries are positions.
#         self.x0 = np.array([0.01, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0])
        
#         self.ocp_solver, self.integrator = self.setup(self.x0, self.N, self.Tf)

#     def setup(self, x0, N_horizon, Tf):
#         # Create an OCP object to formulate the optimal control problem.
#         ocp = AcadosOcp()

#         # Get the acados model from the provided model instance.
#         model = self.model.get_acados_model()
#         Fmax = self.model.max_thrust
#         wmax = self.model.max_rate

#         ocp.model = model

#         # Retrieve dimensions.
#         nx = model.x.size()[0]
#         nu = model.u.size()[0]

#         # Set the number of control intervals.
#         ocp.dims.N = N_horizon

#         # --- Cost Setup: Tracking Only Positions ---
#         # We assume that positions are given by the first three states.
#         # Define weight matrices for the position errors.
#         Q_pos = 2 * np.diag([1e1, 1e1, 1e1])      # stage cost weight for positions
#         Qe_pos = 2 * np.diag([3e2, 3e2, 3e2])       # terminal cost weight for positions

#         # Set the cost type. Here, the cost is formulated as a nonlinear least squares (NONLINEAR_LS)
#         ocp.cost.cost_type = 'NONLINEAR_LS'
#         ocp.cost.cost_type_e = 'NONLINEAR_LS'
#         ocp.cost.W = Q_pos        # weight matrix for the stage cost (only positions)
#         ocp.cost.W_e = Qe_pos      # weight matrix for the terminal cost

#         # Define the cost expressions.
#         # The cost is defined on the first three components of the state (i.e. positions).
#         ocp.model.cost_y_expr = model.x[0:3]
#         ocp.model.cost_y_expr_e = model.x[0:3]

#         # Set default reference values for cost; these are placeholders and will be overwritten in the solve() call.
#         ocp.cost.yref  = np.zeros(3)  # For intermediate stages: desired positions (3-dim)
#         ocp.cost.yref_e = np.zeros(3)  # For terminal stage: desired positions (3-dim)

#         # --- Constraints Setup ---
#         # Define bounds for the control inputs.
#         ocp.constraints.lbu = np.array([0.0, -wmax, -wmax, -0.5*wmax])
#         ocp.constraints.ubu = np.array([+Fmax,  wmax, wmax, 0.5*wmax])
#         ocp.constraints.idxbu = np.array([0, 1, 2, 3])
        
#         # Set the initial condition.
#         ocp.constraints.x0 = x0

#         # --- Solver Options ---
#         ocp.solver_options.qp_solver = 'PARTIAL_CONDENSING_HPIPM'
#         ocp.solver_options.hessian_approx = 'GAUSS_NEWTON'
#         ocp.solver_options.integrator_type = 'ERK'

#         # Optionally, you can use a Real-Time Iteration (RTI) approach.
#         use_RTI = True
#         if use_RTI:
#             ocp.solver_options.nlp_solver_type = 'SQP_RTI'
#             ocp.solver_options.sim_method_num_stages = 4
#             ocp.solver_options.sim_method_num_steps = 3
#         else:
#             ocp.solver_options.nlp_solver_type = 'SQP'

#         ocp.solver_options.qp_solver_cond_N = N_horizon
#         ocp.solver_options.tf = Tf

#         # Create the OCP solver and the simulation integrator.
#         ocp_solver = AcadosOcpSolver(ocp, json_file='acados_ocp.json')
#         acados_integrator = AcadosSimSolver(ocp, json_file='acados_ocp.json')

#         return ocp_solver, acados_integrator

#     def solve(self, x0, pos_ref_traj, pos_ref_terminal, verbose=False):
#         """
#         Solve the MPC problem for a position-only reference trajectory.
        
#         Args:
#             x0: The current state (initial condition).
#             pos_ref_traj: A list or array of length N where each element is a 3-dimensional
#                           vector representing the desired position for that stage.
#             pos_ref_terminal: A 3-dimensional vector representing the desired terminal position.
#             verbose: If True, prints solver statistics.
        
#         Returns:
#             simU: The computed control inputs over the horizon (array of shape (N, nu)).
#             simX: The predicted state trajectory (array of shape (N+1, nx)).
#         """
#         ocp_solver = self.ocp_solver

#         # Set the initial state by fixing it at stage 0.
#         ocp_solver.set(0, "lbx", x0)
#         ocp_solver.set(0, "ubx", x0)

#         # Set the stage cost references. Since our cost expression is only on positions,
#         # each yref is a 3-dimensional vector.
#         for i in range(self.N):
#             ocp_solver.set(i, "yref", pos_ref_traj[i])
#         # Set the terminal stage cost reference.
#         ocp_solver.set(self.N, "yref", pos_ref_terminal)

#         # Solve the optimal control problem.
#         status = ocp_solver.solve()
#         if verbose:
#             ocp_solver.print_statistics()

#         if status != 0:
#             raise Exception(f'acados returned status {status}.')

#         # Retrieve and store the computed state and control trajectories.
#         nx = self.model.get_acados_model().x.size()[0]
#         nu = self.model.get_acados_model().u.size()[0]
#         simX = np.ndarray((self.N+1, nx))
#         simU = np.ndarray((self.N, nu))

#         for i in range(self.N):
#             simX[i, :] = ocp_solver.get(i, "x")
#             simU[i, :] = ocp_solver.get(i, "u")
#         simX[self.N, :] = ocp_solver.get(self.N, "x")

#         return simU, simX




###########################################################################################################################

# #dynamic reference trajectory updation:
# from acados_template import AcadosOcp, AcadosOcpSolver, AcadosSimSolver
# import numpy as np
# import scipy.linalg
# import casadi as cs

# class MultirotorRateMPC():
#     def __init__(self, model, x0=None):
#         self.model = model
#         self.Tf = 0.5  # Prediction horizon time (0.5 seconds for 5 steps)
#         self.N =25#5     # Number of discretization steps

#         if x0 is not None:
#             self.x0 = x0.copy()
#         else:
#             self.x0 = np.array([0.01, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0])
#         self.current_state = self.x0.copy()
#         self.current_time = 0.0

#         self.ocp_solver, self.integrator = self.setup(self.x0, self.N, self.Tf)

#     def set_initial_state(self, x0):
#         """Explicitly set the MPC's initial state."""
#         self.x0 = x0.copy()
#         self.current_state = x0.copy()  # Sync both attributes
#         self.ocp_solver.constraints_set(0, "lbx", self.current_state)
#         self.ocp_solver.constraints_set(0, "ubx", self.current_state)

#     def setup(self, x0, N_horizon, Tf):
#         ocp = AcadosOcp()
#         model = self.model.get_acados_model()
#         Fmax = self.model.max_thrust
#         wmax = self.model.max_rate

#         ocp.model = model
#         nx = model.x.size()[0]
#         nu = model.u.size()[0]
#         ocp.dims.N = N_horizon

#         # Cost setup: Track positions (first 3 states)
#         Q_pos = 2 * np.diag([1e1, 1e1, 1e1])
#         # Q_pos = 2 * np.diag([1e2, 1e2, 2e2])
#         #Qe_pos = 2 * np.diag([3e2, 3e2, 3e2])
#         ocp.cost.cost_type = 'NONLINEAR_LS'
#         #ocp.cost.cost_type_e = 'NONLINEAR_LS'
#         ocp.cost.W = Q_pos
#         #ocp.cost.W_e = Qe_pos
#         ocp.model.cost_y_expr = model.x[0:3]
#         # ocp.model.cost_y_expr_e = model.x[0:3]
#         ocp.cost.yref = np.zeros(3)
#         # ocp.cost.yref_e = np.zeros(3)

#         # Input constraints
#         ocp.constraints.lbu = np.array([0.0, -wmax, -wmax, -0.5*wmax])
#         ocp.constraints.ubu = np.array([+Fmax, wmax, wmax, 0.5*wmax])
#         ocp.constraints.idxbu = np.array([0, 1, 2, 3])
#         ocp.constraints.x0 = x0

#         # Solver options
#         ocp.solver_options.qp_solver = 'PARTIAL_CONDENSING_HPIPM'
#         ocp.solver_options.hessian_approx = 'GAUSS_NEWTON'
#         ocp.solver_options.integrator_type = 'ERK'
#         ocp.solver_options.nlp_solver_type = 'SQP_RTI'
#         ocp.solver_options.sim_method_num_stages = 4
#         ocp.solver_options.sim_method_num_steps = 3
#         ocp.solver_options.tf = Tf

#         ocp_solver = AcadosOcpSolver(ocp, json_file='acados_ocp.json')
#         integrator = AcadosSimSolver(ocp, json_file='acados_ocp.json')
#         return ocp_solver, integrator

    # def update_references(self, reference_trajectory):
    #     """Update reference for each stage in the horizon."""
    #     for k in range(self.N):
    #         t_k = self.current_time + k * (self.Tf / self.N)
    #         yref_k = reference_trajectory(t_k)
    #         self.ocp_solver.set(k, "yref", yref_k)
    #     # Terminal reference
    #     t_e = self.current_time + self.Tf
    #     yref_e = reference_trajectory(t_e)
    #     self.ocp_solver.set(self.N, "yref", yref_e)

#     # def solve_step(self, reference_trajectory):
#     #     """Solve MPC for current step and apply first control input."""
#     #     # Set initial state
#     #     self.ocp_solver.constraints_set(0, "lbx", self.current_state)
#     #     self.ocp_solver.constraints_set(0, "ubx", self.current_state)

#     #     # Update references based on current time
#     #     self.update_references(reference_trajectory)

#     #     # Solve OCP
#     #     status = self.ocp_solver.solve()
#     #     if status != 0:
#     #         raise Exception(f'Acados solver failed with status: {status}')

#     #     # Get first control input
#     #     u0 = self.ocp_solver.get(0, "u")

#     #     # Simulate next state
#     #     self.integrator.set("x", self.current_state)
#     #     self.integrator.set("u", u0)
#     #     status = self.integrator.solve()
#     #     if status != 0:
#     #         raise Exception('Integrator failed.')

#     #     # Update current state and time
#     #     self.current_state = self.integrator.get("x")
#     #     self.current_time += self.Tf / self.N  # 0.1 seconds

#     #     # Retrieve trajectory for logging
#     #     simU = np.array([self.ocp_solver.get(k, "u") for k in range(self.N)])
#     #     simX = np.array([self.ocp_solver.get(k, "x") for k in range(self.N+1)])

#     #     return simU, simX

#     def solve_step(self, x0, reference_trajectory):
#         """Solve MPC for current step and apply first control input."""
#         # Current state
#         self.current_state = x0.flatten()

#         # Set initial state constraint
#         self.ocp_solver.constraints_set(0, "lbx", self.current_state.flatten())
#         self.ocp_solver.constraints_set(0, "ubx", self.current_state.flatten())

#         # Update references based on current time
#         self.update_references(reference_trajectory)

#         # Solve OCP
#         status = self.ocp_solver.solve()
#         if status != 0:
#             raise Exception(f'Acados solver failed with status: {status}')

#         # Get first control input
#         u0 = self.ocp_solver.get(0, "u")

#         # Simulate next state
#         self.integrator.set("x", self.current_state)
#         self.integrator.set("u", u0)
#         status = self.integrator.solve()
#         if status != 0:
#             raise Exception('Integrator failed.')

#         # Update current state and time
#         # self.current_state = self.integrator.get("x")
#         self.current_time += self.Tf / self.N  # 0.1 seconds

#         # Retrieve trajectory for logging
#         simU = np.array([self.ocp_solver.get(k, "u") for k in range(self.N)])
#         simX = np.array([self.ocp_solver.get(k, "x") for k in range(self.N+1)])

#         return simU, simX

##########################################################################################################################

# #dynamic reference trajectory updation:
# from acados_template import AcadosOcp, AcadosOcpSolver, AcadosSimSolver
# import numpy as np
# import scipy.linalg
# import casadi as cs
# import time
# import rclpy
# from rclpy.node import Node
# from rclpy.clock import Clock

# class MultirotorRateMPC():
#     def __init__(self, model, x0=None):
#         self.model = model
#         self.Tf = 5  # Prediction horizon time (0.5 seconds for 5 steps)
#         self.N =25#5     # Number of discretization steps

#         if x0 is not None:
#             self.x0 = x0.copy()
#         else:
#             self.x0 = np.array([0.01, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0])
#         self.current_state = self.x0.copy()
#         self.current_time = 0.0

#         self.ocp_solver, self.integrator = self.setup(self.x0, self.N, self.Tf)

#     def set_initial_state(self, x0):
#         """Explicitly set the MPC's initial state."""
#         self.x0 = x0.copy()
#         self.current_state = x0.copy()  # Sync both attributes
#         self.ocp_solver.constraints_set(0, "lbx", self.current_state)
#         self.ocp_solver.constraints_set(0, "ubx", self.current_state)

#     def setup(self, x0, N_horizon, Tf):
#         ocp = AcadosOcp()
#         model = self.model.get_acados_model()
#         Fmax = self.model.max_thrust
#         wmax = self.model.max_rate

#         ocp.model = model
#         nx = model.x.size()[0]
#         nu = model.u.size()[0]
#         ocp.dims.N = N_horizon

#         # Cost setup: Track positions (first 3 states)
   
#         Q_mat = 2*np.diag([1e3, 1e3, 1e3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
#         R_mat = 2*np.diag([1e1, 5e2, 5e2, 5e2])
#         ocp.cost.W = scipy.linalg.block_diag(Q_mat, R_mat)
#         ocp.model.cost_y_expr = cs.vertcat(model.x, model.u)
#         ocp.cost.yref  = np.array([2e1, 2e1, 2e1, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])


#         # Q_pos = 2 * np.diag([1e1, 1e1, 1e1])
#         # ocp.cost.cost_type = 'NONLINEAR_LS'
#         # ocp.cost.W = Q_pos
#         # ocp.model.cost_y_expr = model.x[0:3]
#         # ocp.cost.yref = np.zeros(3)
#         # Qe_pos = 2 * np.diag([3e2, 3e2, 3e2])
#         # ocp.cost.cost_type_e = 'NONLINEAR_LS'
#         # ocp.cost.W_e = Qe_pos
#         # ocp.model.cost_y_expr_e = model.x[0:3]
#         # ocp.cost.yref_e = np.zeros(3)


#         # Input constraints
#         ocp.constraints.lbu = np.array([0.0, -wmax, -wmax, -0.5*wmax])
#         ocp.constraints.ubu = np.array([+Fmax, wmax, wmax, 0.5*wmax])
#         ocp.constraints.idxbu = np.array([0, 1, 2, 3])
#         ocp.constraints.x0 = x0

#         # Solver options
#         ocp.solver_options.qp_solver = 'PARTIAL_CONDENSING_HPIPM'
#         ocp.solver_options.hessian_approx = 'GAUSS_NEWTON'
#         ocp.solver_options.integrator_type = 'ERK'
#         ocp.solver_options.nlp_solver_type = 'SQP_RTI'
#         ocp.solver_options.sim_method_num_stages = 4
#         ocp.solver_options.sim_method_num_steps = 3
#         ocp.solver_options.tf = Tf

#         ocp_solver = AcadosOcpSolver(ocp, json_file='acados_ocp.json')
#         integrator = AcadosSimSolver(ocp, json_file='acados_ocp.json')
#         return ocp_solver, integrator

#     # def update_references(self, reference_trajectory):
#     #     """Update reference for each stage in the horizon."""
#     #     for k in range(self.N):
#     #         t_k = self.current_time + k * (self.Tf / self.N)
#     #         yref_k = reference_trajectory[k]
#     #     # t_k = self.get_clock().now().nanoseconds / 1e9
#     #     # for k in range(self.N):
#     #     #     t_ref = t_k + k * (self.Tf / self.N)
#     #     #     yref_k = reference_trajectory(t_ref)
#     #         self.ocp_solver.set(k, "yref", yref_k)

#     #     # Terminal reference
#     #     t_e = self.current_time + self.Tf
#     #     yref_e = reference_trajectory(t_e)
#     #     self.ocp_solver.set(self.N, "yref", yref_e)

#     def update_references(self, reference_trajectory):
#         """Update references using precomputed samples for entire horizon."""
#         # Trajectory parameters (match your sampling setup)
#         total_duration = 12.0    # Total duration of the circular trajectory
#         sample_interval = 0.5    # Time between samples (0.5 seconds)
#         num_samples = 25         # Number of precomputed samples

#         # Calculate indices for the horizon
#         for k in range(self.N):
#             # Time for this step in the horizon
#             t_k = self.current_time + k * (self.Tf / self.N)
            
#             # Map time to sample index
#             t_wrapped = t_k % total_duration
#             sample_idx = int((t_wrapped / total_duration) * num_samples) % num_samples
            
#             # Get reference from precomputed array
#             yref_k = reference_trajectory[sample_idx]
#             self.ocp_solver.set(k, "yref", yref_k)

#         # Terminal reference (N+1 step)
#         t_e = self.current_time + self.Tf
#         t_e_wrapped = t_e % total_duration
#         terminal_idx = int((t_e_wrapped / total_duration) * num_samples) % num_samples
#         yref_e = reference_trajectory[terminal_idx]
#         self.ocp_solver.set(self.N, "yref", yref_e)

#     # def update_references(self, reference_trajectory):
#     #     """Update MPC references for entire horizon"""
#     #     for k in range(self.N):
#     #         # Get position reference from trajectory
#     #         t_k = self.current_time + k * (self.Tf / self.N)
#     #         yref_k = reference_trajectory[k]
            
#     #         # Construct full reference vector
#     #         yref = np.zeros(14)
#     #         yref[0:3] = yref_k              # Position reference
#     #         yref[6] = 1.0                    # Quaternion w (no rotation)
#     #         self.ocp_solver.set(k, "yref", yref)

#     def solve_step(self, x0, reference_trajectory,verbose=True):
#         """Solve MPC for current step and apply first control input."""
#         # Current state
#         self.current_state = x0.flatten()

#         # Set initial state constraint
#         self.ocp_solver.constraints_set(0, "lbx", self.current_state.flatten())
#         self.ocp_solver.constraints_set(0, "ubx", self.current_state.flatten())

#         # Update references based on current time
#         self.update_references(reference_trajectory)

#         # Solve OCP
#         status = self.ocp_solver.solve()
#         if status != 0:
#             raise Exception(f'Acados solver failed with status: {status}')

#         # Get first control input
#         u0 = self.ocp_solver.get(0, "u")

#         # Simulate next state
#         self.integrator.set("x", self.current_state)
#         self.integrator.set("u", u0)
#         status = self.integrator.solve()
#         if status != 0:
#             raise Exception('Integrator failed.')

#         # Update current state and time
#         self.current_time += self.Tf / self.N  # 0.1 seconds
#         # self.current_time = self.get_clock().now().nanoseconds / 1e9  # Sync to actual system time


#         # Retrieve trajectory for logging
#         simU = np.array([self.ocp_solver.get(k, "u") for k in range(self.N)])
#         simX = np.array([self.ocp_solver.get(k, "x") for k in range(self.N+1)])
#         # print(f"U values : 0000000000000 {simU}")
#         return simU, simX


############################################################################################################################


from acados_template import AcadosOcp, AcadosOcpSolver, AcadosSimSolver
import numpy as np
import scipy.linalg
import casadi as cs
import time
import rclpy
from rclpy.node import Node


class MultirotorRateMPC():
    def _init_(self, model, x0=None):
        self.model = model
        self.Tf = 5  # Prediction horizon time (0.5 seconds for 25 steps)
        self.N = 25    # Number of discretization steps

        if x0 is not None:
            self.x0 = x0.copy()
        else:
            self.x0 = np.array([0.01, 0.0, 0.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0])
        self.current_state = self.x0.copy()
        self.current_time = 0.0

        self.ocp_solver, self.integrator = self.setup(self.x0, self.N, self.Tf)

    def set_initial_state(self, x0):
        """Explicitly set the MPC's initial state."""
        self.x0 = x0.copy()
        self.current_state = x0.copy()  # Sync both attributes
        self.ocp_solver.constraints_set(0, "lbx", self.current_state)
        self.ocp_solver.constraints_set(0, "ubx", self.current_state)

    def setup(self, x0, N_horizon, Tf):
        ocp = AcadosOcp()
        model = self.model.get_acados_model()
        Fmax = self.model.max_thrust
        wmax = self.model.max_rate

        ocp.model = model
        nx = model.x.size()[0]
        nu = model.u.size()[0]
        ocp.dims.N = N_horizon

        # Cost setup: Track positions (first 3 states) and control inputs.
        # Define weight matrices for positions and controls.
        Q_pos = 2 * np.diag([1e2, 1e2, 1e1])          # 3x3: weight for position error.
        R_u   = 2 * np.diag([1e1, 5e2, 5e2, 5e2])       # 4x4: weight for control effort.
        # Combined weight matrix for the extended cost vector [x[0:3]; u]
        W = scipy.linalg.block_diag(Q_pos, R_u)         # 7x7 matrix

        ocp.cost.cost_type = 'NONLINEAR_LS'
        ocp.cost.W = W
        # The cost expression now includes both the first 3 states and the control input.
        ocp.model.cost_y_expr = cs.vertcat(model.x[0:3], model.u)
        # The reference vector must be 7-dimensional (3 for x and 4 for u).
        ocp.cost.yref = np.zeros(7)

        # Input constraints
        ocp.constraints.lbu = np.array([0.0, -wmax, -wmax, -0.5*wmax])
        ocp.constraints.ubu = np.array([+Fmax, wmax, wmax, 0.5*wmax])
        ocp.constraints.idxbu = np.array([0, 1, 2, 3])
        ocp.constraints.x0 = x0

        # Solver options
        ocp.solver_options.qp_solver = 'PARTIAL_CONDENSING_HPIPM'
        ocp.solver_options.hessian_approx = 'GAUSS_NEWTON'
        ocp.solver_options.integrator_type = 'ERK'
        ocp.solver_options.nlp_solver_type = 'SQP_RTI'
        ocp.solver_options.sim_method_num_stages = 4
        ocp.solver_options.sim_method_num_steps = 3
        ocp.solver_options.tf = Tf

        ocp_solver = AcadosOcpSolver(ocp, json_file='acados_ocp.json')
        integrator = AcadosSimSolver(ocp, json_file='acados_ocp.json')
        return ocp_solver, integrator

    def update_references(self, reference_trajectory):
        """Update reference for each stage in the horizon.
           The reference_trajectory is assumed to have 25 entries, each of dimension 7."""
        for k in range(self.N):
            yref_k = reference_trajectory[k]
            self.ocp_solver.set(k, "yref", yref_k)
        
    def solve_step(self, x0, reference_trajectory):
        """Solve MPC for current step and apply the first control input."""
        # Current state
        self.current_state = x0.flatten()

        # Set initial state constraint
        self.ocp_solver.constraints_set(0, "lbx", self.current_state.flatten())
        self.ocp_solver.constraints_set(0, "ubx", self.current_state.flatten())

        # Update references based on the provided trajectory
        self.update_references(reference_trajectory)

        # Solve OCP
        status = self.ocp_solver.solve()
        if status != 0:
            raise Exception(f'Acados solver failed with status: {status}')

        # Get the first control input
        u0 = self.ocp_solver.get(0, "u")

        # Simulate the next state
        self.integrator.set("x", self.current_state)
        self.integrator.set("u", u0)
        status = self.integrator.solve()
        if status != 0:
            raise Exception('Integrator failed.')

        # Update current time (each step is Tf/N seconds)
        self.current_time += self.Tf / self.N

        # Retrieve the trajectory for logging purposes
        simU = np.array([self.ocp_solver.get(k, "u") for k in range(self.N)])
        simX = np.array([self.ocp_solver.get(k, "x") for k in range(self.N+1)])
        print(f"Control inputs:\n{simU}")
        return simU, simX