import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
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
PURPLE = (128, 0, 128)
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
ball_dx = 0
ball_dy = 0
initial_ball_speed = 5  # Slower initial speed for easier first level

# Bricks setup
BRICK_WIDTH = WIDTH // 16 - 5
BRICK_HEIGHT = 20

# Obstacles setup
obstacles = []

# Function to initialize bricks based on level
def initialize_bricks(level):
    bricks = []
    colors = [MUSTARD, ORANGE, GREEN, BLUE, RED]
    
    # First level: Fewer rows and wider spacing
    if level == 1:
        brick_rows = 3  # Fewer rows
        brick_cols = 10  # Fewer columns
        start_x = (WIDTH - (brick_cols * (BRICK_WIDTH + 5))) // 2  # Center the bricks
        
        for row in range(brick_rows):
            for col in range(brick_cols):
                brick_color = colors[row % len(colors)]
                bricks.append((pygame.Rect(
                    start_x + col * (BRICK_WIDTH + 5),
                    row * (BRICK_HEIGHT + 10) + 50,  # Add more spacing and start lower
                    BRICK_WIDTH, BRICK_HEIGHT), brick_color))
    else:
        # Higher levels: More rows and normal spacing
        brick_rows = min(3 + level, 8)  # Gradually increase rows up to 8
        brick_cols = 16
        
        for row in range(brick_rows):
            for col in range(brick_cols):
                brick_color = colors[row % len(colors)]
                bricks.append((pygame.Rect(
                    col * (BRICK_WIDTH + 5) + 5,
                    row * (BRICK_HEIGHT + 5) + 5,
                    BRICK_WIDTH, BRICK_HEIGHT), brick_color))
    
    return bricks

# Function to initialize obstacles based on level
def initialize_obstacles(level):
    obstacles = []
    
    if level >= 2:  # Only add obstacles from level 2 onwards
        # Number of obstacles increases with level
        num_obstacles = level - 1
        
        for i in range(num_obstacles):
            # Create different obstacle types based on the index
            if i % 3 == 0:  # Horizontal bar
                width = random.randint(100, 200)
                height = 15
                x = random.randint(50, WIDTH - width - 50)
                y = random.randint(150, HEIGHT - 200)
                obstacles.append((pygame.Rect(x, y, width, height), PURPLE))
            elif i % 3 == 1:  # Vertical bar
                width = 15
                height = random.randint(100, 150)
                x = random.randint(50, WIDTH - width - 50)
                y = random.randint(150, HEIGHT - 200)
                obstacles.append((pygame.Rect(x, y, width, height), GRAY))
            else:  # Small block
                size = random.randint(20, 40)
                x = random.randint(50, WIDTH - size - 50)
                y = random.randint(150, HEIGHT - 200)
                obstacles.append((pygame.Rect(x, y, size, size), GREEN))
    
    return obstacles

# Function to display "Press SPACE to Start" message
def show_press_space_message():
    font = pygame.font.SysFont("comicsansms", 50)
    text = font.render("Press SPACE to Start", True, ORANGE)
    text.set_alpha(150) 
    screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2))

# Function to reset ball position after losing
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = 0
    ball_dy = 0

# Function to launch ball with initial velocity
def launch_ball(level):
    global ball_dx, ball_dy
    # Launch at a random angle between 60 and 120 degrees (more upward for first level)
    angle_min = 60 if level == 1 else 45
    angle_max = 120 if level == 1 else 135
    angle = math.radians(random.randint(angle_min, angle_max))
    
    # Ball speed increases with level
    ball_speed = initial_ball_speed + (level - 1) * 0.5
    ball_speed = min(ball_speed, 10)  # Cap at maximum speed
    
    ball_dx = ball_speed * math.cos(angle)
    ball_dy = -ball_speed * math.sin(angle)

# Function to check collision with obstacles
def check_obstacle_collision(ball_rect):
    global ball_dx, ball_dy, ball_x, ball_y
    
    for obstacle, color in obstacles:
        if ball_rect.colliderect(obstacle):
            # Determine which side of the obstacle was hit
            left_overlap = (obstacle.right - ball_rect.left)
            right_overlap = (ball_rect.right - obstacle.left)
            top_overlap = (obstacle.bottom - ball_rect.top)
            bottom_overlap = (ball_rect.bottom - obstacle.top)
            
            # Find the smallest overlap to determine collision direction
            min_overlap = min(left_overlap, right_overlap, top_overlap, bottom_overlap)
            
            if min_overlap == left_overlap or min_overlap == right_overlap:
                ball_dx = -ball_dx  # Horizontal collision
                # Adjust position to prevent sticking
                if min_overlap == left_overlap:
                    ball_x = obstacle.right + BALL_RADIUS
                else:
                    ball_x = obstacle.left - BALL_RADIUS
            else:
                ball_dy = -ball_dy  # Vertical collision
                # Adjust position to prevent sticking
                if min_overlap == top_overlap:
                    ball_y = obstacle.bottom + BALL_RADIUS
                else:
                    ball_y = obstacle.top - BALL_RADIUS
            
            return True
    
    return False

# Main game loop
running = True
game_started = False
game_over = False
score = 0
level = 1
lives = 3

bricks = initialize_bricks(level)
obstacles = initialize_obstacles(level)

clock = pygame.time.Clock()

