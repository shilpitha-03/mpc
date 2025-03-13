import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/px4_uxrce/new/px4-offboard_ws/install/px4_offboard'
