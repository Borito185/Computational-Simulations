import os.path
import numpy as np
import bk7084 as bk
from bk7084.math import *

"""
Exercise 1: Combining transformations and animation
---------------------------------------------------

Start by opening the exercise. You'll see a car on a road.
When this exercise is completed, the car will drive along the path.

The learning goal of the exercise is to get more understanding
of transformations and how you can combine them.

The following code loads all the elements in the scene:
- The car
- The road
- Arrows pointing into the x, y, z directions.

Scroll down to the next comment...
"""
def load_meshes(app, filepath):
    if not os.path.exists(filepath):
        print("File not found: %s" % filepath)
        return
    if os.path.isdir(filepath):
        for root, dirs, files in os.walk(filepath):
            for filename in files:
                if filename.endswith(".obj"):
                    model = app.add_mesh(bk.Mesh.load_from(os.path.join(root, filename)))
                    model.set_visible(True)
                    model.set_transform(Mat4.from_translation(Vec3(0, -1, 0)))
    else:
        model = app.add_mesh(bk.Mesh.load_from(filepath))
        model.set_visible(True)
        model.set_tramsform(Mat4.from_translation(Vec3(0, -1, 0)))


win = bk.Window()
win.set_title('BK7084 - Lab 2 - Advanced Transformation [ex01]')
win.set_size(1024, 1024)
win.set_resizable(True)

app = bk.App()
camera = app.create_camera(pos=Vec3(0, 64, -24), look_at=Vec3(0, 0, -25), fov_v=60.0, near=0.1, far=1000.0)
camera.set_as_main_camera()

"""
We also create a second camera for Task 3.
You can active the second camera by pressing the 'C' key.
"""
camera2 = app.create_camera(pos=Vec3(-1, 0, 0), look_at=Vec3(0, 0, 0), fov_v=60.0, near=0.1, far=500.0)

"""
This is where the entire scene is loaded.
If you want a more detailed look,
uncomment the second line and comment the first line.
"""
# load_meshes(app, bk.res_path("./assets/simple_village/"))
load_meshes(app, bk.res_path("./assets/village/"))
car = app.add_mesh(bk.Mesh.load_from(bk.res_path("./assets/car.obj")))
car.set_visible(True)

cwd = os.path.dirname(os.path.abspath(__file__))
arrow_x_mesh = bk.Mesh.load_from(bk.res_path('../01_transformation/assets/arrow.obj'))
mtl_red = bk.Material()
mtl_red.kd = Vec3(1.0, 0.0, 0.0)
arrow_x_mesh.set_material(mtl_red)

arrow_y_mesh = bk.Mesh.load_from(bk.res_path('../01_transformation/assets/arrow.obj'))
mtl_green = bk.Material()
mtl_green.kd = Vec3(0.0, 1.0, 0.0)
arrow_y_mesh.set_material(mtl_green)

arrow_z_mesh = bk.Mesh.load_from(bk.res_path('../01_transformation/assets/arrow.obj'))
mtl_blue = bk.Material()
mtl_blue.kd = Vec3(0.0, 0.0, 1.0)
arrow_z_mesh.set_material(mtl_blue)

arrows = [
    app.add_mesh(arrow_x_mesh),
    app.add_mesh(arrow_y_mesh),
    app.add_mesh(arrow_z_mesh)
]

# x-axis
arrows[0].set_transform(Mat4.from_translation(Vec3(7.0, 0.0, 0.0)) * Mat4.from_scale(Vec3(0.2)) * Mat4.from_rotation_z(-90.0, degrees=True))
arrows[0].set_visible(True)

# y-axis
arrows[1].set_transform(Mat4.from_translation(Vec3(0.0, 7.0, 0.0)) * Mat4.from_scale(Vec3(0.2)))
arrows[1].set_visible(True)

# z-axis
arrows[2].set_transform(Mat4.from_translation(Vec3(0.0, 0.0, 7.0)) * Mat4.from_scale(Vec3(0.2)) * Mat4.from_rotation_x(90.0, degrees=True))
arrows[2].set_visible(True)

"""
Here, we set the initial transformation of the car.
The car is rotated by 180 degrees around the y axis.
In our world, the y axis points upwards, so the car is rotated around the vertical axis.

Notice that we give a parameter that tells the function that the angle is in degrees.
By default, the function expects the angle to be in radians (from 0 to 2pi).
"""
car_transform = Mat4.from_rotation_y(180.0, degrees=True)

"""
We also set an initial transformation matrix for the second camera for Task 3.
"""
camera_view_transform = app.get_transform(camera2)
camera_transform = Mat4.identity()

"""
The car gets an initial speed and a turn speed.
Assume 1 unit in the virtual world is 1 meter in the real world.
So, if the car is translated by [1, 0, 0], it will move 1 meter in the x direction.
"""
car_speed = 10.0 # m/s
car_turn_speed = 90.0 # degrees/s

