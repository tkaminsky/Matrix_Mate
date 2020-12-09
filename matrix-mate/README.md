Starting the Application:

1. Download all source code in the matrix-mate folder and store along a path known to you.
2. In a terminal window, navigate to the matrix-mate directory
3. Type 'Flask run' and hit enter
4. After the server begins, you should see the line 'Running on ...' followed by a http link.
    Copy and paste the link into an internet browser (preferably Google Chrome) to access the
    website.

Navigating the Website:

1. From any page, you can navigate to any other page by left-clicking the corresponding
    button in the navbar. 
2. Each feature has custom, clearly-marked inputs with which to enter your vectors. In
    general, the top component of a vector input corresponds with its x component and
    the bottom component corresponds with its y input, as is standard.
3. Matrix Mate accepts all integer and decimal numbers as inputs. Invalid responses,
    including fractions, will be interpreted as 0 in all cases of vectors and 1 in the 
    case of scalars.
    
Trouble-Shooting and Additional Information

1. If attempting to run Matrix Mate on the CS50 IDE, or when using different versions of 
    Flask, you may need to change the name of 'app.py' to 'application.py.'
2. If the website appears to not incorporate styles.css, exit the tab, restart the application,
    and try opening it in a private browser window. 
    (see: https://stackoverflow.com/questions/51446095/flask-cached-files-no-new-changes-applied-still-loads-old-css-and-js-files)
3. NOTE: Matrix-Mate has been tested on multiple Mac Computers, as well as on the CS50 IDE, and 
    it has worked successfully (with the small adjustment for the IDE as mentioned above). If 
    you attempt to run the program on another operating system besides Mac, I cannot guarantee
    that it will function properly, so, if you encounter problems launching the application from
    one of those systems, please try running it from one of the other options. Also, matrix mate
    appears to run properly on the most recent updates of Chrome and Safari, so if you encounter 
    problems rendering the canvas or so on, please try viewing the window from one of these
    browsers.


Layout of the Application:

1. The program should be run in the directory containing app.py. Also in this directory should
    be the README.md and DESIGN.md files and three directories––__pycache__, static, templates,
    and venv.
    a) 'static' contains the css stylesheet for the application and the website icon.
    b) 'templates' contains the html files for the website, whose organization is layed out
        in DESIGN.md.
    c) 'venv' contains important python data such as Flask and other imported libraries.
    d)'__pycache__' just contains bytecode-compiled and optimized bytecode-compiled versions of
        the project files, and can be largely ignored.
2. The 'app.py' file contains all of the important backend functions and all of the Flask
    routes. At the top of the file are all of the function declarations (13-127), and below
    it are all of the Flask routes.
3. A brief demonstration of the features of this website can be found in this YouTube video:
    https://www.youtube.com/watch?v=wAgwWz9_eFc