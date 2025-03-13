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
YELLOW = (255, 255, 0)
TEAL = (0, 128, 128)
BACKGROUND_COLOR = (30, 30, 30)  # Dark gray background

# Color mapping for level files
BRICK_COLORS = {
    'b': BLUE,
    'o': ORANGE,
    'g': GREEN,
    'r': RED,
    'p': PURPLE,
    'y': YELLOW,
    't': TEAL,
    'x': (149, 165, 166)  # Grey color for unbreakable bricks
}

# Brick properties
UNBREAKABLE = 'x'  # Identifier for unbreakable bricks

# Paddle setup
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - 50
paddle_speed = 7

# Ball setup
BALL_RADIUS = 8
ball_x = WIDTH // 2
ball_y = HEIGHT - 70  # Position above paddle
ball_dx = 0
ball_dy = 0

# Difficulty settings
DIFFICULTY_SPEEDS = {
    'EASY': 4,
    'NORMAL': 5,
    'HARD': 7
}
difficulty = 'NORMAL'  # Default difficulty
initial_ball_speed = DIFFICULTY_SPEEDS[difficulty]

# Function to change difficulty
def change_difficulty(new_difficulty):
    global difficulty, initial_ball_speed
    difficulty = new_difficulty
    initial_ball_speed = DIFFICULTY_SPEEDS[difficulty]

