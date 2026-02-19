# -*- coding: utf-8 -*-
"""
Sterter Code for the display of CLosest Points in Python
"""

import tkinter as tk
from random import uniform
import time

class Points:
    def __init__(self):
        self.points = []
        self.num = 10

    def generate(self, num):
        # we have a 1000*1000 and there is num = number of grids for each point, so we can divide 1000*1000 into num*num grid to find the x and y 
        x, y = 1000*1000/num/num, 1000*1000/num/num
        d = 1000/y
        i,j = 0,0

        xtimes, ytimes = 1,1

        while i < d:
            while j < d:
                self.points.append((uniform(j, x*xtimes), uniform(i, y*ytimes)))
                j += x
                ytimes += 1
            i += y
            j = 0
            xtimes += 1

       
        
        #
        # *** This needs to be improved to make it interesting ***
        #
    def get_points(self):
        return self.points
    
    
    def distance(self, p1, p2):
        # Calculate the distance between two points
        return ((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5
    
    
    def Split(self, Px, Py, mid):
        midpoint_x = Px[mid][0]
        Ly, Ry = [], []
        for p in Py:
            if p[0] <= midpoint_x:
                Ly.append(p)
            else:
                Ry.append(p)
        return Ly, Ry

    
    def closest_pair(self, Px, Py):
        n = len(Px)

        #print (n, " points in closest_pair") #print function for testing

        if n <= 3:
            min_dist = float('inf')
            closest_pair = (None, None)
            for i in range(n):
                for j in range(i + 1, n):
                    dist = self.distance(Px[i], Px[j])
                    if dist < min_dist:
                        min_dist = dist
                        closest_pair = (Px[i], Px[j])
            return closest_pair[0], closest_pair[1], min_dist
        
        mid = n//2
        midpoint_x = Px[mid][0]

        Lx = Px[:mid]
        Rx = Px[mid:]

        Ly, Ry = self.Split(Px, Py, mid)

        p1L, p2L, distL = self.closest_pair(Lx, Ly)
        p1R, p2R, distR = self.closest_pair(Rx, Ry)

        if distL < distR:
            d = distL
            closest_pair = (p1L, p2L)

        else:
            d = distR
            closest_pair = (p1R, p2R)

        #merge 
        Sy = [p for p in Py if abs(p[0] - midpoint_x) < d]

        for i in range(len(Sy)):
            for j in range(i+1, min(i+16, len(Sy))):
                dist = self.distance(Sy[i], Sy[j])
                if dist < d:
                    d = dist
                    closest_pair = (Sy[i], Sy[j])

        #print (d, " is the distance between ", closest_pair[0], " and ", closest_pair[1], end = "\n") #print function for testing

        return closest_pair[0], closest_pair[1], d
    
    
    def closest_points(self):
        if len(self.points) < 2:
            return None, None, 0.0
        
        Px = sorted(self.points, key=lambda p: p[0])  # Sort by x-coordinate
        Py = sorted(self.points, key=lambda p: p[1])  # Sort by y-coordinate


        return self.closest_pair(Px, Py)
   


    
   
    
class App:
    def __init__(self, root):
        self.root = root
        self.points = Points()

        # Left frame for canvas
        left_frame = tk.Frame(root)
        left_frame.pack(side="left")

        self.canvas = tk.Canvas(left_frame, width=1100, height=1100, bg="white")
        self.canvas.pack()

        # Right frame for controls
        right_frame = tk.Frame(root)
        right_frame.pack(side="right", padx=10, pady=10)

        # Slider to control the number of points
        self.slider = tk.Scale(
            right_frame,
            from_=10,
            to=1000,
            orient="vertical",
            label="Number of points",
            length=300,
            command=self.on_slider
        )
        
        self.slider.set(100)
        self.slider.grid(row=0, column=1, padx=10, pady=10)

        # Button to generate a new set of points
        self.gen_button = tk.Button(right_frame, text="Generate Points", command=self.generate)
        self.gen_button.grid(row=1, column=1, padx=5)

        # Button to trigger the solver to find the closest pair or pairs of points
        self.solve_button = tk.Button(right_frame, text="Solve", command=self.solve)
        self.solve_button.grid(row=2, column=1, padx=5)
        self.time_text_id = None

        self.on_slider(100) # Set up the first set of random points

    def on_slider(self, val):
        num = int(val)
        self.points.generate(num)
        self.draw_points()

    def generate(self):


        num = self.slider.get()
        self.points.generate(num)
        self.draw_points()

    def solve(self):
        start_time = time.perf_counter() # Start a timer
        
        # 
        # *** Add your code here to find and highlight the closest points ***
        # Get the closest distance value and the points as tuple.
        # That gves an accurate estimate of the computation time.
        # The display time should be fairly small.
        # 
        p1, p2, distance = self.points.closest_points()
        #distance = 0.0
        
        end_time = time.perf_counter() # Stop the timer

        print ("Closest pair: {} and {}, distance: {:.3f}".format(p1, p2, distance)) #print function for testing



        elapsed_ms = (end_time - start_time) * 1000

        print ("solve time = {:.2f} ms".format(elapsed_ms)) #print function for testing





        # Format the display string to two decimal places
        time_str = "Solve time: {:.2f} ms  Distance: {:.3f}".format(elapsed_ms, distance)

        # Remove previous timing text if it exists
        if self.time_text_id:
            self.canvas.delete(self.time_text_id)

        # Display the timing in the lower-left corner
        self.time_text_id = self.canvas.create_text(
            50, 1070,
            text=time_str,
            anchor="sw",
            font=("Helvetica", 10),
            fill="black",
            tags="timing"
        )

    def draw_points(self):
        # Clear the area before we redeaw
        self.canvas.delete("all")
        # Draw the black box around the valid 1000x1000 region
        self.canvas.create_rectangle(50, 50, 1050, 1050, outline="black")
        offset = 50 # Offset from the left and top for drawing
        for x, y in self.points.get_points():
            cx = x + offset
            cy = 1000 - y + offset # Flip the screen so that y is up
            self.canvas.create_oval(cx - 2, cy - 2, cx + 2, cy + 2, fill="black", tags="points")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Shortest Distance Between Points - My Name (########)")
    app = App(root)
    root.mainloop()
