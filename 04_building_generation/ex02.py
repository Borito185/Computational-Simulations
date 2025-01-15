import bk7084 as bk
import numpy as np
from bk7084.math import *

"""
Exercise 02: Mesh Construction (continued)
------------------------------------------

In the last exercise, we have learned what a mesh is and how you can construct one.
In this exercise, we will learn some more advanced techniques
to construct a mesh with more complex geometry.
"""

win = bk.Window()
win.set_title("BK7084 - Lab 4 - Building Generation [ex02]")
win.set_size(800, 800)
win.set_resizable(True)

app = bk.App()
camera = app.create_camera(
    pos=Vec3(2, 0, 8), look_at=Vec3(0, 0, 0), fov_v=60.0, background=bk.Color.ICE_BLUE
)
camera.set_as_main_camera()

light = app.add_point_light(Vec3(0, 0, 5.2), bk.Color(0.8, 0.8, 0.8), show_light=False)

"""
Task 1: Construct a wall with a window.

Read the following text and code, and try to understand what is going on. You can also run the code
to see the result.

In this task, you will construct a wall with a window. The wall is a rectangle with a window in the middle.
The window is a square hole in the wall. The wall and the window are both made of triangles.

3 - - - - - - - - - - 2
| \              .  / |
| . \        .     /  |
|    \   .        /   |
|  .  7 - - - - 6     |
|     |         | .   |
|    .|         |     |
|     4 - - - - 5  .  |
|    /        .   \   |
|   /     .        \ .|
| /  .              \ |
0 - - - - - - - - - - 1 
"""
# As a reminder, here is how you construct a mesh:
mesh = bk.Mesh()

"""
The mesh is constructed by specifying the positions of the vertices, the texture coordinates of the vertices,
and the indices of the vertices that form each triangle.

We start by specifying the positions of the vertices. The positions are specified as a list of 3D vectors.
Here we use a NumPy array to help us construct the list of vectors.

NumPy is a Python library that allows us to do math with lists of numbers (arrays).
Say you have a list of grades for three students and a list of bonus points:
>>> grades = [80, 90, 70]
>>> bonus = [5, 10, 15]

If you wanted to add each student's bonus points to their grade, you would have to do it one by one:
>>> grades[0] = grades[0] + bonus[0]    
>>> grades[1] = grades[1] + bonus[1]
>>> grades[2] = grades[2] + bonus[2]

NumPy allows us to do this in one line:
>>> grades = np.array([80, 90, 70])
>>> bonus = np.array([5, 10, 15])
>>> grades = grades + bonus

To construct a NumPy array, we can use the `np.array` function. The first argument is a list of any numeric
type.
>>> np.array([1, 2, 3]) # This creates a 1d array with 3 elements
>>> np.array([[1, 2, 3], [4, 5, 6]]) # This creates an array of arrays, which is a 2d array

With NumPy array, we can do math with arrays. For example, we can add two arrays together:
>>> a = np.array([1, 2, 3])
>>> b = np.array([4, 5, 6])
>>> a + b
array([5, 7, 9])

We can also multiply an array with a number:
>>> a * 2
array([2, 4, 6])

We can also multiply two arrays together. This is called element-wise multiplication:
>>> a * b
array([4, 10, 18])

In our example generating the wall, we first create a array of 3D vectors, and then multiply it with a scalar
to scale the wall to the desired size.

Try to run the following code to see the result.

Remind yourself that the wall is a rectangle with a window in the middle. The window is a square hole in the wall.

Q1: Why do we repeat the 2nd row of vertices?
Hint: Think about how the texture coordinates are used to map the texture to the mesh.
"""
mesh.positions = np.array(
        [
            [-0.5, -0.5, 0.0], [0.5, -0.5, 0.0], [0.5, 0.5, 0.0], [-0.5, 0.5, 0.0],  # 1st row
            [-0.2, -0.2, 0.0], [0.2, -0.2, 0.0], [0.2, 0.2, 0.0], [-0.2, 0.2, 0.0],  # 2nd row
            [-0.2, -0.2, 0.0], [0.2, -0.2, 0.0], [0.2, 0.2, 0.0], [-0.2, 0.2, 0.0],  # 3rd row
        ]
    ) * 8.0
