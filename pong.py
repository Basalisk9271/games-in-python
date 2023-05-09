import pygame
import random

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the dimensions of the screen
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Set the paddle dimensions
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# Set the ball dimensions
BALL_SIZE = 10

BALL_SPEED = 4
PADDLE_SPEED = 6

# Initialize Pygame
pygame.init()

# Set the screen size
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set the window title
pygame.display.set_caption("Pong Game")

# Define the Paddle class
class Paddle:
    def __init__(self, x, y, paddleWidth, paddleHeight):
        self.rect = pygame.Rect(x, y, paddleWidth, paddleHeight)
        self.x = x
        self.y = y
        self.color = WHITE

    def move_up(self):
        if self.top > 0 :
            self.y = self.y - PADDLE_SPEED
        else:
            self.y = self.y

    def move_down(self):
        if self.y + PADDLE_HEIGHT < SCREEN_HEIGHT:
            self.y = min(SCREEN_HEIGHT - PADDLE_HEIGHT, self.y + PADDLE_SPEED)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT))

    def check_bounds(self, SCREEN_HEIGHT):
        if self.y < 0:
            self.y = 0
            self.rect.top = 0
        if self.y + self.rect.height > SCREEN_HEIGHT:
            self.y = SCREEN_HEIGHT - self.rect.height
            self.rect.bottom = SCREEN_HEIGHT

# Define the Ball class
class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.color = WHITE

    def move(self):
        self.x += self.direction_x * 2
        self.y += self.direction_y * 2

        if self.y <= 0 or self.y >= SCREEN_HEIGHT - BALL_SIZE:
            self.direction_y *= -1

    def reset(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, BALL_SIZE, BALL_SIZE))

    def collide(self, paddle_left, paddle_right):
        # Check for collision with left paddle
        if (self.x <= paddle_left.x + PADDLE_WIDTH and 
            self.y + BALL_SIZE >= paddle_left.y and 
            self.y <= paddle_left.y + PADDLE_HEIGHT):
            self.direction_x *= -1

        # Check for collision with right paddle
        if (self.x + BALL_SIZE >= paddle_right.x and 
            self.y + BALL_SIZE >= paddle_right.y and 
            self.y <= paddle_right.y + PADDLE_HEIGHT):
            self.direction_x *= -1

# Set the FPS and clock
clock = pygame.time.Clock()
FPS = 60

# Set the score and font
score_left = 0
score_right = 0
font = pygame.font.Font(None, 30)

# Create the Paddle and Ball objects
paddle_left = Paddle(20, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_right = Paddle(SCREEN_WIDTH - PADDLE_WIDTH - 20, SCREEN_HEIGHT / 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = Ball()

# Start the game loop
running = True
paused = False
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            paused = not paused  # Toggle pause state
    
    if not paused:
    # Get the state of all keyboard keys
        keys = pygame.key.get_pressed()

        # Move the paddles
        if keys[pygame.K_w]:
            paddle_left.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            paddle_left.y += PADDLE_SPEED
        if keys[pygame.K_UP]:
            paddle_right.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            paddle_right.y += PADDLE_SPEED
        
        # Make sure the paddles don't go out of bounds
        paddle_left.check_bounds(SCREEN_HEIGHT)
        paddle_right.check_bounds(SCREEN_HEIGHT)

        # Check for collisions
        ball.collide(paddle_left, paddle_right)

        # Move the ball
        ball.move()

        # Handle ball going off the screen
        if ball.x <= 0:
            score_right += 1
            ball.reset()
        elif ball.x >= SCREEN_WIDTH - BALL_SIZE:
            score_left += 1
            ball.reset()

        # Clear the screen
        screen.fill(BLACK)

        # Draw the paddles and ball
        paddle_left.draw(screen)
        paddle_right.draw(screen)
        ball.draw(screen)

        # Draw the scores
        text_left = font.render(str(score_left), True, WHITE)
        text_right = font.render(str(score_right), True, WHITE)
        screen.blit(text_left, (SCREEN_WIDTH / 4 - text_left.get_width() / 2, 10))
        screen.blit(text_right, (SCREEN_WIDTH * 3 / 4 - text_right.get_width() / 2, 10))

        # Update the screen
        pygame.display.flip()

        # Set the FPS
        clock.tick(FPS)

# Quit Pygame
pygame.quit()
