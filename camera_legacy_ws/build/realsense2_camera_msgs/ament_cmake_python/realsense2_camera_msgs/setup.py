from setuptools import find_packages
from setuptools import setup

setup(
    name='realsense2_camera_msgs',
    version='3.2.3',
    packages=find_packages(
        include=('realsense2_camera_msgs', 'realsense2_camera_msgs.*')),
)
