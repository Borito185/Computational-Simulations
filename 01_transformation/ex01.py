import os.path as osp
import bk7084 as bk
from bk7084.math import *
import numpy as np
import math

window = bk.Window()
window.set_title('BK7084 - Lab 1 - Transformation [ex01]')
window.set_size(1024, 1024)
window.set_resizable(True)

app = bk.App()

camera = app.create_camera(Vec3(-15.0, 8.0, 0.0), Vec3(0, 0, 0), 60.0)

"""
Exercise 1: Basic transformation
--------------------------------

Make sure that you have activated the compsim environment in Visual Studio Code
In the terminal, you should see (compsim) before the prompt, otherwise type:
$ conda activate compsim

In this first exercise, you will create transformation matrices from scratch.
If you succeed, you can control a virtual car with your keyboard when you run this file:
[up, down, left, right, M, N] translate the car forward, backward, left, or right, up, down;
[X] rotate the car 45 degrees around the x-axis;
[Y] rotate the car 45 degrees around the y-axis;
[Z] rotate the car 45 degrees around the z-axis;
[S] scale the car to 90%;
[R] reset the car to its original position;
[esc] close the window (faster than clicking the close button).

Please read the instructions for week 1 on bk7084.github.io
for an introduction and reference to complete this assignment.

Your tasks:
Task 1. Build transformation matrices (do NOT use built-in functions):
  a. translation matrix,
  b. rotation matrices,
  c. scaling matrix.
Task 2. Once the transformation matrices are complete, you can control the car with your keyboard.

Note, angles are typically passed in radians for functions such as cosine and sine.
To convert from degrees to radians use:
>>> math.radians(angle_in_degrees)


Scroll down to complete the tasks. Each task is denoted with "TODO: ...".
"""

"""
This line of code *def*ines a function called translate.
The translate function gets three parameters: x, y, and z.
It is typical in code to explain what a function is in a comment below
the function definition. This is called a docstring and it also specifies 
the input (Args) and output of the function (Returns).

Scroll to the first TODO to complete the translate function.
"""
def translate(x: float, y: float, z: float) -> Mat4:
    """
    Creates a translation matrix.

    Args:
        x (float): Translation along the x-axis.
        y (float): Translation along the y-axis
        z (float): Translation along the z-axis

    Returns:
        Mat4
    """
    # TODO Task 1a: complete this matrix
    mat = Mat4(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    )
    return mat


def rotate_x(angle: float) -> Mat4:
    """
    Creates a rotation matrix around the x-axis.

    Args:
        angle (float): Rotation angle in degrees.

    Returns:
        Mat4
    """
    # TODO Task 1b: complete this matrix
    # hint: you can compute cos and sin with np.cos(angle) and np.sin(angle)
    mat = Mat4(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    )
    return mat


def rotate_y(angle: float) -> Mat4:
    """
    Creates a rotation matrix around the y-axis.

    Args:
        angle (float): Rotation angle in degrees.

    Returns:
        Mat4
    """
    # TODO Task 1b: complete this matrix
    # hint: you can compute cos and sin with np.cos(angle) and np.sin(angle)
    mat = Mat4(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    )
    return mat


def rotate_z(angle: float) -> Mat4:
    """
    Creates a rotation matrix around the z-axis.

    Args:
        angle (float): Rotation angle in degrees.

    Returns:
        Mat4
    """
    # TODO Task 1b: complete this matrix
    # hint: you can compute cos and sin with np.cos(angle) and np.sin(angle)
    mat = Mat4(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    )
    return mat


def scale(x: float, y: float, z: float) -> Mat4:
    """
    Creates a scaling matrix.

    Args:
        x (float): Scaling factor along x-axis.
        y (float): Scaling factor along y-axis.
        z (float): Scaling factor along z-axis.

    Returns:
        Mat4
    """
    # TODO Task 1c: complete this matrix
    mat = Mat4(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ]
    )
    return mat


"""
You don't need to change the code below to finish the assignment.
"""
# Set working directory to the folder where this file is located.
cwd = osp.dirname(osp.abspath(__file__))
car = app.add_mesh(bk.Mesh.load_from(osp.join(cwd, 'assets/car.obj')))
car.set_visible(True)

# grid = Grid(origin=Vec3(0.0, -1.17, 0.0), axis_alignment=AxisAlignment.XZ, axis_marker=True)
arrow_x_mesh = bk.Mesh.load_from(osp.join(cwd, 'assets/arrow.obj'))
mtl_red = bk.Material()
mtl_red.kd = Vec3(1.0, 0.0, 0.0)
arrow_x_mesh.set_material(mtl_red)

arrow_y_mesh = bk.Mesh.load_from(osp.join(cwd, 'assets/arrow.obj'))
mtl_green = bk.Material()
mtl_green.kd = Vec3(0.0, 1.0, 0.0)
arrow_y_mesh.set_material(mtl_green)

arrow_z_mesh = bk.Mesh.load_from(osp.join(cwd, 'assets/arrow.obj'))
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

car_transform = Mat4.identity()

@app.event
def on_update(input, dt, t):
    global car_transform

    if input.is_key_pressed(bk.KeyCode.Up):
        car_transform = car_transform * translate(0.5, 0.0, 0.0)

    if input.is_key_pressed(bk.KeyCode.Down):
        car_transform = car_transform * translate(-0.5, 0.0, 0.0)

    if input.is_key_pressed(bk.KeyCode.N):
        car_transform = car_transform * translate(0.0, 0.5, 0.0)

    if input.is_key_pressed(bk.KeyCode.M):
        car_transform = car_transform * translate(0.0, -0.5, 0.0)

    if input.is_key_pressed(bk.KeyCode.Left):
        car_transform = car_transform * translate(0.0, 0.0, -0.5)

    if input.is_key_pressed(bk.KeyCode.Right):
        car_transform = car_transform * translate(0.0, 0.0, 0.5)

    if input.is_key_pressed(bk.KeyCode.X):
        car_transform = car_transform * rotate_x(15)

    if input.is_key_pressed(bk.KeyCode.Y):
        car_transform = car_transform * rotate_y(15)

    if input.is_key_pressed(bk.KeyCode.Z):
        car_transform = car_transform * rotate_z(15)

    if input.is_key_pressed(bk.KeyCode.S):
        car_transform = car_transform * scale(0.9, 0.9, 0.9)

    if input.is_key_pressed(bk.KeyCode.R):
        car_transform = Mat4.identity()

    car.set_transform(car_transform)


app.run(window)
