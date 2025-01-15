import os.path as osp
import bk7084 as bk
from bk7084.math import *
from bk7084.geometry import Triangle, Ray
import numpy as np

# Setup window and add camera
window = bk.Window()
window.set_title('BK7084 - Lab 1 - Transformation [bonus]')
window.set_size(1024, 1024)
window.set_resizable(True)

# Set working directory to the folder where this file is located.
cwd = osp.dirname(osp.abspath(__file__))

app = bk.App()

camera = app.create_camera(Vec3(0, 0.0, 10.0), Vec3(0, 0, 0), 60.0)

# Create two materials for the triangle
mtl_red = bk.Material()
mtl_red.kd = Vec3(1, 0, 0)
mtl_green = bk.Material()
mtl_green.kd = Vec3(0, 1, 0)

# Create a triangle object (mesh) and ray object (mesh) for display
tri_mesh = bk.Mesh.create_triangle(Vec3(-2, -2, 1), Vec3(2, -2, 1), Vec3(0, 2, 1));
tri_mesh.materials = [mtl_red, mtl_green]
tri_obj = app.add_mesh(tri_mesh)
tri_obj.set_visible(True)

ray_obj = app.add_mesh(bk.Mesh.load_from(osp.join(cwd, '../assets/ray.obj')))
ray_obj.set_visible(True)
angle = (Vec3(4, 4, 1) - Vec3(0, -3, 2)).normalised.dot(Vec3(0, 1, 0))
ray_obj_rot_x = Mat4.from_rotation_x(angle)
ray_obj_trans = Mat4.from_translation(Vec3(0, -3, 2))

triangle = Triangle(Vec3(-2, -2, 1), Vec3(2, -2, 1), Vec3(0, 2, 1))
ray = Ray(Vec3(0, -3, 2), Vec3(4, 4, 1))
animate = True

"""
Assignment 1: Intersection
--------------------------

Please read the accompanying PDF file for an explanation of this assignment.

Your tasks:
1. Build mat_A, vec_b of the linear system.
2. Solve the linear system with NumPy's np.linalg.solve(A, b).
3. Implement the intersection conditions based on the solution.
"""
def intersect_ray_triangle(ray, tri):
    mat_A = Mat3()      # 1. Set up matrix A
    vec_b = Vec3()      # 1. Set up vector b
    vec_x = None        # 2. Solve the linear system

    return False        # 3. Implement the intersection conditions based on the solution
"""
If you have implemented everything correctly,
you should see the triangle turn red when it's intersected by the ray.
"""

ray_obj_transform = Mat4.identity()


@app.event
def on_update(input, dt, t):
    global animate
    global ray_obj_transform
    if input.is_key_pressed(bk.KeyCode.A):
        animate = not animate

    if input.is_key_pressed(bk.KeyCode.R):
        tri_obj.set_material(0)

    if input.is_key_pressed(bk.KeyCode.G):
        tri_obj.set_material(1)

    if animate:
        ray.direction = Mat3.from_rotation_y(dt * 90.0, True) * ray.direction
        if intersect_ray_triangle(ray, triangle):
            tri_obj.set_material(0)
        else:
            tri_obj.set_material(1)

        ray_obj_rot_y = Mat4.from_rotation_y(t * 90.0, True)
        ray_obj.set_transform(ray_obj_trans * ray_obj_rot_y * ray_obj_rot_x)


app.run(window)
