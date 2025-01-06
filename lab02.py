from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18
import random
import time
import math

W_WIDTH, W_HEIGHT = 500, 800 
bullet_list = []
bubble_list = [] 
score = 0
misfires = 0
freeze = False
gameover = 0 
last_frame_time = 0
bullet_speed = 300
rocket_x = 0 

def create_bubble(existing_bubbles):
    is_dynamic = random.random() < 0.2 
    r = random.randint(15, 20)
    color = [0, 0, 1]
    if is_dynamic:
        color = [0, 1, 0]
    while True:
        x = random.randint(-220, 220)
        y = 300

        if not check_bubble_overlap(x, y, r, existing_bubbles):
            bubble = {
                'x': x, 
                'y': y, 
                'r': r, 
                'color': color,
                'is_dynamic': is_dynamic,
                'dynamic_phase': 0,
                'dynamic_direction': 1
            }
            return bubble
        
def update_dynamic_bubble(bubble, delta_time):
    """Update the radius of a dynamic bubble."""
    if bubble.get('is_dynamic', False):
        amplitude = 8 
        frequency = 10 
        bubble['dynamic_phase'] += delta_time * frequency * bubble['dynamic_direction'] 
        radius_change = math.sin(bubble['dynamic_phase']) * amplitude 
        new_radius = bubble['r'] + radius_change 
        new_radius = max(15, min(new_radius, 25)) 
        bubble['r'] = new_radius

        if abs(radius_change) < 0.1:
            bubble['dynamic_direction'] *= -1
def check_bubble_overlap(x, y, r, other_bubbles):
    for i in other_bubbles:
        distance = ((x - i['x']) ** 2 + (y - i['y']) ** 2) ** 0.5
        if distance < (r +i['r']):
            return True
    return False
def plot_point(x, y):
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()
def convert_to_zone0(x, y, zone):
    zone_map = {
        0: (x, y),
        1: (y, x),
        2: (y, -x),
        3: (-x, y),
        4: (-x, -y),
        5: (-y, -x),
        6: (-y, x),
        7: (x, -y)
    }
    return zone_map[zone]

def convert_from_zone0(x, y, zone):
    zone_map = {
        0: (x, y),
        1: (y, x),
        2: (-y, x),
        3: (-x, y),
        4: (-x, -y),
        5: (-y, -x),
        6: (y, -x),
        7: (x, -y)
    }
    return zone_map[zone]

def midpoint_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    zone = 0
    if abs(dx) > abs(dy):
        if dx >= 0 and dy >= 0:
            zone = 0
        elif dx < 0 and dy >= 0:
            zone = 3
        elif dx < 0 and dy < 0:
            zone = 4
        elif dx >= 0 and dy < 0:
            zone = 7
    else:
        if dx >= 0 and dy >= 0:
            zone = 1
        elif dx < 0 and dy >= 0:
            zone = 2
        elif dx < 0 and dy < 0:
            zone = 5
        elif dx >= 0 and dy < 0:
            zone = 6

    x1, y1 = convert_to_zone0(x1, y1, zone)
    x2, y2 = convert_to_zone0(x2, y2, zone)
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)
    x, y = x1, y1
    x0, y0 = convert_from_zone0(x, y, zone)
    plot_point(x0, y0)
    while x < x2:
        if d <= 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1
        x0, y0 = convert_from_zone0(x, y, zone)
        plot_point(x0, y0)


def midpointcircle(radius, centerX=0, centerY=0):
    glBegin(GL_POINTS)
    x = 0
    y = radius
    d = 1 - radius
    while y > x:
        glVertex2f(x + centerX, y + centerY)
        glVertex2f(x + centerX, -y + centerY)
        glVertex2f(-x + centerX, y + centerY)
        glVertex2f(-x + centerX, -y + centerY)
        glVertex2f(y + centerX, x + centerY)
        glVertex2f(y + centerX, -x + centerY)
        glVertex2f(-y + centerX, x + centerY)
        glVertex2f(-y + centerX, -x + centerY)
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * x - 2 * y + 5
            y -= 1
        x += 1
    glEnd()

def bubble_x_position(bubble):
    return bubble['x']

def draw_bullet():
    global bullet_list
    glColor3f(1, 0, 0)
    for i in bullet_list:
        midpointcircle(8, i[0], i[1])

