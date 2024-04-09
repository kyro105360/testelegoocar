# Reference: This code was mostly written by ChatGPT, but it was modified to match the requirements.

import pygame
import sys
import keyboard, serial, time

# Initialize Pygame
pygame.init()
port = input("Enter com port: ")
car = serial.Serial(port, 9600)

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
    def __init__(self, x, y, width, height, color, text, image_paths=None, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action
        self.images = []
        self.image_index = 0
        self.pressed = False
        if image_paths:
            for path in image_paths:
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (width, height))
                self.images.append(image)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.images:
            if self.pressed:
                screen.blit(self.images[1], self.rect.topleft)
            else:
                screen.blit(self.images[0], self.rect.topleft)
        else:
            text_surface = font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def clicked(self):
        if self.action:
            self.action()

class ButtonOnOff:
    def __init__(self, x, y, width, height, color, text, image_paths=None, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.action = action
        self.images = []
        self.image_index = 0
        self.pressed = False
        if image_paths:
            for path in image_paths:
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (width, height))
                self.images.append(image)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.images:
            if self.pressed:
                screen.blit(self.images[1], self.rect.topleft)
            else:
                screen.blit(self.images[0], self.rect.topleft)
        else:
            text_surface = font.render(self.text, True, BLACK)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

    def clicked(self):
        if self.action:
            self.action()
        self.pressed = not self.pressed


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
upButton = Button(button_x, button_y, button_width*2, button_height*2, WHITE, "Up Button", ["Better_buttons/up.png", "Better_buttons/click_u.png"],  action1)

button_y += button_height + button_spacing + 25
onOffButton = ButtonOnOff(button_x, button_y, button_width*2, button_height*2, WHITE, "On/off Button", ["Better_buttons/OFF.png", "Better_buttons/ON.png"], action6)

button_x += (WIDTH - button_width*2)/8 + 290
rightButton = Button(button_x, button_y, button_width*2, button_height*2, WHITE, "Right Button", ["Better_buttons/right.png", "Better_buttons/click_r.png"], action3)

button_x = (WIDTH - button_width*2)/4 - 150
leftButton = Button(button_x, button_y, button_width*2, button_height*2, WHITE, "Left Button", ["Better_buttons/left.png", "Better_buttons/click_l.png"], action4)

button_x = (WIDTH - button_width*2) / 2
button_y += button_height + button_spacing + 25
downButton = Button(button_x, button_y, button_width*2, button_height*2, WHITE, "Down Button", ["Better_buttons/down.png", "Better_buttons/click_d.png"], action5)

# Need to add the emergency stop button on the top left/right or bottom left/right
button_x = WIDTH - button_width - 100 # 10 pixels padding from right edge
button_y = 20  # 10 pixels padding from top edge
# Image reference: https://www.freepik.com/premium-vector/red-warning-emergency-stop-button-brake-danger-alert-sign-isolated-symbol-vector-illustration_94491546.htm
emergencyStopButton = Button(button_x, button_y, button_width+25, button_height+25, WHITE, "Emergency Stop Button", ["Better_buttons/button_image6_Updated.png", "Better_buttons/button_image6_Updated.png"], action6)

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in [upButton, onOffButton, rightButton, leftButton, downButton, emergencyStopButton]:
                    if button.rect.collidepoint(event.pos):
                        button.pressed = True
                        button.clicked()  call the button's action method
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for button in [upButton, rightButton, leftButton, downButton, emergencyStopButton]:
                    button.pressed = False

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