"""

  /$$$$$$$  /$$   /$$ /$$$$$$$$ /$$$$$$   /$$$$$$  /$$   /$$             
 | $$__  $$| $$  /$$/|_____ $$//$$$_  $$ /$$__  $$| $$  | $$             
 | $$  \\ $$| $$ /$$/      /$$/| $$$$\\ $$| $$  \\ $$| $$  | $$             
 | $$$$$$$ | $$$$$/      /$$/ | $$ $$ $$|  $$$$$$/| $$$$$$$$             
 | $$__  $$| $$  $$     /$$/  | $$\\ $$$$ >$$__  $$|_____  $$             
 | $$  \\ $$| $$\\  $$   /$$/   | $$ \\ $$$| $$  \\ $$      | $$             
 | $$$$$$$/| $$ \\  $$ /$$/    |  $$$$$$/|  $$$$$$/      | $$             
 |_______/ |__/  \\__/|__/      \\______/  \\______/       |__/                                                                                                                                                                                                                               

Welcome to the lab exercises of BK7084!
In this assignment, we will introduce you to the basics of graphics in Python:
0. Creating an environment and installing the bk7084 framework.
1. Creating a Window object in which you can draw graphics.
2. Using Vectors to create a triangle.
3. Drawing the triangle to the screen.
4. Scaling and transforming the triangle using a matrix.

Each of the assignments will ask you to complete certain tasks.
Often, the tasks are marked with a TODO: comment.
If you're not sure what to do, look for these comments.
For now, scroll down to section 0.


0. Creating an environment and installing the bk7084 framework
--------------------------------------------------------------

Open this file in Visual Studio Code for the easiest experience.
When you're in Visual Studio code, make sure you can see the terminal window below.
If the terminal is not open yet, click on `Terminal > New Terminal` at the top of the screen.

We assume that you have already installed Conda in the other course.
If that's not the case, follow this manual to install miniconda3:
https://docs.anaconda.com/miniconda/miniconda-install/

Using the terminal, create a new environment with Python 3.9 installed.
You don't have to type the `$`. It's used to show that you should run a line in the terminal.
$ conda create -n compsim python=3.9
$ conda activate compsim

Before we run it, we need to make sure we are running the correct Python interpreter within VSCode.
Open the **Command Palette** (*Ctrl+Shift+P*), and then type **Python:
Select Interpreter** command to search, then select the command. The command presents a list of available interpreters that VSCode can find automatically, you should be able to select **compsim**, the environment we just created.

Next, install the bk7084 framework with pip
$ pip install bk7084

That's it! Remember to activate the compsim environment before you start with your assignments later on.

Now let's get started. The first thing to know: the text you read here is a comment.
Comments are skipped over by Python and used for people to understand your code.
"""
# A comment can be written with a # before every line
"""
Or on multiple
lines between
three quotes.
"""

"""
We sometimes give examples of code. These start with >>> and the expected results start with ...:
>>> print('hello world')
... hello world
"""

"""
Most Python files start by importing dependencies.
These are pieces of code that others wrote which are used by your code.

Here, we import functionality from the framework you just installed.
If you're curious what this framework looks like, click on one of the names below (e.g., app, Window) while pressing ctrl (or command on a Mac)
Visual Studio Code will then open the linked file in another tab. Close the tab to get back to this file.
"""
import bk7084 as bk
from bk7084.math import Vec3, Mat3