"""
Next, we specify the texture coordinates of the vertices. We don't need to do math with texture coordinates,
so we can just use a list of lists instead of a NumPy array to specify the texture coordinates.
"""
mesh.texcoords = [
    [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0, 1.0],
    [0.3, 0.3], [0.7, 0.3], [0.7, 0.7], [0.3, 0.7],
    [0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0, 1.0],
]
"""
Finally, we specify the indices of the vertices that form each triangle. We use a list of lists to specify the
indices.

Task 1.2: Try to draw the triangles on a piece of paper to understand how the indices are used to construct
          the triangles.
"""
mesh.triangles = [
    # This is the outer part of the wall
    [0, 1, 5], [0, 5, 4], [1, 2, 6], [1, 6, 5], [2, 3, 7], [2, 7, 6], [3, 0, 4], [3, 4, 7],
    # This is the inner part of the wall
    [8, 9, 10], [8, 10, 11],
]

# We create a material for the inner part of the wall
mat_inner = bk.Material()
mat_inner.textures = {
    "diffuse_texture": bk.res_path("../03_textures/assets/stone_bricks_col.jpg"),
    "normal_texture": bk.res_path("../03_textures/assets/stone_bricks_nrm.png"),
    "specular_texture": bk.res_path("../03_textures/assets/stone_bricks_refl.jpg"),
    "shininess_texture": bk.res_path("../03_textures/assets/stone_bricks_gloss.jpg"),
}

# We create a material for the outer part of the wall
mat_outer = bk.Material()
mat_outer.textures = {
    "diffuse_texture": bk.res_path("../03_textures/assets/mosaic_tiles_col.png"),
    "normal_texture": bk.res_path("../03_textures/assets/mosaic_tiles_nrm.png"),
    "specular_texture": bk.res_path("../03_textures/assets/mosaic_tiles_refl.png"),
    "shininess_texture": bk.res_path("../03_textures/assets/mosaic_tiles_gloss.png"),
}

"""
We specify the materials of the mesh.

If you still remember from the last exercise, we affect the appearance of the whole mesh by simply setting
the material of the mesh.

>>> mesh.set_material(mat) 

However, in this case, we want to use different materials for different parts of the mesh. To do this, we
need to first specify the materials for the whole mesh. Then we need to specify which part of the mesh uses
which material.
"""
mesh.materials = [mat_inner, mat_outer]
"""
A sub-mesh is a part of the mesh that uses the same material. 

We specify the sub-meshes of the mesh. A sub-mesh is a part of the mesh that uses a specific material. In
this case, we have two sub-meshes: one for the inner part of the wall, and one for the outer part of the wall.

To specify a sub-mesh, we need to specify the starting index of the triangle indices, and the ending index
of the triangle indices. NOTE: The ending index is not included in the sub-mesh.
The index is the index of the triangle, not the index of the vertex.

For example, if we have a mesh with 10 triangles, and we want to specify the first 5 triangles as a sub-mesh,
we need to specify the starting index as 0 and the ending index as 5. The ending index is exclusive, so the
sub-mesh will be:
               start  end   material index
>>> bk.SubMesh(0,     5,    0)

!!! IMPORTANT !!!
1. If you don't specify the sub-meshes, the whole mesh will be rendered with the first material in the list of
materials. In this case, the whole mesh will be rendered with the material of the inner part of the wall.

2. Between sub-meshes, there should be no overlapping triangles.

Task 1.3: Try to add another material to the mesh, and add another sub-mesh to the mesh.
"""
mesh.sub_meshes = [
    bk.SubMesh(0, 8, 1),
    bk.SubMesh(8, 10, 0),
]

# We add the mesh to the app
wall = app.add_mesh(mesh)
wall.set_visible(True)


transform = Mat4.identity()

# Variables to avoid key spamming
is_key_1_pressed = False
is_key_2_pressed = False

enable_backface_culling = True
enable_wireframe = False

app.enable_backface_culling(enable_backface_culling)
app.enable_wireframe(enable_wireframe)


@app.event
def on_update(input, dt, t):
    global transform
    global enable_backface_culling
    global enable_wireframe
    global is_key_1_pressed
    global is_key_2_pressed

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
    if input.is_key_pressed(bk.KeyCode.Key1):
        if not is_key_1_pressed:
            is_key_1_pressed = True
            enable_backface_culling = not enable_backface_culling
            app.enable_backface_culling(enable_backface_culling)
    if input.is_key_released(bk.KeyCode.Key1):
        is_key_1_pressed = False
    if input.is_key_pressed(bk.KeyCode.Key2):
        if not is_key_2_pressed:
            is_key_2_pressed = True
            enable_wireframe = not enable_wireframe
            app.enable_wireframe(enable_wireframe)
    if input.is_key_released(bk.KeyCode.Key2):
        is_key_2_pressed = False

    wall.set_transform(transform)


app.run(win)
