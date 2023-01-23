import rclpy
from rclpy.node import Node
import time

from tkinter import *
import random

from sensor_msgs.msg import Joy


class FacePlayer(Node):

    def __init__(self):
        super().__init__('play_face')
        self.get_logger().info('Playing face...')

        self.subscription = self.create_subscription(
            Joy,
            'joy',
            self.joy_callback,
            10)
        self.subscription  # prevent unused variable warning


        self.width=800
        self.height=480

        # self.width=1920
        # self.height=1080

        # self.width=1024
        # self.height=576

        self.nomwidth = 800
        self.nomheight = 480

        self.pupil_x_l = 0
        self.pupil_y_l = 0
        self.pupil_x_r = 0
        self.pupil_y_r = 0
        self.idle_narrow = 0.6
        self.pupils_linked = False
        self.shut_request = False
        self.is_shut = False

        



        # self.eye_width = self.nom_x(200)
        # self.eye_height = self.nom_y(200)
        # self.blink_factor = 0.002
        # self.x_centre = self.nom_x(400)
        # self.y_centre = self.nom_y(240)
        # self.pupil_size = self.nom_x(50)
        # self.eye_spacing = self.nom_x(300)

        # self.brow_width = 100
        # self.brow_height = 50
        # self.brow_thick = 5


        self.eye_width = self.nom_x(240)
        self.eye_height = self.nom_y(240)
        self.blink_factor = 0.002
        self.x_centre = self.nom_x(400)
        self.y_centre = self.nom_y(260)
        self.pupil_size = self.nom_x(60)
        self.eye_spacing = self.nom_x(340)
        self.pupil_max = 80

        self.brow_width = 150
        self.brow_height = 76
        self.brow_thick = 8


        self.left_centre = self.x_centre - self.eye_spacing/2
        self.right_centre = self.x_centre + self.eye_spacing/2
        self.eye_top = self.y_centre - self.eye_height/2
        self.eye_bottom = self.y_centre + self.eye_height/2
        self.leye_left = self.left_centre - self.eye_width/2
        self.leye_right = self.left_centre + self.eye_width/2
        self.reye_left = self.right_centre - self.eye_width/2
        self.reye_right = self.right_centre + self.eye_width/2




        self.tk = Tk()
        
        self.canvas = Canvas(self.tk, width=self.width, height=self.height)
        self.tk.title("Drawing")
        self.tk.geometry("800x480+0+0")
        self.canvas.pack(anchor='nw')
        # self.canvas.configure(bg='ivory2')
        # self.canvas.configure(bg='rosybrown1')
        # self.canvas.configure(bg='pink2')
        self.canvas.configure(bg='lightpink')
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.tk.attributes("-fullscreen",True)
        self.tk.config(cursor="none")
        
        self.get_logger().info(f'{self.tk.winfo_screenwidth()}')


        self.eye_l = self.canvas.create_oval(self.leye_left, self.eye_top, self.leye_right, self.eye_bottom, width=2, fill="white")
        self.pup_l = self.canvas.create_oval(self.left_centre - self.pupil_size/2, 
                                                self.y_centre - self.pupil_size/2, 
                                                self.left_centre + self.pupil_size/2, 
                                                self.y_centre + self.pupil_size/2,
                                                fill="black")

        self.brow_l = self.canvas.create_arc(self.left_centre-self.brow_width,
                                                self.eye_top - self.brow_height,
                                                self.left_centre+self.brow_width,
                                                self.eye_bottom+self.brow_height,
                                                start=60,
                                                extent=180-60*2,
                                                width=self.brow_thick,
                                                style="arc")

        self.eye_r = self.canvas.create_oval(self.reye_left, self.eye_top, self.reye_right, self.eye_bottom, width=2, fill="white")
        self.pup_r = self.canvas.create_oval(self.right_centre - self.pupil_size/2, 
                                                self.y_centre - self.pupil_size/2, 
                                                self.right_centre + self.pupil_size/2, 
                                                self.y_centre + self.pupil_size/2,
                                                fill="black")

        self.brow_r = self.canvas.create_arc(self.right_centre-self.brow_width,
                                        self.eye_top - self.brow_height,
                                        self.right_centre+self.brow_width,
                                        self.eye_bottom+self.brow_height,
                                        start=60,
                                        extent=180-60*2,
                                        width=self.brow_thick,
                                        style="arc")

        
                                        
        self.counter = 0

    def update_image(self):


        self.tk.update()
        self.counter += 1

        self.set_pupil_centre('l', self.pupil_max*self.pupil_x_l, self.pupil_max*self.pupil_y_l)
        self.set_pupil_centre('r', self.pupil_max*self.pupil_x_r, self.pupil_max*self.pupil_y_r)

        if (self.shut_request and not self.is_shut):
            self.is_shut = True
            self.close_eyes()

        if (not self.shut_request and self.is_shut):
            self.is_shut = False
            self.open_eyes()

        # self.get_logger().info(f'{self.eye_pos}')

        # if self.counter == 300:
        #     self.look_right()
        # elif self.counter == 400:
        #     self.look_straight()
        # elif self.counter == 700:
        #     self.look_left()
        # elif self.counter == 800:
        #     self.look_straight()
        # elif self.counter == 1000:
        #     self.close_eyes()
        # elif self.counter == 1030:
        #     self.open_eyes()
        #     self.counter = 0


    def end_fullscreen(self, event=None):
        self.tk.attributes("-fullscreen", False)
        return "break"

    def set_pupil_centre(self, pupil, offset, y_offset=0):
        pupil_y = self.y_centre + y_offset if self.is_shut else self.y_centre - self.pupil_size/2 + y_offset
        if pupil == 'l':
            self.canvas.moveto(self.pup_l, self.left_centre - self.pupil_size/2 + offset, pupil_y)
        else:
            self.canvas.moveto(self.pup_r, self.right_centre - self.pupil_size/2 + offset, pupil_y)

    def look_left(self):
        self.set_pupil_centre('l',self.nom_x(-25))
        self.set_pupil_centre('r',self.nom_x(-25))

    def look_straight(self):
        self.set_pupil_centre('l',self.nom_x(0))
        self.set_pupil_centre('r',self.nom_x(0))

    def look_right(self):
        self.set_pupil_centre('l',self.nom_x(25))
        self.set_pupil_centre('r',self.nom_x(25))
    
    def close_eyes(self):
        self.canvas.scale(self.eye_l, self.left_centre, self.y_centre, 1, self.blink_factor)
        self.canvas.scale(self.pup_l, self.left_centre, self.y_centre, 1, self.blink_factor)
        self.canvas.scale(self.eye_r, self.right_centre, self.y_centre, 1, self.blink_factor)
        self.canvas.scale(self.pup_r, self.right_centre, self.y_centre, 1, self.blink_factor)

    def open_eyes(self):
        self.canvas.scale(self.eye_l, self.left_centre, self.y_centre, 1, 1/self.blink_factor)
        self.canvas.scale(self.pup_l, self.left_centre, self.y_centre, 1, 1/self.blink_factor)
        self.canvas.scale(self.eye_r, self.right_centre, self.y_centre, 1, 1/self.blink_factor)
        self.canvas.scale(self.pup_r, self.right_centre, self.y_centre, 1, 1/self.blink_factor)

    def px_x(self,val):
        return val*self.width

    def px_y(self,val):
        return val*self.height

    def pc_x(self,val,nomwidth):
        return val/nomwidth

    def pc_y(self,val,nomheight):
        return val/nomheight

    def nom_x(self, val):
        return val * self.width/self.nomwidth

    def nom_y(self, val):
        return val * self.height/self.nomheight

    def apply_deadzone(self, val_in, deadzone=0.2):
        if (abs(val_in) < deadzone):
            return 0
        elif (val_in > 0):
            return (val_in - deadzone)/(1-deadzone)
        else:
            return (val_in + deadzone)/(1-deadzone)


    def joy_callback(self, joy_vals):

        deadzone=0.2

        self.pupil_x_l = self.apply_deadzone(-joy_vals.axes[0])
        self.pupil_y_l = self.apply_deadzone(-joy_vals.axes[1])

        if (self.pupils_linked):
            self.pupil_x_r = self.pupil_x_l
            self.pupil_y_r = self.pupil_y_l
        else:
            self.pupil_x_r = self.apply_deadzone(-joy_vals.axes[3])
            self.pupil_y_r = self.apply_deadzone(-joy_vals.axes[4])


        # Apply narrows

        if (self.pupil_x_l >= 0):
            self.pupil_x_l = self.idle_narrow + (1-self.idle_narrow)*self.pupil_x_l
        else:
            self.pupil_x_l = self.idle_narrow + (1+self.idle_narrow)*self.pupil_x_l

        if (self.pupil_x_r <= 0):
            self.pupil_x_r = -self.idle_narrow + (1-self.idle_narrow)*self.pupil_x_r
        else:
            self.pupil_x_r = -self.idle_narrow + (1+self.idle_narrow)*self.pupil_x_r



        # else:
        #     self.pupil_x_r = -joy_vals.axes[2]

        #     if (abs(self.pupil_x_r) < deadzone):
        #         self.pupil_x_r = 0

        #     self.pupil_y_r = -joy_vals.axes[3]
        #     if (abs(self.pupil_y_r) < deadzone):
        #         self.pupil_y_r = 0

        self.shut_request = joy_vals.buttons[0] == 1

        return




def main(args=None):
    
    rclpy.init(args=args)

    face_player = FacePlayer()


    rate = face_player.create_rate(2)
    while rclpy.ok():
        rclpy.spin_once(face_player)

        face_player.update_image()

        # cv2.waitKey(2)
        time.sleep(0.01)


    tk.mainloop()
    face_player.destroy_node()
    rclpy.shutdown()


