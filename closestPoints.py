# closestPoints.py
# Tori Grasso
# 11/25/19

import os.path
from graphics import *
import math


def main(argv):
    # check for command line argument or file
    if len(argv) > 1:
        filename = argv[1]
    else:
        while True:
            # enter the filename or hit enter to have a blank canvas
            print("To start from scratch hit enter. Other wise enter the file name: ")
            filename = input()
            # check if filename is valid
            if os.path.isfile(filename):
                break
            elif filename == "":
                break
            else:
                print("This file does not exist, try again.")

    win = GraphWin("Closest Points", 800, 800)  # create the window

    title = Text(Point(400, 20), "Click Anywhere: The Closest Two Points Will Be Circled")
    title.draw(win)  # draw instructions

    button(Point(725, 15), Point(775, 45), Point(750, 30), "EXIT", win)  # create exit button

    points_x = []  # initialize list of points
    circled = False  # must start out as false because closest two have yet to be calculated

    # plot all the points in the file and circle the closest two
    if filename != "":
        # open file
        file = open(filename, 'r')
        for line in file:
            row = line.split(",")
            x = float(row[0])
            y = float(row[1])
            points_x.append((x, y))
            plot_points(Point(x, y), win) # plot points

        # sort the lists by x and y
        points_x.sort()
        points_y = sorted(points_x, key=lambda k: [k[1], k[0]])
        # figure out and circle closest two
        d, p1, p2, = closest_two(points_x, points_y)
        c1, c2 = circle_closest(p1, p2, color_rgb(0, 255, 0), win)
        circled = True

    # when there are mouse clicks (new points) update closest
    while True:
        p = win.getMouse()
        x, y = p.getX(), p.getY()

        # if the exit button is clicked
        if 725 <= x <= 775 and 15 <= y <= 45:
            break

        plot_points(Point(x, y), win)  # plot new mouse click
        points_x.append((x, y))  # add the point to lists
        points_x.sort()
        points_y = sorted(points_x, key=lambda k: [k[1], k[0]])

        if len(points_x) > 1:
            # figure out new closest two
            if circled is False:
                d, p1, p2, = closest_two(points_x, points_y)
                c1, c2 = circle_closest(p1, p2, color_rgb(0, 255, 0), win)
                circled = True
            else:
                d, p1, p2, = closest_two(points_x, points_y)
                c1.undraw()
                c2.undraw()
                c1, c2 = circle_closest(p1, p2, color_rgb(0, 255, 0), win)

    win.close()  # close the window

    print("The closest two points are " + str(p1) + " and " + str(p2))
    print("They are " + str(d) + " units apart")


def brute_force(points, num_pts):

    # initialize d, p1, p2 to be ready for updating (if necessary)
    d = distance_formula(points[0], points[1])
    p1, p2 = points[0], points[1]

    for i in range(0, num_pts):
        # this will go to either the length of the list given, but never over 7
        for j in range(i + 1, min(i + 8, num_pts)):
            # the distance between i and j
            temp_d = distance_formula(points[i], points[j])
            # if the new d is smaller than the old d update it
            if temp_d < d:
                d = temp_d
                p1 = points[i]
                p2 = points[j]

    return d, p1, p2


def closest_two(sorted_x, sorted_y):
    num_pts = len(sorted_x)
    # with three points use brute force method
    if num_pts <= 3:
        d, p1, p2 = brute_force(sorted_x, num_pts)

    # with more than three points use divide and conquer
    elif num_pts > 3:
        # split the x list in half
        left_x = sorted_x[:len(sorted_x) // 2]
        right_x = sorted_x[len(sorted_x) // 2:]

        # grab the mid x coordinate
        mid_x = (left_x[-1][0] + right_x[0][0]) / 2

        left_y = []
        right_y = []
        # split the y list in half
        for point in sorted_y:
            if point[0] < mid_x:
                left_y.append(point)
            else:
                right_y.append(point)

        # recursive call
        leftD, leftP1, leftP2 = closest_two(left_x, left_y)
        rightD, rightP1, rightP2 = closest_two(right_x, right_y)

        # smallest delta and points of the two recursive call
        if leftD > rightD:
            d, p1, p2 = rightD, rightP1, rightP2
        else:
            d, p1, p2 = leftD, leftP1, leftP2

        # if the points are within the d put into new list
        delta_span = []
        for point in sorted_y:
            if (mid_x - d) <= point[0] <= (mid_x + d):  # the span of d
                delta_span.append(point)

        if len(delta_span) > 1:
            # check the next seven points in the list (brute_force will only allow up to seven)
            delta, point1, point2 = brute_force(delta_span, len(delta_span))
            if delta < d:
                 d, p1, p2 = delta, point1, point2

    return d, p1, p2


def distance_formula(p1, p2):
    # distance formula
    d = (p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])
    distance = math.sqrt(d)
    return distance


# graphically circling the closest two
def circle_closest(p1, p2, color, win):
    c1 = Circle(Point(p1[0], p1[1]), 7)
    c1.setOutline(color)
    c2 = Circle(Point(p2[0], p2[1]), 7)
    c2.setOutline(color)
    c1.draw(win)
    c2.draw(win)
    return c1, c2


# graphically plotting the points
def plot_points(point, win):
    point = Circle(point, 2)
    point.setFill(color_rgb(0, 0, 0))  # fill is black
    point.draw(win)


# creating a button with text on it
def button(p1, p2, p3, message, win):
    ex = Rectangle(p1, p2)
    ex.setFill(color_rgb(204, 229, 255))  # fill in light blue

    text = Text(p3, message)
    text.setFill(color_rgb(255, 0, 0))  # fill in red

    ex.draw(win)
    text.draw(win)


if __name__ == "__main__":
    main(sys.argv)
