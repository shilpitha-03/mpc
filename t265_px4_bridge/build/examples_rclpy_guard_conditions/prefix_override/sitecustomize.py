import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/px4_uxrce/t265_px4_bridge/install/examples_rclpy_guard_conditions'
