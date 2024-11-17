import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800  
SCREEN_HEIGHT = 600
CAR_WIDTH = 65
CAR_HEIGHT = 110
CAR1_WIDTH = 95
CAR1_HEIGHT = 100
LINE_WIDTH = 5
FPS = 60
INITIAL_LINE_SPEED = 4
ROAD_WIDTH = 300
RECT_WIDTH = 20
RECT_HEIGHT = 70
LEFT_SPEED_INCREASE_RANGE = (-1, 2)
RIGHT_SPEED_INCREASE_RANGE = (-2, 2)

# Centered x-coordinate for the road
ROAD_X = (SCREEN_WIDTH - ROAD_WIDTH) // 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
LEFT_LINE_COLOR = (0, 255, 0)
RIGHT_LINE_COLOR = (255, 0, 0)

# Load and scale images
bg_image = pygame.image.load("bg.jpg")
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
car_image3 = pygame.image.load("car.png")
car_image3 = pygame.transform.scale(car_image3, (CAR1_WIDTH, CAR1_HEIGHT))
car_image1 = pygame.image.load("car2.png")
car_image1 = pygame.transform.scale(car_image1, (CAR_WIDTH, CAR_HEIGHT))
car_image2 = pygame.image.load("car3.png")
car_image2 = pygame.transform.scale(car_image2, (CAR_WIDTH, CAR_HEIGHT))

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Car Game")

# Load the finish point image
finish_image = pygame.image.load("finishedpoint.jpg")
finish_image = pygame.transform.scale(finish_image, (ROAD_WIDTH, 120))  # Adjust dimensions to fit the road

class FinishedPoint:
    def __init__(self):
        self.rect = pygame.Rect(ROAD_X, -120, ROAD_WIDTH, 120)  # Place it off-screen initially
        self.speed = INITIAL_LINE_SPEED
        self.is_visible = False

    def show(self, moving_line_speed):
        self.is_visible = True
        self.speed = moving_line_speed

    def move(self):
        if self.is_visible:
            self.rect.y += self.speed

    def draw(self, surface):
        if self.is_visible:
            surface.blit(finish_image, self.rect)

# Define the Car class
class Car:
    def __init__(self):
        self.rect = car_image1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120))
        self.speed = 5
        self.current_image = car_image1

    def update_image(self, current_speed):
        if current_speed > 6:
            self.current_image = car_image2
        else:
            self.current_image = car_image1

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(ROAD_X, min(self.rect.x, ROAD_X + ROAD_WIDTH - CAR_WIDTH))

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)

