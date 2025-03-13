import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/px4_uxrce/convex_ellipsoid_planner/install/rrt_python_gym'
