
from big_ol_pile_of_manim_imports import *


PI_CREATURE_DIR = "./svgs"


class Nabla(SVGMobject):
    CONFIG = {
    "color" : "#FF862F",
    "stroke_width" : 0,
    "stroke_color" : BLACK,
    "close_new_points":True,
    "fill_opacity" : 1.0,
    "propogate_style_to_family" : True,
    "height" : 3,
    "n_arc_anchors": 20

    }


    def __init__(self, mode = "plain", **kwargs):
        self.parts_named = False
        svg_file = os.path.join(PI_CREATURE_DIR, "Nabla.svg")
        SVGMobject.__init__(self, file_name = svg_file, **kwargs)

    def copy(self):
        copy_mobject = SVGMobject.copy(self)
        copy_mobject.name_parts()
        return copy_mobject

    def init_colors(self):
        SVGMobject.init_colors(self)
        if not self.parts_named:
            self.name_parts()

        self.eyes.set_fill(WHITE,opacity=1)
        self.eyes.set_stroke(BLACK, width=0.8)

        self.pupils.set_fill(BLACK,opacity=1)


        self.inner_body.set_stroke(color=WHITE, width=4)
        self.inner_body.set_fill(RED, opacity=1)


        self.left_hand.set_fill(color=None, opacity=0)
        self.right_hand.set_fill(color=None, opacity=0)

        self.right_hand.set_stroke(WHITE, width=3)
        self.left_hand.set_stroke(WHITE, width=3)


        self.mouth.set_fill(color=WHITE, opacity=1)
        self.mouth.set_stroke(color=BLACK ,width=1)


    def name_parts(self):


        self.eyes =  VGroup(*[ self.submobjects[0], self.submobjects[2]])
        self.pupils = VGroup(*[self.submobjects[1], self.submobjects[3]])


        self.inner_body = self.submobjects[6]
        self.left_hand = self.submobjects[4]

        self.right_hand = self.submobjects[5]
        self.mouth = self.submobjects[7]
        self.parts_named = True


    def look_to_cam(self):
        self.pupils.submobjects[0].move_to(self.eyes.submobjects[0].get_center())
        self.pupils.submobjects[1].move_to(self.eyes.submobjects[1].get_center())
        return self


    def look(self, direction):
        direction = direction/np.linalg.norm(direction)
        self.purposeful_looking_direction = direction
        for pupil, eye in zip(self.pupils.split(), self.eyes.split()):
            pupil_radius = pupil.get_width()/2.0
            eye_radius = eye.get_width()/2.0
            pupil.move_to(eye)
            if direction[1] < 0:
                pupil.shift(pupil_radius*DOWN/3)
            pupil.shift(direction*(eye_radius-(pupil_radius/0.67)))
            bottom_diff = eye.get_bottom()[1] - pupil.get_bottom()[1]
            if bottom_diff > 0:
                 pupil.shift(bottom_diff*UP)


    def look_at(self, point_or_mobject):
        if isinstance(point_or_mobject, Mobject):
            point = point_or_mobject.get_center()
        else:
            point = point_or_mobject
        self.look(point - self.eyes.get_center())
        return self



class ScaleMouth(Animation):

    CONFIG = {
        "rate_func": there_and_back,
        "run_time": 2,
        }

    def __init__(self, mobject,**kwargs):

        digest_config(self, kwargs, locals())   
        Animation.__init__(self, mobject, **kwargs)

    def update_mobject(self, alpha):

        alpha+= 0.7
        self.mobject.mouth.scale_in_place(-1.1*alpha)
        self.mobject.mouth.stretch_in_place(alpha, 0)


class RollEyes(Animation):

    CONFIG = {
        "rate_func": there_and_back,
        "run_time": 4,
        }


    def __init__(self, mobject,**kwargs):
        digest_config(self, kwargs, locals())   
        Animation.__init__(self, mobject, **kwargs)

    def update_mobject(self, alpha):

        alpha*=0.4
        self.mobject.look_at(UP+(alpha));


class NodHead(Transform):

    CONFIG = {
        "rate_func": there_and_back,
        "run_time": 4,
        }

    def __init__(self, mobject, angle ,about_point ,**kwargs):
        digest_config(self, kwargs)

        target = mobject.copy()
        self.about_point = about_point
        self.angle = angle*DEGREES

        target.rotate(self.angle, axis=OUT, about_point=self.about_point)
        Transform.__init__(self, mobject, target, **kwargs)



class WaveHands(Animation):

    CONFIG = {
        "rate_func": there_and_back,
        "run_time": 4,
        }

    def __init__(self, dell, **kwargs):

        digest_config(self, kwargs)
        Animation.__init__(self, dell,  **kwargs)


    def update_mobject(self, alpha):

        r = self.mobject.right_hand
        l = self.mobject.left_hand
        r.rotate(angle= (alpha * -35) *DEGREES, axis=OUT, about_point=self.mobject.get_center())
        l.rotate(angle= (-alpha * 35) *DEGREES, axis=OUT, about_point= self.mobject.get_center())

class AnimateNabla(Scene):

    def construct(self):

        nab = Nabla().scale(0.8).move_to(LEFT*6).look_at(UP)
        nab.mouth.scale(0.75)
        nab.rotate(angle=15*DEGREES, about_point=nab.get_critical_point(DOWN))
        nab.right_hand.rotate(angle= 20*DEGREES, axis=OUT, about_point=nab.get_center())
        move_in_frame = ApplyMethod(nab.move_to, ORIGIN,  rate_func=rush_from, run_time=2.5)
        
        self.add(nab)
        self.play(move_in_frame)

        head = CycleAnimation(NodHead(nab, angle=-40, about_point= nab.get_critical_point(DOWN)), start_up_time=0.1, wind_down_time=0.1)
        hands = CycleAnimation(WaveHands(nab), start_up_time=0.1, wind_down_time=0.1)
        eyes = CycleAnimation(RollEyes(nab), start_up_time=0.1, wind_down_time=0.1)
        mouth = CycleAnimation(ScaleMouth(nab))
        self.add( head,mouth, hands ,eyes)


        self.wait(10)