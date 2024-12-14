import pygame,pigame
from pygame.locals import *
import os
from time import sleep
import RPi.GPIO as GPIO


######### Bail out button #########
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
def bailOutButton(channel):
    print("Quitting")
    pygame.quit()
GPIO.add_event_detect(17, GPIO.FALLING, callback=bailOutButton, bouncetime=200)

######### Variable Initializations ##########
#Timeout
tStep=0
nSteps = 30/.1
#Tap Logging
nTaps=0

#Colours
WHITE = (255,255,255)
black = (0,0,0)

######### Display control ###########
# Makes the program display on monitor with mouse if commented
os.putenv('SDL_VIDEODRV','fbcon')
os.putenv('SDL_FBDEV', '/dev/fb1')
os.putenv('SDL_MOUSEDRV','dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')
# pygame.mouse.set_visible(False)
    
pygame.init()
pitft = pigame.PiTft() ### Comment to switch to monitor
lcd = pygame.display.set_mode((320, 240))
lcd.fill((0,0,0))
pygame.display.update()
     
font_big = pygame.font.Font(None, 30)
      
touch_buttons = {'Quit':(240,200)}
       
for k,v in touch_buttons.items():
    text_surface = font_big.render('%s'%k, True, WHITE)
    rect = text_surface.get_rect(center=v)
    lcd.blit(text_surface, rect)

def drawQuit():
    lcd.blit(text_surface, rect)  
    pygame.display.update()     

pygame.display.update()
try:
    while True:
        pitft.update() ### Comment to switch to monitor
        
        # Scan touchscreen events
        ####### Quit Button #######
        for event in pygame.event.get():
            lcd.fill(black)
            drawQuit()
            if(event.type is MOUSEBUTTONDOWN):
                x,y = pygame.mouse.get_pos()
                print(f"{nTaps}: {x,y}")
                nTaps = nTaps+1
                # print(x,y)
            elif(event.type is MOUSEBUTTONUP):
                x,y = pygame.mouse.get_pos()
                ####### Touch Position Display Code #######
                coordinates = font_big.render(f"Touch at {x},{y}", True, WHITE)
                coordrect = coordinates.get_rect(center=(160,120))
                lcd.blit(coordinates, coordrect)

                ####### Quit Button #######
                lcd.blit(text_surface, rect)
                # print(x,y)
                if x>160 and y>180:
                    pygame.quit()
                    import sys
                    sys.exit(0)
                if x<160 and y>180:
                    pass
                pygame.display.update()
        ####### Timeout Logic #######        
        sleep(0.1)
        tStep = tStep + 1
        if tStep >= nSteps:
            pygame.quit()


except KeyboardInterrupt:
    pass
finally: ### Comment to switch to monitor
    del(pitft)
