from enum import Enum

import numpy as np

from buildings import Office, Highrise, Skyscraper, House, Park
from components import material_basic_ground
from random import randint
from bk7084.math import Mat4, Vec3
import bk7084 as bk
import types


class BuildingType(Enum):
    """Enum for the type of building"""

    EMPTY = 0
    HOUSE = 1
    OFFICE = 2
    HIGHRISE = 3
    SKYSCRAPER = 4
    PARK = 5

    def __str__(self):
        if self is BuildingType.EMPTY:
            return "ET"
        elif self is BuildingType.HOUSE:
            return "HS"
        elif self is BuildingType.OFFICE:
            return "OF"
        elif self is BuildingType.HIGHRISE:
            return "HR"
        elif self is BuildingType.SKYSCRAPER:
            return "SK"
        elif self is BuildingType.PARK:
            return "PK"


Office.type = BuildingType.OFFICE
Highrise.type = BuildingType.HIGHRISE
Skyscraper.type = BuildingType.SKYSCRAPER
House.type = BuildingType.HOUSE
Park.type = BuildingType.PARK


class City:
    """A city class that procedurally generates a city grid given a number of rows
    and columns.

    The city grid is a 2D grid of plots. Each plot can be empty or contain a building.
    The building can be a house, office, highrise, skyscraper, or park.

    The buildings of each plot are stored in a list in the order from the first row
    to the last row, and from the first column to the last column. For example, the
    following city grid has 3 rows and 4 columns:

    +----+----+----+----+
    | HS | OF | HR | PK |
    +----+----+----+----+
    | SK | ET | ET | ET |
    +----+----+----+----+
    | ET | ET | ET | ET |
    +----+----+----+----+

    ET = empty plot
    HS = house
    OF = office
    HR = highrise
    SK = skyscraper
    PK = park

    The buildings are stored in the following order in the list:
    [HS, OF, HR, PK, SK, ET, ET, ET, ET, ET, ET, ET]

    We can use the following formula to get the index of the building in the list:

    index = row * num_cols + col

    For example, the index of the building at row 1 and column 2 is:

    index = 1 * 4 + 2 = 6

    This means that the building at row 1 and column 2 is the 7th building in the list.

    To facilitate the access of the buildings in the city grid, you can use the methods
    `get_building`, `set_building`, and `get_building_type` to get the building at a
    specific row and column, set the building at a specific row and column, and get
    the type of the building at a specific row and column, respectively.
    """
    def __init__(self, app, plots_per_col=8, plots_per_row=8, plot_width=3):
        """Initializes the city grid.
        Args:
            app (bk.App):
                The app instance.
            plots_per_col (int):
                The number of plots per column.
            plots_per_row (int):
                The number of plots per row.
            plot_width (float):
                The width of each plot.
        """
        self._app = app
        self._plots_per_col = plots_per_col
        self._plots_per_row = plots_per_row
        self._plot_width = plot_width
        self._plots = [None] * plots_per_col * plots_per_row
        self._ground = self.create_ground(app, self.width, self.height, *self.spacing)
        self._grid = self.create_grid(app, self.width, self.height, *self.spacing)
        app.update_shadow_map_ortho_proj(max(plots_per_col, plots_per_row) * plot_width)
        # Reset (initialize) the city grid by assigning building to each plot
        self.reset_grid()

    @staticmethod
    def create_ground(app, width, height, spacing_x, spacing_y):
        """Creates the ground of the city."""
        ground_mesh = bk.Mesh.create_quad(1, bk.Alignment.XY)
        ground_mesh.set_material(material_basic_ground)
        ground = app.add_mesh(ground_mesh)
        ground.set_transform(
            Mat4.from_translation(Vec3(-spacing_x * 0.5, 0.0, -spacing_y * 0.5))
            * Mat4.from_scale(Vec3(width, 1.0, height))
            * Mat4.from_rotation_x(-90, True)
        )
        ground.set_visible(True)
        ground.set_cast_shadows(False)
        return ground

    @staticmethod
    def create_grid(app, width, height, spacing_x, spacing_y):
        """Creates the grid of the city."""
        grid_mesh = bk.Mesh.create_grid(width, height, (spacing_x, spacing_y), bk.Alignment.XZ, bk.Color.WHITE)
        grid = app.add_mesh(grid_mesh)
        grid.set_transform(Mat4.from_translation(Vec3(-spacing_x * 0.5, 0.1, -spacing_x * 0.5)))
        grid.set_visible(True)
        grid.set_cast_shadows(False)
        return grid

    def set_ground_visibility(self, visible: bool):
        self._ground.set_visible(visible)

    @property
    def width(self) -> float:
        """Returns the width of the city."""
        return self._plots_per_col * self._plot_width * 1.5

    @property
    def height(self) -> float:
        """Returns the height of the city."""
        return self._plots_per_row * self._plot_width * 1.5

    @property
    def plots_per_row(self) -> int:
        """Returns the number of plots per row."""
        return self._plots_per_row

    @property
    def plots_per_col(self) -> int:
        """Returns the number of plots per column."""
        return self._plots_per_col

    @property
    def spacing(self) -> (float, float):
        """Returns the spacing between plots."""
        return self._plot_width * 1.5, self._plot_width * 1.5

    def reset_grid(self):
        """Resets the city grid.
        Can be also used to initialize the city grid.
        This method will reset the plots and then randomly assign plot types to each
        plot in the city grid.

        Complete this method to initialize your city to match the required specification:

        - 5% of the plots should be skyscrapers
        - 8% of the plots should be highrises
        - 25% of the plots should be offices
        - 37% of the plots should be houses
        - 15% of the plots should be parks
        - the remaining plots can be whatever you want
        """
        # TODO: Randomize the city grid in a smart way.
        for row in range(self._plots_per_row):
            for col in range(self._plots_per_col):
                # Generate a random number between 0 and 5 (inclusive)
                # and set the plot type accordingly
                building_type = BuildingType(randint(0, 5))
                self.construct_building(row, col, building_type)

    def clear_grid(self):
        """Clears the city grid.
        This method will clear the plots and set all plots to empty.
        """
        for i in range(self._plots_per_col * self._plots_per_row):
            self._plots[i] = None

    @property
    def rows(self) -> int:
        """Returns the number of rows in the city grid."""
        return self._plots_per_row

    @property
    def cols(self) -> int:
        """Returns the number of columns in the city grid."""
        return self._plots_per_col

    def construct_building(self, row: int, col: int, building_type: BuildingType):
        """Constructs a building at the given row and column.
        Args:
            row (int):
                The row of the plot.
            col (int):
                The column of the plot.
            building_type (BuildingType):
                The type of building to construct.
        """
        building = None

        if building_type is BuildingType.HOUSE:
            building = House(self._app)
        elif building_type is BuildingType.OFFICE:
            # TODO: replace the following line with your own code to create an office
            num_floors = randint(3, 8)
            building = Office(self._app, num_floors, 3)
        elif building_type is BuildingType.HIGHRISE:
            # TODO: replace the following line with your own code to create a highrise
            building = Skyscraper(
                self._app, 5, 3
            )
        elif building_type is BuildingType.SKYSCRAPER:
            # TODO: replace the following line with your own code to create a skyscraper
            building = Skyscraper(self._app, 8, 3)
        elif building_type is BuildingType.PARK:
            building = Park(self._app)

        self._plots[row * self._plots_per_col + col] = building

    def get_building(self, row: int, col: int):
        """Returns the building at the given row and column.
        Args:
            row (int):
                The row of the plot.
            col (int):
                The column of the plot.
        """
        return self._plots[row * self._plots_per_col + col]

    def set_building(self, row: int, col: int, building):
        """Sets the building at the given row and column.
        Args:
            row (int):
                The row of the plot.
            col (int):
                The column of the plot.
            building:
                The building to set.
        """
        self._plots[row * self._plots_per_col + col] = building

    def get_building_type(self, row: int, col: int) -> BuildingType:
        """Returns the type of the building at the given row and column.
        Args:
            row (int):
                The row of the plot.
            col (int):
                The column of the plot.
        """
        if self.get_building(row, col) is None:
            return BuildingType.EMPTY
        else:
            return self.get_building(row, col).type

    def swap_buildings(self, row1: int, col1: int, row2: int, col2: int):
        """Swaps the building at the given rows and columns.
        Args:
            row1 (int):
                The row of the first plot.
            col1 (int):
                The column of the first plot.
            row2 (int):
                The row of the second plot.
            col2 (int):
                The column of the second plot.
        """
        self._plots[row1 * self._plots_per_col + col1], self._plots[row2 * self._plots_per_col + col2] = (
            self._plots[row2 * self._plots_per_col + col2], self._plots[row1 * self._plots_per_col + col1])

    def compute_sunlight_scores(self) -> np.array(float):
        """Computes the sunlight scores of the city during the day. Lower scores are
        better, the best score is 1.
        Returns:
            list:
                The sunlight scores of the city at different times of the day, in total
                11 scores.
        """
        return np.array(self._app.compute_sunlight_scores()[:11])

    def print_plots(self):
        """Prints the city grid in the console.
        This method will print the building type of each plot in the city grid.
        The output will be a grid of characters, where each 2 characters represent
        a single plot.
        """
        for row in range(self._plots_per_row):
            for col in range(self._plots_per_col):
                print(self.get_building_type(row, col), end=" ")
            print()

    def get_plot_center(self, row: int, col: int) -> Vec3:
        """Returns the center of the plot at the given row and column."""
        half_width = self._plots_per_col / 2
        half_height = self._plots_per_row / 2
        return Vec3(
            (col - half_width) * self._plot_width * 1.5,
            0,
            (row - half_height) * self._plot_width * 1.5,
        )

    def update(self, dt, t):
        """Updates all buildings in the city.
        This method will update the transform of each building in the city grid.
        """
        for i, plot_building in enumerate(self._plots):
            if plot_building is not None:
                # Get the row and column of the building
                row = i // self._plots_per_col
                col = i % self._plots_per_col
                # Update the transform of the building according to the row and column
                half_width = self._plots_per_col / 2
                half_height = self._plots_per_row / 2
                pre_transform = Mat4.identity()
                if hasattr(plot_building, "pre_transform"):
                    pre_transform = plot_building.pre_transform
                plot_building.building.set_transform(
                    Mat4.from_translation(
                        Vec3(
                            (col - half_width) * self._plot_width * 1.5,
                            0,
                            (row - half_height) * self._plot_width * 1.5,
                        )
                    )
                    * pre_transform
                )
