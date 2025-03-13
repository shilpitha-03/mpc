import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/px4_uxrce/t265_px4_bridge/install/launch_testing_examples'
