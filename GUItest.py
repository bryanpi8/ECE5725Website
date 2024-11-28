import pygame
from pygame.locals import *
# import RPi.GPIO as GPIO
# import board
# import busio
# from adafruit_mlx90614 import MLX90614

# PID Variables
Kp = 1.0  # Proportional gain
Ki = 0.1  # Integral gain
Kd = 0.05  # Derivative gain

previous_error = 0
integral = 0

# Initialize Pygame
pygame.init()

# Screen dimensions for TFT display
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Fonts
pygame.font.init()
font_large = pygame.font.Font(None, 50)
font_small = pygame.font.Font(None, 30)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Temperature Controller")

# Variables
current_temp = 22  # Placeholder for current temperature (Celsius)
target_temp = 24  # Target temperature (Celsius)
running = True
MAX_TEMP = 150

# Initialize GPIO for relay
# GPIO.setmode(GPIO.BCM)
# outlist=(20, 5, 6, 19, 13)
# GPIO.setup(outlist, GPIO.OUT)


# Initialize I2C for MLX90614 (Commented Out)
# i2c = busio.I2C(board.SCL, board.SDA)
# mlx = MLX90614(i2c)

# Button dimensions and positions
button_increase = pygame.Rect((30, 160), (60, 40))  # Increase button
button_increase5 = pygame.Rect((100, 160), (60, 40))  # Increase button

button_decrease = pygame.Rect((180, 160), (60, 40))  # Decrease button
button_decrease5 = pygame.Rect((250, 160), (60, 40))  # Decrease button


# Function to draw the GUI
def draw_gui():
    screen.fill(BLACK)

    # Display current temperature
    temp_text = font_large.render(f"Current: {current_temp:.1f}°C", True, WHITE)
    temp_rect = temp_text.get_rect(center=(160, 40))
    screen.blit(temp_text, temp_rect)

    # Display target temperature
    target_text = font_large.render(f"Target: {target_temp}°C", True, BLUE)
    target_rect = target_text.get_rect(center=(160, 100))
    screen.blit(target_text, target_rect)

    # Draw buttons
    pygame.draw.rect(screen, GRAY, button_increase)
    pygame.draw.rect(screen, GRAY, button_increase5)
    pygame.draw.rect(screen, GRAY, button_decrease)
    pygame.draw.rect(screen, GRAY, button_decrease5)
    
    # Add button labels
    increase_text = font_small.render("+1C", True, BLACK)
    increase_text5 = font_small.render("+5C", True, BLACK)
    decrease_text = font_small.render("-1C", True, BLACK)
    decrease_text5 = font_small.render("-5C", True, BLACK)
    screen.blit(increase_text, increase_text.get_rect(center=button_increase.center))
    screen.blit(increase_text5, increase_text.get_rect(center=button_increase5.center))
    screen.blit(decrease_text, decrease_text.get_rect(center=button_decrease.center))
    screen.blit(decrease_text5, decrease_text.get_rect(center=button_decrease5.center))

    # Draw temperature bar
    bar_width = 20
    bar_height = SCREEN_HEIGHT
    bar_x = 0
    bar_y = (SCREEN_HEIGHT - bar_height)/2

    # Background bar
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))

    # Fill current temperature proportionally (max temp = 50°C)
    filled_height = int((current_temp / MAX_TEMP) * bar_height)
    fill_y = bar_y + bar_height - filled_height  # Calculate the starting y-coordinate for the red fill
    pygame.draw.rect(screen, RED, (bar_x, fill_y, bar_width, filled_height))

    pygame.display.update()

# Main loop
while running:
    # Read temperature from sensor (Commented Out)
    # try:
    #     current_temp = mlx.object_temperature  # Replace placeholder with sensor reading
    # except Exception as e:
    #     print(f"Error reading from sensor: {e}")
    #     current_temp = 0  # Fallback in case of sensor error

    draw_gui()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        # Handle touchscreen input
        if event.type == MOUSEBUTTONDOWN:
            touch_pos = pygame.mouse.get_pos()
            if target_temp <= 150:
                if button_increase.collidepoint(touch_pos):
                    target_temp += 1
                elif button_increase5.collidepoint(touch_pos):
                    target_temp += 5
            if target_temp >= 20:
                if button_decrease.collidepoint(touch_pos):
                    target_temp -= 1
                elif button_decrease5.collidepoint(touch_pos):
                    target_temp -= 5

    # Simulate current temperature approaching the target for testing
    if current_temp < target_temp:
        current_temp += 0.1
    elif current_temp > target_temp:
        current_temp -= 0.1

    # # PID Control Logic
    # error = target_temp - current_temp  # Calculate error
    # integral += error                  # Accumulate integral
    # derivative = error - previous_error  # Calculate derivative
    # output = Kp * error + Ki * integral + Kd * derivative  # PID formula

    # # Control relay based on PID output
    # if output > 0:  # Turn on heater if PID output is positive
    #     GPIO.output(20, GPIO.HIGH)
    # else:  # Turn off heater if PID output is negative or zero
    #     GPIO.output(20, GPIO.LOW)

    # # Update previous error for next iteration
    # previous_error = error
pygame.quit()