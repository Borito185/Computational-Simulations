import bk7084 as bk
from buildings import *
from components import material_basic_ground

"""
Exercise 04: Building Generation
--------------------------------

In the last exercise, we have learned how to construct a mesh with more complex
geometry. In this exercise, we will learn how to generate buildings with
different shapes and sizes.

In this exercise, we have provided you with a buildings.py file that contains
the Skyscraper, Highrise, and Office classes; a components.py file that
contains the methods to generate the components of a building; and a main.py
file that contains the code to generate the buildings.

# Classes

We've discussed the basics of classes and objects in the introduction assignment.
A quick recap: a class is like a blueprint to create objects.
The class describes what information the object should store (attributes) and
how you can interact with the object and its information (methods).

In this case, the Skyscraper class tells Python how to create a skyscraper
and every time a skyscraper is created, it is an instance of the Skyscraper class.
An important method in Python classes is the __init__ method:
this method is called when an instance of the class is created
and is often used to set up all the starting values of the object.

## Sub-classes

We can often re-use functionality from one class in another. For example:
We have a general Mesh class and we want to create a Mesh in the shape of a cube.
To be able to re-use the functionality of the Mesh class, we can create a Cube
class that is a sub-class of the Mesh class. The Cube class will *inherit*
the functionality of the Mesh class, meaning that it can do everything that the Mesh class can do.

# Back to the exercise

Before you start, check out the second line of the code at the top of this document.
It imports the buildings.py file. You can use everything defined in the buildings.py file
in this file. This is how we can reuse code in Python. You can also import
other Python files in the same way.

Task 1: Check out the Skyscraper class and the code that creates the skyscraper in buildings.py.
        Then run this file (main.py) and see what it looks like.
        
Task 2: Check out the components.py file. It contains the methods and classes
        to generate the components of a building. Recall that in the last two
        exercises, we have created a basic wall mesh and a wall mesh with a
        window. Here we just put them in a file so that we can reuse them.
        
        The classes in the components.py file are sub-classes of the Mesh class.
        That means they can be used in places where the program expects a Mesh class,
        for example, when you add a mesh to the scene:
        >>> wall = BasicWindowWall(max_width, max_width) # BasicWindowWall is a sub-class of Mesh
        >>> app.add_mesh(wall)                           # add_mesh expects a Mesh, so wall is a valid argument
        
        You can check out how these components are used in the buildings.py file
        in the Skyscraper class. You can also use them to create other buildings.

Final assignment: Use what you have learned to create your own signature building.
        Be creative and have fun!
"""

win = bk.Window()
win.set_title("BK7084 - Lab 4 - Building Generation [ex03]")
win.set_size(800, 800)
win.set_resizable(True)

app = bk.App()
camera = app.create_camera(
    pos=Vec3(18, 18, 26), look_at=Vec3(0, 0, 0), fov_v=60.0, background=bk.Color.ICE_BLUE
)
camera.set_as_main_camera()

app.add_directional_light(Vec3(-1, -1, -1), bk.Color(0.8, 0.8, 0.8))

skyscraper = Skyscraper(app, 5, 3)
skyscraper.building.set_transform(Mat4.identity())

highrise = Skyscraper(app, 1, 3)
highrise.building.set_transform(Mat4.from_translation(Vec3(6, 0, 0)))

office = Skyscraper(app, 2, 3)
office.building.set_transform(Mat4.from_translation(Vec3(-6, 0, 0)))

ground_mesh = bk.Mesh.create_quad(48, bk.Alignment.XY)
ground_mesh.set_material(material_basic_ground)
ground = app.add_mesh(ground_mesh)
ground.set_transform(Mat4.from_rotation_x(-90, True))
ground.set_visible(True)

# Variables to avoid key spamming
is_key_1_pressed = False
is_key_2_pressed = False

enable_backface_culling = True
enable_wireframe = False

app.enable_backface_culling(enable_backface_culling)
app.enable_wireframe(enable_wireframe)


@app.event
def on_update(input, dt, t):
    global enable_backface_culling
    global enable_wireframe
    global is_key_1_pressed
    global is_key_2_pressed

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


app.run(win)
