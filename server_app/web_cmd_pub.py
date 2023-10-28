import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class WebCmdVelPublisher(Node):

    def __init__(self):
        super().__init__('web_cmd_vel_publisher')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.declare_parameter('scale_linear_x', 0.2)
        self.declare_parameter('scale_angular_yaw', 0.5)
        # Add other parameters as needed
        self.timer_period = 0.5
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.command = 'stop'

    def timer_callback(self):
        # print(f"Timer callback triggered! Command: {self.command}")
        msg = Twist()
        if self.command == 'forward':
            msg.linear.x = self.get_parameter('scale_linear_x').value
        elif self.command == 'backward':
            msg.linear.x = -self.get_parameter('scale_linear_x').value
        elif self.command == 'left':
            msg.angular.z = self.get_parameter('scale_angular_yaw').value
        elif self.command == 'right':
            msg.angular.z = -self.get_parameter('scale_angular_yaw').value
        elif self.command == 'stop':
            pass  # No movement
        # Add other conditions as required

        self.publisher_.publish(msg)

    def set_command(self, command):
        self.command = command


def main(args=None):
    rclpy.init(args=args)
    web_cmd_vel_publisher = WebCmdVelPublisher()
    rclpy.spin(web_cmd_vel_publisher)

    web_cmd_vel_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
