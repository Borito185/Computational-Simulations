import os.path as osp
import bk7084 as bk
from bk7084.math import *
import numpy as np

window = bk.Window()
window.set_title('BK7084 - Lab 1 - Transformation [ex02]')
window.set_size(1024, 1024)
window.set_resizable(True)

app = bk.App()

camera = app.create_camera(Vec3(-100.0, 50.0, 0.0), Vec3(0, 0, 0), 60.0, far=500.0)

"""
Exercise 2: Hierarchical transformation
-----------------------------------------

For your final assignment, you will apply the transformations you created
and the knowledge about compositions to animate a solar system.

First start the program and see what happens.
You're supposed to see one shape that resembles a planet. This is the sun.
There are also an earth and a moon, but they are currently hidden by the sun.

The goal of this assignment is to use transformation matrices to
1. Place the earth and moon in the solar system.
2. Animate the earth and moon.

First, copy your finished transformation functions.
If you have copied these and restart the program,
you should see the sun, earth and moon, since they are scaled down and translated.

After you've copied the transformation functions, scroll down to Task 1.
"""
# TODO copy the completed functions from ex01
# Note that the functions below currently return the identity matrix
# this matrix does not change the shape at all.

def translate(x: float, y: float, z: float) -> Mat4:
    return Mat4.identity()

def rotate_x(angle: float) -> Mat4:
    return Mat4.identity()

def rotate_y(angle: float) -> Mat4:
    return Mat4.identity()

def rotate_z(angle: float) -> Mat4:
    return Mat4.identity()

def scale(x: float, y: float, z: float) -> Mat4:
    return Mat4.identity()

# Set working directory to the folder where this file is located.
cwd = osp.dirname(osp.abspath(__file__))

"""
Here, we load the planets, no need to adjust anything here yet.
"""
earth = app.add_mesh(bk.Mesh.load_from(osp.join(cwd, 'assets/earth.obj')))
earth.set_visible(True)

moon = app.add_mesh(bk.Mesh.load_from(osp.join(cwd, 'assets/moon.obj')))
moon.set_visible(True)

sun = app.add_mesh(bk.Mesh.load_from(osp.join(cwd, 'assets/sun.obj')))
sun.set_visible(True)


"""
The on_update function is called every time the screen is updated.
This happens every few milliseconds - as fast as your computer can handle.
That means you can use this function to update the solar system and animate it.

The on_update function gets three parameters:
- input: this tells the update event what happened, for example if a button has been pressed.
- dt: the change in time since the last update.
- t: the current time.

You will use the t parameter to animate your solar system.

Scroll down for the task.
"""
@app.event
def on_update(input, dt, t):
    """
    Task 1. Place the planets in the right place.
    ---------------------------------------------
    We've set up a few transformations to start with:
    the planets are scaled to have a realistic size and the earth and moon are translated.

    If this is not happening, you might have forgotten to copy your transformation functions above.
    
    Read on until you see the TODO comment.
    """
    earth_scale = scale(0.1, 0.1, 0.1)
    moon_scale = scale(0.2, 0.2, 0.2)
    sun_scale = scale(0.15, 0.15, 0.15)
    earth_translation = translate(40, 0, 0)
    moon_from_earth_translation = translate(10, 0, 0)

    """
    We then combine the transformations by multiplying them together
    and we set the transformation matrices for the planets.
    
    TODO: Complete the transformations, so that:
    - The earth is distance 40 away from the sun.
    - The moon is distance 10 away from the earth - hint: you can use the earth's transformation matrix.
    
    After you're done, continue with Task 2.
    """
    sun_transform = Mat4.identity()
    earth_transform = earth_translation
    moon_transform = moon_from_earth_translation

    """
    Task 2: Animate the planets
    ---------------------------
    Now, we want to animate the planets.
    
    We want the following animation:
    - The earth rotates around its own axis.
    - The moon rotates around its own axis.
    - The moon rotates around the earth.
    - The earth rotates around the sun.

    TODO: Update your transformations above to animate the planets.
    HINT: Start with a plan. Draw out the relationships on paper.
          You'll need to combine the transformations in the right way to get the desired result.
    HINT: Parameter t increases every frame.
          That means you can use it to animate the planets. 
    """

    """
    This is where the complete transformations are applied to the planets.
    """
    sun.set_transform(sun_transform * sun_scale)
    earth.set_transform(earth_transform * earth_scale)
    moon.set_transform(moon_transform * moon_scale)

    pass


app.run(window)
