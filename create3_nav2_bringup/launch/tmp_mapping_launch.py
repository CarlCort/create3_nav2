# THIS IS A TEMPORARY LAUNCH FILE THAT SHOULD BE REPLACED BY bringup_launch.py ONCE 
# THE ISSUES WITH THE MAP FILE HAVE BEEN RESOLVED!!!!

# launches self-contained navigation stack and slam_toolbox for create3

#!/usr/bin/env python3

"""
Launch file intended to start SLAM Toolbox and Nav2 navigation stack simultaneously 
for closed-loop navigation.

This launch file:
1. Expects that the robot has properly been started and publishes a /odomtopic with 
   RELIABLE QoS and that a laser scanner has been started, publishing the /scan topic. 
2. Defaults to the default_nav2_params.yaml param file but can be changed with the launch argument
3. Starts SLAM Toolbox and Nav2 simultaneously
4. Can optionally launch RViz

Arguments:
    use_sim_time:=<true/false> - Use simulation time (default: false)
"""
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition

this_pkg_name = 'create3_nav2_bringup'

def generate_launch_description():
    this_pkg_dir = FindPackageShare(package=this_pkg_name)
    bringup_dir = get_package_share_directory('create3_nav2_bringup')
    
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(bringup_dir, 'params', 'create3_nav2_params.yaml'),
        description='Full path to the ROS2 parameters file to use for all launched nodes')

    # SLAM Toolbox launch
    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('slam_toolbox'),
                'launch',
                'online_async_launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }.items()
    )

    # Nav2 launch using bringup_launch.py
    nav2_bringup_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                this_pkg_dir,
                'launch',
                'self_contained_nav_launch.py'
            ])
        ]),
        launch_arguments={
            'params_file': LaunchConfiguration('params_file'),
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        }.items()
    )
    return LaunchDescription([
        # Launch arguments
        use_sim_time_arg,
        declare_params_file_cmd,
        
        # Launch everything simultaneously - no artificial delays needed
        slam_toolbox_launch,
        nav2_bringup_launch,
    ])
