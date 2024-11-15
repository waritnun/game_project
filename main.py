import pygame
import sys
import random

# Initialize Pygame
pygame.init()

#เพิ่ม ชนรถแล้ว game over และ จุดสิ้นสุด
# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CAR_WIDTH = 90      
CAR_HEIGHT = 150
LINE_WIDTH = 5
FPS = 60
INITIAL_LINE_SPEED = 5  # Initial speed at which the line moves down
ROAD_WIDTH = 300  # Width of the road
RECT_WIDTH = 20   # Width of the moving rectangle
RECT_HEIGHT = 70  # Height of the moving rectangle
LEFT_SPEED_INCREASE_RANGE = (-2, 2)  # Random speed increase range for the left side
RIGHT_SPEED_INCREASE_RANGE = (-3, 3)  # Random speed increase range for the right side

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)  # Color for the moving rectangles
LEFT_LINE_COLOR = (0, 255, 0)  # Color for the left side of the line
RIGHT_LINE_COLOR = (255, 0, 0)  # Color for the right side of the line

# Load car image (you can replace this with your own image)
car_image1 = pygame.image.load("car2.png")  # Original car image
car_image1 = pygame.transform.scale(car_image1, (CAR_WIDTH, CAR_HEIGHT))
car_image2 = pygame.image.load("car3.png")  # New car image when speed exceeds 5
car_image2 = pygame.transform.scale(car_image2, (CAR_WIDTH, CAR_HEIGHT))

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Car Game")

# Define the Car class
class Car:
    def __init__(self):
        self.rect = car_image1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120))
        self.speed = 5
        self.current_image = car_image1  # Start with the original car image

    def update_image(self, current_speed):
        if current_speed > 10:
            self.current_image = car_image2  # Switch to car2.png when speed exceeds 5
        else:
            self.current_image = car_image1  # Use car3.png for lower speeds

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        # Keep the car within the road bounds
        self.rect.x = max(200, min(self.rect.x, 200 + ROAD_WIDTH - CAR_WIDTH))

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)

# Create a Moving Rectangle class
class MovingRectangle:
    def __init__(self, y_start):
        self.rect = pygame.Rect(200 + (ROAD_WIDTH - RECT_WIDTH) // 2, y_start, RECT_WIDTH, RECT_HEIGHT)  # Start at a specified y position
        self.speed = INITIAL_LINE_SPEED  # Initial speed of the rectangle

    def move(self):
        self.rect.y += self.speed  # Move the rectangle down
        if self.rect.y > SCREEN_HEIGHT:  # Reset position if it moves off screen
            self.rect.y = 0

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

    def increase_speed(self, amount):
        self.speed += amount  # Increase speed when called

# Create a Line class with two sides
class MovingLine:
    def __init__(self):
        self.y = 0  # Start position of the line
        self.length = ROAD_WIDTH  # Length of the line
        self.speed = INITIAL_LINE_SPEED  # Initial speed for the line

    def move(self):
        self.y += self.speed  # Move the line down
        if self.y > SCREEN_HEIGHT:  # Reset position if it moves off screen
            self.y = 0  # Reset to the top

    def draw(self, surface):
        # Draw the line across the road, separating left and right
        pygame.draw.line(surface, LEFT_LINE_COLOR, (200, self.y), (200 + self.length / 2, self.y), LINE_WIDTH)
        pygame.draw.line(surface, RIGHT_LINE_COLOR, (200 + self.length / 2, self.y), (200 + self.length, self.y), LINE_WIDTH)

# Start screen
def start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    title_text = font.render("2D Car Game", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 36)
    start_text = font.render("Press S to Start", True, WHITE)
    screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    # Wait for the user to press 'S' to start the game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                return  # Exit the start screen to begin the game

# Game over screen
def game_over_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    
    font = pygame.font.Font(None, 36)
    restart_text = font.render("Press R to Restart", True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    # Wait for the user to press 'R' to restart
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                main()  # Restart the game

# Main game loop
def main():
    clock = pygame.time.Clock()
    car = Car()
    
    moving_rectangle1 = MovingRectangle(-100)
    moving_rectangle2 = MovingRectangle(-400)
    moving_line = MovingLine()

    left_speed_increase = random.randint(*LEFT_SPEED_INCREASE_RANGE)
    right_speed_increase = random.randint(*RIGHT_SPEED_INCREASE_RANGE)
    left_speed_display = left_speed_increase
    right_speed_display = right_speed_increase

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        car.move()

        moving_rectangle1.move()
        moving_rectangle2.move()
        moving_line.move()

        car.update_image(moving_line.speed)  # Update car image based on current speed

        if car.rect.bottom < moving_line.y and moving_line.y > SCREEN_HEIGHT - 120:
            if car.rect.centerx < SCREEN_WIDTH // 2:
                moving_rectangle1.increase_speed(left_speed_increase)
                moving_rectangle2.increase_speed(left_speed_increase)
                moving_line.speed += left_speed_increase
            else:
                moving_rectangle1.increase_speed(right_speed_increase)
                moving_rectangle2.increase_speed(right_speed_increase)
                moving_line.speed += right_speed_increase

            left_speed_increase = random.randint(*LEFT_SPEED_INCREASE_RANGE)
            right_speed_increase = random.randint(*RIGHT_SPEED_INCREASE_RANGE)
            left_speed_display = left_speed_increase
            right_speed_display = right_speed_increase

            moving_line.y = SCREEN_HEIGHT

        if moving_line.speed < 1:
            game_over_screen()
            return

        screen.fill(GRAY)

        for i in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH // 2 - 5, i, 10, 20))

        pygame.draw.rect(screen, BLACK, (200, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        moving_rectangle1.draw(screen)
        moving_rectangle2.draw(screen)
        moving_line.draw(screen)
        car.draw(screen)

        font = pygame.font.Font(None, 36)
        left_speed_text = font.render(f"{left_speed_display}", True, WHITE)
        right_speed_text = font.render(f"{right_speed_display}", True, WHITE)
        screen.blit(left_speed_text, (220, moving_line.y - 30))
        screen.blit(right_speed_text, (520, moving_line.y - 30))

        current_speed_text = font.render(f"Current Speed: {moving_line.speed}", True, WHITE)
        screen.blit(current_speed_text, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    start_screen()
    main()