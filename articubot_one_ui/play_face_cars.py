import time
import math

from tkinter import *
import random
import itertools



class FacePlayerCars():

    def __init__(self, root):


        self.width=1024
        self.height=600



        self.nomwidth = 800
        self.nomheight = 480

        self.eye_pos = 0
        self.squint_amount = 0


        self.eye_width = self.nom_x(100)
        self.eye_height = self.nom_y(280)
        self.blink_factor = 0.002
        self.x_centre = self.nom_x(400)
        self.y_centre = self.nom_y(300)
        self.iris_size = self.nom_x(150)
        self.pupil_size = self.nom_x(76)
        self.highlight_size = self.nom_x(20)
        self.highlight_offset = self.nom_x(25)
        self.eye_spacing = self.nom_x(310)



        self.left_centre = self.x_centre - self.eye_spacing/2
        self.right_centre = self.x_centre + self.eye_spacing/2
        self.eye_top = self.y_centre - self.eye_height/2
        self.eye_bottom = self.y_centre + self.eye_height/2
        self.leye_left = self.left_centre - self.eye_width/2
        self.leye_right = self.left_centre + self.eye_width/2
        self.reye_left = self.right_centre - self.eye_width/2
        self.reye_right = self.right_centre + self.eye_width/2


        self.tk = Frame(root)
        self.tk.pack(expand=True, fill="both")
        
        self.canvas = Canvas(self.tk, width=self.width, height=self.height)
        self.canvas.pack(anchor='nw')
        self.canvas.configure(bg='white')



        self.col_a = "#ff7b00"
        self.col_b = "#a65000"

        # Create eyes
        iris_colour = "deepskyblue2"




        self.iris_l = self.canvas.create_oval(self.left_centre - self.iris_size/2, 
                                                self.y_centre - self.iris_size/2, 
                                                self.left_centre + self.iris_size/2, 
                                                self.y_centre + self.iris_size/2,
                                                fill=iris_colour)

        

        self.pup_l = self.canvas.create_oval(self.left_centre - self.pupil_size/2, 
                                                self.y_centre - self.pupil_size/2, 
                                                self.left_centre + self.pupil_size/2, 
                                                self.y_centre + self.pupil_size/2,
                                                fill="black")
        self.highlight_l = self.canvas.create_oval(self.left_centre - self.highlight_size/2 + self.highlight_offset, 
                                self.y_centre - self.highlight_size/2 - self.highlight_offset, 
                                self.left_centre + self.highlight_size/2 + self.highlight_offset, 
                                self.y_centre + self.highlight_size/2 - self.highlight_offset,
                                fill="white",
                                outline="")

        self.iris_r = self.canvas.create_oval(self.right_centre - self.iris_size/2, 
                self.y_centre - self.iris_size/2, 
                self.right_centre + self.iris_size/2, 
                self.y_centre + self.iris_size/2,
                fill=iris_colour)


        self.pup_r = self.canvas.create_oval(self.right_centre - self.pupil_size/2, 
                                                self.y_centre - self.pupil_size/2, 
                                                self.right_centre + self.pupil_size/2, 
                                                self.y_centre + self.pupil_size/2,
                                                fill="black")

        self.highlight_r = self.canvas.create_oval(self.right_centre - self.highlight_size/2 + self.highlight_offset, 
                                self.y_centre - self.highlight_size/2 - self.highlight_offset, 
                                self.right_centre + self.highlight_size/2 + self.highlight_offset, 
                                self.y_centre + self.highlight_size/2 - self.highlight_offset,
                                fill="white",
                                outline="")

        # Create upper lids

        self.lid_ul_pts = [(self.nom_x(0),self.nom_y(-200)),
                            (self.nom_x(0),self.nom_y(-200)),
                            (self.nom_x(0),self.nom_y(150)),
                            (self.nom_x(0),self.nom_y(150)),
                            (self.nom_x(150),self.nom_y(130)),
                            (self.nom_x(280),self.nom_y(130)),
                            (self.nom_x(370),self.nom_y(150)),
                            (self.nom_x(400),self.nom_y(150)),
                            (self.nom_x(410),self.nom_y(100)),
                            (self.nom_x(400),self.nom_y(-200)),
                            (self.nom_x(400),self.nom_y(-200))]

        # self.lid_ul_pts = [(self.nom_x(0),self.nom_y(-200)),
        #                     (self.nom_x(0),self.nom_y(-200)),
        #                     (self.nom_x(0),self.nom_y(110)),
        #                     (self.nom_x(0),self.nom_y(110)),
        #                     (self.nom_x(150),self.nom_y(95)),
        #                     (self.nom_x(280),self.nom_y(95)),
        #                     (self.nom_x(370),self.nom_y(100)),
        #                     (self.nom_x(400),self.nom_y(150)),
        #                     (self.nom_x(400),self.nom_y(-200)),
        #                     (self.nom_x(400),self.nom_y(-200))]


        self.lid_ul_pts_closed = [(self.nom_x(0),self.nom_y(0)),
                            (self.nom_x(0),self.nom_y(0)),
                            (self.nom_x(0),self.nom_y(418)),
                            (self.nom_x(0),self.nom_y(418)),
                            (self.nom_x(100),self.nom_y(408)),
                            (self.nom_x(300),self.nom_y(408)),
                            (self.nom_x(400),self.nom_y(418)),
                            (self.nom_x(410),self.nom_y(418)),
                            (self.nom_x(400),self.nom_y(0)),
                            (self.nom_x(400),self.nom_y(0))]



        self.lid_ur_pts = [(self.nom_x(400),self.nom_y(-200)),
                            (self.nom_x(400),self.nom_y(-200)),
                            (self.nom_x(400),self.nom_y(150)),
                            (self.nom_x(420),self.nom_y(150)),
                            (self.nom_x(520),self.nom_y(130)),
                            (self.nom_x(680),self.nom_y(130)),
                            (self.nom_x(800),self.nom_y(150)),
                            (self.nom_x(800),self.nom_y(150)),
                            (self.nom_x(800),self.nom_y(-200)),
                            (self.nom_x(800),self.nom_y(-200))]

        self.lid_ur_pts_closed = [(self.nom_x(400),self.nom_y(0)),
                            (self.nom_x(400),self.nom_y(0)),
                            (self.nom_x(390),self.nom_y(418)),
                            (self.nom_x(400),self.nom_y(418)),
                            (self.nom_x(500),self.nom_y(408)),
                            (self.nom_x(700),self.nom_y(408)),
                            (self.nom_x(800),self.nom_y(418)),
                            (self.nom_x(800),self.nom_y(418)),
                            (self.nom_x(800),self.nom_y(0)),
                            (self.nom_x(800),self.nom_y(0))]


        self.lid_ul_shadow = self.canvas.create_polygon(self.lid_ul_pts, width=8, smooth=True, fill=self.col_a, outline=self.col_b)
        self.lid_ur_shadow = self.canvas.create_polygon(self.lid_ur_pts, width=8, smooth=True, fill=self.col_a, outline=self.col_b)
        self.lid_ul = self.canvas.create_polygon(self.lid_ul_pts, smooth=True, fill=self.col_a, outline="")
        self.lid_ur = self.canvas.create_polygon(self.lid_ur_pts, smooth=True, fill=self.col_a, outline="")


        # Create lower lids

        self.lid_ll_pts = [(self.nom_x(0),self.nom_y(550)),
                            (self.nom_x(0),self.nom_y(550)),
                            (self.nom_x(400),self.nom_y(550)),
                            (self.nom_x(400),self.nom_y(550)),
                            (self.nom_x(430),self.nom_y(420)),
                            (self.nom_x(400),self.nom_y(420)),
                            (self.nom_x(300),self.nom_y(410)),
                            (self.nom_x(100),self.nom_y(410)),
                            (self.nom_x(0),self.nom_y(420)),
                            (self.nom_x(0),self.nom_y(420))]


        self.lid_lr_pts = [(self.nom_x(400),self.nom_y(550)),
                            (self.nom_x(400),self.nom_y(550)),
                            (self.nom_x(800),self.nom_y(550)),
                            (self.nom_x(800),self.nom_y(550)),
                            (self.nom_x(800),self.nom_y(420)),
                            (self.nom_x(800),self.nom_y(420)),
                            (self.nom_x(700),self.nom_y(410)),
                            (self.nom_x(500),self.nom_y(410)),
                            (self.nom_x(400),self.nom_y(420)),
                            (self.nom_x(390),self.nom_y(420))]


        self.lid_ll_shadow = self.canvas.create_polygon(self.lid_ll_pts, width=6, smooth=True, fill=self.col_a, outline=self.col_b)
        self.lid_lr_shadow = self.canvas.create_polygon(self.lid_lr_pts, width=6, smooth=True, fill=self.col_a, outline=self.col_b)

        self.lid_ll = self.canvas.create_polygon(self.lid_ll_pts, smooth=True, fill=self.col_a, outline="")       


        self.lid_lr = self.canvas.create_polygon(self.lid_lr_pts, smooth=True, fill=self.col_a, outline="")










        
                                        
        self.counter = 0

    def update_image(self):


        self.tk.update()
        self.counter += 1

        self.set_pupil_centre('l', 140*self.eye_pos)
        self.set_pupil_centre('r', 140*self.eye_pos)

        self.set_squint(self.squint_amount)

        # if self.counter == 300:
        #     self.look_right()
        # elif self.counter == 400:
        #     self.look_straight()
        # elif self.counter == 700:
        #     self.look_left()
        # elif self.counter == 800:
        #     self.look_straight()
        # elif self.counter == 1000:
        #     # pass
        #     self.close_eyes()
        # elif self.counter == 1050:
        #     self.open_eyes()
        #     self.counter = 0


    def end_fullscreen(self, event=None):
        self.tk.attributes("-fullscreen", False)
        return "break"

    def set_pupil_centre(self, pupil, offset):
        if pupil == 'l':
            self.canvas.moveto(self.iris_l, self.left_centre - self.iris_size/2 + offset, self.y_centre-self.iris_size/2)
            self.canvas.moveto(self.pup_l, self.left_centre - self.pupil_size/2 + offset, self.y_centre-self.pupil_size/2)
            self.canvas.moveto(self.highlight_l, self.left_centre - self.highlight_size/2 + offset + self.highlight_offset, self.y_centre-self.highlight_size/2 - self.highlight_offset)
        else:
            self.canvas.moveto(self.iris_r, self.right_centre - self.iris_size/2 + offset, self.y_centre-self.iris_size/2)
            self.canvas.moveto(self.pup_r, self.right_centre - self.pupil_size/2 + offset, self.y_centre-self.pupil_size/2)
            self.canvas.moveto(self.highlight_r, self.right_centre - self.highlight_size/2 + offset + self.highlight_offset, self.y_centre-self.highlight_size/2 - self.highlight_offset)

    def look_left(self):
        self.set_pupil_centre('l',self.nom_x(-85))
        self.set_pupil_centre('r',self.nom_x(-85))

    def look_straight(self):
        self.set_pupil_centre('l',self.nom_x(0))
        self.set_pupil_centre('r',self.nom_x(0))

    def look_right(self):
        self.set_pupil_centre('l',self.nom_x(85))
        self.set_pupil_centre('r',self.nom_x(85))
    
    def close_eyes(self):
        self.canvas.coords(self.lid_ul_shadow, *itertools.chain.from_iterable(self.lid_ul_pts_closed))
        self.canvas.coords(self.lid_ur_shadow, *itertools.chain.from_iterable(self.lid_ur_pts_closed))
        self.canvas.coords(self.lid_ul, *itertools.chain.from_iterable(self.lid_ul_pts_closed))
        self.canvas.coords(self.lid_ur, *itertools.chain.from_iterable(self.lid_ur_pts_closed))

    def open_eyes(self):
        self.canvas.coords(self.lid_ul_shadow, *itertools.chain.from_iterable(self.lid_ul_pts))
        self.canvas.coords(self.lid_ur_shadow, *itertools.chain.from_iterable(self.lid_ur_pts))
        self.canvas.coords(self.lid_ul, *itertools.chain.from_iterable(self.lid_ul_pts))
        self.canvas.coords(self.lid_ur, *itertools.chain.from_iterable(self.lid_ur_pts))

    def set_squint(self, squint_amount):
        self.canvas.moveto(self.lid_ul_shadow, self.nom_x(-3), self.nom_y(-200 + 100*(squint_amount) -3 ))
        self.canvas.moveto(self.lid_ur_shadow, self.nom_x(400-3), self.nom_y(-200 + 100*(squint_amount) -3 ))
        self.canvas.moveto(self.lid_ul, self.nom_x(0), self.nom_y(-200 + 80*(squint_amount)))
        self.canvas.moveto(self.lid_ur, self.nom_x(400), self.nom_y(-200 + 80*(squint_amount)))


        self.canvas.moveto(self.lid_ll_shadow, self.nom_x(0-3), self.nom_y(380 + 50*(1-squint_amount) -3))
        self.canvas.moveto(self.lid_lr_shadow, self.nom_x(400-3), self.nom_y(380 + 50*(1-squint_amount) -3))
        self.canvas.moveto(self.lid_ll, self.nom_x(0), self.nom_y(380 + 50*(1-squint_amount)))
        self.canvas.moveto(self.lid_lr, self.nom_x(400), self.nom_y(380 + 50*(1-squint_amount)))



        # self.canvas.moveto(self.lid_ul_shadow, -3, -200 + 100*(squint_amount) -3 )
        # self.canvas.moveto(self.lid_ur_shadow, 400-3, -200 + 100*(squint_amount) -3 )
        # self.canvas.moveto(self.lid_ul, 0, -200 + 80*(squint_amount))
        # self.canvas.moveto(self.lid_ur, 400, -200 + 80*(squint_amount))


        # self.canvas.moveto(self.lid_ll_shadow, 0-3, 380 + 50*(1-squint_amount) -3)
        # self.canvas.moveto(self.lid_lr_shadow, 400-3, 380 + 50*(1-squint_amount) -3)
        # self.canvas.moveto(self.lid_ll, 0, 380 + 50*(1-squint_amount))
        # self.canvas.moveto(self.lid_lr, 400, 380 + 50*(1-squint_amount))
        # self.canvas.coords(self.lid_ul_shadow, *itertools.chain.from_iterable(self.lid_ul_pts))
        # self.canvas.coords(self.lid_ur_shadow, *itertools.chain.from_iterable(self.lid_ur_pts))
        # self.canvas.coords(self.lid_ul, *itertools.chain.from_iterable(self.lid_ul_pts))
        # self.canvas.coords(self.lid_ur, *itertools.chain.from_iterable(self.lid_ur_pts))

    def px_x(self,val):
        return math.floor(val*self.width)

    def px_y(self,val):
        return math.floor(val*self.height)

    def pc_x(self,val,nomwidth):
        return math.floor(val/nomwidth)

    def pc_y(self,val,nomheight):
        return math.floor(val/nomheight)

    def nom_x(self, val):
        return math.floor(val * self.width/self.nomwidth)

    def nom_y(self, val):
        return math.floor(val * self.height/self.nomheight)

    def set_left_eye_pts(self, ptA, ptB, ptC, ptD):
        self.pts[8] = ptD
        self.pts[9] = ptD
        self.pts[10] = ptC
        self.pts[11] = ptB
        self.pts[12] = ptA
        self.pts[13] = ptA

    def set_right_eye_pts(self, ptA, ptB, ptC, ptD):
        self.pts[2] = ptD
        self.pts[3] = ptD
        self.pts[4] = ptC
        self.pts[5] = ptB
        self.pts[6] = ptA
        self.pts[7] = ptA

    def update_values(self, eye_pos, squint_amount):
        self.eye_pos = eye_pos
        if (abs(self.eye_pos) < 0.2):
            self.eye_pos = 0

        self.squint_amount = squint_amount

        if (self.squint_amount < 0.2):
            self.squint_amount = 0




    def destroy(self):
        self.tk.destroy()
