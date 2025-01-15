import bk7084 as bk
from bk7084.math import *

"""
Exercise 1: Textures & Shading
------------------------------

In the first exercise of this week, you will learn how to shade objects in a scene.
Shading is the task of simulating how much light reflects from the surface
into the camera.

Start by running this file. You should see a white sphere and a grayish plane. The
sphere represents the light source, and the plane is the object that will be shaded.

The goal of this assignment is to understand and observe the effect of different
shading parameters on the plane.

Explore the scene by moving the plane around with the following keys
then scroll down to the first task.

- [P, L] toggle between moving the plane or the light; P = plane, L = light;
- [Q, E] rotate the chosen object around the y-axis;
- [R, T] rotate the chosen object around the x-axis;
- [F, G] rotate the chosen object around the z-axis;
- [W, S] translate the chosen object along the y-axis, up (+Y) or down (-Y);
- [A, D] translate the chosen object along the x-axis, left (-X) or right (+X);
- [Z, X] translate the chosen object along the z-axis, forward (-Z) or backward (+Z);
- [I] reset all transformations;
"""

win = bk.Window()
win.set_title('BK7084 - Lab 3 - Textures & Shading [ex01]')
win.set_size(800, 800)
win.set_resizable(True)

app = bk.App()
camera = app.create_camera(pos=Vec3(2, 0, 8), look_at=Vec3(0, 0, 0), fov_v=60.0, background=bk.Color.ICE_BLUE)
camera.set_as_main_camera()

"""
This is where we create the light source and the plane. The light source is a point 
light represented by a sphere with a radius of 0.1.
The plane is a quad (quadrilateral, four sides) with a size of 4.0 x 4.0.

Task 1.1: Change the color of the light source to a different color and observe the effect.
"""
light, sphere = app.add_point_light(Vec3(0, 0, 5.2), bk.Color(0.8, 0.8, 0.8), show_light=True)
plane_mesh = bk.Mesh.create_quad(4.0, bk.Alignment.XY)

"""
As you have seen in the lecture, the material of an object determines how it's
visual appearance in the real world. In computer graphics, we try to express
the material of an object with a set of parameters that are easy to manipulate
and compute. 

The material is a collection of parameters that determine the color of the object.
In the framework, we use the bk.Material class to represent the material of an
object. In this exercise, we will use the following parameters:

- ambient:
   The ambient color simulates what the object looks like in ambient lighting,
   such as indirect sunlight. You'll notice that it does not change
   as you move the light source.

- diffuse: 
   This is the color of the object when it is lit by light sources in the scene.
   It changes as you move the light source, but does not change
   when you move the camera around. That is because it models the light
   that is reflected in a diffuse way: the light scatters in all directions.

- specular:
   This is the color of the light that is reflected into a specific direction.
   Unlike diffuse color, the specular lighting takes the camera position into account.

- shininess:
   This determines how sharp the specular reflections are.
   High shininess simulates the effect that all light-rays reflect into the same direction,
   which give sharper highlights. Lower shininess simulates light rays
   that shoot in many different directions, which means you have softer highlights.
  
The parameters above are the most important parameters for shading. More specifically,
we are using Phong illumination model where the color is computed per pixel.
There are different models that are more realistic (physically based rendering models), 
but we will not discuss them in this course.
"""
mat = bk.Material()

"""
Task 1.2: Change the color of ambient to a different color and observe the effect.
          Try to move the light source behind the plane (press L and then X)
          and observe the effect.
          
Tip: to change the color, use the bk.Color class. For example, to create a red color:
     bk.Color(1, 0, 0), where the first parameter is the red component, the second
     parameter is the green component, and the third parameter is the blue component.
     Be careful, the values should be between 0 and 1, not between 0 and 255. When
     you use the bk.Color class, you can also use the predefined colors, for example:
     bk.Color.RED, bk.Color.GREEN, bk.Color.BLUE, bk.Color.WHITE, bk.Color.BLACK, etc.
     The predefined colors are just shortcuts for the bk.Color class.
"""
# Uncomment the following line to change the color.
# mat.ambient = bk.Color(1, 0, 0)

"""
Task 1.3: Change the color of diffuse to a different color and observe the effect.
          Try to move the camera around. Does the shading change?
"""
# Uncomment the following line to change the color.
mat.diffuse = bk.Color(0.8, 0.8, 0.8)

"""
Task 1.4: Change the color of specular to a different color and observe the effect.

Remember that specular reflection is the light that reflects on the surface
in a mirror-like way.
Q1. Where would you expect to see this color on the object? 
Q2. When the specular color is black, what happens when you move the light source around? 
Q3. Is the appearance the same everywhere on the square when you
    remove the specular component? Why or why not?
"""
# Uncomment the following line to change the color.
# mat.specular = bk.Color(1.0, 0.0, 0.0)

"""
Task 1.5: Change the shininess to a different value and observe the effect.

The shininess determines how the reflected light is distributed. 

Q1. What happens when you increase the shininess?
Q2. What happens when you decrease the shininess?
"""
# mat.shininess = 32.0

plane_mesh.set_material(mat)

wall = app.add_mesh(plane_mesh)
wall.set_visible(True)

transform = Mat4.identity()
light_transform = app.get_transform(light)
is_plane = True


@app.event
def on_update(input, dt, t):
    global transform
    global is_plane

    if input.is_key_pressed(bk.KeyCode.Q):
        transform = transform * Mat4.from_rotation_y(-dt * 45, degrees=True)
    if input.is_key_pressed(bk.KeyCode.E):
        transform = transform * Mat4.from_rotation_y(dt * 45, degrees=True)
    if input.is_key_pressed(bk.KeyCode.R):
        transform = transform * Mat4.from_rotation_x(dt * 45, degrees=True)
    if input.is_key_pressed(bk.KeyCode.T):
        transform = transform * Mat4.from_rotation_x(-dt * 45, degrees=True)
    if input.is_key_pressed(bk.KeyCode.F):
        transform = transform * Mat4.from_rotation_z(dt * 45, degrees=True)
    if input.is_key_pressed(bk.KeyCode.G):
        transform = transform * Mat4.from_rotation_z(-dt * 45, degrees=True)
    if input.is_key_pressed(bk.KeyCode.W):
        transform = transform * Mat4.from_translation(Vec3(0, dt, 0))
    if input.is_key_pressed(bk.KeyCode.S):
        transform = transform * Mat4.from_translation(Vec3(0, -dt, 0))
    if input.is_key_pressed(bk.KeyCode.A):
        transform = transform * Mat4.from_translation(Vec3(-dt, 0, 0))
    if input.is_key_pressed(bk.KeyCode.D):
        transform = transform * Mat4.from_translation(Vec3(dt, 0, 0))
    if input.is_key_pressed(bk.KeyCode.Z):
        transform = transform * Mat4.from_translation(Vec3(0, 0, dt))
    if input.is_key_pressed(bk.KeyCode.X):
        transform = transform * Mat4.from_translation(Vec3(0, 0, -dt))
    if input.is_key_pressed(bk.KeyCode.I):
        transform = Mat4.identity()
    if input.is_key_pressed(bk.KeyCode.P):
        is_plane = True
    if input.is_key_pressed(bk.KeyCode.L):
        is_plane = False

    if is_plane:
        wall.set_transform(transform)
    else:
        light.set_transform(transform * light_transform)
        sphere.set_transform(transform * light_transform)


app.run(win)
