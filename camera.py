from manim import *
import numpy as np

class SpringMassOscillation3D(ThreeDScene):
    def construct(self):
        # Set up the 3D camera
        self.set_camera_orientation(phi=75 * DEGREES, theta=45 * DEGREES)

        # Create 3D axes
        axes = ThreeDAxes()
        self.add(axes)

        # Define positions and mass dimensions
        spring_top = np.array([0, 0, 2])       # fixed top of the spring
        mass_height = 0.5                      # height of the cylinder mass
        # At t=0, let displacement be: new_top = [0, 0, 0.5*cos(0)] = [0, 0, 0.5]
        initial_top = np.array([0, 0, 0.5])
        # Calculate mass center so that the top of the mass is at initial_top
        mass_center = initial_top - np.array([0, 0, mass_height / 2])

        # Create the mass (cylinder) oriented vertically
        mass = Cylinder(
            radius=0.3,
            height=mass_height,
            direction=DOWN,            # oriented vertically (top attached)
            resolution=(1, 2)
        )
        mass.rotate(90 * DEGREES, axis=RIGHT, about_point=mass.get_center())
        mass.move_to(mass_center)

        # Function to create a spring using Line3D between two points
        def create_spring(top, bottom, coils=20, radius=0.1):
            points = []
            num_points = coils * 20
            z_vals = np.linspace(top[2], bottom[2], num_points)
            for i, z in enumerate(z_vals):
                angle = 2 * np.pi * i / 20
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                points.append(np.array([x, y, z]))
            spring_line = Line3D(stroke_width=2)
            spring_line.set_points_as_corners(points)
            return spring_line

        # Create the initial spring connecting the fixed top to the mass top
        spring = create_spring(spring_top, initial_top)

        # Function to create a camera (cube with a label rotated 90° for proper 3D orientation)
        def make_camera(label, position):
            cam = Cube(side_length=0.3, fill_opacity=0.8, fill_color=GREY)
            cam.move_to(position)
            text = Text(label, font_size=20)
            text.rotate(90 * DEGREES, axis=OUT)
            text.rotate(-90 * DEGREES, axis=RIGHT)
            text.rotate(-90 * DEGREES, axis=DOWN)



            text.next_to(cam, OUT, buff=0.4)
            return VGroup(cam, text)

        cam1 = make_camera("Camera 1", [0, 0, -2])
        cam2 = make_camera("Camera 2", [5, 2.5, 0.5])
        cam3 = make_camera("Camera 3", [1.5, -1.5, 0.5])


        self.add(mass, spring, cam1, cam2, cam3)

        # Create a ValueTracker to drive the oscillation (time parameter)
        time_tracker = ValueTracker(0)

        # Updater for the mass:
        # Calculate new_top position based on simple harmonic motion,
        # then place the mass so that its top is at new_top.
        mass.add_updater(
            lambda m: m.move_to(
                np.array([0, 0, 0.5 * np.cos(2 * np.pi * 0.5 * time_tracker.get_value())])
                - np.array([0, 0, mass_height / 2])
            )
        )

        # Updater for the spring:
        # Redraw the spring from the fixed spring_top to the current top of the mass.
        spring.add_updater(
            lambda s: s.become(
                create_spring(
                    spring_top,
                    np.array([0, 0, 0.5 * np.cos(2 * np.pi * 0.5 * time_tracker.get_value())])
                )
            )
        )

        # Animate the time_tracker from 0 to 6 seconds (continuous oscillation)
        self.play(time_tracker.animate.set_value(6), run_time=6, rate_func=linear)

        # Clear updaters after the animation is complete
        mass.clear_updaters()
        spring.clear_updaters()
        self.wait(1)
