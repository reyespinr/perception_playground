from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        ExecuteProcess(
            cmd=['rosbridge'],
            output='screen'
        ),
        Node(
            package='n1x_core',
            executable='web_cmd_pub',
            name='web_cmd_pub',
            output='screen'
        )
    ])
