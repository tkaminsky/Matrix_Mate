Hello, and welcome to Matrix Mate!

I'll go over the design of my project part-by-part, starting with the back-end 
and then moving to the front-end.

1) General

I decided that, given our course material, it would make the most sense to make my website
using Flask. As a broad outline, the flow of the application is something like this:

a. Get data from the website using input forms (html).

b. Transform that data into coordinates which can be graphed on a canvas (Python/Flask).

c. Render that data (javascript/html).

With this flow in mind, I'll talk about each component in turn.

2) Frond-End: HTML

The design of the html files is centered around a layout file, with every other file (with the
exception of instructions.html) extending layout.html. The layout consists of a top bar with the
title "Matrix Mate!" and a navbar with buttons corresponding to each of the components of the site.
Forms are used to input the necessary data for each feature, which is handled in app.py.

3) Back-End: Python

The top of app.py contains functions to do some of the computations common to multiple routes:
one to find the number of gridlines to draw, one to take vectors and output coordinates, and 
so on. You'll notice that all of these take one or more of v and ws as inputs--the first, v, is
a one-dimensional list corresponding to the input vector, and the second, ws, is a measure of the 
scalar with which to multiply the vector to get a graphable coordinate. Like the overall logic of the
program, all of these functions take the unprocessed v information (the input vector in human-graphable
coordinates) and output processed coordinates which can be graphed on a canvas element. To simplify the
javascript-side of things as much as possible, I tried to make the arguments passed to flask almost
exclusively be coordinate-pairs. 

4) Back-End: Flask

To process the information within the routes, I naturally split up GET and POST requests, as demonstrated
in previous labs and psets. All render_templates must be passed a resolution argument to know how many gridlines
to draw, so when a GET request is called the default values are [10,10] (showing that no transformation has taken
place). The specific information varies from function to function, but both involve making the responses into valid
lists of numbers and then finding the coordinates to graph for the given context of the problem. I was able to 
have the vector visualizer and all of the vector operations visualizers render on vresult.html because of the 
universality of the functions. Still, for the sake of efficiency, I made the matrix transformation visualizer
go to mresult.html instead, because it was graphing so many lines.

5) Frond-End (ish): JavaScript

Once I had all the necessary information, I just needed to visualize it. After looking through the matplotlib documentation,
I decided that I actually wanted the freedom of a simple canvas element, and so I ended up using that. For simplicity
I made the canvas size always 400px by 400 px, which allows for information to be comfortably displayed on all reasonable
screen sizes (I did add some additional CSS to make sure that information was never cut off by changing screen size, of course).
For some sense of continuity I made graph1 be a common element on every page (except instructions.html), and so the
corresponding logic is housed in layout.html. The only time that additional canvases are used is for the matrix 
transformation visualizer, in which case that logic is housed in the extension mresult.html.