def draw_bubble():
    
    global bubble_list
    for i in bubble_list:
        glColor3f(i['color'][0], i['color'][1], i['color'][2])
        midpointcircle(i['r'], i['x'], i['y'])

def draw_ui():
    global rocket_x, score, misfires, freeze

    # Shooter
    glPointSize(2)
    glColor3f(1, 1, 1)
    
    # Draw the rocket body
    midpoint_line(rocket_x - 10, -345, rocket_x - 10, -315)
    midpoint_line(rocket_x + 10, -345, rocket_x + 10, -315)
    midpoint_line(rocket_x - 10, -315, rocket_x + 10, -315)
    
    # Draw the rocket tip
    midpoint_line(rocket_x - 10, -315, rocket_x, -295)
    midpoint_line(rocket_x + 10, -315, rocket_x, -295)
    
    # Draw the rocket fins
    midpoint_line(rocket_x - 10, -345, rocket_x - 15, -355)
    midpoint_line(rocket_x + 10, -345, rocket_x + 15, -355)
    midpoint_line(rocket_x - 15, -355, rocket_x - 10, -355)
    midpoint_line(rocket_x + 15, -355, rocket_x + 10, -355)
    
    # Draw the rocket fire
    glColor3f(1, 0.5, 0)
    midpoint_line(rocket_x - 5, -355, rocket_x, -375)
    midpoint_line(rocket_x + 5, -355, rocket_x, -375)
    midpoint_line(rocket_x - 5, -355, rocket_x + 5, -355)

    # Draw black box around rocket for collision detection
    glColor3f(0, 0, 0)  
    midpoint_line(rocket_x - 20, -375, rocket_x + 20, -375)  # Bottom line
    midpoint_line(rocket_x - 20, -295, rocket_x + 20, -295)  # Top line
    midpoint_line(rocket_x - 20, -375, rocket_x - 20, -295)  # Left line
    midpoint_line(rocket_x + 20, -375, rocket_x + 20, -295)  # Right line


    glPointSize(4)
    glColor3f(0, 0.8, 1)
    midpoint_line(-208, 350, -160, 350)
    glPointSize(3)
    midpoint_line(-210, 350, -190, 370)
    midpoint_line(-210, 350, -190, 330)

    glPointSize(4)
    glColor3f(0.9, 0, 0)
    midpoint_line(210, 365, 180, 335)
    midpoint_line(210, 335, 180, 365)

    glPointSize(4)
    glColor3f(1, .5, 0)
    if freeze:
        midpoint_line(-15, 370, -15, 330)
        midpoint_line(-15, 370, 15, 350)
        midpoint_line(-15, 330, 15, 350)
    else:
        midpoint_line(-10, 370, -10, 330)
        midpoint_line(10, 370, 10, 330)

    
    glColor3f(1, 1, 1)
    
    glRasterPos2f(-240, -390)
    for ch in f"Score: {score}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    glRasterPos2f(140, -390)
    for ch in f"Misfires: {misfires}/3":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))
    
    glRasterPos2f(-80, -390)
    for ch in f"Missed Bubble: {gameover}":
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

def convert_coordinate(x, y):
    """Convert screen coordinates to OpenGL coordinates."""
    a = x - (W_WIDTH / 2)
    b = (W_HEIGHT / 2) - y
    return a, b

def restart_game():
    global freeze, bubble_list, score, gameover, misfires, bullet_list, rocket_x
    freeze = False
    bubble_list = []
    num_starting_bubbles = random.randint(3, 5)
    for _ in range(num_starting_bubbles):
        new_bubble = create_bubble(bubble_list)
        bubble_list.append(new_bubble)
    bubble_list.sort(key=bubble_x_position)
    score = 0
    gameover = 0
    misfires = 0
    bullet_list = []
    rocket_x = 0

