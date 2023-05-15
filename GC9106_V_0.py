
# Routines for LCD display 1.8 inch for micro:bit v.2 only
# 128 * 160 pixels, GC9106 controller, 262144 colors
 
# Programmer: Arne Paulsen, Denmark
# File name:  gc9106.py
# Version:    20230514

#   Pins in use by LCD display
#  1  Backlight (analog or digital)
#  8  Reset
# 12  DC = Data/Command
# 13  SCK
# 14  MISO
# 15  MOSI
# 16  CS = Chip select

from microbit import *
from random import *
from math import *
from font import *
import sys

spi.init(baudrate = 8000000)                       # 8 MHz clock
display.off()                                      # disable LED's on micro:bit

# debug = True                                     # no debug info
debug = False                                      # show debug info

#           R    G    B
colors = [[000, 000, 000],                         # 0 black
          [255, 000, 000],  # 1 red
          [000, 255, 000],  # 2 green
          [255, 255, 000],  # 3 yellow 
          [000, 000, 255],  # 4 blue
          [255, 000, 255],  # 5 purple 
          [000, 255, 255],  # 6 cyan 
          [255, 255, 255],  # 7 white
          [000, 000, 000],  # 8 user defined
          [000, 000, 000],] # 9 user defined

LCD_colorNames = ["Black","Red","Green","Yellow","Blue","Purple","Cyan","White", "User", "User"]

def sendCmd(cmd):                                  # send command byte
    pin12.write_digital(0)   # DC command mode
    spi.write(bytes([cmd]))    #val) 
    pin12.write_digital(1)   # DC data mode

def setAddr(xFrom, xTo, yFrom, yTo):               # send window-address to LCD
    a = bytearray(4)
    a[0] = 0 
    a[1] = xFrom
    a[2] = 0
    a[3] = xTo 
    pin12.write_digital(0)   # DC cmd mode
    spi.write(bytes([0x2B])) # set adr command
    pin12.write_digital(1)   # DC data mode
    spi.write(a)             # write array
    a[1] = yFrom
    a[3] = yTo
    pin12.write_digital(0)   # DC cmd mode
    spi.write(bytes([0x2A])) # set adr command
    pin12.write_digital(1)   # DC data mode
    spi.write(a)             # write array

def fillAry(size, color):                          # fill array with color data
    r = (255 - colors[color][0])   # rgb
    g = (255 - colors[color][1]) 
    b = (255 - colors[color][2]) 
    a = bytearray(size * 3)        # 3 bytes per pixel
    ix = 0
    for x in range (size):         # fill array 3 bytes per count
        a[ix] = r
        ix += 1
        a[ix] = g
        ix += 1
        a[ix] = b
        ix += 1 
    return a
    
def sendData(color, count):                        # send color-data to LCD
    if debug:
        print ("Color:", LCD_colorNames[color], "(", count, "bytes)")
    sendCmd(0x2c)
    size = 256
    if (count >= size):
        a = fillAry(size, color) 
        while(count >= size): 
            spi.write(a)                       # send 
            count -= size
    spi.write(fillAry(count, color))           # send remaing part
    
# ====================================================================================================

def LCD_fill(xFrom, xTo, yFrom, yTo, color):       # x start, x end, y start, y end, color no
    count = (xTo-xFrom+1) * (yTo-yFrom+1)          # pixel count
    if (count > 0):
        setAddr(xFrom, xTo, yFrom, yTo)
        if (debug):
            print("Fill: X", xFrom, "-", xTo, "\tY", yFrom, "-", yTo)
        sendData(color, count)
    else:
        print("*** Error: X", xFrom, "-", xTo, "\tY", yFrom, "-", yTo, "\tCount", count)
        sys.exit()                          # stop program

def LCD_frame(x, y, size, border, color ):         # x, y, size, border, color
    if (debug):
        print("Frame: x", x, "\ty", y, "\tw", size, "\tb", border)
    LCD_fill(x, x+size-1, y, y+border-1, color)                           # top
    LCD_fill(x, x+border-1, y+border-1, y+size-border-1, color)           # left
    LCD_fill(x+size-border, x+size-1, y+border-1, y+size-border-1, color) # right
    LCD_fill(x, x+size-1, y+size-border, y+size-1, color)                 # buttom

def LCD_pixel(x, y, size, color):                  # x, y, size, color
    if (debug):
        print("Pixel: x", x, "\ty", y, "\ts", size)
    LCD_fill(x, x+size-1, y, y+size-1, color) 

def LCD_draw_line(x, y, x_, y_, pen, color):       # draw line
    x_steps = abs(x_ - x)
    y_steps = abs(y_ - y)
    if (x_steps >= y_steps):  # plot on x axis
        plots = x_steps
        if (x < x_):          # plot direction
            x_step = 1        
        else:
            x_step = -1
        y_step = y_steps / x_steps
        if (y > y_):          # backwords   
            y_step *= -1        
    else:                     # plot on y axis
        plots = y_steps
        if (y < y_):           # direction
            y_step = 1
        else:    
            y_step = -1
        x_step = x_steps / y_steps
        if (x > x_):   # backwords   
            x_step *= -1        
    if debug:    
        print ("\nPlots:", plots, ", x_step", x_step, ", y_step", y_step )
    for p in range(plots):
    #    if debug and p % 10 == 0:
    #        print ("x:", x, "y:", y )
        LCD_pixel(int(x), int(y), pen, color)
        x += x_step
        y += y_step

