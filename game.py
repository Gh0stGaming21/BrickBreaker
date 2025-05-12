import pygame
import random
import math
import uuid
import time
import json
import os
import sys

# Initialize pygame
pygame.init()

# High scores file
HIGH_SCORES_FILE = "high_scores.json"

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CRACKSHOT ARCADE")

# Load arcade fonts if available, otherwise use fallbacks
try:
    # Try to load arcade-style fonts if they exist in the system
    TITLE_FONT = pygame.font.SysFont("Press Start 2P", 50)
    SUBTITLE_FONT = pygame.font.SysFont("Press Start 2P", 24)
    REGULAR_FONT = pygame.font.SysFont("Press Start 2P", 18)
except:
    # Fallback to default fonts with pixel-like appearance
    TITLE_FONT = pygame.font.Font(None, 74)
    SUBTITLE_FONT = pygame.font.Font(None, 36)
    REGULAR_FONT = pygame.font.Font(None, 24)

# Neon arcade colors
WHITE = (244, 244, 244)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)  # Brighter blue
RED = (255, 50, 50)   # Neon red
GREEN = (0, 255, 120)  # Neon green
GRAY = (128, 128, 128)
MUSTARD = (255, 200, 0)  # Brighter mustard
ORANGE = (255, 120, 0)   # Neon orange
PURPLE = (200, 0, 255)   # Neon purple
YELLOW = (255, 255, 0)   # Bright yellow
TEAL = (0, 200, 200)     # Brighter teal
PINK = (255, 0, 200)     # Neon pink
CYAN = (0, 255, 255)     # Neon cyan
BACKGROUND_COLOR = (10, 10, 30)  # Darker blue-black

# Scanline effect surface
scanlines = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
for i in range(0, HEIGHT, 4):  # Draw scanlines every 4 pixels
    pygame.draw.line(scanlines, (0, 0, 0, 50), (0, i), (WIDTH, i), 2)


# Function to generate unique game ID
def generate_game_id():
    return str(uuid.uuid4())[:8].upper()