"""
1. Creating a Window and BK7084 Application
--------------------

We will create a Window *object* here. If you haven't heard of an *object* in the context of programming yet:
An *object* is a packet of
(1) information describing an object, called attributes; and
(2) tools to use and change this information, called methods.
Objects are a way to organize your code so that you always have information and the corresponding tools in the same place.
To create an object, we first need a recipe of what an object will look like and how it behaves: this recipe is called a *class*.

Let's start with a simple example: a Rectangle class. Note that there is no such class, this is just for the sake of illustration. Nevertheless, you could create one yourself if needed.

One way to describe a Rectangle is by it's width and height. These are the *attributes* of a Rectangle class.
A common task that you might do with a Rectangle is to calculate it's area. This would be a *method* on the Rectangle.

When we create an object, we first tell Python which class we want to use to create the object.
Then we can also give it some of the attributes of the object to start with. For example:
>>> rectangle1 = Rectangle(width=4, height=5)
This constructs the object `rectangle1` following the recipe of the Rectangle class. It's width and height are set to 4 and 5.

We can look at the attributes of `rectangle1` by the . notation:
>>> rectangle1.width   # Returns the width of the rectangle
... 4
>>> rectangle1.height  # Returns the height of the rectangle
... 5

If we want to call a method on rectangle, we use the . notation and end with ():
>>> rectangle1.compute_area()
... 20
The compute_area() method knows the width and height of rectangle1,
because it can see the attributes of the rectangle1 object.

Sometimes, a method needs more information from the user.
You can give this to the method using *parameters*.
An example could be a method that resizes your rectangle. You could give it a scale parameter:
>>> rectangle1.resize(scale=2)
>>> rectangle1.width
... 8
>>> rectangle1.height
... 10
Not all parameters need to be given with their name. Most of the times, you can simply give the value:
>>> rectangle1.resize(2)

Note that inside the class the methods resize and compute_area should also be implemented (coded) for the example above to work.
But we'll stop here, as it's all you need to know for now. 

Let's start by creating a window object using the Window class.
"""

# This creates a window object, which we can use to draw graphics to the screen. 
# Think of it as any other program window (such as the VSCode window you are using).
window = bk.Window()
# This sets the title of the window and the size. You can change these values.
window.set_title('BK7084 - Lab 0 - Introduction')
# The size is given in pixels. You can change this by setting the width and height.
window.set_size(800, 600)
# The window is resizable by default. You can change this by setting resizable to False.
window.set_resizable(True)


# The window is now created, but it's not yet visible. To show the window, we need to create an application to
# run the window in. This is done by creating an App object.
app = bk.App()

"""
The App class has a method called `create_camera()`, which puts a camera in the 3D world.
This camera is used by the window to draw elements that you add to the 3D world.
This camera is positioned at [0, 0, 10], looks at the point [0, 0, 0] and the field-of-view (fov) is 60 degrees.

Try changing some of these values and see what happens to the image.
You will need to restart the application to see the changes.
"""
                           # Change this...   # And this...          # And also this...
camera = app.create_camera(pos=Vec3(0, 0, 10), look_at=Vec3(0, 0, 0), fov_v=60.0)

"""
2. Creating a triangle
----------------------

Congratulations! You just drew your first triangle to the screen without even writing any code for it.
Here's the triangle that was drawn:
"""
# This creates a mesh, which represents a triangle by it's three vertices.
triangle0_mesh = bk.Mesh.create_triangle(Vec3(-2, -2, 1), Vec3(2, -2, 1), Vec3(0, 2, 1))
# This creates an object, which is used to draw the triangle to the screen.
triangle0 = app.add_mesh(triangle0_mesh)

"""
Now it's up to you to create another triangle and draw it to the screen.
A triangle is defined by it's three corners, or *vertices*. These vertices are points in 3D, which we can describe by a 3D vector.
In these assignments, you will use a class for this, called Vec3.

You can create a 3D vector as follows:
>>> vec = Vec3(1, 2, 3)

Now create your own triangle by:
[a] Creating three vertices v0, v1, v2 as three Vec3 vectors. You can place the triangle where you like.
It helps to first draw the triangle on a piece of paper.
"""
v0 = None # Complete this...
v1 = None # Complete this...
v2 = None # Complete this...

# [Bookmark for part 4] Skip this until you reach part 4.