while running:
    screen.fill(BACKGROUND_COLOR)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_started:
                    game_started = True
                    launch_ball(level)
                elif game_over:
                    game_over = False
                    game_started = True
                    level = 1
                    lives = 3
                    score = 0
                    bricks = initialize_bricks(level)
                    obstacles = initialize_obstacles(level)
                    reset_ball()
                    launch_ball(level)

    if not game_started:
        show_press_space_message()
    elif game_over:
        font = pygame.font.SysFont("comicsansms", 50)
        text = font.render(f"Game Over! Score: {score}", True, RED)
        restart_text = font.render("Press SPACE to Restart", True, ORANGE)
        screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2 - 40))
        screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, HEIGHT // 2 + 20))
    else:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += paddle_speed

        # Ball movement
        if ball_dx != 0 or ball_dy != 0:  # Only move if the ball has been launched
            ball_x += ball_dx
            ball_y += ball_dy

        # Ball collision with screen borders
        if ball_x - BALL_RADIUS <= 0:  # Left wall
            ball_x = BALL_RADIUS
            ball_dx = -ball_dx
        elif ball_x + BALL_RADIUS >= WIDTH:  # Right wall
            ball_x = WIDTH - BALL_RADIUS
            ball_dx = -ball_dx
            
        if ball_y - BALL_RADIUS <= 0:  # Top wall
            ball_y = BALL_RADIUS
            ball_dy = -ball_dy

        # Create a ball rect for collision detection
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        
        # Ball collision with paddle
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        if ball_rect.colliderect(paddle_rect) and ball_dy > 0:
            # Calculate relative intersection point on the paddle
            relative_intersect_x = (ball_x - (paddle_x + PADDLE_WIDTH/2)) / (PADDLE_WIDTH/2)
            
            # Calculate new angle based on where it hits the paddle (between -60 and 60 degrees)
            bounce_angle = relative_intersect_x * 60
            
            # Calculate ball speed based on current velocity
            current_speed = math.sqrt(ball_dx**2 + ball_dy**2)
            
            # Convert angle to velocity components
            ball_dx = current_speed * math.sin(math.radians(bounce_angle))
            ball_dy = -current_speed * math.cos(math.radians(bounce_angle))
            
            # Ensure ball is above paddle after collision
            ball_y = paddle_y - BALL_RADIUS

        # Ball collision with obstacles
        check_obstacle_collision(ball_rect)

        # Ball collision with bricks
        collision_occurred = False
        for i, (brick, color) in enumerate(bricks[:]):
            if ball_rect.colliderect(brick) and not collision_occurred:
                collision_occurred = True
                score += 10 * level  # Higher levels give more points
                
                # Determine which side of the brick was hit
                left_overlap = (brick.right - ball_rect.left)
                right_overlap = (ball_rect.right - brick.left)
                top_overlap = (brick.bottom - ball_rect.top)
                bottom_overlap = (ball_rect.bottom - brick.top)
                
                # Find the smallest overlap to determine collision direction
                min_overlap = min(left_overlap, right_overlap, top_overlap, bottom_overlap)
                
                if min_overlap == left_overlap or min_overlap == right_overlap:
                    ball_dx = -ball_dx  # Horizontal collision
                    if min_overlap == left_overlap:
                        ball_x = brick.right + BALL_RADIUS
                    else:
                        ball_x = brick.left - BALL_RADIUS
                else:
                    ball_dy = -ball_dy  # Vertical collision
                    if min_overlap == top_overlap:
                        ball_y = brick.bottom + BALL_RADIUS
                    else:
                        ball_y = brick.top - BALL_RADIUS
                        
                bricks.pop(i)
                break

        # Ball falls below screen - lose a life
        if ball_y + BALL_RADIUS >= HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                reset_ball()
                # Wait for spacebar to launch again
                ball_dx = 0
                ball_dy = 0

        # Level up logic (if all bricks are cleared)
        if len(bricks) == 0:
            level += 1
            bricks = initialize_bricks(level)
            obstacles = initialize_obstacles(level)
            reset_ball()
            # Show level up message
            font = pygame.font.SysFont("comicsansms", 50)
            text = font.render(f"Level {level}!", True, GREEN)
            screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(1000)  # Show level message for 1 second

        # Draw elements
        # Draw paddle
        pygame.draw.rect(screen, BLUE, paddle_rect)
        
        # Draw ball
        pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), BALL_RADIUS)
        
        # Draw bricks
        for brick, color in bricks:
            pygame.draw.rect(screen, color, brick)
        
        # Draw obstacles
        for obstacle, color in obstacles:
            pygame.draw.rect(screen, color, obstacle)
            
        # Display score, level, and lives
        font = pygame.font.SysFont("comicsansms", 20)
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        
        screen.blit(score_text, (10, HEIGHT - 30))
        screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, HEIGHT - 30))
        screen.blit(lives_text, (WIDTH - 100, HEIGHT - 30))
        
        # Show hint if ball not launched
        if ball_dx == 0 and ball_dy == 0 and not game_over:
            hint_font = pygame.font.SysFont("comicsansms", 20)
            hint_text = hint_font.render("Press SPACE to launch ball", True, ORANGE)
            screen.blit(hint_text, ((WIDTH - hint_text.get_width()) // 2, HEIGHT // 2 + 50))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()