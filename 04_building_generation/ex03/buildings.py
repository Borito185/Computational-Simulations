from bk7084.math import *
from components import *
from random import randint
import math

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

        for i in range(self.num_floors):
            for j in range(max_width):
                for k in range(max_width):
                    list = sides_ground if i == 0 else sides_upper
                    walls = [list[j], list[k], list[j], list[k]]
                    transform = Mat4.from_translation(Vec3(j - max_width/2 + 0.5, i, k - max_width/2 + 0.5))
                    CreateVoxel(app, self.building, transform, 1, BasicFloor, walls)


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
            for j in range(max_width):
                for k in range(max_width):
                    list = sides_ground if i == 0 else sides_upper
                    walls = [list[j], list[k], list[j], list[k]]
                    transform = Mat4.from_translation(Vec3(j - max_width/2 + 0.5, i, k - max_width/2 + 0.5))
                    CreateVoxel(app, self.building, transform, 1, BasicFloor, walls)


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

        for i in range(self.num_floors):
            for j in range(max_width):
                for k in range(max_width):
                    list = sides_ground if i == 0 else sides_upper
                    walls = [list[j], list[k], list[j], list[k]]
                    transform = Mat4.from_translation(Vec3(j - max_width/2 + 0.5, i, k - max_width/2 + 0.5))
                    CreateVoxel(app, self.building, transform, 1, BasicFloor, walls)

def SelectRandomComponent(components):
    count = len(components)
    if count <= 0:
        return
    if count <=1:
        return components[0]
    return components[randint(0, count-1)]

def CreateVoxel(app, parent, pos, size, roof, walls):
    adjust = size/3
    # ground
    floor1 = app.add_mesh(BasicFloor(3, 3), parent=parent)
    floor1.set_transform(pos * Mat4.from_scale(Vec3(adjust,adjust,adjust)))
    floor1.set_visible(True)
    # roof 
    floor2 = app.add_mesh(roof(3, 3), parent=floor1)
    floor2.set_transform(Mat4.from_translation(Vec3(0, 3, 0)))
    floor2.set_visible(True)
    # walls
    for i in range(4):
        wall = app.add_mesh(walls[i](3, 3), parent=floor1)
        transform = Mat4.from_rotation_y((math.pi/2) * i) 
        transform *= Mat4.from_translation(Vec3(0, 3 / 2, 3 / 2))
        wall.set_transform(transform)
        wall.set_visible(True)