import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    package_dir = get_package_share_directory('mi_dron_sim')
    urdf_file = os.path.join(package_dir, 'urdf', 'prisma_dron.urdf')

    return LaunchDescription([
        # 1. Abrir Gazebo
        ExecuteProcess(cmd=['gazebo', '--verbose', '-s', 'libgazebo_ros_factory.so'], output='screen'),

        # 2. Publicar el estado del robot
         Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': open(urdf_file).read()}]
        ),

        # 3. Meter el prisma en Gazebo
        Node(package='gazebo_ros', executable='spawn_entity.py',
             arguments=['-entity', 'mi_prisma', '-file', urdf_file], output='screen'),
    ])
