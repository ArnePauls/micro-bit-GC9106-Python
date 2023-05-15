# micro-bit-GC9106-Python

Python code for the GC9106 based 1.8" LCD display for micro:bit (V.2 only)
  
  Guide:
  ------
  Open the micro-bit Python Editor https://python.microbit.org/v/3 
  Create a new project: This will open 'main.py'
  Create file: font.py
  Create file: gc9106.py
  
  Copy contents of these 3 files to the editor:
  font.py        --> font.py
  GC9106_V_0.py  --> gc9106.py
  demo.py        --> main.py  
  
  Send to mico:bit --> A short demo (LCD_demo_OL) will be shown on the LCD display.
  
  There is an array of color definitions, that may be changed or 
  extended to include user defined colors as well.

  Functions in  GC9106_V_0.py:
  ------------------------------

     sendCmd(cmd):                                  # send command byte
     setAddr(xFrom, xTo, yFrom, yTo):               # send window-address to LCD
     fillAry(size, color):                          # fill array with color data
     sendData(color, count):                        # send color-data to LCD
   
     LCD_fill(xFrom, xTo, yFrom, yTo, color):       # x start, x end, y start, y end, color no
     LCD_frame(x, y, size, border, color ):         # x, y, size, border, color
     LCD_pixel(x, y, size, color):                  # x, y, size, color
     LCD_draw_line(x, y, x_, y_, pen, color):       # draw line
     LCD_draw_circle(x, y, radius, pen, color):     # draw circle
     LCD_star(x, y, radius, pen, col):              # draw star symbol
     LCD_text(left, right, top, size, text, color): # write text
     LCD_clear(color):                              # color
     LCD_demo_OL():                                 # demo picture
     LCD_setup():                                   # initial LCD configuration

