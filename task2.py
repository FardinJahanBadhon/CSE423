from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

w_width = 800
w_height = 600


s_inc = 0.2
max_points =100
g = 0.1
rad = 100


points = []

is_frozen = False
gravity_mode = False
attraction_mode = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.choice([-1, 1]) * random.uniform(1, 3)
        self.dy = random.choice([-1, 1]) * random.uniform(1, 3)
        self.color = [random.random() for _ in range(3)]
        self.is_blinking = False
        self.blink_state = True
        self.size = random.uniform(2, 6) 
        self.trail = [] 
        self.trail_length = 5

    def move(self):
        if not is_frozen:
           
            if gravity_mode:
                self.dy -= g

            
            if attraction_mode:
                for other in points:
                    if other != self:
                        dx = other.x - self.x
                        dy = other.y - self.y
                        distance = math.sqrt(dx**2 + dy**2)
                        if distance < rad:
                            attraction_factor = 1 - (distance / rad)
                            self.dx += dx * 0.05 * attraction_factor
                            self.dy += dy * 0.05 * attraction_factor

            self.x += self.dx
            self.y += self.dy

            if self.x <= 0 or self.x >= WINDOW_WIDTH:
                self.dx = -self.dx * 0.9
                self.x = max(0, min(self.x, WINDOW_WIDTH))
            if self.y <= 0 or self.y >= WINDOW_HEIGHT:
                self.dy = -self.dy * 0.9
                self.y = max(0, min(self.y, WINDOW_HEIGHT))

            self.trail.append((self.x, self.y))
            if len(self.trail) > self.trail_length:
                self.trail.pop(0)

    def draw(self):
        for i, (tx, ty) in enumerate(self.trail):
            trail_alpha = 1 - (i / len(self.trail))
            glColor4f(self.color[0], self.color[1], self.color[2], trail_alpha * 0.5)
            glPointSize(self.size * trail_alpha)
            glBegin(GL_POINTS)
            glVertex2f(tx, ty)
            glEnd()

        if self.is_blinking:
            if self.blink_state:
                glColor3f(*self.color)
            else:
                glColor3f(0, 0, 0)
        else:
            glColor3f(*self.color)

        glPointSize(self.size)
        glBegin(GL_POINTS)
        glVertex2f(self.x, self.y)
        glEnd()

    def adjust_speed(self, factor):
        self.dx *= factor
        self.dy *= factor

    def toggle_blink(self):
        self.is_blinking = not self.is_blinking

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    for point in points:
        point.draw()
    glutSwapBuffers()

def idle():
    if not is_frozen:
        for point in points:
            point.move()

    for i in points:
        if i.is_blinking:
            i.blink_state = not i.blink_state

    glutPostRedisplay()

def mouse(button, state, x, y):
    global is_frozen, points
    if not is_frozen:
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            y = WINDOW_HEIGHT - y
            if len(points) < max_points:
                points.append(Point(x, y))
        elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
            for point in points:
                point.toggle_blink()

def reshape(width, height):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    WINDOW_WIDTH, WINDOW_HEIGHT = width, height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def special_keys(key, x, y):
    global is_frozen, gravity_mode, attraction_mode
    if not is_frozen:
        if key == GLUT_KEY_UP:
            for point in points:
                point.adjust_speed(1 + s_inc)
        elif key == GLUT_KEY_DOWN:
            for point in points:
                point.adjust_speed(max(0.1, 1 - s_inc))
        elif key == GLUT_KEY_F1:
            gravity_mode = not gravity_mode
        elif key == GLUT_KEY_F2:
            attraction_mode = not attraction_mode

def keyboard(key, x, y):
    global is_frozen, points
    if key == b' ':
        is_frozen = not is_frozen
    elif key == b'c':
        points.clear() 
    elif key == b'r':
        for point in points:
            point.dx = random.choice([-1, 1]) * random.uniform(1, 3)
            point.dy = random.choice([-1, 1]) * random.uniform(1, 3)

def main():
    try:
        glutInit()
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
        glutInitWindowSize(w_width, w_height)
        glutCreateWindow(b"Buinding the amazing box")

        glClearColor(0, 0, 0, 1)

        glutDisplayFunc(display)
        glutIdleFunc(idle)
        glutMouseFunc(mouse)
        glutReshapeFunc(reshape)
        glutSpecialFunc(special_keys)
        glutKeyboardFunc(keyboard)

        print("Controls:")
        print("Left Click: Add point")
        print("Right Click: Toggle blinking")
        print("Space: Pause/Resume")
        print("Up/Down Arrows: Adjust speed")
        print("F1: Toggle Gravity")
        print("F2: Toggle Attraction")
        print("'c': Clear points")
        print("'r': Randomize velocities")

        glutMainLoop()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()