# Function to show welcome screen
def show_welcome_screen():
    game_id = generate_game_id()
    welcome = True
    
    # Animation variables
    title_glow = 0
    glow_direction = 1
    start_alpha = 0
    start_alpha_dir = 5
    
    while welcome:
        screen.fill(BACKGROUND_COLOR)
        
        # Draw arcade cabinet decorative elements
        pygame.draw.rect(screen, (30, 30, 50), (0, 0, WIDTH, 40))  # Top border
        pygame.draw.rect(screen, (30, 30, 50), (0, HEIGHT-40, WIDTH, 40))  # Bottom border
        pygame.draw.rect(screen, (30, 30, 50), (0, 0, 40, HEIGHT))  # Left border
        pygame.draw.rect(screen, (30, 30, 50), (WIDTH-40, 0, 40, HEIGHT))  # Right border
        
        # Draw neon border
        pygame.draw.rect(screen, (ORANGE[0], ORANGE[1], ORANGE[2], title_glow), (45, 45, WIDTH-90, HEIGHT-90), 3)
        
        # Update glow effect
        title_glow += glow_direction * 2
        if title_glow > 200 or title_glow < 50:
            glow_direction *= -1
        
        # Draw title with glow effect
        for offset in range(3, 0, -1):
            shadow_color = (MUSTARD[0]//2, MUSTARD[1]//2, MUSTARD[2]//2, 100)
            title_shadow = TITLE_FONT.render("CRACKSHOT", True, shadow_color)
            screen.blit(title_shadow, (WIDTH//2 - title_shadow.get_width()//2 + offset, HEIGHT//3 + offset))
        
        title_text = TITLE_FONT.render("CRACKSHOT", True, MUSTARD)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//3))
        screen.blit(title_text, title_rect)
        
        # Draw arcade subtitle
        arcade_text = SUBTITLE_FONT.render("ARCADE EDITION", True, CYAN)
        arcade_rect = arcade_text.get_rect(center=(WIDTH//2, HEIGHT//3 + 60))
        screen.blit(arcade_text, arcade_rect)
        
        # Draw game ID with pixel border
        id_bg = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 20, 300, 40)
        pygame.draw.rect(screen, (50, 50, 70), id_bg)
        pygame.draw.rect(screen, BLUE, id_bg, 2)
        
        id_text = SUBTITLE_FONT.render(f"GAME ID: {game_id}", True, WHITE)
        id_rect = id_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(id_text, id_rect)
        
        # Draw start instruction with blinking effect
        start_alpha = (start_alpha + start_alpha_dir) % 255
        if start_alpha < 50 or start_alpha > 200:
            start_alpha_dir *= -1
            
        # Create a highlighted background for the PRESS SPACE message
        message_bg = pygame.Rect(WIDTH//2 - 200, HEIGHT*2//3 - 15, 400, 70)
        pygame.draw.rect(screen, (50, 50, 80), message_bg)
        pygame.draw.rect(screen, CYAN, message_bg, 3)
        
        # Draw "INSERT COIN" text
        start_text = SUBTITLE_FONT.render("INSERT COIN", True, YELLOW)
        start_text.set_alpha(255)  # Full opacity
        start_rect = start_text.get_rect(center=(WIDTH//2, HEIGHT*2//3 - 30))
        screen.blit(start_text, start_rect)
        
        # Draw "PRESS SPACE TO START" text with glow effect
        # Draw glow effect
        for offset in range(3, 0, -1):
            glow_color = (GREEN[0]//2, GREEN[1]//2, GREEN[2]//2)
            glow_text = SUBTITLE_FONT.render("PRESS SPACE TO START", True, glow_color)
            screen.blit(glow_text, (WIDTH//2 - glow_text.get_width()//2 + offset, HEIGHT*2//3 + 20 + offset))
            screen.blit(glow_text, (WIDTH//2 - glow_text.get_width()//2 - offset, HEIGHT*2//3 + 20 - offset))
        
        # Main text with full opacity
        press_space_text = SUBTITLE_FONT.render("PRESS SPACE TO START", True, GREEN)
        press_space_rect = press_space_text.get_rect(center=(WIDTH//2, HEIGHT*2//3 + 20))
        screen.blit(press_space_text, press_space_rect)
        
        # Draw decorative arrows pointing at the message
        arrow_size = 15
        # Left arrow
        pygame.draw.polygon(screen, CYAN, [
            (WIDTH//2 - 210, HEIGHT*2//3 + 20),
            (WIDTH//2 - 210 + arrow_size, HEIGHT*2//3 + 20 - arrow_size//2),
            (WIDTH//2 - 210 + arrow_size, HEIGHT*2//3 + 20 + arrow_size//2)
        ])
        # Right arrow
        pygame.draw.polygon(screen, CYAN, [
            (WIDTH//2 + 210, HEIGHT*2//3 + 20),
            (WIDTH//2 + 210 - arrow_size, HEIGHT*2//3 + 20 - arrow_size//2),
            (WIDTH//2 + 210 - arrow_size, HEIGHT*2//3 + 20 + arrow_size//2)
        ])
        
        # Draw decorative joysticks
        pygame.draw.circle(screen, GRAY, (150, HEIGHT-100), 30)
        pygame.draw.circle(screen, BLACK, (150, HEIGHT-100), 25)
        pygame.draw.circle(screen, GRAY, (WIDTH-150, HEIGHT-100), 30)
        pygame.draw.circle(screen, BLACK, (WIDTH-150, HEIGHT-100), 25)
        
        # Apply scanlines for retro effect
        screen.blit(scanlines, (0, 0))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Play coin sound effect here if available
                    return True, game_id
        
        # Control the animation speed
        pygame.time.delay(30)
    
    return False, None

# Color mapping for level files
BRICK_COLORS = {
    'b': BLUE,
    'o': ORANGE,
    'g': GREEN,
    'r': RED,
    'p': PURPLE,
    'y': YELLOW,
    't': TEAL,
    'x': (149, 165, 166) 
}

# Brick properties
UNBREAKABLE = 'x'  

# Paddle setup
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - 50
paddle_speed = 7

# Ball setup
BALL_RADIUS = 8
ball_x = WIDTH // 2
ball_y = HEIGHT - 70 
ball_dx = 0
ball_dy = 0

# Difficulty settings
DIFFICULTY_SPEEDS = {
    'EASY': 4,
    'NORMAL': 5,
    'HARD': 7
}
difficulty = 'NORMAL' 
initial_ball_speed = DIFFICULTY_SPEEDS[difficulty]

# Function to change difficulty
def change_difficulty(new_difficulty):
    global difficulty, initial_ball_speed
    difficulty = new_difficulty
    initial_ball_speed = DIFFICULTY_SPEEDS[difficulty]

# Function to display difficulty selection menu
def show_difficulty_menu():
    screen.fill(BACKGROUND_COLOR)
    
    # Draw arcade cabinet frame
    pygame.draw.rect(screen, (30, 30, 50), (0, 0, WIDTH, 40))  # Top border
    pygame.draw.rect(screen, (30, 30, 50), (0, HEIGHT-40, WIDTH, 40))  # Bottom border
    pygame.draw.rect(screen, (30, 30, 50), (0, 0, 40, HEIGHT))  # Left border
    pygame.draw.rect(screen, (30, 30, 50), (WIDTH-40, 0, 40, HEIGHT))  # Right border
    
    # Draw grid background for arcade feel
    grid_size = 40
    for x in range(40, WIDTH-40, grid_size):
        pygame.draw.line(screen, (40, 40, 60), (x, 40), (x, HEIGHT-40), 1)
    for y in range(40, HEIGHT-40, grid_size):
        pygame.draw.line(screen, (40, 40, 60), (40, y), (WIDTH-40, y), 1)
    
    # Draw title with neon glow effect
    title_y = HEIGHT // 8
    
    # Outer glow
    for offset in range(5, 0, -1):
        glow_color = (CYAN[0]//offset, CYAN[1]//offset, CYAN[2]//offset)
        shadow_title = TITLE_FONT.render("SELECT LEVEL", True, glow_color)
        screen.blit(shadow_title, ((WIDTH - shadow_title.get_width()) // 2 + offset, title_y + offset))
        screen.blit(shadow_title, ((WIDTH - shadow_title.get_width()) // 2 - offset, title_y - offset))
    
    # Main title
    title = TITLE_FONT.render("SELECT LEVEL", True, CYAN)
    screen.blit(title, ((WIDTH - title.get_width()) // 2, title_y))
    
    difficulties = ['NOVICE', 'EXPERT', 'MASTER']
    button_width = 300
    button_height = 80
    spacing = 50
    total_height = len(difficulties) * (button_height + spacing)
    start_y = (HEIGHT - total_height) // 2 + 80
    
    selected = None
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = pygame.mouse.get_pressed()[0]
    
    # Draw cabinet art
    cabinet_art = pygame.Rect(60, 60, 120, HEIGHT-120)
    pygame.draw.rect(screen, (20, 20, 40), cabinet_art)
    pygame.draw.rect(screen, PINK, cabinet_art, 2)
    
    cabinet_art2 = pygame.Rect(WIDTH-180, 60, 120, HEIGHT-120)
    pygame.draw.rect(screen, (20, 20, 40), cabinet_art2)
    pygame.draw.rect(screen, PINK, cabinet_art2, 2)
    
    # Draw pixelated joystick on cabinet art
    pygame.draw.circle(screen, GRAY, (120, HEIGHT-150), 25)
    pygame.draw.circle(screen, BLACK, (120, HEIGHT-150), 20)
    pygame.draw.circle(screen, GRAY, (WIDTH-120, HEIGHT-150), 25)
    pygame.draw.circle(screen, BLACK, (WIDTH-120, HEIGHT-150), 20)
    
    # Draw buttons
    button_colors = [GREEN, YELLOW, RED]
    button_glow_colors = [(0, 255, 0), (255, 255, 0), (255, 0, 0)]
    
    for i, diff in enumerate(difficulties):
        button_rect = pygame.Rect((WIDTH - button_width) // 2, start_y + i * (button_height + spacing), button_width, button_height)
        is_hovered = button_rect.collidepoint(mouse_pos)
        
        # Arcade cabinet style buttons
        if is_hovered:
            # Outer glow
            for offset in range(5, 0, -1):
                glow_alpha = 150 - (offset * 20)
                glow_rect = button_rect.inflate(offset*2, offset*2)
                glow_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(glow_surf, (*button_glow_colors[i], glow_alpha), (0, 0, glow_rect.width, glow_rect.height))
                screen.blit(glow_surf, glow_rect)
            
            if mouse_clicked:
                # Clicked state with pixel inset
                pygame.draw.rect(screen, (50, 50, 70), button_rect)
                pygame.draw.rect(screen, button_colors[i], button_rect, 3)
                selected = diff
            else:
                # Hover state with neon outline
                pygame.draw.rect(screen, (40, 40, 60), button_rect)
                pygame.draw.rect(screen, button_colors[i], button_rect, 3)
        else:
            # Normal state with pixel border
            pygame.draw.rect(screen, (30, 30, 50), button_rect)
            # Pixelated border
            for px in range(0, button_rect.width, 4):
                pygame.draw.rect(screen, button_colors[i], (button_rect.x + px, button_rect.y, 2, 2))
                pygame.draw.rect(screen, button_colors[i], (button_rect.x + px, button_rect.y + button_rect.height - 2, 2, 2))
            for py in range(0, button_rect.height, 4):
                pygame.draw.rect(screen, button_colors[i], (button_rect.x, button_rect.y + py, 2, 2))
                pygame.draw.rect(screen, button_colors[i], (button_rect.x + button_rect.width - 2, button_rect.y + py, 2, 2))
        
        # Button text with pixel style
        text_color = WHITE
        
        # Main text
        text = SUBTITLE_FONT.render(diff, True, text_color)
        text_rect = text.get_rect(center=(button_rect.centerx, button_rect.centery - 15))
        screen.blit(text, text_rect)
        
        # Description text with arcade style
        desc_text = ""
        if diff == "NOVICE":
            desc_text = "1 CREDIT"
        elif diff == "EXPERT":
            desc_text = "2 CREDITS"
        elif diff == "MASTER":
            desc_text = "3 CREDITS"
        
        desc = REGULAR_FONT.render(desc_text, True, button_colors[i])
        desc_rect = desc.get_rect(center=(button_rect.centerx, button_rect.centery + 20))
        screen.blit(desc, desc_rect)
    
    # Draw insert coin text at bottom
    coin_text = REGULAR_FONT.render("INSERT COIN TO PLAY", True, YELLOW)
    coin_rect = coin_text.get_rect(center=(WIDTH//2, HEIGHT - 70))
    screen.blit(coin_text, coin_rect)
    
    # Apply scanlines for retro effect
    screen.blit(scanlines, (0, 0))
    
    # Map the difficulty names to the actual difficulty levels
    if selected == "NOVICE":
        return "EASY"
    elif selected == "EXPERT":
        return "NORMAL"
    elif selected == "MASTER":
        return "HARD"
    
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
    # Arcade-style blinking text
    alpha = 150 + int(100 * math.sin(pygame.time.get_ticks() / 200))
    alpha = max(50, min(alpha, 255))  # Keep alpha between 50 and 255
    
    # Pixel-style text with glow
    text = SUBTITLE_FONT.render("INSERT COIN (SPACE)", True, YELLOW)
    text.set_alpha(alpha) 
    
    # Add glow effect
    glow = SUBTITLE_FONT.render("INSERT COIN (SPACE)", True, (YELLOW[0]//2, YELLOW[1]//2, 0))
    glow.set_alpha(alpha // 2)
    
    screen.blit(glow, ((WIDTH - glow.get_width()) // 2 + 2, HEIGHT // 2 + 2))
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
    global ball_x, ball_y, ball_dx, ball_dy
    
    for obstacle, color in obstacles:
        if ball_rect.colliderect(obstacle):
            # Calculate overlaps for precise collision direction
            overlaps = {
                'left': obstacle.right - ball_rect.left,
                'right': ball_rect.right - obstacle.left,
                'top': obstacle.bottom - ball_rect.top,
                'bottom': ball_rect.bottom - obstacle.top
            }
            
            # Find the smallest overlap to determine collision side
            min_overlap_side = min(overlaps, key=overlaps.get)
            
            # Reflect ball based on collision side
            if min_overlap_side in ['left', 'right']:
                # Horizontal collision (side hit)
                ball_dx = -ball_dx
                ball_x = obstacle.right + BALL_RADIUS if min_overlap_side == 'left' else obstacle.left - BALL_RADIUS
            else:
                # Vertical collision (top/bottom hit)
                ball_dy = -ball_dy
                ball_y = obstacle.bottom + BALL_RADIUS if min_overlap_side == 'top' else obstacle.top - BALL_RADIUS
            
            return True
    
    return False

def check_brick_collision(ball_rect, bricks):
    global ball_x, ball_y
    collision_occurred = False
    score_increment = 0
    new_ball_dx, new_ball_dy = ball_dx, ball_dy

    for i, (brick, color, unbreakable) in enumerate(bricks[:]):
        if ball_rect.colliderect(brick):
            collision_occurred = True
            
            if not unbreakable:
                bricks.pop(i)
                score_increment = 10 * level
            
            # Calculate overlaps for precise collision direction
            overlaps = {
                'left': brick.right - ball_rect.left,
                'right': ball_rect.right - brick.left,
                'top': brick.bottom - ball_rect.top,
                'bottom': ball_rect.bottom - brick.top
            }
            
            # Find the smallest overlap to determine collision side
            min_overlap_side = min(overlaps, key=overlaps.get)
            
            # Reflect ball based on collision side
            if min_overlap_side in ['left', 'right']:
                # Horizontal collision (side hit)
                new_ball_dx = -ball_dx
                ball_x = brick.right + BALL_RADIUS if min_overlap_side == 'left' else brick.left - BALL_RADIUS
            else:
                # Vertical collision (top/bottom hit)
                new_ball_dy = -ball_dy
                ball_y = brick.bottom + BALL_RADIUS if min_overlap_side == 'top' else brick.top - BALL_RADIUS
            
            break  # Only handle one brick collision per frame
    
    return collision_occurred, bricks, score_increment, new_ball_dx, new_ball_dy

def check_level_complete(bricks):
    # Check if there are any breakable bricks left
    for brick, color, unbreakable in bricks:
        if not unbreakable:
            return False
    return True

# Function to load high scores
def load_high_scores():
    if os.path.exists(HIGH_SCORES_FILE):
        try:
            with open(HIGH_SCORES_FILE, 'r') as file:
                content = file.read().strip()
                if content:  # Check if file is not empty
                    return json.loads(content)
                else:
                    return []
        except Exception as e:
            print(f"Error loading high scores: {e}")
            # If there's an error, create a new high scores file
            with open(HIGH_SCORES_FILE, 'w') as file:
                file.write('[]')
            return []
    else:
        # Create the file if it doesn't exist
        with open(HIGH_SCORES_FILE, 'w') as file:
            file.write('[]')
        return []

# Function to save high scores
def save_high_score(game_id, player_score, difficulty_level):
    # Don't save scores of 0
    if player_score <= 0:
        return
        
    high_scores = load_high_scores()
    
    # Create new score entry
    new_score = {
        'game_id': game_id,
        'score': player_score,
        'difficulty': difficulty_level,
        'date': time.strftime("%Y-%m-%d %H:%M")
    }
    
    # Check for duplicate game_id entries and only keep the highest score
    existing_ids = [score['game_id'] for score in high_scores]
    if game_id in existing_ids:
        # Find the index of the existing score with the same game_id
        index = existing_ids.index(game_id)
        # Only replace if the new score is higher
        if player_score > high_scores[index]['score']:
            high_scores[index] = new_score
    else:
        # Add the new score
        high_scores.append(new_score)
    
    # Sort by score in descending order
    high_scores.sort(key=lambda x: x['score'], reverse=True)
    
    # Keep only top 10 scores
    high_scores = high_scores[:10]
    
    try:
        with open(HIGH_SCORES_FILE, 'w') as file:
            json.dump(high_scores, file, indent=2)
    except Exception as e:
        print(f"Error saving high scores: {e}")

# Function to display high scores screen
def show_high_scores():
    high_scores = load_high_scores()
    viewing_scores = True
    scroll_offset = 0
    scroll_speed = 1
    
    # Animation variables
    title_glow = 0
    glow_direction = 1
    
    while viewing_scores:
        screen.fill(BACKGROUND_COLOR)
        
        # Draw arcade cabinet frame
        pygame.draw.rect(screen, (30, 30, 50), (0, 0, WIDTH, 40))  # Top border
        pygame.draw.rect(screen, (30, 30, 50), (0, HEIGHT-40, WIDTH, 40))  # Bottom border
        pygame.draw.rect(screen, (30, 30, 50), (0, 0, 40, HEIGHT))  # Left border
        pygame.draw.rect(screen, (30, 30, 50), (WIDTH-40, 0, 40, HEIGHT))  # Right border
        
        # Draw grid background for arcade feel
        grid_size = 40
        for x in range(40, WIDTH-40, grid_size):
            pygame.draw.line(screen, (40, 40, 60), (x, 40), (x, HEIGHT-40), 1)
        for y in range(40, HEIGHT-40, grid_size):
            pygame.draw.line(screen, (40, 40, 60), (40, y), (WIDTH-40, y), 1)
        
        # Update glow effect
        title_glow += glow_direction * 2
        if title_glow > 200 or title_glow < 50:
            glow_direction *= -1
        
        # Draw title with neon glow effect
        for offset in range(4, 0, -1):
            glow_alpha = 50 * offset
            shadow_title = TITLE_FONT.render("HIGH SCORES", True, (MUSTARD[0]//2, MUSTARD[1]//2, 0, glow_alpha))
            screen.blit(shadow_title, ((WIDTH - shadow_title.get_width()) // 2 + offset, 80 + offset))
            screen.blit(shadow_title, ((WIDTH - shadow_title.get_width()) // 2 - offset, 80 - offset))
        
        title_text = TITLE_FONT.render("HIGH SCORES", True, MUSTARD)
        title_rect = title_text.get_rect(center=(WIDTH//2, 80))
        screen.blit(title_text, title_rect)
        
        # Create arcade cabinet style scoreboard
        scoreboard_rect = pygame.Rect(80, 140, WIDTH - 160, HEIGHT - 240)
        pygame.draw.rect(screen, (20, 20, 40), scoreboard_rect)
        pygame.draw.rect(screen, CYAN, scoreboard_rect, 3)
        
        # Add scanlines to scoreboard
        for y in range(scoreboard_rect.y, scoreboard_rect.y + scoreboard_rect.height, 4):
            pygame.draw.line(screen, (0, 0, 0, 30), 
                            (scoreboard_rect.x, y), (scoreboard_rect.x + scoreboard_rect.width, y), 1)
        
        # Draw scores with arcade style
        y_pos = 150
        
        if not high_scores:
            no_scores_text = SUBTITLE_FONT.render("NO SCORES YET!", True, YELLOW)
            no_scores_rect = no_scores_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(no_scores_text, no_scores_rect)
        else:
            # Create header with arcade style
            header_bg = pygame.Rect(100, y_pos - 10, WIDTH - 200, 40)
            pygame.draw.rect(screen, (50, 50, 70), header_bg)
            pygame.draw.rect(screen, PINK, header_bg, 2)
            
            # Headers with pixel font
            rank_header = SUBTITLE_FONT.render("RANK", True, PINK)
            score_header = SUBTITLE_FONT.render("SCORE", True, PINK)
            diff_header = SUBTITLE_FONT.render("MODE", True, PINK)
            date_header = SUBTITLE_FONT.render("DATE", True, PINK)
            
            screen.blit(rank_header, (120, y_pos))
            screen.blit(score_header, (220, y_pos))
            screen.blit(diff_header, (370, y_pos))
            screen.blit(date_header, (550, y_pos))
            
            y_pos += 50
            
            # Scrolling effect for scores - only if there are more than 5 scores
            if len(high_scores) > 5:
                scroll_offset = (scroll_offset + scroll_speed) % (len(high_scores) * 40)
            else:
                scroll_offset = 0  # No scrolling needed for few scores
            
            # Draw each score with arcade style
            for i, score_data in enumerate(high_scores):
                # Calculate position with scroll effect
                row_y = y_pos + i * 40 - scroll_offset
                
                # Only draw visible rows
                if row_y >= y_pos and row_y < HEIGHT - 100:
                    # Alternate row colors for readability
                    row_bg = pygame.Rect(100, row_y - 5, WIDTH - 200, 35)
                    if i % 2 == 0:
                        pygame.draw.rect(screen, (30, 30, 50), row_bg)
                    else:
                        pygame.draw.rect(screen, (40, 40, 60), row_bg)
                    
                    # Highlight top 3 scores
                    if i < 3:
                        medal_colors = [YELLOW, (200, 200, 200), (205, 127, 50)]  # Gold, Silver, Bronze
                        pygame.draw.circle(screen, medal_colors[i], (105, row_y + 12), 10)
                    
                    # Draw score data with pixel font
                    rank_text = REGULAR_FONT.render(f"{i+1}", True, WHITE)
                    score_text = REGULAR_FONT.render(f"{score_data['score']}", True, YELLOW)
                    diff_text = REGULAR_FONT.render(f"{score_data['difficulty']}", True, GREEN)
                    date_text = REGULAR_FONT.render(f"{score_data['date']}", True, CYAN)
                    
                    screen.blit(rank_text, (120, row_y + 5))
                    screen.blit(score_text, (220, row_y + 5))
                    screen.blit(diff_text, (370, row_y + 5))
                    screen.blit(date_text, (550, row_y + 5))
        
        # Draw back button with arcade style
        button_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT - 80, 300, 40)
        pygame.draw.rect(screen, (40, 40, 60), button_rect)
        pygame.draw.rect(screen, ORANGE, button_rect, 2)
        
        back_text = SUBTITLE_FONT.render("EXIT (ESC)", True, ORANGE)
        back_rect = back_text.get_rect(center=(WIDTH//2, HEIGHT - 60))
        screen.blit(back_text, back_rect)
        
        # Apply scanlines for retro effect
        screen.blit(scanlines, (0, 0))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    viewing_scores = False
        
        # Control animation speed
        pygame.time.delay(30)
    
    return True

# Main game loop
running = True
game_started = False
game_over = False
game_paused = False
current_game_id = None

# Show welcome screen first
running, current_game_id = show_welcome_screen()
selecting_difficulty = running
score = 0
level = 1
lives = 3
selecting_difficulty = True  # New state for difficulty selection
viewing_high_scores = False

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if selecting_difficulty:
                    continue  # Ignore space during difficulty selection
                if not game_started and not game_over and not game_paused:  
                    game_started = True
                    launch_ball(level)
                elif game_over:
                    # Save high score before restarting
                    save_high_score(current_game_id, score, difficulty)
                    
                    game_over = False
                    game_started = True
                    level = 1
                    lives = 3
                    score = 0
                    selecting_difficulty = True  # Return to difficulty selection on restart
                    bricks = initialize_bricks(level)
                    obstacles = initialize_obstacles(level)
                    reset_ball()
            elif event.key == pygame.K_p and not game_over and not selecting_difficulty:
                # Toggle pause state
                game_paused = not game_paused
            elif event.key == pygame.K_s and game_started and not game_over and not game_paused:
                # Skip to next level
                level += 1
                bricks = initialize_bricks(level)
                obstacles = initialize_obstacles(level)
                reset_ball()
                # Show level up message with arcade style
                # Darken screen
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
                
                # Draw level up text with neon glow
                for offset in range(5, 0, -1):
                    glow_alpha = 50 * offset
                    glow_color = (GREEN[0]//2, GREEN[1]//2, GREEN[2]//2, glow_alpha)
                    shadow_text = TITLE_FONT.render(f"LEVEL {level}", True, glow_color)
                    screen.blit(shadow_text, ((WIDTH - shadow_text.get_width()) // 2 + offset, HEIGHT // 2 - 50 + offset))
                    screen.blit(shadow_text, ((WIDTH - shadow_text.get_width()) // 2 - offset, HEIGHT // 2 - 50 - offset))
                
                text = TITLE_FONT.render(f"LEVEL {level}", True, GREEN)
                screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2 - 50))
                
                # Draw decorative elements
                pygame.draw.rect(screen, CYAN, (WIDTH//2 - 150, HEIGHT//2, 300, 5))
                pygame.draw.rect(screen, CYAN, (WIDTH//2 - 100, HEIGHT//2 + 20, 200, 3))
                
                # Draw get ready message
                ready_text = SUBTITLE_FONT.render("GET READY!", True, YELLOW)
                ready_text.set_alpha(int(127 + 127 * math.sin(pygame.time.get_ticks() / 200)))
                screen.blit(ready_text, ((WIDTH - ready_text.get_width()) // 2, HEIGHT // 2 + 50))
                
                pygame.display.flip()
                
                # Countdown timer
                for countdown in range(3, 0, -1):
                    # Clear previous number
                    screen.blit(overlay, (0, 0))
                    text = TITLE_FONT.render(f"LEVEL {level}", True, GREEN)
                    screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2 - 50))
                    pygame.draw.rect(screen, CYAN, (WIDTH//2 - 150, HEIGHT//2, 300, 5))
                    pygame.draw.rect(screen, CYAN, (WIDTH//2 - 100, HEIGHT//2 + 20, 200, 3))
                    
                    # Draw countdown number with glow
                    for offset in range(3, 0, -1):
                        glow_alpha = 80 * offset
                        glow_color = (YELLOW[0]//2, YELLOW[1]//2, 0, glow_alpha)
                        shadow_num = TITLE_FONT.render(f"{countdown}", True, glow_color)
                        screen.blit(shadow_num, ((WIDTH - shadow_num.get_width()) // 2 + offset, HEIGHT // 2 + 50 + offset))
                        screen.blit(shadow_num, ((WIDTH - shadow_num.get_width()) // 2 - offset, HEIGHT // 2 + 50 - offset))
                    
                    countdown_text = TITLE_FONT.render(f"{countdown}", True, YELLOW)
                    screen.blit(countdown_text, ((WIDTH - countdown_text.get_width()) // 2, HEIGHT // 2 + 50))
                    
                    pygame.display.flip()
                    pygame.time.delay(800)  # Pause for countdown
            elif event.key == pygame.K_h and not game_started and not game_over:
                # Show high scores
                viewing_high_scores = True
                running = show_high_scores()
            elif event.key == pygame.K_ESCAPE and game_paused:
                # Unpause with escape key
                game_paused = False

    if selecting_difficulty:
        selected = show_difficulty_menu()
        if selected:
            change_difficulty(selected)
            selecting_difficulty = False
        pygame.display.flip()
        continue

    # Draw background with arcade grid effect
    screen.fill(BACKGROUND_COLOR)
    
    # Draw grid lines for arcade feel
    grid_size = 40
    grid_alpha = 30
    for x in range(0, WIDTH, grid_size):
        pygame.draw.line(screen, (*BLUE, grid_alpha), (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, grid_size):
        pygame.draw.line(screen, (*BLUE, grid_alpha), (0, y), (WIDTH, y), 1)

    # Always draw game elements
    # Draw bricks with arcade-style effects
    for brick, color, unbreakable in bricks:
        # Brick glow effect
        if unbreakable:
            # Unbreakable bricks have stronger glow
            for offset in range(3, 0, -1):
                glow_alpha = 50 * offset
                glow_rect = pygame.Rect(brick.x - offset, brick.y - offset, 
                                       brick.width + offset*2, brick.height + offset*2)
                pygame.draw.rect(screen, (*WHITE, glow_alpha), glow_rect, 1)
            
            # Metallic look for unbreakable bricks
            pygame.draw.rect(screen, (180, 180, 180), brick)
            pygame.draw.rect(screen, (220, 220, 220), 
                            (brick.x, brick.y, brick.width, brick.height//2))
            pygame.draw.rect(screen, (100, 100, 100), 
                            (brick.x, brick.y + brick.height//2, brick.width, brick.height//2))
            
            # Add rivets to unbreakable bricks
            rivet_radius = 2
            rivet_positions = [(brick.x + 5, brick.y + 5), 
                              (brick.x + brick.width - 5, brick.y + 5),
                              (brick.x + 5, brick.y + brick.height - 5), 
                              (brick.x + brick.width - 5, brick.y + brick.height - 5)]
            for rx, ry in rivet_positions:
                pygame.draw.circle(screen, (50, 50, 50), (rx, ry), rivet_radius)
        else:
            # Regular bricks with neon glow
            pygame.draw.rect(screen, color, brick)
            
            # Inner highlight for 3D effect
            highlight_rect = pygame.Rect(brick.x + 2, brick.y + 2, brick.width - 4, brick.height//2 - 2)
            highlight_color = (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255))
            pygame.draw.rect(screen, highlight_color, highlight_rect)
            
            # Pixel border
            pygame.draw.rect(screen, BLACK, brick, 1)
    
    # Draw obstacles with arcade-style effects
    for obstacle, color in obstacles:
        # Obstacle glow
        for offset in range(3, 0, -1):
            glow_alpha = 40 * offset
            glow_rect = pygame.Rect(obstacle.x - offset, obstacle.y - offset, 
                                   obstacle.width + offset*2, obstacle.height + offset*2)
            pygame.draw.rect(screen, (*color, glow_alpha), glow_rect, 1)
        
        # Main obstacle with gradient effect
        pygame.draw.rect(screen, color, obstacle)
        
        # Add scanline effect to obstacles
        for y in range(obstacle.y, obstacle.y + obstacle.height, 4):
            pygame.draw.line(screen, (0, 0, 0, 100), 
                            (obstacle.x, y), (obstacle.x + obstacle.width, y), 1)
    
    # Draw paddle with neon glow effect
    # Outer glow
    for offset in range(4, 0, -1):
        glow_alpha = 40 + 20 * offset
        glow_rect = pygame.Rect(paddle_x - offset, paddle_y - offset, 
                               PADDLE_WIDTH + offset*2, PADDLE_HEIGHT + offset*2)
        pygame.draw.rect(screen, (*CYAN, glow_alpha), glow_rect, 1)
    
    # Main paddle with gradient
    pygame.draw.rect(screen, CYAN, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (paddle_x + 2, paddle_y + 2, PADDLE_WIDTH - 4, PADDLE_HEIGHT - 4))
    
    # Add decorative elements to paddle
    for i in range(3):
        x_pos = paddle_x + (i+1) * (PADDLE_WIDTH // 4)
        pygame.draw.line(screen, CYAN, (x_pos, paddle_y), (x_pos, paddle_y + PADDLE_HEIGHT), 2)
    
    # Draw ball with arcade-style glow
    # Outer glow
    for offset in range(5, 0, -1):
        glow_alpha = 30 * offset
        pygame.draw.circle(screen, (255, 255, 100, glow_alpha), 
                          (int(ball_x), int(ball_y)), BALL_RADIUS + offset, 1)
    
    # Main ball
    pygame.draw.circle(screen, YELLOW, (int(ball_x), int(ball_y)), BALL_RADIUS)
    
    # Highlight effect (makes ball look more 3D)
    pygame.draw.circle(screen, WHITE, (int(ball_x - BALL_RADIUS/3), int(ball_y - BALL_RADIUS/3)), 
                      BALL_RADIUS/3)

    # Display score, level, and lives with arcade-style UI
    # Create arcade-style score panel at top
    pygame.draw.rect(screen, (20, 20, 40), (0, 0, WIDTH, 50))
    pygame.draw.line(screen, CYAN, (0, 50), (WIDTH, 50), 2)
    
    # Create arcade-style status panel at bottom
    pygame.draw.rect(screen, (20, 20, 40), (0, HEIGHT-40, WIDTH, 40))
    pygame.draw.line(screen, CYAN, (0, HEIGHT-40), (WIDTH, HEIGHT-40), 2)
    
    # Use pixel font for all text
    score_text = REGULAR_FONT.render(f"SCORE: {score}", True, YELLOW)
    level_text = REGULAR_FONT.render(f"LEVEL: {level}", True, GREEN)
    
    # Lives with iconic representation
    lives_label = REGULAR_FONT.render("LIVES:", True, PINK)
    
    # Get highest score for display
    high_scores = load_high_scores()
    highest_score = high_scores[0]['score'] if high_scores else 0
    high_score_text = REGULAR_FONT.render(f"HI-SCORE: {highest_score}", True, ORANGE)
    
    # Display difficulty with arcade style
    diff_text = REGULAR_FONT.render(f"MODE: {difficulty}", True, CYAN)
    
    # Display controls hint
    controls_text = REGULAR_FONT.render("P:PAUSE | S:SKIP | H:SCORES", True, (150, 150, 150))
    
    # Position all UI elements
    screen.blit(score_text, (20, 15))
    screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 20, 15))
    screen.blit(diff_text, (WIDTH//2 - diff_text.get_width()//2, 15))
    screen.blit(level_text, (20, HEIGHT - 30))
    
    # Draw lives with ball icons
    screen.blit(lives_label, (WIDTH - 150, HEIGHT - 30))
    for i in range(lives):
        pygame.draw.circle(screen, YELLOW, (WIDTH - 80 + i*20, HEIGHT - 20), 8)
        pygame.draw.circle(screen, WHITE, (WIDTH - 82 + i*20, HEIGHT - 22), 3)
    
    # Display controls hint at bottom center
    screen.blit(controls_text, (WIDTH//2 - controls_text.get_width()//2, HEIGHT - 30))

    if game_over:
        # Create arcade-style game over screen
        # Darken the background
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Flashing "GAME OVER" text
        flash_intensity = int(127 + 127 * math.sin(pygame.time.get_ticks() / 200))
        game_over_color = (255, flash_intensity//2, flash_intensity//2)  # Pulsing red
        
        # Draw "GAME OVER" with neon glow effect
        for offset in range(5, 0, -1):
            glow_alpha = 50 * offset
            glow_color = (game_over_color[0]//2, game_over_color[1]//2, game_over_color[2]//2, glow_alpha)
            shadow_text = TITLE_FONT.render("GAME OVER", True, glow_color)
            screen.blit(shadow_text, ((WIDTH - shadow_text.get_width()) // 2 + offset, HEIGHT // 2 - 80 + offset))
            screen.blit(shadow_text, ((WIDTH - shadow_text.get_width()) // 2 - offset, HEIGHT // 2 - 80 - offset))
        
        text = TITLE_FONT.render("GAME OVER", True, game_over_color)
        screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2 - 80))
        
        # Draw score with arcade style
        score_text = SUBTITLE_FONT.render(f"FINAL SCORE: {score}", True, YELLOW)
        screen.blit(score_text, ((WIDTH - score_text.get_width()) // 2, HEIGHT // 2 - 20))
        
        # Draw pixelated border around restart button
        button_rect = pygame.Rect(WIDTH//2 - 180, HEIGHT//2 + 20, 360, 50)
        pygame.draw.rect(screen, (50, 50, 70), button_rect)
        
        # Pixelated button border
        for px in range(0, button_rect.width, 4):
            pygame.draw.rect(screen, CYAN, (button_rect.x + px, button_rect.y, 2, 2))
            pygame.draw.rect(screen, CYAN, (button_rect.x + px, button_rect.y + button_rect.height - 2, 2, 2))
        for py in range(0, button_rect.height, 4):
            pygame.draw.rect(screen, CYAN, (button_rect.x, button_rect.y + py, 2, 2))
            pygame.draw.rect(screen, CYAN, (button_rect.x + button_rect.width - 2, button_rect.y + py, 2, 2))
        
        # Blinking restart text
        restart_alpha = int(127 + 127 * math.sin(pygame.time.get_ticks() / 300))
        restart_text = SUBTITLE_FONT.render("INSERT COIN (SPACE)", True, (255, 255, restart_alpha))
        screen.blit(restart_text, ((WIDTH - restart_text.get_width()) // 2, HEIGHT // 2 + 35))
        
        # Show player's rank with arcade style
        high_scores = load_high_scores()
        # Add current score to determine rank
        temp_scores = high_scores.copy()
        temp_scores.append({'score': score})
        temp_scores.sort(key=lambda x: x['score'], reverse=True)
        rank = temp_scores.index({'score': score}) + 1
        
        # Draw rank with arcade cabinet style
        rank_bg = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 90, 200, 40)
        pygame.draw.rect(screen, (40, 40, 60), rank_bg)
        pygame.draw.rect(screen, ORANGE, rank_bg, 2)
        
        rank_text = SUBTITLE_FONT.render(f"RANK: {rank}", True, ORANGE)
        screen.blit(rank_text, ((WIDTH - rank_text.get_width()) // 2, HEIGHT // 2 + 100))
        
        # Draw decorative arcade elements
        pygame.draw.line(screen, CYAN, (100, HEIGHT//2 - 120), (WIDTH - 100, HEIGHT//2 - 120), 2)
        pygame.draw.line(screen, CYAN, (100, HEIGHT//2 + 150), (WIDTH - 100, HEIGHT//2 + 150), 2)
    elif game_paused:
        # Display pause message
        pause_font = pygame.font.SysFont("comicsansms", 50)
        pause_text = pause_font.render("GAME PAUSED", True, ORANGE)
        resume_text = pygame.font.SysFont("comicsansms", 30).render("Press P to Resume or ESC to Unpause", True, WHITE)
        screen.blit(pause_text, ((WIDTH - pause_text.get_width()) // 2, HEIGHT // 2 - 30))
        screen.blit(resume_text, ((WIDTH - resume_text.get_width()) // 2, HEIGHT // 2 + 30))
    elif not game_started:
        # Update ball position to follow paddle
        ball_x = paddle_x + PADDLE_WIDTH // 2
        ball_y = paddle_y - BALL_RADIUS
        show_press_space_message()
        
        # Display high scores hint
        high_scores_hint = pygame.font.SysFont("comicsansms", 24).render("Press H to view High Scores", True, YELLOW)
        screen.blit(high_scores_hint, ((WIDTH - high_scores_hint.get_width()) // 2, HEIGHT // 2 + 50))
        
        # Allow paddle movement before game starts
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += paddle_speed
    else:
        # Only process game logic if not paused
        if not game_paused:
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
            
        # Top border collision - fix to prevent ball from disappearing
        if ball_y - BALL_RADIUS <= 50:  # Use 50 instead of 0 to account for the top UI panel
            ball_y = 50 + BALL_RADIUS
            ball_dy = -ball_dy
            
            # Add visual feedback for top collision
            pygame.draw.line(screen, CYAN, (ball_x - 20, 50), (ball_x + 20, 50), 3)
            pygame.display.update(pygame.Rect(ball_x - 20, 48, 40, 5))

        # Create a ball rect for collision detection
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)
        
        # Ball collision with paddle - with arcade-style effects
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
            
            # Add paddle hit visual effects
            # Flash the paddle briefly
            pygame.draw.rect(screen, WHITE, paddle_rect)
            pygame.display.update(paddle_rect)
            
            # Draw impact particles
            for _ in range(10):
                particle_x = ball_x
                particle_y = paddle_y
                particle_size = random.randint(1, 3)
                particle_color = random.choice([CYAN, WHITE, YELLOW])
                pygame.draw.rect(screen, particle_color, 
                               (particle_x - particle_size//2, 
                                particle_y - particle_size//2, 
                                particle_size, particle_size))

        # Ball collision with obstacles
        check_obstacle_collision(ball_rect)

        # Check brick collision with arcade-style effects
        collision, bricks, score_bonus, ball_dx, ball_dy = check_brick_collision(ball_rect, bricks)
        if collision:
            score += score_bonus
            
            # Show score popup at collision point
            if score_bonus > 0:
                score_popup_font = REGULAR_FONT
                score_popup = score_popup_font.render(f"+{score_bonus}", True, YELLOW)
                screen.blit(score_popup, (ball_x - score_popup.get_width()//2, ball_y - 30))
                pygame.display.update(pygame.Rect(ball_x - score_popup.get_width()//2, 
                                                ball_y - 30, 
                                                score_popup.get_width(), 
                                                score_popup.get_height()))
                
                # Draw brick break particles
                for _ in range(15):
                    particle_x = ball_x + random.randint(-20, 20)
                    particle_y = ball_y + random.randint(-20, 20)
                    particle_size = random.randint(1, 4)
                    particle_color = random.choice([WHITE, YELLOW, ORANGE, RED])
                    pygame.draw.rect(screen, particle_color, 
                                   (particle_x - particle_size//2, 
                                    particle_y - particle_size//2, 
                                    particle_size, particle_size))
            
            # Check if level is complete (all breakable bricks destroyed)
            if check_level_complete(bricks):
                level += 1
                bricks = initialize_bricks(level)
                obstacles = initialize_obstacles(level)
                reset_ball()
                # Show level up message
                font = pygame.font.SysFont("comicsansms", 50)
                text = font.render(f"Level {level}!", True, GREEN)
                screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.delay(1000)  # Pause for a second

        # Ball falls below screen - lose a life
        if ball_y + BALL_RADIUS >= HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
                # Save high score when game is over
                save_high_score(current_game_id, score, difficulty)
            else:
                # Show life lost message with arcade style
                # Flash screen red
                flash = pygame.Surface((WIDTH, HEIGHT))
                flash.fill(RED)
                for alpha in range(100, 0, -20):  # Fade out
                    flash.set_alpha(alpha)
                    screen.blit(flash, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(30)
                
                # Draw life lost message
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))
                screen.blit(overlay, (0, 0))
                
                # Draw warning text with flashing effect
                for i in range(3):  # Flash 3 times
                    text = SUBTITLE_FONT.render("BALL LOST", True, RED)
                    screen.blit(text, ((WIDTH - text.get_width()) // 2, HEIGHT // 2 - 20))
                    
                    lives_text = REGULAR_FONT.render(f"LIVES REMAINING: {lives}", True, YELLOW)
                    screen.blit(lives_text, ((WIDTH - lives_text.get_width()) // 2, HEIGHT // 2 + 20))
                    
                    pygame.display.flip()
                    pygame.time.delay(200)
                    
                    # Clear and redraw background
                    screen.blit(overlay, (0, 0))
                    pygame.display.flip()
                    pygame.time.delay(200)
                reset_ball()

        # Show hint if ball not launched
        if ball_dx == 0 and ball_dy == 0 and not game_over:
            hint_font = pygame.font.SysFont("comicsansms", 20)
            hint_text = hint_font.render("Press SPACE to launch ball", True, ORANGE)
            screen.blit(hint_text, ((WIDTH - hint_text.get_width()) // 2, HEIGHT // 2 + 50))

    # Apply scanlines for retro effect
    screen.blit(scanlines, (0, 0))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()