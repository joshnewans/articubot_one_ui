import rclpy
from rclpy.node import Node
import time

from tkinter import *
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

from articubot_one_ui.play_face_cars import FacePlayerCars
from articubot_one_ui.button_page import ButtonPage


class UiNode(Node):

    def __init__(self):
        super().__init__('ui_node')
        self.get_logger().info('Setting up UI...')

        # Configuration

        self.use_cmd_vel_for_face = True
        self.disable_cursor = True
        self.fullscreen = False


        # ROS Interactions

        self.joy_sub = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10)
        self.joy_sub  # prevent unused variable warning

        self.cmd_sub = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10)
        self.cmd_sub  # prevent unused variable warning

        self.motor_start = self.create_client(Empty, 'start_motor')
        if not self.motor_start.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('WARNING: start_motor service not available')

        self.motor_stop = self.create_client(Empty, 'stop_motor')
        if not self.motor_stop.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('WARNING: stop_motor service not available')
        
        self.motor_req = Empty.Request()

        self.client_futures = []


        # Build UI

        self.ttk = Tk()
        self.ttk.title("Bot UI")
        self.ttk.geometry("1024x600+0+0")

        if self.fullscreen:
            self.ttk.bind("<Escape>", self.end_fullscreen)
            self.ttk.attributes("-fullscreen",True)

        if self.disable_cursor:
            self.ttk.config(cursor="none")

        self.ttk.rowconfigure(0, weight=1)
        self.ttk.columnconfigure(0, weight=1)

        self.face_page = None
        self.button_page = None

        
        self.build_face_page()


    def send_start_motor_req(self):
        if self.motor_start.service_is_ready():
            print("Starting lidar...")
            self.client_futures.append(self.motor_start.call_async(self.motor_req))
        else:
            print("start_motor not ready!")

    def send_stop_motor_req(self):
        if self.motor_stop.service_is_ready():
            print("Stopping lidar...")
            self.client_futures.append(self.motor_stop.call_async(self.motor_req))
        else:
            print("stop_motor not ready!")

    def do_nothing_cb(self):
        print("Doing nothing!")


    def joy_callback(self, joy_vals):
        if self.button_page:
            self.button_page.process_joy(joy_vals)

        if self.face_page and not self.use_cmd_vel_for_face:
            self.face_page.update_values(joy_vals.axes[0], abs(joy_vals.axes[1]))

        if self.button_page and joy_vals.buttons[8]:
            self.destroy_button_page()
            self.build_face_page()

        if self.face_page and joy_vals.buttons[9]:
            self.destroy_face_page()
            self.build_button_page()
        return

    def cmd_vel_callback(self, cmd_vel):

        if self.face_page and self.use_cmd_vel_for_face:
            self.face_page.update_values(cmd_vel.angular.z/1.0, abs(cmd_vel.linear.x/1.0))

        return

    def update_image(self):

        if self.face_page:
            self.face_page.update_image()

        if self.button_page:
            self.button_page.update_image()

        return


    def end_fullscreen(self, event=None):
        self.ttk.attributes("-fullscreen", False)
        return "break"

    def build_button_page(self):
        self.button_page = ButtonPage(self.ttk)
        self.button_page.assign_button(self.button_page.b1, 4, "Y: Thing 1", self.do_nothing_cb)
        self.button_page.assign_button(self.button_page.b2, 3, "X: Thing 2", self.do_nothing_cb)
        self.button_page.assign_button(self.button_page.b3, 1, "B: Stop Lidar", self.send_stop_motor_req)
        self.button_page.assign_button(self.button_page.b4, 0, "A: Start Lidar", self.send_start_motor_req)

    def destroy_button_page(self):
        self.button_page.destroy()
        self.button_page = None

    def build_face_page(self):
        self.face_page = FacePlayerCars(self.ttk)

    def destroy_face_page(self):
        self.face_page.destroy()
        self.face_page = None


    def check_for_finished_calls(self):
        incomplete_futures = []
        for f in self.client_futures:
            if f.done():
                res = f.result()
            else:
                incomplete_futures.append(f)





def main(args=None):
    
    rclpy.init(args=args)

    ui_node = UiNode()

    # ui_node.send_stop_motor_req()

    # rate = face_player.create_rate(2)
    while rclpy.ok():
        rclpy.spin_once(ui_node)
        ui_node.check_for_finished_calls()
        ui_node.update_image()
        time.sleep(0.01)

    ui_node.destroy_node()
    rclpy.shutdown()