def LCD_draw_circle(x, y, radius, pen, color):     # draw circle
    rx2    = radius * radius
    count  = round(radius / 1.36)  # 0 to 45 degres numbers
    cntx2  = count << 1
    x_ary = bytearray(count << 1) 
    y_ary = bytearray(count << 1) 
    for ix in range (count):         # build an x and y array for 90 degrees
        v = int(sqrt(rx2 - (ix * ix)))
        x_ary[ix] = v
        x_ary[cntx2 - ix - 1] = ix
        y_ary[ix] = ix
        y_ary[cntx2 - ix - 1] = v
    for ix in range (cntx2):                       # NE part
        LCD_pixel(x + y_ary[ix], y - x_ary[ix] , pen, color)
    for ix in range (cntx2):                       # SE part
        LCD_pixel(x + x_ary[ix], y + y_ary[ix] , pen, color)
    for ix in range (cntx2):                       # SW part
        LCD_pixel(x - y_ary[ix], y + x_ary[ix] , pen, color)
    for ix in range (cntx2):                       # NW part
        LCD_pixel(x - x_ary[ix], y - y_ary[ix] , pen, color)

def LCD_star(x, y, radius, pen, col):              # draw star symbol
    k = sqrt(radius * radius / 2)
    LCD_draw_line(x , y - radius, x, y + radius, pen, col)  # horisontal line
    LCD_draw_line(x - radius, y, x + radius, y, pen, col)   # vertical line
    LCD_draw_line(x + k, y - k, x - k, y + k, pen, col)
    LCD_draw_line(x + k, y + k, x - k, y - k, pen, col)

def LCD_text(left, right, top, size, text, color): # write text
    start_x = left
    start_y = top
    line = 0
    for ix in range (len(text)):
        chr = ord(text[ix])
        a = fontData(chr)
        y = start_y + (line * size * 8)
        for bit in range(7):
            for byte in range (5):
                if (a[byte] >> bit) & 1 == 1:  # print pixel
                    LCD_pixel(left + byte * size, y, size, color)
            y += size      # next pixel row
        left += (size * 6)

        if left > (right - (size * 6)):   # new line of characters
            left = start_x
            line += 1

def LCD_clear(color):                              # color
    setAddr(0, 159, 0, 127)
#    writeRow(0, 159) 
#    writeColumn(0, 127)                # y = 0 ~ 127
    sendCmd(0x2c)                      # write to memory 
    a = fillAry(320, color)
    for x in range(64):
        spi.write(a)

def LCD_demo_OL():                                 # demo picture
    colors[8] = [255, 128, 80]                   # user color = Coral
    LCD_clear(0)
    LCD_fill(0, 159, 24, 102, 7 )
    x = 2 
    y = 27
    rad = 23  # radius
    rings = [[rad * 3 + 6 , rad    , 0],  # black = middel
             [rad * 2 + 3 , rad * 2, 3],  # yellow
             [rad * 4 + 9 , rad * 2, 2],  # green 
             [rad         , rad    , 4],  # blue
             [rad * 5 + 12, rad    , 1]]  # red
     # 5 rings definition of x, y of center, color codes                                 
    for i in range(5):
        LCD_draw_circle(x + rings[i][0], y + rings[i][1], rad, 6, rings[i][2])
    LCD_text(20, 160, 0, 3, "Olympic", 8)   
    LCD_text(20, 160, 107, 3, " GAMES", 8)    
    LCD_star(15, 116, 10, 3, 6)
    LCD_star(143, 116, 10, 3, 6)
  
def LCD_setup():                                   # initial LCD configuration
    pin1.write_digital(0)    # backlight off
    pin8.write_digital(0)    # HW reset = 0
    sleep(10)
    pin8.write_digital(1)    # run = 1
    sleep(100)
    pin16.write_digital(0)   # CS chip select constant on (only SPI device)

    # Datasheet https://www.phoenixdisplay.com/wp-content/uploads/2019/07/GC9106_DS_V1.0_20170308.pdf
    
    sendCmd(0x36)            # Memory direction control  p.102
    spi.write(bytes([0x80])) # bit 7 = MY Row address order  ***
                             # bit 6 = MX Row / Column Exchange
                             # bit 5 = MV Column Address Order
                             # bit 4 = ML Vertical Refresh Order
                             # bit 3 = BGR RGB-BGR Order
                             # bit 2 = MH Horizontal Refresh Order
                      
    sendCmd(0x3a)            # Pixel Format Set  p.38
                             # 0x03 = 4+4+4 bit color format - 1.5 bytes
                             # 0x05 = 5+6+5 bit color format - 2 bytes
    spi.write(bytes([0x06])) # 0x06 = 8 bit color format - 3 bytes
                      
    sendCmd(0x11)            # Sleep Out Mode p. 78
    sleep(10)                # Wait min. 5 mS for wake up
    sendCmd(0x29)            # Display ON  p.85
    LCD_clear(0)             # clear screen to black
    pin1.write_digital(1)    # backlight on
