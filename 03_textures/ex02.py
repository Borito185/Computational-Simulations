import bk7084 as bk
from bk7084.math import *

"""
Exercise 2: Textures & Shading
------------------------------

Objects in the real world have lots of different colors that vary over the surface.
In computer graphics, we model this with textures. 
A texture is an image that is wrapped over the surface of an object.

The goal of this assignment is to understand and learn how to use textures while
shading objects in a scene.

Start by running this file. Just like in the previous exercise, you will see
a white sphere representing the light source, and a plane representing the object
that will be shaded. The only difference is that the plane now has a brick texture.
"""

win = bk.Window()
win.set_title('BK7084 - Lab 3 - Textures & Shading [ex02]')
win.set_size(1024, 1024)
win.set_resizable(True)

app = bk.App()

camera = app.create_camera(pos=Vec3(2, 0, 8), look_at=Vec3(0, 0, 0), fov_v=60.0, background=bk.Color.ICE_BLUE)
camera.set_as_main_camera()

light, sphere = app.add_point_light(Vec3(0, 0, 2.5), bk.Color(0.8, 0.8, 0.8), show_light=True)
plane_mesh = bk.Mesh.create_quad(4.0, bk.Alignment.XY)

"""
Here we create the material for the plane as in the previous exercise.
The only difference is that we now load a texture from a file and assign it
to the material. Just like in the previous exercise, we specify different
parameters for the material: ambient, diffuse, specular, and shininess.

Instead of one value for these parameters for the entire object,
we can also specify textures (images) for each of these parameters.
That way we can vary the parameters over the object.

Task 2.1: Run the program and explain why the plane is shaded with greenish color. 
"""
mat = bk.Material()
mat.diffuse = bk.Color(0.9, 0.8, 0.8)
mat.shininess = 32.0
mat.specular = bk.Color(0.0, 0.9, 0.0)
mat.ambient = bk.Color(0.8, 0.8, 0.8)

"""
Here we create a dictionary to store the textures we want to use for the material.

A dictionary is like a list, but instead of using indices,
we can use labels to store and retrieve objects.

For example, we can create a dictionary that stores the grades of Yang, Laura, and Steve:
>>> grades = {'Yang': 9, 'Laura': 9.5, 'Steve': 8}
We can add and retrieve entries by simply using brackets:
>>> grades['Anne'] = 8.5
>>> print(grades['Anne'])
"""
material_textures = {}

"""
Start with the diffuse texture. We load the texture from a file and assign it to 
the material. The texture is the stone_bricks_col.jpg file in the assets folder.

The function bk.res_path() resolves the path to the file relative to the current
python file. This is useful when you want to load files from a different folder.
You can also use the absolute path to the file, but this is not recommended.

Task 2.2: Try to load a different texture from the assets folder and observe the effect.

Hint: in the assets folder, all textures named with the suffix "_col" are diffuse textures.
But you can also load other textures, just to see what happens.
"""
material_textures["diffuse_texture"] = bk.res_path("./assets/stone_bricks_col.jpg")

"""
We can also use a texture to control the color of the specular highlights for each point
on the surface of the object.

Task 2.3: Load the specular texture "stone_bricks.refl.jpg", and see what happens.          
          
Hint: in the assets folder, all textures named with the suffix "_refl" are specular textures.
You are free to load other textures, just to see what happens.
          
Q1: What happens compared to the previous task? Why?
"""
material_textures["specular_texture"] = None

"""
Task 2.4: Just like what we did in the previous task, now load the shininess (glossiness) texture 
          from the assets folder and assign it to the material.
          
Hint: in the assets folder, all textures named with the suffix "_gloss" are shininess textures.
"""
material_textures["shininess_texture"] = None

"""
Our plane now has a diffuse texture, a specular texture, and a shininess texture.
Take a close look at the plane you will see that the plane is not that realistic.
Real brick walls have lots of bumps and cracks. Since we used a flat plane,
none of these small surface details show up.
How can we simulate these details without adding a lot of extra triangles?

We can use a normal texture to represent the bumps and dents of the surface. A normal texture 
is an image that stores the normal vectors of the surface. The normal vectors are the vectors 
that are perpendicular to the surface. By using a normal texture, we can control the direction 
of the surface normals for each point on the surface. This will make the surface look more realistic.

Task 2.5: Load the normal texture "stone_bricks_nrm.png" and observe the effect.
          What happens if you change the normal texture to "mosaic_tiles_nrm.png"?

Hint: in the assets folder, all textures named with the suffix "_nrm" are normal textures.
"""
material_textures["normal_texture"] = None

"""
Task 2.6: Now try to mix different textures together and observe the effect.

For example, you can try to load the diffuse texture "brickwall_col.jpg", the normal texture
"mosaic_tiles_nrm.png", the specular texture "stone_bricks_refl.jpg", and the shininess texture
"mosaic_tiles_gloss.png".
"""

"""
Task 2.7: Take the diffuse texture of the brick wall from the assets folder
          and try to draw a window on the image by modifying the it using an image editor.
          Don't forget to modify textures for the specular, shininess, and the normal texture. 
          For this task, you can manually modify the texture, for example using Photoshop,
          GIMP or Photopea (https://www.photopea.com/).
"""

"""
Extra task: Generate the normal map from your diffuse texture.
            See the link on the course website for more details.
"""

"""
We assign all the textures to the material. The material will later be assigned to the plane.
"""
mat.textures = material_textures

plane = bk.Mesh.create_quad(4.0, bk.Alignment.XY)
plane.set_material(mat)
wall = app.add_mesh(plane)
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
