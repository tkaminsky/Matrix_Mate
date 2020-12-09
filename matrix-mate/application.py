from flask import Flask, render_template, request
import math
import json

app = Flask(__name__)

# The size of the canvas in px
S = 400
# The coordinates of the origin
ORIGIN = [S / 2, S / 2]


# Returns the coordinates of the axes under a matrix transformation
# Argument v is a 1-D list with every two elements corresponding to one column of the input matrix.
# Return is a 2-D list with each element being a graphable coordinate pair.
def get_axes(v):
    axes = []

    # For each row of the input
    for i in range(0, len(v), 2):
        # If both vector components aren't zero
        if not (v[i] == 0 and v[i + 1] == 0):
            # If the x-component is 0
            if v[i] == 0:
                axes.append([[S / 2, 0], [S / 2, S]])
            # If the y-component is 0
            elif v[i + 1] == 0:
                axes.append([[0, S / 2], [S, S / 2]])
            else:
                axes.append([[0, S / 2 * (1 + v[i + 1] / v[i])],
                             [S, S / 2 * (1 - v[i + 1] / v[i])]])
    # removes duplicate lines
    final_axes = []
    for a in axes:
        if final_axes.count(a) == 0:
            final_axes.append(a)

    return final_axes


# Returns the coordinates of the gridlines under a matrix transformation
# Argument v is a 1-D list with every two elements corresponding to one column of the input matrix.
# Argument axes is the 2-D list of axes from get_axes
# Argument ws is the integer number of gridlines in the untransformed matrix
# Return is a 2-D list with each element being a pair of graphable coordinates.
def get_gridlines(v, axes, ws):
    coords = []
    # If there are two axes (determinant is nonzero)
    if len(axes) == 2:
        # For each axis (between 0 and 2)
        for i in range(len(axes)):
            # If axis isn't vertical, add gridlines to coords
            if v[2 * i] != 0:
                increment = abs((v[2 * (1 - i) + 1] - (v[2 * i + 1] / v[2 * i]) * v[2 * (1 - i)]) * S / ws)
                delta_y = increment
                # While either endpoint of a transformed gridline is 'above' y = 0
                while axes[i][0][1] - delta_y > 0 or axes[i][1][1] - delta_y > 0:
                    # Draws a gridline below the axis
                    coords.append([[axes[i][0][0], axes[i][0][1] + delta_y],
                                   [axes[i][1][0], axes[i][1][1] + delta_y]])
                    # Draws a gridline above the axis
                    coords.append([[axes[i][0][0], axes[i][0][1] - delta_y],
                                   [axes[i][1][0], axes[i][1][1] - delta_y]])
                    delta_y += increment
            # If axis is vertical
            else:
                increment = abs(v[2 * (1 - i)] * S / ws)
                delta_x = increment
                # While the gridline is still on the canvas
                while delta_x < S / 2:
                    # Draws a gridline to the right of the axis
                    coords.append([[S / 2 + delta_x, 0],
                                   [S / 2 + delta_x, S]])
                    # Draws a gridline to the left of the axis
                    coords.append([[S / 2 - delta_x, 0],
                                   [S / 2 - delta_x, S]])
                    delta_x += increment
    return coords


# Returns the graphable coordinates of a list of input vectors
# Argument v is 1-D list with every two elements corresponding to one vector.
# Argument ws is the integer number of gridlines in the graph
# Return is a 2-D list with each element being a graphable coordinate
def get_coords(v, ws):
    coords = []
    # For every vector
    for i in range(0, len(v), 2):
        # Add the coordinate to coords, transformed to be graphable
        coords.append([200 + 400 / ws * v[i],
                       200 - 400 / ws * v[i + 1]])
    return coords


# Returns the window size
# Argument v is a 1-d list with each element being the magnitude of a vector in the x or y direction
# Return is an integer list with two values corresponding to the number units that the graph should
#   cover and the number of gridlines to be displayed by the canvas
def get_resolution(v):
    pos_vectors = []
    for i in v:
        pos_vectors.append(abs(i))
    ws = max(10, int(2 * max(pos_vectors) + 2))
    scaled_ws = ws

    while scaled_ws > 50:
        scaled_ws = math.floor(scaled_ws / 2)
        if scaled_ws % 2 != 0:
            scaled_ws += 1
    return [ws, scaled_ws]


# Checks if an input string contains a number (parses signs '-' and '.')
# Returns a boolean, true if it is a number
def is_num(string):
    # If string is empty, returns false
    if len(string) == 0:
        return False
    # If string looks like a negative number, checks if it's a number
    if string[0] == '-':
        if not string.replace('-', '', 1).replace('.', '', 1).isnumeric():
            return False
    # If string doesn't look negative, checks if it's a number
    else:
        if not string.replace('.', '', 1).isnumeric():
            return False
    return True


# Default Screen
@app.route('/')
def index():
    resolution = [10, 10]
    return render_template("index.html", resolution=json.dumps(resolution))


# Matrix Transformation Visualizer
@app.route("/matrix", methods=["GET", "POST"])
def matrix():
    if request.method == 'POST':
        # Colects form input
        raw = [request.form.get("a"), request.form.get("b"), request.form.get("c"), request.form.get("d")]
        vectors = []

        # Deals with invalid responses and converts raw data to floats
        for i in range(len(raw)):
            if raw[i] == "" or not is_num(raw[i]):
                raw[i] = 0
            vectors.append(float(raw[i]))

        # Generates the scaled window size and coordinate pairs for new gridlines
        resolution = get_resolution([(vectors[0] + vectors[2]), (vectors[1] + vectors[3])])
        axes = get_axes(vectors)
        gridlines = get_gridlines(vectors, axes, resolution[0])

        return render_template("mresult.html", resolution=json.dumps(resolution),
                               axes=json.dumps(axes), gridlines=json.dumps(gridlines))
    else:
        resolution = [10, 10]
        return render_template("matrix.html", resolution=json.dumps(resolution))


