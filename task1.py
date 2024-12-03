from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

class Rain_Animation:
    def __init__(self, num_drops=200, w_width=1024, w_height=768):
        self.num_rd = num_drops
        self.raindrops = []
        self.rain_direction = 0.0
        self.bg_color = 1.0
        self.w_width = w_width
        self.w_height = w_height
        
        self.drop_speed = 0.05
        self.drop_length = 0.1
        self.max_rain_direction = 0.01

    def init_raindrops(self):
        self.raindrops = [
            [random.uniform(-1.0, 1.0), 
             random.uniform(0.0, 1.0), 
             random.uniform(0.01, 0.05)]  
            for i in range(self.num_rd)
        ]


    def draw_house(self):
        house_color = 1.0 - self.bg_color 
        glColor3f(house_color, house_color, house_color) 

        #Windows
        glBegin(GL_LINES)
       
        glVertex2f(-0.35, -0.2)  # Top left
        glVertex2f(-0.15, -0.2)  # Top right
        glVertex2f(-0.35, -0.2)  # Top left
        glVertex2f(-0.35, -0.4)  # Bottom left
        glVertex2f(-0.15, -0.2)  # Top right
        glVertex2f(-0.15, -0.4)  # Bottom right
        glVertex2f(-0.35, -0.4)  # Bottom left
        glVertex2f(-0.15, -0.4)  # Bottom right

        # Window cross lines
        glVertex2f(-0.35, -0.3)  # Horizontal mid line
        glVertex2f(-0.15, -0.3)
        glVertex2f(-0.25, -0.2)  # Vertical mid line
        glVertex2f(-0.25, -0.4)

        # Right window (similar structure)
        glVertex2f(0.15, -0.2)
        glVertex2f(0.35, -0.2)
        glVertex2f(0.15, -0.2)
        glVertex2f(0.15, -0.4)
        glVertex2f(0.35, -0.2)
        glVertex2f(0.35, -0.4)
        glVertex2f(0.15, -0.4)
        glVertex2f(0.35, -0.4)

        # Right window cross lines
        glVertex2f(0.15, -0.3)
        glVertex2f(0.35, -0.3)
        glVertex2f(0.25, -0.2)
        glVertex2f(0.25, -0.4)
        glEnd()

        # Roof
        glBegin(GL_LINES)
        glVertex2f(-0.5, 0.0)
        glVertex2f(0.0, 0.5)
        glVertex2f(0.0, 0.5)
        glVertex2f(0.5, 0.0)
        glVertex2f(0.5, 0.0)
        glVertex2f(-0.5, 0.0)
        glEnd()

        # Walls
        glBegin(GL_LINES)
        glVertex2f(-0.4, 0.0)
        glVertex2f(-0.4, -0.6)
        glVertex2f(0.4, 0.0)
        glVertex2f(0.4, -0.6)
        glVertex2f(-0.4, -0.6)
        glVertex2f(0.4, -0.6)
        glEnd()

        # Door
        glBegin(GL_LINES)
        glVertex2f(-0.1, -0.6)
        glVertex2f(-0.1, -0.3)
        glVertex2f(0.1, -0.6)
        glVertex2f(0.1, -0.3)
        glVertex2f(-0.1, -0.3)
        glVertex2f(0.1, -0.3)
        glEnd()

    def draw_raindrops(self):
        rain_color = 1.0 - self.bg_color
        glColor3f(rain_color, rain_color, rain_color)
        glLineWidth(1.5) 
        
        glBegin(GL_LINES)
        for i in self.raindrops:
            glVertex2f(i[0], i[1])
            glVertex2f(i[0] + self.rain_direction, 
                       i[1] - i[2])  
        glEnd()

    def update_raindrops(self):
        for i in self.raindrops:
            i[1] -=i[2]
            i[0] += self.rain_direction
            
            if i[1] < -1.0:
                i[1] = 1.0
                i[0] = random.uniform(-1.0, 1.0)
                i[2] = random.uniform(0.01, 0.05) 

            if i[0] < -1.0:
                i[0] = 1.0
            elif i[0] > 1.0:
                i[0] = -1.0

    def key_pressed(self, key, x, y):
        if key == b'\x1b':
            glutLeaveMainLoop()
        elif key == GLUT_KEY_LEFT:
            self.rain_direction = max(-self.max_rain_direction, self.rain_direction - 0.001)
                                      
        elif key == GLUT_KEY_RIGHT:
            self.rain_direction = min(self.max_rain_direction, self.rain_direction + 0.001)

        elif key == b'd':
            self.bg_color = min(1.0, self.bg_color + 0.05)
        elif key == b'n':
            self.bg_color = max(0.0, self.bg_color - 0.05)

    def display(self):
        glClearColor(self.bg_color, 
                     self.bg_color, 
                     self.bg_color, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)
        self.draw_house()
        self.draw_raindrops()
        glutSwapBuffers()

    def timer(self, value):
        self.update_raindrops()
        glutPostRedisplay()
        glutTimerFunc(16, self.timer, 0)

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
        glutInitWindowSize(self.w_width, self.w_height)
        glutCreateWindow(b"Building a House in Rainfall")
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        self.init_raindrops()
        
        glutDisplayFunc(self.display)
        glutSpecialFunc(self.key_pressed)
        glutKeyboardFunc(self.key_pressed)
        glutTimerFunc(0, self.timer, 0)
        glutMainLoop()

def main():
    animation = Rain_Animation()
    animation.run()

if __name__ == "__main__":
    main()