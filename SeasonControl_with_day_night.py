from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time
import random
from math import cos, sin, pi

class SeasonalCycle:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.season = 1  # 0:Rainy, 1:Summer, 2:Spring, 3:Winter
        self.day_time = 0  # 0 to 1 representing time of day
        self.last_update = time.time()
        self.in_menu = True
        self.transition_speed = 0.1  # Control day/night cycle speed
        self.raindrops = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(100)]
        self.snowflakes = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(100)]
        self.leaves = [(random.randint(0, self.width), random.randint(0, self.height)) for _ in range(50)] 
        
    def init_gl(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glPointSize(2.0)
        gluOrtho2D(0, self.width, 0, self.height)

    def plot_point(self, x, y):
        glBegin(GL_POINTS)
        glVertex2f(x, y)
        glEnd()

    def draw_text(self, string, x, y, color=(1.0, 1.0, 1.0)):
        glColor3f(*color)
        glRasterPos2f(x, y)
        for char in string:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    def handle_keyboard(self, key, x, y):
        if key == b'm':  
            self.season = 2 #Spring
        elif key == b'n':  
            self.season = 3 #Winter
        elif key == b'o':  
            self.season = 0 #Rainy
        elif key == b'p':
            self.season = 1 #Summer

        if key == b'\r' or key == b'\n':  # Handle both Enter and Return
            self.in_menu = False
            self.last_update = time.time()  # Reset timer when starting
            glutPostRedisplay()
        elif key == b'q' or key == b'Q':  # Add quit functionality
            glutLeaveMainLoop()

    # def draw_house(self):
        
    #     glColor3f(1.0, 1.0, 0.0)  
       
    #     self.midpoint_line(300, 200, 500, 200)  
    #     self.midpoint_line(300, 200, 300, 280)  
    #     self.midpoint_line(500, 200, 500, 280) 
    #     self.midpoint_line(300, 280, 500, 280)  

       
    #     glColor3f(1.0, 0.0, 0.0)  
        
    #     self.midpoint_line(280, 280, 520, 280) 
    #     self.midpoint_line(280, 280, 400, 350)  
    #     self.midpoint_line(520, 280, 400, 350)  

        
    #     glColor3f(0.4, 0.2, 0.1)  
       
    #     self.midpoint_line(370, 200, 370, 265)  
    #     self.midpoint_line(430, 200, 430, 265)  
    #     self.midpoint_line(370, 265, 430, 265)
    def draw_house(self):
        
        glColor3f(1.0, 1.0, 0.0)  
       
        self.midpoint_line(280, 200, 480, 200)  
        self.midpoint_line(280, 200, 280, 280)  
        self.midpoint_line(480, 200, 480, 280) 
        self.midpoint_line(280, 280, 480, 280)  

       
        glColor3f(1.0, 0.0, 0.0)  
        
        self.midpoint_line(260, 280, 500, 280) 
        self.midpoint_line(260, 280, 380, 350)  
        self.midpoint_line(500, 280, 380, 350)  

        
        glColor3f(0.4, 0.2, 0.1)  
       
        self.midpoint_line(350, 200, 350, 255)  
        self.midpoint_line(410, 200, 410, 255)  
        self.midpoint_line(350, 255, 410, 255)


    def draw_menu(self):
        glClear(GL_COLOR_BUFFER_BIT)
        # Center the text better
        title = "Seasonal Cycle Simulation"
        instruction = "Press ENTER to start"
        quit_text = "Press Q to quit"
        
        self.draw_text(title, self.width//2 - len(title)*4.5, self.height//2 + 50, (0.0, 1.0, 0.0))
        self.draw_text(instruction, self.width//2 - len(instruction)*4.5, self.height//2)
        self.draw_text(quit_text, self.width//2 - len(quit_text)*4.5, self.height//2 - 50)

    def draw_ground(self):
        season_colors = {
            0: (0.4, 0.8, 0.4),  # Rainy: Light green
            1: (0.2, 0.8, 0.2),  # Summer: Vibrant green
            2: (0.8, 0.4, 0.2),  # Spring: Orange-brown
            3: (0.9, 0.9, 0.8),  # Winter: White
        }
        
        glColor3f(*season_colors[self.season])
        glBegin(GL_QUADS)
        glVertex2f(0, 0)
        glVertex2f(self.width, 0)
        glVertex2f(self.width, self.height/3)
        glVertex2f(0, self.height/3)
        glEnd()

    def draw_sky(self):
        if self.day_time < 0.25:  # Night
            sky_color = (0.0, 0.0, 0.1)
        elif self.day_time < 0.4:  # Dawn
            sky_color = (0.7, 0.5, 0.3)
        elif self.day_time < 0.7:  # Day
            sky_color = (0.4, 0.6, 1.0)
        elif self.day_time < 0.8:  # Dusk
            sky_color = (0.7, 0.5, 0.3)
        else:  # Night
            sky_color = (0.0, 0.0, 0.1)

        glColor3f(*sky_color)
        glBegin(GL_QUADS)
        glVertex2f(0, self.height/3)
        glVertex2f(self.width, self.height/3)
        glVertex2f(self.width, self.height)
        glVertex2f(0, self.height)
        glEnd()

    def draw_rain(self):
        if self.season == 0:
            glColor3f(1.0, 1.0, 1.0)
            speed = 30
            for i in range(len(self.raindrops)):
                x, y = self.raindrops[i]
                for offset in range(5):
                    self.plot_point(x, y - offset)
                y -= speed
                if y <= 0:
                    x = random.randint(0, self.width)
                    y = random.randint(self.height, self.height + 100)
                self.raindrops[i] = (x, y)

    def draw_snow(self):
        if self.season == 3:
            glColor3f(1.0, 1.0, 1.0)
            for i in range(len(self.snowflakes)):
                x, y = self.snowflakes[i]
                x += random.randint(-1, 1)
                y -= 2
                if y <= 0:
                    x = random.randint(0, self.width)
                    y = random.randint(self.height, self.height + 100)
                self.snowflakes[i] = (x, y)
                self.plot_point(x, y)
                
    def draw_leaves(self):
        if self.season == 2: 
            glColor3f(0.8, 0.4, 0.2)  
            for i in range(len(self.leaves)):
                x, y = self.leaves[i]
                x += random.randint(-2, 2)  
                y -= random.randint(1, 3)   
                
                if y <= 0:
                    x = random.randint(0, self.width)
                    y = random.randint(self.height, self.height + 100)
                    
                self.leaves[i] = (x, y)
                
                self.plot_point(x, y)        
                self.plot_point(x, y + 2)    
                self.plot_point(x - 2, y)    
                self.plot_point(x, y - 2)    
                self.plot_point(x + 2, y)

    def draw_sun(self, x, y):
        if self.season != 0:
            if self.day_time < 0.25 or self.day_time >= 0.8:  # Night
                sun_color = (1.0, 1.0, 1.0)  # Moon: White
            else:
                if self.season == 3:
                    sun_color = (0.9, 0.9, 0.8)  # Sun: Yellow
                else:
                    sun_color = (1.0, 1.0, 0.0)

            glColor3f(*sun_color)
            segments = 32
            glBegin(GL_TRIANGLE_FAN)
            glVertex2f(x, y)  # Center
            radius = 30
            for i in range(segments + 1):
                angle = 2 * pi * i / segments
                glVertex2f(x + radius * cos(angle), y + radius * sin(angle))
            glEnd() 

    def midpoint_line(self, x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.plot_point(x1, y1)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def midpoint_circle(self, center_x, center_y, radius):
        x = radius
        y = 0
        decision = 1 - radius

        while y <= x:
            self.plot_point(center_x + x, center_y + y)
            self.plot_point(center_x + y, center_y + x)
            self.plot_point(center_x - y, center_y + x)
            self.plot_point(center_x - x, center_y + y)
            self.plot_point(center_x - x, center_y - y)
            self.plot_point(center_x - y, center_y - x)
            self.plot_point(center_x + y, center_y - x)
            self.plot_point(center_x + x, center_y - y)

            y += 1
            if decision <= 0:
                decision += 2 * y + 1
            else:
                x -= 1
                decision += 2 * (y - x) + 1
    
    # def draw_tree(self):
       
    #     glColor3f(0.55, 0.27, 0.07)
        
    #     self.midpoint_line(700, 200, 700, 400)  
    #     self.midpoint_line(720, 200, 720, 400)  
    #     self.midpoint_line(700, 400, 720, 400)  

        
    #     branch_points = [
            
    #         (710, 400, 660, 450),  
    #         (710, 400, 760, 450),  
    #         (710, 450, 670, 500),  
    #         (710, 450, 750, 500),  
    #         (710, 500, 680, 550),  
    #         (710, 500, 740, 550),  
           
    #         (660, 450, 640, 500), (760, 450, 780, 500),  
    #         (670, 500, 650, 550), (750, 500, 770, 550),  
    #         (680, 550, 660, 600), (740, 550, 760, 600),  
    #         (710, 550, 710, 650)  
    #     ]

    #     for start_x, start_y, end_x, end_y in branch_points:
    #         self.midpoint_line(start_x, start_y, end_x, end_y)

       
    #     if self.season == 2:  # Spring
    #         glColor3f(1.0, 0.647, 0.0)  
    #     elif self.season == 3:  
    #         glColor3f(1.0, 1.0, 1.0)
    #     else:
    #         glColor3f(0.1, 0.5, 0.1) 
        
    #     leaf_positions = [
    #         (660, 450), (760, 450), (670, 500), (750, 500),
    #         (680, 550), (740, 550), (710, 550),

    #         (640, 500), (780, 500), (650, 550), (770, 550),
    #         (660, 600), (760, 600), (710, 650)
    #     ]

        
    #     for center_x, center_y in leaf_positions:
    #         for dx in range(-15, 16, 5):
    #             for dy in range(-15, 16, 5):
    #                 if dx**2 + dy**2 <= 225:  
    #                     self.midpoint_circle(center_x + dx, center_y + dy, random.randint(2, 5))

        
    #     for _ in range(100):
    #         random_x = random.randint(640, 780)
    #         random_y = random.randint(500, 650)
    #         self.midpoint_circle(random_x, random_y, random.randint(2, 5))
    def draw_tree(self):
        def draw_branch(x, y, length, angle, depth):
            """Draws branches recursively."""
            if depth == 0:
                return

            # Calculate the end point of the current branch
            end_x = x + length * math.cos(math.radians(angle))
            end_y = y + length * math.sin(math.radians(angle))

            # Draw the branch
            glColor3f(0.55, 0.27, 0.07)  # Brown color for trunk/branches
            glBegin(GL_LINES)
            glVertex2f(x, y)
            glVertex2f(end_x, end_y)
            glEnd()

            # Draw sub-branches
            new_length = length * 0.7  # Reduce length for sub-branches
            draw_branch(end_x, end_y, new_length, angle - random.randint(20, 30), depth - 1)
            draw_branch(end_x, end_y, new_length, angle + random.randint(20, 30), depth - 1)

            # Draw leaves at the end of branches
            if depth == 1:
                draw_leaves(end_x, end_y)

        def draw_leaves(x, y):
            """Draws a cluster of leaves at the given position."""
            if self.season == 2:  # Fall
                glColor3f(1.0, 0.5, 0.0)  # Orange leaves
            elif self.season == 3:  # Winter
                return  # No leaves in winter
            else:
                glColor3f(0.1, 0.8, 0.1)  # Green leaves for spring/summer

            # Draw a cluster of small circles as leaves
            glBegin(GL_POINTS)
            for _ in range(100):
                dx = random.uniform(-10, 10)
                dy = random.uniform(-10, 10)
                if dx ** 2 + dy ** 2 <= 100:  # Within a circle of radius 10
                    glVertex2f(x + dx, y + dy)
            glEnd()

        # Start drawing the trunk and branches
        draw_branch(self.width // 5, 150, 100, 90, 5)  # Start point, initial length, angle, depth


    def draw_stars(self):
        if self.day_time > 0.8 or self.day_time < 0.3:
            glColor3f(1.0, 1.0, 1.0)
            glPointSize(2.0)
            glBegin(GL_POINTS)
            # for _ in range(100):
            #     x = (hash(str(_ * 123)) % self.width)
            #     y = (hash(str(_ * 456)) % (self.height - self.height//3)) + self.height//3
            #     glVertex2f(x, y)
            current_time = time.time()  # Get the current time
            for i in range(100):
                x = (hash(str(i * 123)) % self.width)
                y = (hash(str(i * 456)) % (self.height - self.height // 3)) + self.height // 3
                brightness = 0.5 + 0.5 * math.sin(current_time + i * 0.1)  # Vary brightness over time
                glColor3f(brightness, brightness, brightness)  # Apply brightness to star color
                glVertex2f(x, y)
            glEnd()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT)
        
        if self.in_menu:
            self.draw_menu()
        else:
            self.draw_sky()
            self.draw_stars()
            self.draw_house()
            #self.draw_tree() 
            self.draw_rain()
            self.draw_snow()
            self.draw_leaves()
            # Calculate sun/moon position
            sun_x = int(self.width * self.day_time)
            sun_y = int(self.height/2 + math.sin(self.day_time * math.pi) * 200)
            self.draw_sun(sun_x, sun_y)
            self.draw_tree()
            self.draw_ground()
            
            # Display current season
            seasons = ["Rainy", "Summer", "Spring", "Winter"]
            self.draw_text(f"Season: {seasons[self.season]}", 10, self.height - 30)
            
        glutSwapBuffers()

    def update(self, value):
        if not self.in_menu:
            current_time = time.time()
            elapsed = current_time - self.last_update
            
            self.day_time += elapsed * self.transition_speed
            if self.day_time >= 1.0:
                self.day_time = 0.0
                #self.season = (self.season + 1) % 4

            self.last_update = current_time
        
        glutPostRedisplay()
        glutTimerFunc(16, self.update, 0)

def main():
    cycle = SeasonalCycle()
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(cycle.width, cycle.height)
    glutCreateWindow(b"Seasonal Cycle")
    
    cycle.init_gl()
    glutDisplayFunc(cycle.display)
    glutKeyboardFunc(cycle.handle_keyboard)
    glutTimerFunc(0, cycle.update, 0)
    
    try:
        glutMainLoop()
    except SystemExit:
        pass

if __name__ == "__main__":
    main()