# Function to display difficulty selection menu
def show_difficulty_menu():
    screen.fill(BACKGROUND_COLOR)
    
    # Draw decorative elements - gradient-like effect
    for i in range(5):
        alpha = 255 - (i * 40)
        s = pygame.Surface((WIDTH, HEIGHT))
        s.fill(BLUE)
        s.set_alpha(alpha)
        screen.blit(s, (0, i * 2))
        screen.blit(s, (0, HEIGHT - (i * 2)))
    
    # Draw title with enhanced shadow effect
    title_y = HEIGHT // 8  # Moved higher up
    font = pygame.font.SysFont("comicsansms", 72)
    for offset in range(3):  # Multiple layers of shadow
        shadow_title = font.render("Select Difficulty", True, (20 + offset * 20, 20 + offset * 20, 20 + offset * 20))
        screen.blit(shadow_title, ((WIDTH - shadow_title.get_width()) // 2 + 3 - offset, title_y + 3 - offset))
    title = font.render("Select Difficulty", True, ORANGE)
    screen.blit(title, ((WIDTH - title.get_width()) // 2, title_y))
    
    difficulties = ['EASY', 'NORMAL', 'HARD']
    button_width = 300
    button_height = 80
    spacing = 40
    total_height = len(difficulties) * (button_height + spacing)
    start_y = (HEIGHT - total_height) // 2 + 80  # Adjusted for better vertical spacing
    
    selected = None
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    
    for i, diff in enumerate(difficulties):
        button_rect = pygame.Rect((WIDTH - button_width) // 2, start_y + i * (button_height + spacing), button_width, button_height)
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        # Enhanced button visuals
        if is_hovered:
            if mouse_clicked:
                # Clicked state with inner glow
                pygame.draw.rect(screen, ORANGE, button_rect)
                pygame.draw.rect(screen, (255, 200, 100), button_rect.inflate(-6, -6))
                selected = diff
            else:
                # Hover state with gradient
                pygame.draw.rect(screen, (80, 80, 80), button_rect)
                pygame.draw.rect(screen, ORANGE, button_rect, 3)
                # Inner glow
                pygame.draw.rect(screen, (100, 100, 100), button_rect.inflate(-6, -6))
        else:
            # Normal state with subtle gradient
            pygame.draw.rect(screen, (40, 40, 40), button_rect)
            pygame.draw.rect(screen, (60, 60, 60), button_rect.inflate(-4, -4))
            pygame.draw.rect(screen, WHITE, button_rect, 2)
        
        # Button text with shadow
        diff_font = pygame.font.SysFont("comicsansms", 40)
        text_color = BLACK if is_hovered and mouse_clicked else WHITE
        
        # Shadow for main text
        text_shadow = diff_font.render(diff, True, (50, 50, 50))
        text_shadow_rect = text_shadow.get_rect(center=(button_rect.centerx + 2, button_rect.centery - 10 + 2))
        screen.blit(text_shadow, text_shadow_rect)
        
        # Main text
        text = diff_font.render(diff, True, text_color)
        text_rect = text.get_rect(center=(button_rect.centerx, button_rect.centery - 10))
        screen.blit(text, text_rect)
        
        # Description text with new positioning and style
        desc_text = ""
        if diff == "EASY":
            desc_text = "For a relaxing break"
        elif diff == "NORMAL":
            desc_text = "The classic experience"
        elif diff == "HARD":
            desc_text = "For the brave!"
        
        desc_font = pygame.font.SysFont("comicsansms", 22)
        desc_color = BLACK if is_hovered and mouse_clicked else (200, 200, 200)
        desc = desc_font.render(desc_text, True, desc_color)
        desc_rect = desc.get_rect(center=(button_rect.centerx, button_rect.centery + 20))
        screen.blit(desc, desc_rect)
    
    return selected

# Bricks setup
BRICK_WIDTH = WIDTH // 16 - 5
BRICK_HEIGHT = 20

# Obstacles setup
obstacles = []

# Function to initialize bricks based on level
def initialize_bricks(level):
    bricks = []
    
    try:
        # Adjust level number to match file naming (level 1 is in 0.txt)
        file_level = level - 1
        with open(f"{file_level}.txt", "r") as file:
            lines = file.readlines()
            for row, line in enumerate(lines):
                line = line.strip()
                for col, char in enumerate(line):
                    if char != '.':  # '.' represents empty space
                        brick_color = BRICK_COLORS.get(char.lower(), GRAY)  # Default to gray if unknown color
                        bricks.append((pygame.Rect(
                            col * (BRICK_WIDTH + 5) + 5,
                            row * (BRICK_HEIGHT + 5) + 5,
                            BRICK_WIDTH, BRICK_HEIGHT), brick_color, char.lower() == UNBREAKABLE))  # Added unbreakable flag
    except FileNotFoundError:
        # Fallback to default layout if file doesn't exist
        colors = [MUSTARD, ORANGE, GREEN, BLUE, RED]
        brick_rows = min(3 + level, 8)
        brick_cols = 16
        
        for row in range(brick_rows):
            for col in range(brick_cols):
                brick_color = colors[row % len(colors)]
                bricks.append((pygame.Rect(
                    col * (BRICK_WIDTH + 5) + 5,
                    row * (BRICK_HEIGHT + 5) + 5,
                    BRICK_WIDTH, BRICK_HEIGHT), brick_color, False))  # Added unbreakable flag (False for default bricks)
    
    return bricks

# Function to initialize obstacles based on level
def initialize_obstacles(level):
    obstacles = []
    
    if level >= 1:  # Only add obstacles from level 2 onwards
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
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x, game_started
    paddle_x = (WIDTH - PADDLE_WIDTH) // 2  # Reset paddle to center
    ball_x = paddle_x + PADDLE_WIDTH // 2   # Place ball on paddle center
    ball_y = paddle_y - BALL_RADIUS
    ball_dx = 0
    ball_dy = 0
    game_started = False  # Reset game started state so ball sticks to paddle

# Function to launch ball with initial velocity
def launch_ball(level):
    global ball_dx, ball_dy
    
    # Ball speed increases with level
    ball_speed = initial_ball_speed + (level - 1) * 0.5
    ball_speed = min(ball_speed, 10)  # Cap at maximum speed
    
    # Launch straight up
    ball_dx = 0
    ball_dy = -ball_speed

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
selecting_difficulty = True  # New state for difficulty selection

bricks = initialize_bricks(level)
obstacles = initialize_obstacles(level)

# Set initial ball position on paddle
ball_x = paddle_x + PADDLE_WIDTH // 2
ball_y = paddle_y - BALL_RADIUS

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and selecting_difficulty:
            selected = show_difficulty_menu()
            if selected:
                change_difficulty(selected)
                selecting_difficulty = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if selecting_difficulty:
                continue  # Ignore space during difficulty selection
            if not game_started and not game_over:  
                game_started = True
                launch_ball(level)
            elif game_over:
                game_over = False
                game_started = True
                level = 1
                lives = 3
                score = 0
                selecting_difficulty = True  # Return to difficulty selection on restart
                bricks = initialize_bricks(level)
                obstacles = initialize_obstacles(level)
                reset_ball()

    if selecting_difficulty:
        selected = show_difficulty_menu()
        if selected:
            change_difficulty(selected)
            selecting_difficulty = False
        pygame.display.flip()
        continue

    # Draw background
    screen.fill(BACKGROUND_COLOR)

    # Always draw game elements
    # Draw bricks
    for brick, color, unbreakable in bricks:
        pygame.draw.rect(screen, color, brick)
    
    # Draw obstacles
    for obstacle, color in obstacles:
        pygame.draw.rect(screen, color, obstacle)
    
    # Draw paddle
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    
    # Draw ball
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), BALL_RADIUS)

    # Display score, level, and lives (always shown)
    font = pygame.font.SysFont("comicsansms", 20)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    diff_text = font.render(f"Mode: {difficulty}", True, WHITE)
    
    screen.blit(score_text, (10, HEIGHT - 30))
    screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, HEIGHT - 30))
    screen.blit(lives_text, (WIDTH - 100, HEIGHT - 30))
    screen.blit(diff_text, (10, 10))  # Display difficulty in top-left corner

    if game_over:
        font = pygame.font.SysFont("comicsansms", 50)
        text = font.render(f"Game Over! Score: {score}", True, RED)
        restart_text = font.render("Press SPACE to Restart", True, ORANGE)
        screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2 - 40))
        screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, HEIGHT // 2 + 20))
    elif not game_started:
        # Update ball position to follow paddle
        ball_x = paddle_x + PADDLE_WIDTH // 2
        ball_y = paddle_y - BALL_RADIUS
        show_press_space_message()
        
        # Allow paddle movement before game starts
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += paddle_speed
    else:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += paddle_speed

        # Ball movement
        if ball_dx != 0 or ball_dy != 0:  
            ball_x += ball_dx
            ball_y += ball_dy

        # Ball collision with screen borders
        if ball_x - BALL_RADIUS <= 0:  
            ball_x = BALL_RADIUS
            ball_dx = -ball_dx
        elif ball_x + BALL_RADIUS >= WIDTH:  
            ball_x = WIDTH - BALL_RADIUS
            ball_dx = -ball_dx
            
        if ball_y - BALL_RADIUS <= 0:  
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
        for i, (brick, color, unbreakable) in enumerate(bricks[:]):
            if ball_rect.colliderect(brick) and not collision_occurred:
                collision_occurred = True
                if not unbreakable:
                    bricks.pop(i)
                    score += 10 * level  
                
                # Determine which side of the brick was hit
                left_overlap = (brick.right - ball_rect.left)
                right_overlap = (ball_rect.right - brick.left)
                top_overlap = (brick.bottom - ball_rect.top)
                bottom_overlap = (ball_rect.bottom - brick.top)
                
                # Find the smallest overlap to determine collision direction
                min_overlap = min(left_overlap, right_overlap, top_overlap, bottom_overlap)
                
                if min_overlap == left_overlap or min_overlap == right_overlap:
                    ball_dx = -ball_dx  
                    if min_overlap == left_overlap:
                        ball_x = brick.right + BALL_RADIUS
                    else:
                        ball_x = brick.left - BALL_RADIUS
                else:
                    ball_dy = -ball_dy  
                    if min_overlap == top_overlap:
                        ball_y = brick.bottom + BALL_RADIUS
                    else:
                        ball_y = brick.top - BALL_RADIUS
                        
        # Ball falls below screen - lose a life
        if ball_y + BALL_RADIUS >= HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                # Show life lost message
                font = pygame.font.SysFont("comicsansms", 50)
                text = font.render("Life Lost!", True, RED)
                screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(1000)  # Pause for a second
                reset_ball()

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
            pygame.time.delay(1000)  

        # Show hint if ball not launched
        if ball_dx == 0 and ball_dy == 0 and not game_over:
            hint_font = pygame.font.SysFont("comicsansms", 20)
            hint_text = hint_font.render("Press SPACE to launch ball", True, ORANGE)
            screen.blit(hint_text, ((WIDTH - hint_text.get_width()) // 2, HEIGHT // 2 + 50))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()