"""
The path of the car is split up in segments.
Each segment is either a straight line or a turn.
Below, we define the segment types and the length of each segment.

Task 1: Familiarize yourself with the path
------------------------------------------
1. On a piece of paper, draw the path of the car. Don't worry about getting the distances exactly right.
   Observe what you do when you draw the path.
   What are the steps you take to turn the instructions into a drawing?
   E.g., for each element in the list, I look at the type of segment ...
2. Start the program and see if you can match the path you drew.
   We've positioned the camera in a top-view setting, so that positive x-axis points to the left
   and the negative z-axis points to the bottom of the screen.

Once you're done, continue reading the comments util you see Task 2.
"""
segment_type = ['straight', 'right_turn', 'straight', 'right_turn', 'straight', 'left_turn', 'straight', 'right_turn', 'straight']
segment_length = [7.0, 90.0, 20.5, 90.0, 8.5, 90.0, 36.0, 90.0, 10.0]

"""
We start with segment 0, which is the first segment if you count from 0.
"""
current_segment = 0

"""
And we keep track of the distance the car has covered in the current segment.
That way, we know when we should proceed to the next segment.
"""
distance_covered_in_segment = 0.0
turned_angle = 0.0

"""
We only start the animation when the user presses the space bar.
"""
start = False # Set to True if you want the car to start when you open the program.

"""
We also keep track of the current camera.
"""
current_camera = 0
is_key_c_pressed = False # This is used to make sure the camera doesn't switch too fast.

"""
The on_update function is called every time the screen is updated (every frame).
This happens every few milliseconds - as fast as your computer can handle.

The on_update function gets three parameters:
- input: this tells the update event what happened. For example, if a button has been pressed.
- dt: the change in time since the last update.
- t: the current time.

The dt parameter will tell you how much time passed since the last frame was rendered.
Using the speed defined above and dt, 
you can calculate how far the car moved since the last frame.

Scroll down for the task...
"""
@app.event
def on_update(input, dt, t):
    global is_key_c_pressed
    global current_camera
    global car_transform
    global camera_transform
    global current_segment
    global distance_covered_in_segment
    global turned_angle
    global start

    """
    Task 2: Animating the car
    -------------------------
    Animate the car, by adjusting car_transform.
    If you scroll down, you'll see that car_transform is applied to the car every frame.     
    It's important to know that the car is positioned at [0, 0, 0] at the start of each update.
    Fortunately, you know where the car was in a previous frame,
    because it is stored in car_transform.
    
    It your task to multiply car_transform with the correct transformation matrix
    to get it to the right location for the current frame.
    
    We've given you code that keeps track of the segment that you are in.
    Try to read through the code, to understand what it does.
    
    Then scroll down to the next TODO.
    """
    if input.is_key_pressed(bk.KeyCode.Space):
        start = True

    if input.is_key_pressed(bk.KeyCode.C):
        if not is_key_c_pressed:
            current_camera = (current_camera + 1) % 2
            if current_camera == 0:
                camera.set_as_main_camera()
            else:
                camera2.set_as_main_camera()
            is_key_c_pressed = True
    else:
        is_key_c_pressed = False
        
    if start and current_segment < len(segment_length):
        if segment_type[current_segment] == 'straight':
            distance_covered_in_segment += car_speed * dt
            if distance_covered_in_segment > segment_length[current_segment]:
                distance_covered_in_segment = 0.0
                current_segment += 1
        elif 'turn' in segment_type[current_segment]:
            turned_angle += car_turn_speed * dt
            if turned_angle > segment_length[current_segment]:
                turned_angle = 0.0
                current_segment += 1

        current_type = segment_type[current_segment]
        current_length = segment_length[current_segment]
        
        """
        TODO: Write the code that updates car_transform.
        When you're done, scroll down to Task 3.

        HINT: Use your drawing from before to figure out what transformations you need.

        HINT: You can use Mat4 to create transformation matrices:
        >>> Mat4.from_translation(Vec3(1, 2, 3))
        >>> Mat4.from_scale(Vec3(1, 2, 3))
        >>> Mat4.from_rotation_x(90.0, degrees=True)
        >>> Mat4.from_rotation_y(90.0, degrees=True)
        >>> Mat4.from_rotation_z(90.0, degrees=True)

        IMPORTANT: The car only starts the animation once you press the space bar.
        If you want it to start right away, change start to True in the code above.
    
        """
        car_transform_update = Mat4.identity()
        car_transform = car_transform_update * car_transform

    """
    Task 3: Follow the car with the camera
    --------------------------------------
    Use the transformation matrices that you had for the car to update the camera
    so that the camera follows the car.

    TODO: Update this transformation matrix, so that the camera follows the car.
          Scroll to the next TODO to make sure this update is applied to the camera.

    HINT: If you want the camera to get closer to the car,
          You can change the original camera_transform matrix above (Mat4.lookat_gl)
          to set the original position and viewing direction of the camera.
              
    HINT: If you get a strange stroboscope effect, you might have included the
          initial rotation of the car in the camera_transform when you update the camera.
    """
    camera_transform = Mat4.identity() * camera_view_transform

    camera2.set_transform(camera_transform)
    car.set_transform(car_transform)


app.run(win)
