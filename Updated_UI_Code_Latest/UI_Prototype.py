# Reference: This code was mostly written by ChatGPT, but it was modified to match the requirements.

import pygame
import sys
import keyboard, serial, time

# Initialize Pygame
pygame.init()
car = serial.Serial("com3", 9600)

# Set up the screen
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame GUI")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Define fonts
font = pygame.font.SysFont(None, 30)

# Define Button class
class Button:
    # def __init__(self, x, y, width, height, color, text, action=None):
    #     self.rect = pygame.Rect(x, y, width, height)
    #     self.color = color
    #     self.text = text
    #     self.action = action

    def __init__(self, x, y, width, height, color, text, image_path=None, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action
        self.image = None
        if image_path:
            self.image = pygame.image.load(image_path)
            # Scale the image to fit the button
            self.image = pygame.transform.scale(self.image, (width, height))

    # def draw(self, screen):
    #     pygame.draw.rect(screen, self.color, self.rect)
    #     text_surface = font.render(self.text, True, BLACK)
    #     text_rect = text_surface.get_rect(center=self.rect.center)
    #     screen.blit(text_surface, text_rect)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.image:
            screen.blit(self.image, self.rect.topleft)  # Draw image at button's top-left corner
        else:
            text_surface = font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def clicked(self):
        if self.action:
            self.action()

# Define actions for buttons
def action1():
    car.write(b'f')

def stop():
    car.write(b's')

def action3():
    car.write(b'r')

def action4():
    car.write(b'l')

def action5():
    car.write(b'b')

def action6():
    car.write(b'E')

# Create buttons
button_width, button_height = 200, 100
button_spacing = 100
button_x = (WIDTH - button_width*2) / 2 
button_y = (HEIGHT - (button_height + button_spacing) * 2) / 2 - 100  # Center vertically with spacing
upButton = Button(button_x, button_y, button_width*2, button_height*2, WHITE, "Up Button", "Better_buttons/button_image1.png",  action1)

button_y += button_height + button_spacing + 25
onOffButton = Button(button_x, button_y, button_width*2, button_height*2, WHITE, "On/off Button", "Better_buttons/button_image2.png", action6)

button_x += (WIDTH - button_width*2)/8 + 290
rightButton = Button(button_x, button_y, button_width*2, button_height*2, WHITE, "Right Button", "Better_buttons/button_image3.png", action3)

button_x = (WIDTH - button_width*2)/4 - 150
leftButton = Button(button_x, button_y, button_width*2, button_height*2, WHITE, "Left Button", "Better_buttons/button_image4.png", action4)

button_x = (WIDTH - button_width*2) / 2
button_y += button_height + button_spacing + 25
downButton = Button(button_x, button_y, button_width*2, button_height*2, WHITE, "Down Button", "Better_buttons/button_image5.png", action5)

# Need to add the emergency stop button on the top left/right or bottom left/right
button_x = WIDTH - button_width - 100 # 10 pixels padding from right edge
button_y = 20  # 10 pixels padding from top edge
# Image reference: https://www.freepik.com/premium-vector/red-warning-emergency-stop-button-brake-danger-alert-sign-isolated-symbol-vector-illustration_94491546.htm
emergencyStopButton = Button(button_x, button_y, button_width+25, button_height+25, WHITE, "Emergency Stop Button", "Better_buttons/button_image6_Updated.png", action6)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in [upButton, onOffButton, rightButton, leftButton, downButton, emergencyStopButton]:
                    if button.rect.collidepoint(event.pos):
                        button.clicked()
        else:
            stop()

    # Clear the screen
    screen.fill(BLACK)

    # Draw buttons
    upButton.draw(screen)
    onOffButton.draw(screen)
    rightButton.draw(screen)
    leftButton.draw(screen)
    downButton.draw(screen)
    emergencyStopButton.draw(screen)

    # Update the display
    pygame.display.flip()
    time.sleep(0.1)

# Quit Pygame
pygame.quit()
sys.exit()