# Define the Moving Rectangle class
# Define the Moving Rectangle class
class MovingRectangle:
    def __init__(self, y_start):
        self.rect = pygame.Rect(ROAD_X + (ROAD_WIDTH - RECT_WIDTH) // 2, y_start, RECT_WIDTH, RECT_HEIGHT)
        self.speed = INITIAL_LINE_SPEED

    def move(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = 0

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)

    def increase_speed(self, amount):
        self.speed += amount


# Define the Moving Line class
class MovingLine:
    def __init__(self):
        self.y = 0
        self.length = ROAD_WIDTH
        self.speed = INITIAL_LINE_SPEED

    def move(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0

    def draw(self, surface):
        pygame.draw.line(surface, LEFT_LINE_COLOR, (ROAD_X, self.y), (ROAD_X + self.length / 2, self.y), LINE_WIDTH)
        pygame.draw.line(surface, RIGHT_LINE_COLOR, (ROAD_X + self.length / 2, self.y), (ROAD_X + self.length, self.y), LINE_WIDTH)


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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                return

# Game over screen
def game_over_screen(message):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    text = font.render(message, True, RED)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 36)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Return True to restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()  # Exit the game
                    sys.exit()

# Winner screen with restart option
def winner_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    winner_text = font.render("You Are a Winner!", True, WHITE)
    screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

    font = pygame.font.Font(None, 36)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Return True to restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()  # Exit the game
                    sys.exit()


# Define the Obstacle class
# Define the Obstacle class (now representing cars)
class Obstacle:
    def __init__(self, moving_line_speed):
        self.width = 95
        self.height = 100
        # Randomly place the obstacle (car) within the road area
        self.rect = pygame.Rect(
            random.randint(ROAD_X, ROAD_X + ROAD_WIDTH - self.width),
            -self.height,  # Start above the screen
            self.width,
            self.height,
        )
        self.speed = moving_line_speed
        self.current_image = car_image3  # Default car image, can switch to another image based on speed

    def move(self, moving_line_speed):
        self.speed = moving_line_speed+1  # Move at the same speed as the moving line
        self.rect.y += self.speed  # Move the car down

    def draw(self, surface):
        surface.blit(self.current_image, self.rect)  # Draw the car on the screen




# Modify the main function to show the winner screen
def main():
    clock = pygame.time.Clock()
    car = Car()
    moving_rectangle1 = MovingRectangle(-100)
    moving_rectangle2 = MovingRectangle(-400)
    moving_line = MovingLine()
    finished_point = FinishedPoint()

    obstacle = None
    lines_passed = 0  # Counter for passed lines
    finished_point_shown = False  # Flag to check if finished point is shown
    left_speed_increase = random.randint(*LEFT_SPEED_INCREASE_RANGE)
    right_speed_increase = random.randint(*RIGHT_SPEED_INCREASE_RANGE)
    left_speed_display = left_speed_increase
    right_speed_display = right_speed_increase

    start_time = pygame.time.get_ticks()  # Track the start time
    countdown_time = 30 * 1000  # 30 seconds in milliseconds

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # คำนวณเวลาที่เหลือ
        elapsed_time = pygame.time.get_ticks() - start_time
        remaining_time = max(0, countdown_time - elapsed_time) // 1000  # Convert to seconds

        # Create an obstacle (car) if none exists and finished point is not shown
        if obstacle is None and not finished_point_shown:
            obstacle = Obstacle(moving_line.speed)

        car.move()
        moving_rectangle1.move()
        moving_rectangle2.move()

        if not finished_point_shown:
            moving_line.move()

        if obstacle and not finished_point_shown:
            obstacle.move(moving_line.speed)

        car.update_image(moving_line.speed)

        # Check for collision with the obstacle (car)
        if obstacle and car.rect.colliderect(obstacle.rect):
            if game_over_screen("Game Over"):
                return  # Restart game after Game Over

        # Reset obstacle (car) if it moves out of the screen
        if obstacle and obstacle.rect.top > SCREEN_HEIGHT:
            obstacle = None

        # Check if the car passes the moving line
        if not finished_point_shown and car.rect.bottom < moving_line.y and moving_line.y > SCREEN_HEIGHT - 120:
            lines_passed += 1
            moving_line.y = SCREEN_HEIGHT  # Reset the line position

            # Speed adjustment logic
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

            # Show finished point after passing 5 lines
            if lines_passed == 10:
                finished_point.show(moving_line.speed)
                finished_point_shown = True
                obstacle = None  # Remove the obstacle when the finished point is shown

        if moving_line.speed < 1:
            if game_over_screen("Game Over"):
                return  # Restart game after Game Over

        # Move the finished point if it's visible
        if finished_point_shown:
            finished_point.move()
            # Check if the player passed the finished point
            if car.rect.top < finished_point.rect.bottom and car.rect.colliderect(finished_point.rect):
                if winner_screen():  # Show winner screen and wait for restart
                    return  # Restart game after winning

        # Draw the game elements
        screen.blit(bg_image, (0, 0))
        pygame.draw.rect(screen, BLACK, (ROAD_X, 0, ROAD_WIDTH, SCREEN_HEIGHT))

        moving_rectangle1.draw(screen)
        moving_rectangle2.draw(screen)

        if not finished_point_shown:
            moving_line.draw(screen)

        car.draw(screen)

        if obstacle and not finished_point_shown:
            obstacle.draw(screen)

        if finished_point_shown:
            finished_point.draw(screen)

        # Display game info
        if not finished_point_shown:  # Only display speed numbers if the finished point is not shown
            font = pygame.font.Font(None, 36)
            left_speed_text = font.render(f"{left_speed_display}", True, WHITE)
            right_speed_text = font.render(f"{right_speed_display}", True, WHITE)
            screen.blit(left_speed_text, (ROAD_X + 20, moving_line.y - 30))
            screen.blit(right_speed_text, (ROAD_X + ROAD_WIDTH - 40, moving_line.y - 30))

        current_speed_text = font.render(f"Current Speed: {moving_line.speed}", True, WHITE)
        screen.blit(current_speed_text, (20, 20))

        # Display remaining time
        time_text = font.render(f"Time Left: {remaining_time}s", True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 20))

        # End game if time is up
        if remaining_time == 0:
            if game_over_screen("You Ran Out of Time!"):
                return  # Restart game after Game Over

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    while True:
        start_screen()
        main()