# Vector Visualizer
@app.route('/vector', methods=["GET", "POST"])
def vector():
    if request.method == "POST":
        # Declares some variables
        vectors = []
        i = 1
        j = 1

        # Because do-while loops don't exist :(
        # Finds all of the non-null vectors (empty inputs default to 0)
        v = request.form.get("11")
        while v is not None:
            # Sets default value to 0
            if v == "" or not is_num(v):
                v = 0
            # Adds the current entry to the list
            vectors.append(float(v))
            # Grabs the next vector
            if j == 2:
                i += 1
                j = 1
            else:
                j += 1
            v = request.form.get(str(i) + str(j))

        # Gets the window size, corresponding start/end coordinates, and colors
        resolution = get_resolution(vectors)
        end_coords = get_coords(vectors, resolution[0])
        start_coords = [ORIGIN, ORIGIN, ORIGIN, ORIGIN, ORIGIN]
        colors = ['#ff0000', '#0000ff', '#00ff00', '#ffff00', '#ff00ff']
        message = ""

        return render_template("vresult.html", resolution=json.dumps(resolution), end_coords=json.dumps(end_coords),
                               start_coords=json.dumps(start_coords), colors=json.dumps(colors), message=message)
    else:
        resolution = [10, 10]
        return render_template("vector.html", resolution=json.dumps(resolution))


# Vector Operations Selector Page
@app.route('/operations')
def operations():
    resolution = [10, 10]
    return render_template('operations.html', resolution=json.dumps(resolution))


# Scalar Multiplication
@app.route('/multiplication', methods=["GET", "POST"])
def multiplication():
    if request.method == "POST":
        c = request.form.get('c')
        raw = [request.form.get('a'), request.form.get('b')]
        vectors = []

        # Deals with invalid responses and converts raw data to floats
        for i in range(len(raw)):
            if not is_num(raw[i]):
                raw[i] = 0
            vectors.append(float(raw[i]))
        if not is_num(c):
            c = 1
        c = float(c)

        # Adds the scaled vector to vectors
        vectors.append(c * vectors[0])
        vectors.append(c * vectors[1])

        # Gets all of the data to be visualized
        resolution = get_resolution(vectors)
        message = "Here is the output of your operation. Argument vectors are red, and result vectors are blue:"
        colors = ['#ff0000', '#0000ff']
        end_coords = get_coords(vectors, resolution[0])
        start_coords = [ORIGIN, ORIGIN]

        return render_template("vresult.html", resolution=json.dumps(resolution), end_coords=json.dumps(end_coords),
                               start_coords=json.dumps(start_coords), colors=json.dumps(colors), message=message)
    else:
        resolution = [10, 10]
        return render_template("multiplication.html", resolution=json.dumps(resolution))


# Component decomposition
@app.route('/decomposition', methods=["GET", "POST"])
def decomposition():
    if request.method == "POST":
        raw = [request.form.get('a'), request.form.get('b')]
        vectors = []

        # Checks for invalid inputs and casts the inputs to floats
        for i in range(len(raw)):
            if not is_num(raw[i]):
                raw[i] = 0
            if i == 0:
                vectors.append(float(raw[i]))
                vectors.append(0)
            else:
                vectors.append(vectors[0])
                vectors.append(float(raw[i]))

        # Gets all of the data to be visualized
        resolution = get_resolution(vectors)
        end_coords = get_coords(vectors, resolution[0])
        start_coords = [ORIGIN, end_coords[0]]
        message = "Here is your decomposition:"
        colors = ['#ff0000', '#ff0000']

        return render_template("vresult.html", resolution=json.dumps(resolution), end_coords=json.dumps(end_coords),
                               start_coords=json.dumps(start_coords), colors=json.dumps(colors), message=message)
    else:
        resolution = [10, 10]
        return render_template("decomposition.html", resolution=json.dumps(resolution))


# Vector Addition
@app.route('/addition', methods=["GET", "POST"])
def addition():
    if request.method == "POST":
        raw = [request.form.get('a'), request.form.get('b'), request.form.get('c'), request.form.get('d')]
        vectors = []

        # Deals with invalid responses
        for i in range(len(raw)):
            if not is_num(raw[i]):
                raw[i] = 0
            vectors.append(float(raw[i]))

        for i in range(2):
            vectors.append(vectors[0] + vectors[2])
            vectors.append(vectors[1] + vectors[3])
        vectors[2] = vectors[4]
        vectors[3] = vectors[5]

        # Gets all of the data do be visualized
        resolution = get_resolution(vectors)
        end_coords = get_coords(vectors, resolution[0])
        start_coords = [ORIGIN, end_coords[0], ORIGIN]
        message = "Here is the result vector:"
        colors = ['#ff0000', '#ff0000', '#0000ff']

        return render_template("vresult.html", resolution=json.dumps(resolution), end_coords=json.dumps(end_coords),
                               start_coords=json.dumps(start_coords), colors=json.dumps(colors), message=message)
    else:
        resolution = [10, 10]
        return render_template("addition.html", resolution=json.dumps(resolution))


# Instructions screen
@app.route('/instructions')
def instructions():
    return render_template("instructions.html")


if __name__ == '__main__':
    app.run()