"""
[b] Construct a Triangle with these vertices.
>>> triangle1_mesh = bk.Mesh.create_triangle(.., .., ..)
>>> triangle1 = app.add_mesh(triangle1_mesh)
"""


"""
3. Drawing the triangle to the screen
-------------------------------------

Now draw the triangle to the screen by simply calling the draw() function or setting
the visible property of the triangle to True.
"""
triangle0.set_visible(True)

# A light is needed to see the triangle's color. You can add a point light to the scene like this:
app.add_directional_light(dir=Vec3(0.0, 0.0, -1.0), color=bk.Color.WHITE)

# enable triangle1 drawing here...


"""
4. Scaling and transforming the triangle using a matrix
-------------------------------------------------------

During the lectures, you will be introduced to many Linear Algebra concepts that allow you to transform your geometry. In this section we start to look into how to use those concepts in practice.

    Quick tip: As extra material, you might want to check out 3Blue1Brown's YouTube series on linear algebra
    The first 4 video's should be enough to get you started.
    https://www.youtube.com/watch?v=kjBOesZCoqc&list=PL0-GT3co4r2y2YErbmuJw2L5tW4Ew2O5B

With two triangles drawn, let's introduce some more concepts for you to try.
You can try these concepts on triangle1 by scrolling back up to the comment [Bookmark for part 4].

You created a vector by simply typing three numbers. There's a more intuitive way to think of a vector:
A vector describes a point in space. Each number in the vector is a coordinate for one of the axes in space, for example, x, y, z.
A vector [a b c] means that the point is `a` steps in the x-axis, `b` steps on the y-axis and `c` steps on the z-axis.
Another way to write this is:
position = a * [1 0 0] + b * [0 1 0] + c * [0 0 1]

Vectors can be transformed by *matrices*. A matrix is a grid of numbers that tells you how to transform each axis.
Each axis corresponds to a column in the matrix, which tells you where that axis moves.
Let's start with a very simple matrix, one that does not change any of the axes:
  x  y  z
| 1  0  0 |
| 0  1  0 |
| 0  0  1 |

The x axis is now [1 0 0], which is already exactly the x axis. y is [0 1 0] and z is [0 0 1].
Because the output is identical, we call this matrix the Identity matrix.

Let's see another example: a matrix that scales only the x-axis by 3:
  x  y  z
| 3  0  0 |
| 0  1  0 |
| 0  0  1 |

The x axis is changed to [3 0 0] (the first column) and the y and z axis stay the same.

What do you think the following matrix does to the axes?
  x  y  z
| 0  2  0 |
| 1  0  0 |
| 0  0  3 |

This is how you create a matrix in code:
You can use Mat3 to create a 3x3 matrix. Be aware of each bracket [] and comma ,
>>> matrix_scale = Mat3([
    [3, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])

If you want to apply a matrix to a vector to transform it, you can multiply it with a vector.
In Python, you can use the @ symbol for matrix multiplication.
>>> v0 = Vec3([2, 2, 2])
>>> v0_scaled = matrix_scale @ v0

The result is a vector [6 2 2].

For your convenience, some commonly used matrices have functions to easily create them.
For example, you can create a scaling matrix from a scaling factor per axis:
>>> matrix_scale = Mat3.from_scale([3, 1, 1])
This will give you the scaling matrix we created before.

Another matrix to rotate points around the x axis:
>>> matrix_rotate = Mat3.from_rotation_x(90, degrees=True)

You can find out what other methods are available by ctrl + clicking (command + click on Mac) on the Mat3 name.

[a] Go back to the [Bookmark for part 4] and multiply a scaling matrix with each vertex (v0, v1, v2)
[b] Make sure that the result of this multiplication is stored, i.e.:
>>> v0_scaled = matrix_scale @ v0
>>> v1_scaled = ...
[c] Draw another triangle with these changed coordinates.
[d] Create some more matrices and try to understand what they do to the triangle.
"""

"""
These last line tells the application the window that you want to use, and then runs the app.
"""
app.run(window)
