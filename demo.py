

# Imports go at the top

from gc9106 import *
    
def LCD_draw_circle_test():
    col = 1
    pen = 2
    for i in range(4):
        x = 40 + randrange(80) 
        y = 40 + randrange(50)
        radius = 5 + randrange(40)
        LCD_draw_circle(x, y, radius, pen, col)
        col += 1
        pen += 1
  
def LCD_draw_line_test(x, y, pen):
 #   x = 40     # x, y - start from center
 #   y = 64     #     
    for x_ in range(0, 160, 15):
        LCD_draw_line(x, y, x_, 0, pen, 1)       # y_ = 0 
    for y_ in range(0, 130, 15):
        LCD_draw_line(x, y, 159, y_, pen, 2)     # x_ = 159
    for x_ in range(159, 0, -15):
        LCD_draw_line(x, y, x_, 127, pen, 4)     # y_ = 127 
    for y_ in range(127, 0, -15):
        LCD_draw_line(x, y, 0, y_, pen, 3)       # x_ = 0

def LCD_randomFill():
    sx = randrange(150)                # x - start      0 - ex
    ex = sx + randrange(160 - sx)      # X - end        sx - 159
    sy = randrange(120)                # y - start      0 - ey
    ey = sy + randrange(128 - sy)      # y - end        sy - 127
    co = randrange(7) + 1
    LCD_fill(sx, ex, sy, ey, co ) 
 
def LCD_randomFrame():
    z = 25 + randrange(30)         # size
    x = randrange(159 - z) 
    y = randrange(127 - z)
    b = 1 + randrange(int(z / 3))  # border size
    c = randrange(7) + 1           # color
    LCD_frame(x, y, z, b, c)       # x, y, size, border, color
    
def LCD_randomPixel():
    x = randrange(150) 
    y = randrange(118)
    s = randrange(20)     # size
    c = randrange(7) + 1
    LCD_pixel(x, y, s, c)
    
def LCD_demo():
    LCD_clear(0)
    print ("\n *** Pixel test:***")
    LCD_randomPixel()
    LCD_text(40, 160, 0, 3, "Pixels", 7)
    sleep(1000)
    print ("\n *** Block test: ***")
    LCD_randomFill() 
    LCD_text(40, 160, 30, 3, "Fill", 7)
    sleep(1000)
    print ("\n *** Frame test: ***")
    LCD_randomFrame()
    LCD_text(40, 160, 60, 3, "Frames", 7)
    sleep(1000)
    LCD_clear(0)
    print ("\n *** Lines test: ***")
    LCD_draw_line_test(80, 64, 1)
    LCD_text(10, 160, 0, 3, "Lines", 7)
    sleep(1000)
    LCD_clear(0)
    print ("\n *** Circle test: ***")
    LCD_draw_circle_test()
    LCD_text(10, 160, 0, 3, "Circles", 7)
    sleep(1000)
    LCD_clear(0)
    print ("\n *** Character test: ***")
    colors[8] = [255,127, 80]     # Coral color
    LCD_text(3,100, 4, 5, ">", 8)
    LCD_text(35, 130, 1, 3, "1234567890", 3)
    LCD_text(130,160, 4, 5, "<", 8)
    LCD_text(10, 100, 50, 2, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", 2)
    LCD_text(65, 150, 112, 1, "abcdefghijklmnopqrstuwwxyz", 6)
    sleep(1000)
    print ("\n *** Olymic test: ***")
    LCD_demo_OL()
    
LCD_setup()


# Code in a 'while True:' loop repeats forever
while True:
    LCD_demo()
    input("Enter: ")