def keyboardListener(key, _, __):
    """Handle keyboard input."""
    global bullet_list, freeze, gameover, rocket_x
    if key == b' ':
        if not freeze and gameover < 3:
            bullet_list.append([rocket_x, -365])
    elif key == b'a':
        if rocket_x > -230 and not freeze:
            rocket_x -= 20
    elif key == b'd':
        if rocket_x < 230 and not freeze:
            rocket_x += 20
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    """Handle mouse input."""
    global freeze, gameover, score, bubble_list, bullet_list, misfires
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        c_x, c_y = convert_coordinate(x, y)
        if -209 < c_x < -170 and 325 < c_y < 375:
            restart_game()
        elif 170 < c_x < 216 and 330 < c_y < 370:
            print(f'Goodbye! Score: {score}')
            glutLeaveMainLoop()
        elif -25 < c_x < 25 and 325 < c_y < 375:
            freeze = not freeze
    glutPostRedisplay()
def animate():
    """Main game animation and logic loop."""
    global freeze, bubble_list, gameover, score, bullet_list, misfires, last_frame_time, rocket_x
    
    current_time = time.time()
    delta_time = current_time - last_frame_time
    last_frame_time = current_time

    if not freeze and gameover < 3 and misfires < 3:
        
        new_bullet = []
        for b in bullet_list:
            if b[1] < 400: 
                new_bullet.append([b[0], b[1] + bullet_speed * delta_time])
            else: 
                misfires += 1
        bullet_list = new_bullet

        for i in range(len(bubble_list) - 1, -1, -1):
            bubble = bubble_list[i]
            box_left = rocket_x - 20
            box_right = rocket_x + 20
            box_top = -295
            box_bottom = -375
            closest_x = max(box_left, min(bubble['x'], box_right))
            closest_y = max(box_bottom, min(bubble['y'], box_top))
            dx = bubble['x'] - closest_x
            dy = bubble['y'] - closest_y
            distance = math.sqrt(dx**2 + dy**2)
            if distance < bubble['r']:
                gameover = 3
                break
        
        for i in range(len(bubble_list) - 1, -1, -1): 
            bubble = bubble_list[i]
            if bubble.get('is_dynamic', False):
                update_dynamic_bubble(bubble, delta_time)
            if bubble['y'] > -400:
                new_y = bubble['y'] - (10 + score * 5) * delta_time
                bubble['y'] = new_y
                if check_bubble_overlap(bubble['x'], bubble['y'], bubble['r'], 
                                        [b for b in bubble_list if b != bubble]):
                    bubble['y'] = bubble['y'] + (10 + score * 5) * delta_time 
            else:
                gameover += 1
                bubble_list.pop(i)
                new_bubble = create_bubble(bubble_list)
                bubble_list.append(new_bubble)

        bubble_list.sort(key=bubble_x_position)
        
        for i in range(len(bubble_list) - 1, -1, -1):
            bubble = bubble_list[i]
            dx = bubble['x'] - rocket_x
            dy = bubble['y'] - (-345)
            distance = math.sqrt(dx**2 + dy**2)
            if distance < (bubble['r'] + 20):
                gameover = 3
                break  
            for j in range(len(bullet_list) - 1, -1, -1):
                bull = bullet_list[j]
                bullet_dx = bubble['x'] - bull[0]
                bullet_dy = bubble['y'] - bull[1]
                bullet_distance = math.sqrt(bullet_dx**2 + bullet_dy**2)
                if bullet_distance < (bubble['r'] + 8):  
                    if bubble.get('is_dynamic', False):
                        score += 2
                        print(f"Dynamic Bubble Hit! Score: {score}")
                    else:
                        score += 1
                        print(f"Score: {score}")
                    bubble_list.pop(i)
                    bullet_list.pop(j)
                    new_bubble = create_bubble(bubble_list)
                    bubble_list.append(new_bubble)
                    break  

    if (gameover >= 3 or misfires >= 3) and not freeze:
        print(f"Game Over! Score: {score}")
        freeze = True
        bubble_list = []  
    glutPostRedisplay()
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    draw_ui()
    draw_bullet()
    draw_bubble()
    glutSwapBuffers()
def init():
    global last_frame_time
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-250, 250, -400, 400, -1, 1)
    last_frame_time = time.time()
glutInit()
glutInitWindowSize(W_WIDTH, W_HEIGHT)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
wind = glutCreateWindow(b"Shoot The Circles!")
init()
num_starting_bubbles = random.randint(3, 5)
for _ in range(num_starting_bubbles):
    new_bubble = create_bubble(bubble_list)
    bubble_list.append(new_bubble)
bubble_list.sort(key=bubble_x_position)
glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutMainLoop()