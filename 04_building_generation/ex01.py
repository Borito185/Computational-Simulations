import bk7084 as bk
import numpy as np
from bk7084.math import *

"""
Exercise 01: Mesh Construction
-------------------------------

In this exercise, you will learn how to construct a mesh from scratch.

Start by running this file. You should only see a white sphere and a grey plane. The sphere represents
the light source, and the plane represents the wall. You can use the mouse to rotate the camera, and
use the keyboard to move the camera around. It's the same as the previous exercise. Except this time,
you can only control the plane. 

Try to move the camera around and observe the plane. You will notice that the plane is not visible from
the back. This is because we have enabled backface culling. Backface culling is a technique used in
computer graphics to improve rendering performance. It works by discarding the faces that are not visible
to the camera. In our framework, backface culling is enabled by default. You can toggle it on and off by
pressing the `1` key on your keyboard.

Scroll down to the first task.
"""

win = bk.Window()
win.set_title("BK7084 - Lab 4 - Building Generation [ex01]")
win.set_size(800, 800)
win.set_resizable(True)

app = bk.App()
camera = app.create_camera(pos=Vec3(2, 0, 8), look_at=Vec3(0, 0, 0), fov_v=60.0, background=bk.Color.ICE_BLUE)
camera.set_as_main_camera()

light = app.add_point_light(Vec3(0, 0, 5.2), bk.Color(0.8, 0.8, 0.8), show_light=True)

"""
What is a mesh?

A mesh is a way to represent 3D objects. Because most interactions with objects happen
on the outer surface (e.g. light bounces, collisions), we often only encode the surface of a 3D object.
This is done by gluing together flat pieces of surface, typically triangles.
These flat pieces of surface are called faces.
Each face is defined by its corners (vertices) and the edges connecting the corners.

In more detail:

- Vertex: A vertex is a point in 3D space. It's the most basic component of a mesh.
          It can have different attributes such as position, normal, texture coordinate,
          color, etc.

- Edge: An edge is a line segment that connects two vertices (Not used in the exercise).

- Face: A face is a flat surface that connects any number of vertices. When each face
        is a triangle, the mesh is also called a triangle mesh.
        
For example, a square can be represented by a mesh with four vertices, four edges, and
one face. A cube can be represented by a mesh with eight vertices, twelve edges, and
six faces.

Even though faces can be any polygon, triangle meshes are the most common type of mesh
used in computer graphics. This is because triangle meshes are simple, efficient, and
flexible.

Take the example of a square again. A square can be represented by a mesh with four
vertices, four edges, and one face. However, it can also be represented by a mesh with
six vertices, six edges, and two faces. Shown below is the same square represented by

O - - - - O
|         |
|         |
|         |
O - - - - O

O - - -  O O
|      / / |
|    / /   |
|  / /     |
O  O - - - O

As you can see, the two added vertices are shared by the two faces. Now instead of
listing the repeated vertices again for each face, we use something called
indices. Think of indices as shortcuts to the actual vertices.
Instead of writing out the position of each vertex for each face (3x2=6 positions), we can just
keep a list of vertex positions (4 positions) and the faces refer to the vertices by their
indices. For example, the square above can be represented by the following indices:

3 - - - - 2
|      /  |
|    /    |
|  /      |
0 - - - - 1

To construct the square, we can use the following indices:

[[0, 1, 2], [0, 2, 3]]

This tells us to connect the vertices with indices 0, 1, and 2 to form the first face,
and connect the vertices with indices 0, 2, and 3 to form the second face.

Now that you know what a mesh is, let's construct one from scratch.

Task 1: Construct a wall

Read the code below and try to understand what each line does.
- Adjust the positions and see what happens.
- Try to create a square with the same vertices, but using a different set of faces.

Hint: In our framework, `bk.Mesh.positions` corresponds to the position attribute of
      each vertex, `bk.Mesh.texcoords` corresponds to the texture coordinate attribute of
      each vertex, and `bk.Mesh.triangles` corresponds to the indices of the vertices, which
      are used to construct triangle faces.
      
      By pressing the `2` key on you keyboard, you can switch between the wireframe and
      solid mode. This will help you understand the structure of the mesh.
"""
# We start by creating a mesh object, which will store all the information about the mesh.
mesh = bk.Mesh()

# Next, we need to specify the positions of the vertices. We do this by setting the `positions`
# attribute of the mesh. The positions are specified as a list of 3 floats for each vertex.
mesh.positions = [[-3.0, -3.0, 0.0], [3.0, -3.0, 0.0], [3.0, 3.0, 0.0], [-3.0, 3.0, 0.0]]

# Next, we need to specify the texture coordinates of the vertices. We do this by setting the
# `texcoords` attribute of the mesh. The texture coordinates are specified as a list of 2 floats
# for each vertex.
mesh.texcoords = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0, 1.0]]

# Finally, we need to specify the indices of the vertices that form each face. We do this by setting
# the `triangles` attribute of the mesh. The indices are specified as a list of 3 integers for each
# face.
mesh.triangles = [[0, 1, 3], [1, 2, 3]]

"""
Task 2: Add textures to the wall.

Now that we have a wall, let's add some textures to it. We will use the same textures as the previous
exercise. The textures are already provided in the `assets` folder of last exercise. You can use the 
`bk.res_path` function to get the absolute path of the texture files.
"""
mat = bk.Material()
mat.textures = {
     "diffuse_texture": bk.res_path("./../03_textures/assets/stone_bricks_col.jpg"),
     "normal_texture": bk.res_path("./../03_textures/assets/stone_bricks_nrm.png"), 
     "specular_texture": bk.res_path("./../03_textures/assets/stone_bricks_gloss.jpg"),   
     "shininess_texture": bk.res_path("./../03_textures/assets/stone_bricks_refl.jpg"), 
}
mesh.set_material(mat)

# Finally, we add the mesh to the app and set it to be visible.
wall = app.add_mesh(mesh)
wall.set_visible(True)

"""
Task 3: Add a hexagon (six-sided face) to the scene.

Now that you know how to construct a mesh, let's add a hexagon to the scene.
The simplest way to construct a hexagon from triangles is to draw a dot in the center of the hexagon
and draw six lines from the center to the vertices of the hexagon.
You can also be creative and use other triangulations.

Hint: Draw a hexagon on a piece of paper and label the vertices. Then, use the same method as above
      to construct the mesh.
      
      You can set the wall to be invisible by calling `wall.set_visible(False)`.
      
      You can create a list of vertices by using the following code:
      >>> positions = []
      >>> for i in range(6):
      >>>     positions.append([x, y, z])
      
      Then you can set the positions of the vertices by calling `mesh.positions = positions`.
"""

positions = []
texcoords = []

for i in range(6):
    c = - np.pi + (1/3) * i * np.pi
    positions.append([np.cos(c) * 3, np.sin(c) * 3, 1])
    texcoords.append([(np.cos(c) + 1) / 2, (np.sin(c) + 1) / 2])

hexagon_mesh = bk.Mesh()

hexagon_mesh.positions = positions
hexagon_mesh.texcoords = texcoords
hexagon_mesh.triangles = [[0,1,2], [2,3,4], [4,5,0], [0,2,4]]

# Uncomment the following lines once you have completed the above TODOs.
hexagon_mesh.set_material(mat)
hexagon = app.add_mesh(hexagon_mesh)
hexagon.set_visible(True)

# TODO: Set the transform of the hexagon to make it possible to manipulate with the keyboard.
#       Set the transform after the wall.set_transform(transform) line, at the end of the on_update function.

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
    hexagon.set_transform(transform)


app.run(win)
