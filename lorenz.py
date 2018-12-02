
from big_ol_pile_of_manim_imports import *


class LorenzAttractor(VMobject):

    CONFIG = {    
        "stroke_opacity": 1.0,
        "stroke_color": "FF8C00",
        "stroke_width":2,
        "sheen":   0, #0.04
        "sheen_direction": UR,

    }


    def __init__(self, iterations=5000, x=0.01, y=0.0, z=0.0,**kwargs):
        self.iterations = iterations
        self.x , self.y , self.z = x,y,z

        VMobject.__init__(self, **kwargs)


    def generate_points(self):

        a = 10.0
        b = 28.0
        c = 8.0/3.0

        x,y,z = self.x, self.y, self.z

        self.pts = []

        for _ in range(self.iterations):
            dt = 0.01
            dx = (a * (y - x))*dt
            dy = (x * (b - z) - y)*dt
            dz = (x * y - c * z)*dt;

            x = x + dx;
            y = y + dy;
            z = z + dz;

            self.pts.append(np.array([x,y,z]))


        self.set_points_smoothly(self.pts)
        self.scale(0.1)
        self.move_to(ORIGIN)


class Lorenz(ThreeDScene):

    CONFIG = {
        "should_apply_shading": False,
    }


    def construct(self):

        #rainbow = ["#9400D3","#4B0082","#0000FF","#00FF00","#FFFF00","#FF7F00","#FF0000"]
        #loren = LorenzAttractor().set_color_by_gradient(rainbow)

        loren = LorenzAttractor()
        anim =  ShowCreation(loren, run_time=10)
        self.set_camera_orientation(phi=-TAU/4, theta=None, distance=20.0, gamma=0)
        self.begin_ambient_camera_rotation(rate=0.05)
        self.play(anim)
        self.wait(1)
