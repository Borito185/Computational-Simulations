from bk7084.math import *
from components import *
from random import randint
import math
import random

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

        ground_floor = [SkyscraperDoor, SkyscraperWindow3, SkyscraperWindow3R, SkyscraperWindow4]
        upper_floors = [SkyscraperWindow1, SkyscraperWindow1R, SkyscraperWindow2, SkyscraperWindow3, SkyscraperWindow3R, SkyscraperWindow4]
        max_width = math.floor(max_width)

        replacement_map = {
            SkyscraperWindow1: SkyscraperWindow1R,
            SkyscraperWindow3: SkyscraperWindow3R,
            SkyscraperWindow1R: SkyscraperWindow1,
            SkyscraperWindow3R: SkyscraperWindow3
        }

        half = math.floor(max_width/2)
        sides_h = [SelectRandomComponent(ground_floor) for i in range(half)]
        sides_ground = []
        sides_ground.extend(sides_h)
        if max_width % 2 == 1:
            sides_ground.append(SelectRandomComponent(ground_floor))
        sides_h = [replacement_map.get(cls, cls) for cls in reversed(sides_h)]
        sides_ground.extend(sides_h)

        sides_h = [SelectRandomComponent(upper_floors) for i in range(half)]
        sides_upper = []
        sides_upper.extend(sides_h)
        if max_width % 2 == 1:
            sides_upper.append(SelectRandomComponent(ground_floor))
        sides_h = [replacement_map.get(cls, cls) for cls in reversed(sides_h)]
        sides_upper.extend(sides_h)

        rotate_factor = randint(3, 15)

        for i in range(self.num_floors):
            rotation = Mat4.from_rotation_y(rotate_factor * i, degrees=True)
            for j in range(max_width):
                for k in range(max_width):
                    include = [True, True, k==max_width-1, j==max_width-1, k==0, j==0]
                    list = sides_ground if i == 0 else sides_upper
                    walls = [list[j], list[k], list[j], list[k]]
                    transform = rotation * Mat4.from_translation(Vec3(j - max_width/2 + 0.5, i, k - max_width/2 + 0.5)) 
                    CreateVoxel(app, self.building, transform, BasicFloor, walls, include)


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
        self.num_floors = num_floors
        # Spawn the building and save the reference to the building
        self.building = app.spawn_building()
        self.building.set_visible(True)

        ground_floor = [HighriseDoor, HighriseLowerWindow]
        upper_floors = [HighriseWindow]
        max_width = math.floor(max_width)

        replacement_map = {}

        half = math.floor(max_width/2)
        max_width = half * 2
        sides_h = [SelectRandomComponent(ground_floor) for i in range(half)]
        sides_ground = []
        sides_ground.extend(sides_h)
        if max_width % 2 == 1:
            sides_ground.append(SelectRandomComponent(ground_floor))
        sides_h = [replacement_map.get(cls, cls) for cls in reversed(sides_h)]
        sides_ground.extend(sides_h)

        sides_h = [SelectRandomComponent(upper_floors) for i in range(half)]
        sides_upper = []
        sides_upper.extend(sides_h)
        if max_width % 2 == 1:
            sides_upper.append(SelectRandomComponent(ground_floor))
        sides_h = [replacement_map.get(cls, cls) for cls in reversed(sides_h)]
        sides_upper.extend(sides_h)

        for i in range(self.num_floors):
            for j in range(half):
                for k in range(half):
                    for l in range(6):
                        include = [False, i==self.num_floors-1, k==half-1, False, False, False]
                        rotation = Mat4.from_rotation_y(60 * l, True)
                        list = sides_ground if i == 0 else sides_upper
                        walls = [list[j], list[k], list[j], list[k]]
                        transform = rotation * Mat4.from_translation(Vec3(j - half/2 + 0.5, i, k - half/2 + 0.5)) * Mat4.from_translation(Vec3(0,0,1.1))
                        CreateVoxel(app, self.building, transform, BasicFloor, walls, include)


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
        # Spawn the building and save the reference to the building
        self.building = app.spawn_building()
        self.building.set_visible(True)

        ground_floor = [OfficeDoor, OfficeWindow]
        upper_floors = [OfficeWindow]
        max_width = math.floor(max_width)

        replacement_map = {}

        half = math.floor(max_width/2)
        sides_h = [SelectRandomComponent(ground_floor) for i in range(half)]
        sides_ground = []
        sides_ground.extend(sides_h)
        if max_width % 2 == 1:
            sides_ground.append(SelectRandomComponent(ground_floor))
        sides_h = [replacement_map.get(cls, cls) for cls in reversed(sides_h)]
        sides_ground.extend(sides_h)

        sides_h = [SelectRandomComponent(upper_floors) for i in range(half)]
        sides_upper = []
        sides_upper.extend(sides_h)
        if max_width % 2 == 1:
            sides_upper.append(SelectRandomComponent(ground_floor))
        sides_h = [replacement_map.get(cls, cls) for cls in reversed(sides_h)]
        sides_upper.extend(sides_h)

        skip_x = randint(0,max_width-3)
        skip_z = randint(0,max_width-3)

        for i in range(self.num_floors):
            for j in range(max_width):
                for k in range(max_width):
                    if ((skip_x <= j <= skip_x + 2) and (skip_z <= k <= skip_z + 2)): continue
                    include = [False, i==self.num_floors-1, True, True, True, True]
                    list = sides_ground if i == 0 else sides_upper
                    walls = [list[j], list[k], list[j], list[k]]
                    transform = Mat4.from_translation(Vec3(j - max_width/2 + 0.5, i, k - max_width/2 + 0.5))
                    CreateVoxel(app, self.building, transform, BasicFloor, walls, include)

def SelectRandomComponent(components):
    count = len(components)
    if count <= 0:
        return
    if count <=1:
        return components[0]
    return components[randint(0, count-1)]

def CreateVoxel(app, parent, pos, roof, walls, include):
    # ground
    floor1 = app.add_mesh(BasicFloor(), parent=parent)
    floor1.set_transform(pos)
    floor1.set_visible(True)

    if(include[0]):
        # floor overhang
        floor3 = app.add_mesh(BasicFloor(), parent=floor1)
        floor3.set_transform(Mat4.from_rotation_x(180, True))
        floor3.set_visible(True)

    if(include[1]):
        # roof 
        floor2 = app.add_mesh(roof(), parent=floor1)
        floor2.set_transform(Mat4.from_translation(Vec3(0, 1, 0)))
        floor2.set_visible(True)
    # walls
    for i in range(4):
        if(not include[i + 2]): continue
        wall = app.add_mesh(walls[i](1, 1), parent=floor1)
        transform = Mat4.from_rotation_y((math.pi/2) * i) 
        transform *= Mat4.from_translation(Vec3(0, 1 / 2, 1 / 2))
        wall.set_transform(transform)
        wall.set_visible(True)


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
