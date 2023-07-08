import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
import time

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.declare_parameter('bot_list', ['tb_1','tb_2'])
        self.bot_list = self.get_parameter('bot_list').get_parameter_value().string_array_value
        self.current_bot = 0
        print(self.bot_list[self.current_bot])

        self.linear_map = {
            'x': 1,
            'y': -1,
            'z': -1
        }

        self.angular_map = {
            'roll': -1,
            'pitch': -1,
            'yaw': 0
        }

        self.button_map = {
            'enable': 5,
            'switch': 3,
        }


        self.publisher = []
        for i in self.bot_list:
            p = self.create_publisher(Twist, "/"+i+"/cmd_vel", 10)
            self.publisher.append(p)

        self.create_subscription(Joy, '/joy', self.joy_cb, 10)


    def joy_cb(self, msg):
        if(msg.buttons[self.button_map['switch']]):
            self.current_bot += 1
            if(self.current_bot >= len(self.bot_list)):
                self.current_bot = 0
            print(f"switch to {self.bot_list[self.current_bot]} !!")
            time.sleep(1)

        elif(msg.buttons[self.button_map['enable']]):
            vel_msg = Twist()
            vel_msg.linear.x = msg.axes[self.linear_map['x']]
            vel_msg.angular.z = msg.axes[self.angular_map['yaw']]
            self.publisher[self.current_bot].publish(vel_msg)
        
        else:
            for i in self.publisher:
                i.publish(Twist())

def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()