import pygame
import random

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Color definitions
WHITE = (244, 244, 244)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
MUSTARD = (240, 165, 0)
ORANGE = (207, 117, 0)
BACKGROUND_COLOR = (30, 30, 30)  # Dark gray background

# Paddle setup
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - 50
paddle_speed = 7

# Ball setup
BALL_RADIUS = 8
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = random.choice([-4, 4])
ball_dy = -4

# Bricks setup
BRICK_ROWS = 5
BRICK_COLS = 8
BRICK_WIDTH = WIDTH // BRICK_COLS - 5
BRICK_HEIGHT = 20
bricks = []
colors = [MUSTARD, ORANGE, GREEN, BLUE, RED]  # Different colors for each row
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_color = colors[row % len(colors)]
        bricks.append((pygame.Rect(col * (BRICK_WIDTH + 5) + 5, row * (BRICK_HEIGHT + 5) + 5, BRICK_WIDTH, BRICK_HEIGHT), brick_color))

# Function to display "Press SPACE to Start" message
def show_press_space_message():
    font = pygame.font.SysFont("comicsansms", 50)
    text = font.render("Press SPACE to Start", True, ORANGE)
    text.set_alpha(150) 
    screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2))

# Main game loop
running = True
game_started = False
while running:
    screen.fill(BACKGROUND_COLOR)  

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_started:
                game_started = True

    if not game_started:
        show_press_space_message()
    else:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += paddle_speed

        # Ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with screen borders
        if ball_x - BALL_RADIUS <= 0 or ball_x + BALL_RADIUS >= WIDTH:
            ball_dx *= -1
        if ball_y - BALL_RADIUS <= 0:
            ball_dy *= -1

        # Ball collision with paddle
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        if paddle_rect.collidepoint(ball_x, ball_y + BALL_RADIUS):
            relative_intersect_x = (ball_x - paddle_x) / PADDLE_WIDTH
            ball_dx = (relative_intersect_x - 0.5) * 8  # Adjust angle based on hit position
            ball_dy *= -1

        # Ball collision with bricks
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        for brick, color in bricks[:]:
            if brick.colliderect(ball_rect):
                # Determine collision side
                if abs(ball_y - brick.bottom) < BALL_RADIUS or abs(ball_y - brick.top) < BALL_RADIUS:
                    ball_dy *= -1  # Bounce vertically
                else:
                    ball_dx *= -1  # Bounce horizontally
                bricks.remove((brick, color))
                break

        # Game Over if ball falls below the screen
        if ball_y + BALL_RADIUS >= HEIGHT:
            running = False

        # Draw paddle, ball, and bricks
        pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.circle(screen, RED, (ball_x, ball_y), BALL_RADIUS)
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)

    # Update the display
    pygame.display.flip()
    pygame.time.delay(20)

pygame.quit()