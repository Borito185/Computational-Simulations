import random

from bk7084.math import *
from components import *


"""
This file contains the Skyscraper, Highrise, and Office classes.
These classes are used to generate buildings with different shapes and sizes.
The Skyscraper class is already implemented for you as an example.
You will need to implement the Highrise and Office classes yourself.

A building is made up of multiple components. Each component is a mesh. For
example, a skyscraper is made up of multiple floors, walls, and windows. Each
floor, wall, and window is a component. To generate a building, we need to
generate each component and place them in the correct position. 
 
But how do we place each component in the correct position? Of course, we can
place each component manually. But what if we want to translate the whole
building? We will need to translate each component individually. This is
tedious and error-prone.

Recall what we have learned in the hierarchy lecture, how do we construct the 
solar system? We parent each planet to the sun, and moon to each planet by 
multiplying the transformation of the parent right before the transformation
of the child. This way, all the children will be transformed correctly when
the parent is transformed.
 
We can do the same thing here. We can parent each component to a base 
component and only transform the base component. This way, all the children 
will be transformed correctly when the base component is transformed. This
time, we will use the app.spawn_building() function to spawn a base component
for us. The app.spawn_building() function will spawn a base component with
nothing in it. You can then parent other components to this base component.

Check out the `self.building` variable in the Skyscraper class. It is the base
component that we will use to parent other components. Go back to the main.py
file and you will see that we apply a transformation to the self.building
component. This transformation will be applied to all the children of the
self.building component. This is how we can translate the whole building.
"""


class Skyscraper:
    """A basic skyscraper class that procedurally generates
    a skyscraper given a number of floors and width.

    Args:
        app (bk.App):
            The app instance.
        num_floors (int):
            Number of floors to generate.
        max_width (float):
            The maximum width for each component.
    """

    def __init__(self, app, num_floors, max_width):
        self.num_floors = num_floors
        # Spawn the building and save the reference to the building
        self.building = app.spawn_building()
        self.building.set_visible(True)
        for i in range(self.num_floors):
            # To place each floor higher than the previous one, we parent all
            # components to one 'base' component (floor1, see below). Then we
            # only have to move the base component up higher and the framework
            # takes care of the rest.
            floor1 = app.add_mesh(
                BasicFloor(max_width, max_width), parent=self.building
            )
            # Place the base component higher each time (i)
            floor1.set_transform(Mat4.from_translation(Vec3(0, max_width * i, 0)))
            floor1.set_visible(True)
            floor2 = app.add_mesh(BasicFloor(max_width, max_width), parent=floor1)
            floor2.set_transform(Mat4.from_translation(Vec3(0, max_width, 0)))
            floor2.set_visible(True)
            wall1 = app.add_mesh(BasicWindowWall(max_width, max_width), parent=floor1)
            wall1.set_transform(
                Mat4.from_translation(Vec3(0, max_width / 2, max_width / 2))
            )
            wall1.set_visible(True)
            wall2 = app.add_mesh(BasicWall(max_width, max_width), parent=floor1)
            wall2.set_transform(
                Mat4.from_translation(Vec3(max_width / 2, max_width / 2, 0))
                * Mat4.from_rotation_y(90, True)
            )
            wall2.set_visible(True)
            wall3 = app.add_mesh(BasicWall(max_width, max_width), parent=floor1)
            wall3.set_transform(
                Mat4.from_translation(Vec3(0, max_width / 2, -max_width / 2))
                * Mat4.from_rotation_y(180, True)
            )
            wall3.set_visible(True)
            wall4 = app.add_mesh(BasicWall(max_width, max_width), parent=floor1)
            wall4.set_transform(
                Mat4.from_translation(Vec3(-max_width / 2, max_width / 2, 0))
                * Mat4.from_rotation_y(-90, True)
            )
            wall4.set_visible(True)


class Highrise:
    """A highrise class that procedurally generates
    a highrise building given a number of floors and width.

    Args:
        app (bk.App):
            The app instance.
        num_floors (int):
            Number of floors to generate.
        max_width (float):
            The maximum width for each component.
    """

    def __init__(self, app, num_floors, max_width):
        pass


office_floor_model = bk.Mesh.load_from(bk.res_path("./assets/office_floor.obj"))
office_base_model = bk.Mesh.load_from(bk.res_path("./assets/office_base.obj"))
office_roof_model = bk.Mesh.load_from(bk.res_path("./assets/office_roof.obj"))


class Office:
    """An office class that procedurally generates
    an office building given a number of floors and width.

    Args:
        app (bk.App):
            The app instance.
        num_floors (int):
            Number of floors to generate.
        max_width (float):
            The maximum width for each component.
    """

    def __init__(self, app, num_floors, max_width):
        self.num_floors = num_floors
        self.building = app.spawn_building()
        self.building.set_visible(True)
        self.pre_transform = (
                Mat4.from_translation(Vec3(0, 1.4, 0))
                * Mat4.from_scale(Vec3(0.5))
        )
        base = app.add_mesh(office_base_model, parent=self.building)
        base_height = 2.0
        base.set_visible(True)
        for i in range(1, self.num_floors-1):
            floor = app.add_mesh(office_floor_model, parent=base)
            floor.set_transform(Mat4.from_translation(Vec3(0, 3 * i + base_height, 0)))
            floor.set_visible(True)
        roof = app.add_mesh(office_roof_model, parent=base)
        roof.set_visible(True)
        roof.set_transform(Mat4.from_translation(Vec3(0, 3 * (self.num_floors-1) + base_height, 0)))


# pre-loaded park model
park_model = bk.Mesh.load_from(bk.res_path("./assets/park.obj"))


class Park:
    def __init__(self, app):
        self.building = app.add_mesh(park_model)
        self.building.set_visible(True)
        angle = random.randint(0, 3) * 90
        self.pre_transform = (
            Mat4.from_translation(Vec3(0, 1.4, 0))
            * Mat4.from_scale(Vec3(0.5))
            * Mat4.from_rotation_y(angle, True)
        )


# pre-loaded house model
house_model = bk.Mesh.load_from(bk.res_path("./assets/house.obj"))


class House:
    def __init__(self, app):
        self.building = app.add_mesh(house_model)
        self.building.set_visible(True)
        angle = random.randint(0, 3) * 90
        self.pre_transform = (
            Mat4.from_scale(Vec3(0.5))
            * Mat4.from_translation(Vec3(0, 6.8, 0))
            * Mat4.from_rotation_y(angle, True)
        )
