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
    SUBTITLE_FONT = pygame.font.SysFont("Press Start 2P", 26)  # Increased for readability
    REGULAR_FONT = pygame.font.SysFont("Press Start 2P", 20)  # Increased for readability
    SMALL_FONT = pygame.font.SysFont("Press Start 2P", 16)  # Increased for readability
except:
    # Fallback to default fonts with pixel-like appearance
    TITLE_FONT = pygame.font.Font(None, 74)
    SUBTITLE_FONT = pygame.font.Font(None, 40)  # Increased for readability
    REGULAR_FONT = pygame.font.Font(None, 30)  # Increased for readability
    SMALL_FONT = pygame.font.Font(None, 24)  # Increased for readability

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

# Function to show game manual (page 1 - Controls and Objective)
def show_game_manual_page1():
    manual_active = True
    
    # Animation variables
    title_glow = 0
    glow_direction = 1
    start_time = pygame.time.get_ticks()
    
    while manual_active:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        
        # Create a gradient background
        screen.fill(BACKGROUND_COLOR)
        
        # Draw a more modern frame with rounded corners
        # Outer frame (dark with glow)
        frame_color = (40, 40, 60)
        inner_color = (20, 20, 30)
        frame_rect = pygame.Rect(30, 30, WIDTH-60, HEIGHT-60)
        pygame.draw.rect(screen, frame_color, frame_rect, border_radius=15)
        
        # Inner frame (darker)
        inner_rect = pygame.Rect(40, 40, WIDTH-80, HEIGHT-80)
        pygame.draw.rect(screen, inner_color, inner_rect, border_radius=10)
        
        # Animated neon border with pulse effect
        glow_value = 128 + int(127 * math.sin(elapsed_time / 500))
        glow_color = (0, glow_value, glow_value)  # Cyan-ish glow
        pygame.draw.rect(screen, glow_color, inner_rect, 3, border_radius=10)
        
        # Draw header with background
        header_rect = pygame.Rect(60, 50, WIDTH-120, 50)
        pygame.draw.rect(screen, (60, 60, 100), header_rect, border_radius=10)
        
        # Draw title with shadow effect
        title_shadow = TITLE_FONT.render("GAME CONTROLS", True, (0, 0, 0))
        title_text = TITLE_FONT.render("GAME CONTROLS", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH//2, 75))
        screen.blit(title_shadow, (title_rect.x+2, title_rect.y+2))
        screen.blit(title_text, title_rect)
        
        # Page indicator
        page_text = SMALL_FONT.render("Page 1/3", True, WHITE)
        screen.blit(page_text, (WIDTH-120, 60))
        
        # Content sections with visual separation
        # Section 1: Objective
        section_y = 120
        section_rect = pygame.Rect(60, section_y-10, WIDTH-120, 80)
        pygame.draw.rect(screen, (50, 50, 70, 180), section_rect, border_radius=8)
        
        # Section header
        header_text = SUBTITLE_FONT.render("OBJECTIVE", True, GREEN)
        header_rect = header_text.get_rect(midtop=(WIDTH//2, section_y))
        screen.blit(header_text, header_rect)
        
        # Section content
        content_lines = [
            "• Break all bricks to advance levels",
            "• Get the highest score possible"
        ]
        
        line_y = section_y + 35
        for line in content_lines:
            line_text = REGULAR_FONT.render(line, True, WHITE)
            line_rect = line_text.get_rect(midtop=(WIDTH//2, line_y))
            screen.blit(line_text, line_rect)
            line_y += 30
        
        # Section 2: Controls
        section_y = 220
        section_rect = pygame.Rect(60, section_y-10, WIDTH-120, 160)
        pygame.draw.rect(screen, (50, 50, 70, 180), section_rect, border_radius=8)
        
        # Section header
        header_text = SUBTITLE_FONT.render("CONTROLS", True, GREEN)
        header_rect = header_text.get_rect(midtop=(WIDTH//2, section_y))
        screen.blit(header_text, header_rect)
        
        # Section content with icons
        control_lines = [
            ("LEFT/RIGHT or A/D", "Move paddle"),
            ("SPACE", "Launch ball"),
            ("P", "Pause game"),
            ("ESC", "Return to menu")
        ]
        
        line_y = section_y + 35
        for key, action in control_lines:
            # Key box with 3D effect
            key_text = REGULAR_FONT.render(key, True, YELLOW)
            key_width = key_text.get_width() + 20
            key_rect = pygame.Rect(WIDTH//2 - 150 - key_width//2, line_y-5, key_width, 30)
            
            # Draw key background with 3D effect
            pygame.draw.rect(screen, (80, 80, 100), key_rect, border_radius=5)
            pygame.draw.rect(screen, (100, 100, 120), key_rect, 2, border_radius=5)
            
            # Draw key text
            key_text_rect = key_text.get_rect(center=key_rect.center)
            screen.blit(key_text, key_text_rect)
            
            # Draw action text
            action_text = REGULAR_FONT.render(action, True, CYAN)
            action_rect = action_text.get_rect(midleft=(WIDTH//2 - 50, line_y + 10))
            screen.blit(action_text, action_rect)
            
            line_y += 30
        
        # Navigation hint with animation
        hint_alpha = 128 + int(127 * math.sin(elapsed_time / 300))
        hint_color = (0, 255, 0, hint_alpha)
        hint_text = SUBTITLE_FONT.render("PRESS SPACE FOR NEXT PAGE", True, hint_color)
        hint_rect = hint_text.get_rect(midbottom=(WIDTH//2, HEIGHT - 50))
        screen.blit(hint_text, hint_rect)
        
        # Apply subtle scanlines for retro effect
        screen.blit(scanlines, (0, 0))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return show_game_manual_page2()  # Go to page 2
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        # Control the animation speed
        pygame.time.delay(20)
    
    return False

# Function to show game manual (page 2 - Brick Types and Difficulty)
def show_game_manual_page2():
    manual_active = True
    
    # Animation variables
    start_time = pygame.time.get_ticks()
    
    while manual_active:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        
        # Create a gradient background
        screen.fill(BACKGROUND_COLOR)
        
        # Draw a more modern frame with rounded corners
        # Outer frame (dark with glow)
        frame_color = (40, 40, 60)
        inner_color = (20, 20, 30)
        frame_rect = pygame.Rect(30, 30, WIDTH-60, HEIGHT-60)
        pygame.draw.rect(screen, frame_color, frame_rect, border_radius=15)
        
        # Inner frame (darker)
        inner_rect = pygame.Rect(40, 40, WIDTH-80, HEIGHT-80)
        pygame.draw.rect(screen, inner_color, inner_rect, border_radius=10)
        
        # Animated neon border with pulse effect
        glow_value = 128 + int(127 * math.sin(elapsed_time / 500))
        glow_color = (0, glow_value, glow_value)  # Cyan-ish glow
        pygame.draw.rect(screen, glow_color, inner_rect, 3, border_radius=10)
        
        # Draw header with background
        header_rect = pygame.Rect(60, 50, WIDTH-120, 50)
        pygame.draw.rect(screen, (60, 60, 100), header_rect, border_radius=10)
        
        # Draw title with shadow effect
        title_shadow = TITLE_FONT.render("GAME ELEMENTS", True, (0, 0, 0))
        title_text = TITLE_FONT.render("GAME ELEMENTS", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH//2, 75))
        screen.blit(title_shadow, (title_rect.x+2, title_rect.y+2))
        screen.blit(title_text, title_rect)
        
        # Page indicator
        page_text = SMALL_FONT.render("Page 2/3", True, WHITE)
        screen.blit(page_text, (WIDTH-120, 60))
        
        # Section 1: Scoring
        section_y = 120
        section_rect = pygame.Rect(60, section_y-10, WIDTH-120, 100)
        pygame.draw.rect(screen, (50, 50, 70, 180), section_rect, border_radius=8)
        
        # Section header
        header_text = SUBTITLE_FONT.render("SCORING", True, GREEN)
        header_rect = header_text.get_rect(midtop=(WIDTH//2, section_y))
        screen.blit(header_text, header_rect)
        
        # Section content
        scoring_lines = [
            "• Bricks give points based on level",
            "• Level completion gives bonus points",
            "• Press H to view high scores"
        ]
        
        line_y = section_y + 35
        for line in scoring_lines:
            line_text = REGULAR_FONT.render(line, True, WHITE)
            line_rect = line_text.get_rect(midtop=(WIDTH//2, line_y))
            screen.blit(line_text, line_rect)
            line_y += 25
        
        # Section 2: Brick Types
        section_y = 230
        section_rect = pygame.Rect(60, section_y-10, WIDTH-120, 90)
        pygame.draw.rect(screen, (50, 50, 70, 180), section_rect, border_radius=8)
        
        # Section header
        header_text = SUBTITLE_FONT.render("BRICK TYPES", True, GREEN)
        header_rect = header_text.get_rect(midtop=(WIDTH//2, section_y))
        screen.blit(header_text, header_rect)
        
        # Draw brick examples with descriptions
        brick_types = [
            (BLUE, "Standard - Break in one hit"),
            (GRAY, "Unbreakable - Acts as obstacle")
        ]
        
        brick_y = section_y + 35
        for color, description in brick_types:
            # Draw brick example
            brick_rect = pygame.Rect(WIDTH//2 - 180, brick_y, 40, 20)
            pygame.draw.rect(screen, color, brick_rect)
            pygame.draw.rect(screen, WHITE, brick_rect, 1)  # White border
            
            # Draw description
            desc_text = REGULAR_FONT.render(description, True, CYAN)
            desc_rect = desc_text.get_rect(midleft=(WIDTH//2 - 130, brick_y + 10))
            screen.blit(desc_text, desc_rect)
            
            brick_y += 30
        
        # Section 3: Difficulty Levels
        section_y = 330
        section_rect = pygame.Rect(60, section_y-10, WIDTH-120, 120)
        pygame.draw.rect(screen, (50, 50, 70, 180), section_rect, border_radius=8)
        
        # Section header
        header_text = SUBTITLE_FONT.render("DIFFICULTY LEVELS", True, GREEN)
        header_rect = header_text.get_rect(midtop=(WIDTH//2, section_y))
        screen.blit(header_text, header_rect)
        
        # Difficulty descriptions with visual indicators
        difficulty_levels = [
            (GREEN, "EASY", "Slower ball, wider paddle"),
            (YELLOW, "NORMAL", "Balanced gameplay"),
            (RED, "HARD", "Faster ball, narrower paddle")
        ]
        
        diff_y = section_y + 35
        for color, level, description in difficulty_levels:
            # Draw difficulty indicator
            diff_rect = pygame.Rect(WIDTH//2 - 180, diff_y, 15, 15)
            pygame.draw.rect(screen, color, diff_rect, border_radius=7)
            
            # Draw level name
            level_text = REGULAR_FONT.render(level, True, color)
            level_rect = level_text.get_rect(midleft=(WIDTH//2 - 155, diff_y + 8))
            screen.blit(level_text, level_rect)
            
            # Draw description
            desc_text = REGULAR_FONT.render(description, True, WHITE)
            desc_rect = desc_text.get_rect(midleft=(WIDTH//2 - 70, diff_y + 8))
            screen.blit(desc_text, desc_rect)
            
            diff_y += 25
        
        # Navigation hint with animation
        hint_alpha = 128 + int(127 * math.sin(elapsed_time / 300))
        hint_color = (0, 255, 0, hint_alpha)
        hint_text = SUBTITLE_FONT.render("PRESS SPACE FOR NEXT PAGE", True, hint_color)
        hint_rect = hint_text.get_rect(midbottom=(WIDTH//2, HEIGHT - 50))
        screen.blit(hint_text, hint_rect)
        
        # Apply subtle scanlines for retro effect
        screen.blit(scanlines, (0, 0))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return show_game_manual_page3()  # Go to page 3
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        # Control the animation speed
        pygame.time.delay(20)
    
    return False

# Function to show game manual (page 3 - Tips and Power-ups)
def show_game_manual_page3():
    manual_active = True
    
    # Animation variables
    start_time = pygame.time.get_ticks()
    
    while manual_active:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        
        # Create a gradient background
        screen.fill(BACKGROUND_COLOR)
        
        # Draw a more modern frame with rounded corners
        # Outer frame (dark with glow)
        frame_color = (40, 40, 60)
        inner_color = (20, 20, 30)
        frame_rect = pygame.Rect(30, 30, WIDTH-60, HEIGHT-60)
        pygame.draw.rect(screen, frame_color, frame_rect, border_radius=15)
        
        # Inner frame (darker)
        inner_rect = pygame.Rect(40, 40, WIDTH-80, HEIGHT-80)
        pygame.draw.rect(screen, inner_color, inner_rect, border_radius=10)
        
        # Animated neon border with pulse effect
        glow_value = 128 + int(127 * math.sin(elapsed_time / 500))
        glow_color = (0, glow_value, glow_value)  # Cyan-ish glow
        pygame.draw.rect(screen, glow_color, inner_rect, 3, border_radius=10)
        
        # Draw header with background
        header_rect = pygame.Rect(60, 50, WIDTH-120, 50)
        pygame.draw.rect(screen, (60, 60, 100), header_rect, border_radius=10)
        
        # Draw title with shadow effect
        title_shadow = TITLE_FONT.render("POWER-UPS & TIPS", True, (0, 0, 0))
        title_text = TITLE_FONT.render("POWER-UPS & TIPS", True, YELLOW)
        title_rect = title_text.get_rect(center=(WIDTH//2, 75))
        screen.blit(title_shadow, (title_rect.x+2, title_rect.y+2))
        screen.blit(title_text, title_rect)
        
        # Page indicator
        page_text = SMALL_FONT.render("Page 3/3", True, WHITE)
        screen.blit(page_text, (WIDTH-120, 60))
        
        # Section 1: Basic Power-ups
        section_y = 120
        section_rect = pygame.Rect(60, section_y-10, WIDTH-120, 130)
        pygame.draw.rect(screen, (50, 50, 70, 180), section_rect, border_radius=8)
        
        # Section header
        header_text = SUBTITLE_FONT.render("POWER-UPS", True, GREEN)
        header_rect = header_text.get_rect(midtop=(WIDTH//2, section_y))
        screen.blit(header_text, header_rect)
        
        # Power-up examples with descriptions
        powerups = [
            (GREEN, "Extends paddle (12s)"),
            (RED, "Speeds up ball (10s)"),
            (BLUE, "Extra life (instant)"),
            (YELLOW, "Multi-ball (15s)"),
            (PURPLE, "Slows ball (10s)"),
            (CYAN, "Ghost ball (8s)"),
            ((255, 0, 255), "Magnetic paddle (10s)")
        ]
        
        powerup_y = section_y + 35
        for color, description in powerups:
            # Draw power-up example
            powerup_rect = pygame.Rect(WIDTH//2 - 180, powerup_y, 20, 20)
            pygame.draw.rect(screen, color, powerup_rect, border_radius=5)
            pygame.draw.rect(screen, WHITE, powerup_rect, 1, border_radius=5)  # White border
            
            # Draw description
            desc_text = REGULAR_FONT.render(description, True, WHITE)
            desc_rect = desc_text.get_rect(midleft=(WIDTH//2 - 150, powerup_y + 10))
            screen.blit(desc_text, desc_rect)
            
            powerup_y += 25
        
        # Section 2: Tips
        section_y = 260
        section_rect = pygame.Rect(60, section_y-10, WIDTH-120, 130)
        pygame.draw.rect(screen, (50, 50, 70, 180), section_rect, border_radius=8)
        
        # Section header
        header_text = SUBTITLE_FONT.render("TIPS & STRATEGIES", True, GREEN)
        header_rect = header_text.get_rect(midtop=(WIDTH//2, section_y))
        screen.blit(header_text, header_rect)
        
        # Tips with icons
        tips = [
            "Aim for brick corners for unpredictable bounces",
            "Use paddle edges to control ball direction",
            "Catch falling power-ups for advantages",
            "Clear a path to upper bricks early"
        ]
        
        tip_y = section_y + 35
        for i, tip in enumerate(tips):
            # Draw tip icon
            tip_icon_rect = pygame.Rect(WIDTH//2 - 180, tip_y, 15, 15)
            pygame.draw.rect(screen, YELLOW, tip_icon_rect, border_radius=7)
            pygame.draw.rect(screen, WHITE, tip_icon_rect, 1, border_radius=7)  # White border
            
            # Draw tip number
            num_text = SMALL_FONT.render(f"{i+1}", True, BLACK)
            num_rect = num_text.get_rect(center=tip_icon_rect.center)
            screen.blit(num_text, num_rect)
            
            # Draw tip text
            tip_text = REGULAR_FONT.render(tip, True, CYAN)
            tip_rect = tip_text.get_rect(midleft=(WIDTH//2 - 155, tip_y + 8))
            screen.blit(tip_text, tip_rect)
            
            tip_y += 25
        
        # Start button with animation
        button_pulse = 200 + int(55 * math.sin(elapsed_time / 200))
        button_color = (0, button_pulse, 0)
        button_rect = pygame.Rect(WIDTH//2 - 120, HEIGHT - 80, 240, 45)
        pygame.draw.rect(screen, button_color, button_rect, border_radius=25)
        pygame.draw.rect(screen, WHITE, button_rect, 2, border_radius=25)  # White border
        
        # Button text
        button_text = SUBTITLE_FONT.render("START GAME", True, WHITE)
        button_rect = button_text.get_rect(center=(WIDTH//2, HEIGHT - 58))
        screen.blit(button_text, button_rect)
        
        # Hint text
        hint_text = SMALL_FONT.render("PRESS SPACE TO BEGIN", True, WHITE)
        hint_rect = hint_text.get_rect(center=(WIDTH//2, HEIGHT - 25))
        screen.blit(hint_text, hint_rect)
        
        # Apply subtle scanlines for retro effect
        screen.blit(scanlines, (0, 0))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True  # Continue to game
                elif event.key == pygame.K_ESCAPE:
                    return False
        
        # Control the animation speed
        pygame.time.delay(20)
    
    return False

# Function to show game manual (wrapper function)
def show_game_manual():
    return show_game_manual_page1()  # Start with page 1, which links to pages 2 and 3

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
    # No randomly generated obstacles - obstacles should only be grey bricks from level files
    return []

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
                # Add small offset to prevent sticking
                ball_x = obstacle.right + BALL_RADIUS + 1 if min_overlap_side == 'left' else obstacle.left - BALL_RADIUS - 1
            else:
                # Vertical collision (top/bottom hit)
                ball_dy = -ball_dy
                # Add small offset to prevent sticking
                ball_y = obstacle.bottom + BALL_RADIUS + 1 if min_overlap_side == 'top' else obstacle.top - BALL_RADIUS - 1
            
            return True
    
    return False

def check_brick_collision(ball_rect, bricks):
    global ball_x, ball_y
    collision_occurred = False
    score_increment = 0
    new_ball_dx, new_ball_dy = ball_dx, ball_dy
    spawn_power_up = False
    power_up_position = (0, 0)

    for i, (brick, color, unbreakable) in enumerate(bricks[:]):
        if ball_rect.colliderect(brick):
            collision_occurred = True
            
            if not unbreakable:
                # Store brick position for potential power-up spawn
                power_up_position = (brick.x + brick.width // 2, brick.y + brick.height // 2)
                
                # Remove brick and add score
                bricks.pop(i)
                score_increment = 10 * level
                
                # Chance to spawn a power-up (1 in power_up_spawn_chance)
                if random.randint(1, power_up_spawn_chance) == 1:
                    spawn_power_up = True
            
            # Calculate overlaps for precise collision direction
            overlaps = {
                'left': brick.right - ball_rect.left,
                'right': ball_rect.right - brick.left,
                'top': brick.bottom - ball_rect.top,
                'bottom': ball_rect.bottom - brick.top
            }
            
            # Find the smallest overlap to determine collision side
            min_overlap_side = min(overlaps, key=overlaps.get)
            
            # Reflect ball based on collision side with small offset to prevent sticking
            if min_overlap_side in ['left', 'right']:
                # Horizontal collision (side hit)
                new_ball_dx = -ball_dx
                # Add a small offset to prevent sticking
                ball_x = brick.right + BALL_RADIUS + 1 if min_overlap_side == 'left' else brick.left - BALL_RADIUS - 1
            else:
                # Vertical collision (top/bottom hit)
                new_ball_dy = -ball_dy
                # Add a small offset to prevent sticking
                ball_y = brick.bottom + BALL_RADIUS + 1 if min_overlap_side == 'top' else brick.top - BALL_RADIUS - 1
            
            break  # Only handle one brick collision per frame
    
    return collision_occurred, bricks, score_increment, new_ball_dx, new_ball_dy, spawn_power_up, power_up_position

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

# Define additional colors
PURPLE = (128, 0, 255)

# Initialize particle system
particles = []

# Initialize power-up effect tracking
power_up_effects = {
    'extend': {'active': False, 'start_time': 0},
    'speed': {'active': False, 'start_time': 0},
    'life': {'active': False, 'start_time': 0},
    'multi': {'active': False, 'start_time': 0},
    'slow': {'active': False, 'start_time': 0},
    'ghost': {'active': False, 'start_time': 0},
    'magnet': {'active': False, 'start_time': 0}
}

# Initialize special ball states
ball_is_ghost = False
paddle_is_magnetic = False

# Power-up system
class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.width = 20
        self.height = 20
        self.active = False
        self.collected = False
        self.start_time = 0
        self.fall_speed = random.uniform(1.5, 3.0)  # Random fall speed for more dynamic gameplay
        self.wobble_amount = random.uniform(0.5, 1.5)  # Random wobble for visual interest
        self.wobble_speed = random.uniform(0.05, 0.1)  # Random wobble speed
        self.wobble_offset = random.uniform(0, 6.28)  # Random starting phase
        self.rotation = 0  # For rotating power-ups
        
        # Set properties based on power-up type
        if self.type == 'extend':  # Green - extend paddle
            self.duration = 12000  # 12 seconds
            self.color = GREEN
            self.shape = 'rect'  # Rectangle shape
            self.icon = '⬅➡'  # Directional arrows icon
        elif self.type == 'speed':  # Red - speed up ball
            self.duration = 10000  # 10 seconds
            self.color = RED
            self.shape = 'circle'  # Circle shape
            self.icon = '⚡'  # Lightning bolt icon
        elif self.type == 'life':  # Blue - extra life
            self.duration = 0  # Instant effect
            self.color = BLUE
            self.shape = 'heart'  # Heart shape
            self.icon = '♥'  # Heart icon
        elif self.type == 'multi':  # Yellow - multi-ball
            self.duration = 15000  # 15 seconds
            self.color = YELLOW
            self.shape = 'circle'  # Circle shape
            self.icon = '⚪'  # Circle icon
        elif self.type == 'slow':  # Purple - slow ball
            self.duration = 10000  # 10 seconds
            self.color = PURPLE
            self.shape = 'circle'  # Circle shape
            self.icon = '⏱'  # Clock icon
        elif self.type == 'ghost':  # Cyan - ghost ball (passes through bricks)
            self.duration = 8000  # 8 seconds
            self.color = CYAN
            self.shape = 'diamond'  # Diamond shape
            self.icon = '👻'  # Ghost icon
        elif self.type == 'magnet':  # Magenta - magnetic paddle
            self.duration = 10000  # 10 seconds
            self.color = (255, 0, 255)  # Magenta
            self.shape = 'rect'  # Rectangle shape
            self.icon = '🧲'  # Magnet icon
    
    def update(self, current_time):
        # Update position if not collected (falling)
        if not self.collected and not self.active:
            self.y += self.fall_speed
            # Add wobble effect while falling
            self.x += math.sin(current_time * self.wobble_speed + self.wobble_offset) * self.wobble_amount
            # Rotate the power-up
            self.rotation = (self.rotation + 2) % 360
        
        # For active power-ups with duration, check if they've expired
        if self.active and self.duration > 0:
            return current_time - self.start_time < self.duration
        return True  # Power-ups with no duration (like extra life) stay active
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        if not self.collected:
            # Create a surface for rotation
            power_up_surface = pygame.Surface((self.width + 6, self.height + 6), pygame.SRCALPHA)
            
            # Draw the power-up based on its shape
            if self.shape == 'rect':
                pygame.draw.rect(power_up_surface, self.color, (3, 3, self.width, self.height))
                pygame.draw.rect(power_up_surface, WHITE, (3, 3, self.width, self.height), 1)
            elif self.shape == 'circle':
                pygame.draw.circle(power_up_surface, self.color, (self.width//2 + 3, self.height//2 + 3), self.width//2)
                pygame.draw.circle(power_up_surface, WHITE, (self.width//2 + 3, self.height//2 + 3), self.width//2, 1)
            elif self.shape == 'diamond':
                points = [
                    (self.width//2 + 3, 3),  # Top
                    (self.width + 3, self.height//2 + 3),  # Right
                    (self.width//2 + 3, self.height + 3),  # Bottom
                    (3, self.height//2 + 3)  # Left
                ]
                pygame.draw.polygon(power_up_surface, self.color, points)
                pygame.draw.polygon(power_up_surface, WHITE, points, 1)
            elif self.shape == 'heart':
                # Draw a heart shape
                center_x, center_y = self.width//2 + 3, self.height//2 + 3
                radius = self.width//2 - 2
                
                # Draw two circles for the top of the heart
                pygame.draw.circle(power_up_surface, self.color, (center_x - radius//2, center_y - radius//2), radius//2)
                pygame.draw.circle(power_up_surface, self.color, (center_x + radius//2, center_y - radius//2), radius//2)
                
                # Draw a triangle for the bottom of the heart
                points = [
                    (center_x - radius, center_y - radius//2),
                    (center_x + radius, center_y - radius//2),
                    (center_x, center_y + radius)
                ]
                pygame.draw.polygon(power_up_surface, self.color, points)
                
                # Draw outline
                pygame.draw.circle(power_up_surface, WHITE, (center_x - radius//2, center_y - radius//2), radius//2, 1)
                pygame.draw.circle(power_up_surface, WHITE, (center_x + radius//2, center_y - radius//2), radius//2, 1)
                pygame.draw.polygon(power_up_surface, WHITE, points, 1)
            
            # Add a glow effect
            glow_alpha = 100 + int(50 * math.sin(pygame.time.get_ticks() / 200))
            glow_surface = pygame.Surface((self.width + 12, self.height + 12), pygame.SRCALPHA)
            
            if self.shape == 'rect':
                pygame.draw.rect(glow_surface, (*self.color, glow_alpha), (3, 3, self.width + 6, self.height + 6))
            elif self.shape == 'circle':
                pygame.draw.circle(glow_surface, (*self.color, glow_alpha), (self.width//2 + 6, self.height//2 + 6), self.width//2 + 3)
            elif self.shape == 'diamond' or self.shape == 'heart':
                # Use a simple rect glow for complex shapes
                pygame.draw.rect(glow_surface, (*self.color, glow_alpha), (3, 3, self.width + 6, self.height + 6), border_radius=8)
            
            # Rotate the power-up
            rotated_surface = pygame.transform.rotate(power_up_surface, self.rotation)
            rotated_rect = rotated_surface.get_rect(center=(self.width//2 + 3, self.height//2 + 3))
            
            # Blit the glow and rotated power-up
            surface.blit(glow_surface, (self.x - 6, self.y - 6))
            surface.blit(rotated_surface, (self.x - rotated_rect.width//2 + self.width//2, self.y - rotated_rect.height//2 + self.height//2))

# Score popup system
class ScorePopup:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
        self.alpha = 255  # Full opacity
        self.timer = 0
        self.duration = 60  # Frames to display (60 frames = 1 second at 60 FPS)
        self.font = REGULAR_FONT
        self.color = YELLOW
        self.y_offset = 0  # For floating effect
    
    def update(self):
        self.timer += 1
        self.y_offset -= 0.5  # Float upward
        
        # Start fading out after 70% of duration
        if self.timer > self.duration * 0.7:
            fade_factor = 1 - ((self.timer - (self.duration * 0.7)) / (self.duration * 0.3))
            self.alpha = max(0, int(255 * fade_factor))
        
        return self.timer < self.duration
    
    def draw(self, surface):
        # Create text with current alpha
        text = self.font.render(f"+{self.value}", True, self.color)
        
        # Create a surface with per-pixel alpha
        text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)
        text_surface.fill((0, 0, 0, 0))  # Transparent background
        text_surface.blit(text, (0, 0))
        
        # Apply alpha to the entire surface
        text_surface.set_alpha(self.alpha)
        
        # Draw at position with floating effect
        surface.blit(text_surface, (self.x - text.get_width()//2, self.y - 30 + self.y_offset))

# Define power-up system functions
def apply_power_up_effect(power_up_type):
    global PADDLE_WIDTH, ball_dx, ball_dy, lives, original_paddle_width, max_lives, power_up_effects
    current_time = pygame.time.get_ticks()
    
    # Update the power-up effects dictionary
    power_up_effects[power_up_type] = {'active': True, 'start_time': current_time}
    
    # Play power-up sound effect
    # pygame.mixer.Sound('powerup.wav').play()  # Uncomment if sound file exists
    
    # Apply the specific power-up effect
    if power_up_type == 'extend':
        # Extend paddle
        PADDLE_WIDTH = original_paddle_width * 1.8  # Increased from 1.5 to 1.8
        # Create a visual effect at the paddle
        create_particle_effect(paddle_x + PADDLE_WIDTH//2, paddle_y, GREEN, 15)
        
    elif power_up_type == 'speed':
        # Speed up ball with better control
        current_speed = math.sqrt(ball_dx**2 + ball_dy**2)
        target_speed = current_speed * 1.4  # Increased from 1.3 to 1.4
        
        # Normalize the direction vector and apply the new speed
        if current_speed > 0:
            ball_dx = (ball_dx / current_speed) * target_speed
            ball_dy = (ball_dy / current_speed) * target_speed
        
        # Create a visual effect around the ball
        create_particle_effect(ball_x, ball_y, RED, 10)
        
    elif power_up_type == 'life':
        # Add extra life (up to max_lives) with visual feedback
        if lives < max_lives:
            lives += 1
            # Create a heart particle effect
            create_particle_effect(WIDTH//2, HEIGHT//2, BLUE, 20, 'heart')
        
    elif power_up_type == 'multi':
        # Create additional balls with improved mechanics
        global extra_balls
        
        # Limit the total number of balls to prevent glitching
        max_balls = 4  # Increased from 3 to 4 maximum balls
        current_ball_count = 1 + len(extra_balls)  # Main ball + existing extra balls
        
        # Only add new balls if we're under the limit
        balls_to_add = min(3, max_balls - current_ball_count)  # Increased from 2 to 3 potential new balls
        
        # Create additional balls with better spread of angles
        angle_offsets = [-30, 0, 30][:balls_to_add]  # Use only as many offsets as balls we need
        
        for angle_offset in angle_offsets:
            # Calculate new velocities based on current ball's speed and the offset angle
            current_speed = min(math.sqrt(ball_dx**2 + ball_dy**2), 6)  # Lower max speed to prevent glitches
            angle = math.degrees(math.atan2(ball_dx, -ball_dy))  # Convert current direction to angle
            new_angle = angle + angle_offset  # Add offset to create different trajectory
            
            # Convert back to velocity components
            new_dx = current_speed * math.sin(math.radians(new_angle))
            new_dy = -current_speed * math.cos(math.radians(new_angle))
            
            # Make sure the new ball is positioned slightly away from the main ball to prevent collision issues
            offset_x = 8 * math.sin(math.radians(new_angle))  # Increased from 5 to 8
            offset_y = 8 * math.cos(math.radians(new_angle))  # Increased from 5 to 8
            
            # Add the new ball to extra_balls list with a unique ID
            extra_balls.append({
                'x': ball_x + offset_x,
                'y': ball_y + offset_y,
                'dx': new_dx,
                'dy': new_dy,
                'active': True,
                'id': str(uuid.uuid4())[:8],  # Add unique ID to each ball
                'ghost': False  # Track if this ball has ghost power
            })
            
            # Create a burst effect at spawn point
            create_particle_effect(ball_x + offset_x, ball_y + offset_y, YELLOW, 8)
    
    elif power_up_type == 'slow':
        # Slow down ball for better control
        current_speed = math.sqrt(ball_dx**2 + ball_dy**2)
        target_speed = max(current_speed * 0.6, 3)  # Slow to 60% but maintain minimum speed
        
        # Normalize the direction vector and apply the new speed
        if current_speed > 0:
            ball_dx = (ball_dx / current_speed) * target_speed
            ball_dy = (ball_dy / current_speed) * target_speed
        
        # Apply to extra balls too
        for extra_ball in extra_balls:
            if extra_ball['active']:
                extra_speed = math.sqrt(extra_ball['dx']**2 + extra_ball['dy']**2)
                if extra_speed > 0:
                    slow_factor = 0.6
                    extra_ball['dx'] = (extra_ball['dx'] / extra_speed) * (extra_speed * slow_factor)
                    extra_ball['dy'] = (extra_ball['dy'] / extra_speed) * (extra_speed * slow_factor)
        
        # Create a visual effect
        create_particle_effect(ball_x, ball_y, PURPLE, 12, 'clock')
    
    elif power_up_type == 'ghost':
        # Ghost ball - passes through bricks without breaking them
        global ball_is_ghost
        ball_is_ghost = True
        
        # Apply to extra balls too
        for extra_ball in extra_balls:
            if extra_ball['active']:
                extra_ball['ghost'] = True
        
        # Create a visual effect
        create_particle_effect(ball_x, ball_y, CYAN, 15, 'ghost')
    
    elif power_up_type == 'magnet':
        # Magnetic paddle - attracts the ball slightly
        global paddle_is_magnetic
        paddle_is_magnetic = True
        
        # Create a visual effect
        create_particle_effect(paddle_x + PADDLE_WIDTH//2, paddle_y, (255, 0, 255), 12, 'magnet')

# Function to create particle effects for power-ups
def create_particle_effect(x, y, color, count, shape='circle'):
    global particles
    
    for _ in range(count):
        # Random velocity
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        velocity = [speed * math.cos(angle), speed * math.sin(angle)]
        
        # Random size
        size = random.randint(2, 6)
        
        # Random lifetime
        lifetime = random.randint(20, 40)
        
        # Add particle
        particles.append({
            'x': x,
            'y': y,
            'velocity': velocity,
            'color': color,
            'size': size,
            'lifetime': lifetime,
            'shape': shape
        })

def remove_power_up_effect(power_up_type):
    global PADDLE_WIDTH, ball_dx, ball_dy, original_paddle_width, extra_balls, ball_is_ghost, paddle_is_magnetic, power_up_effects
    
    # Update the power-up effects dictionary
    if power_up_type in power_up_effects:
        power_up_effects[power_up_type]['active'] = False
    
    # Remove the specific power-up effect
    if power_up_type == 'extend':
        PADDLE_WIDTH = original_paddle_width
        # Create a visual effect at the paddle
        create_particle_effect(paddle_x + PADDLE_WIDTH//2, paddle_y, (100, 150, 100), 5)
        
    elif power_up_type == 'speed':
        # Return ball to normal speed with smooth transition
        current_speed = math.sqrt(ball_dx**2 + ball_dy**2)
        target_speed = current_speed / 1.4
        
        # Normalize the direction vector and apply the new speed
        if current_speed > 0:
            ball_dx = (ball_dx / current_speed) * target_speed
            ball_dy = (ball_dy / current_speed) * target_speed
        
    elif power_up_type == 'multi':
        # Clear all extra balls when multi-ball power-up expires
        # Create a fade-out effect for each ball before clearing
        for extra_ball in extra_balls:
            if extra_ball['active']:
                create_particle_effect(extra_ball['x'], extra_ball['y'], (200, 200, 100), 8)
        
        extra_balls.clear()
    
    elif power_up_type == 'slow':
        # Return ball to normal speed
        current_speed = math.sqrt(ball_dx**2 + ball_dy**2)
        target_speed = current_speed / 0.6
        
        # Normalize the direction vector and apply the new speed
        if current_speed > 0:
            ball_dx = (ball_dx / current_speed) * target_speed
            ball_dy = (ball_dy / current_speed) * target_speed
        
        # Apply to extra balls too
        for extra_ball in extra_balls:
            if extra_ball['active']:
                extra_speed = math.sqrt(extra_ball['dx']**2 + extra_ball['dy']**2)
                if extra_speed > 0:
                    speed_factor = 1 / 0.6
                    extra_ball['dx'] = (extra_ball['dx'] / extra_speed) * (extra_speed * speed_factor)
                    extra_ball['dy'] = (extra_ball['dy'] / extra_speed) * (extra_speed * speed_factor)
    
    elif power_up_type == 'ghost':
        # Remove ghost ball effect
        ball_is_ghost = False
        
        # Remove from extra balls too
        for extra_ball in extra_balls:
            if extra_ball['active']:
                extra_ball['ghost'] = False
        
        # Create a visual effect
        create_particle_effect(ball_x, ball_y, (100, 200, 200), 8)
    
    elif power_up_type == 'magnet':
        # Remove magnetic paddle effect
        paddle_is_magnetic = False
        
        # Create a visual effect
        create_particle_effect(paddle_x + PADDLE_WIDTH//2, paddle_y, (150, 50, 150), 5)

# Main game loop
running = True
game_started = False
game_over = False
game_paused = False
current_game_id = None
showed_manual = False  # Track if we've shown the manual
extra_balls = []  # List to store additional balls for multi-ball power-up

# Show welcome screen first
running, current_game_id = show_welcome_screen()
if running:
    # Show game manual after welcome screen
    showed_manual = show_game_manual()
    if not showed_manual:
        running = False

selecting_difficulty = running
score = 0
level = 1
lives = 3
max_lives = 5  # Cap maximum lives at 5
selecting_difficulty = True  # New state for difficulty selection
viewing_high_scores = False

# Power-up variables
active_power_ups = []  # List to store active power-ups
power_up_types = ['extend', 'speed', 'life', 'multi']
power_up_spawn_chance = 15  # 1 in 15 chance to spawn a power-up
power_up_weights = {'extend': 30, 'speed': 30, 'life': 10, 'multi': 30}  # Lower chance for extra life
power_up_effects = {
    'extend': {'active': False, 'start_time': 0, 'duration': 10000},  # 10 seconds
    'speed': {'active': False, 'start_time': 0, 'duration': 8000},     # 8 seconds
    'life': {'active': False, 'start_time': 0, 'duration': 0},         # Instant
    'multi': {'active': False, 'start_time': 0, 'duration': 15000}     # 15 seconds
}

# Original paddle width to restore after power-up expires
original_paddle_width = PADDLE_WIDTH
original_ball_speed = 0  # Will be set when the game starts

# List to store active score popups
active_score_popups = []

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
                overlay.fill((0, 0, 0, 180))  # Semi-transparent black
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
    # Draw ball with glow effect
    for offset in range(3, 0, -1):
        glow_alpha = 40 + 20 * offset
        pygame.draw.circle(screen, (255, 255, 100, glow_alpha), 
                          (int(ball_x), int(ball_y)), BALL_RADIUS + offset, 1)
    
    pygame.draw.circle(screen, YELLOW, (int(ball_x), int(ball_y)), BALL_RADIUS)
    
    # Add a small highlight to the ball for 3D effect
    pygame.draw.circle(screen, WHITE, (int(ball_x - BALL_RADIUS/3), int(ball_y - BALL_RADIUS/3)), 
                      BALL_RADIUS//3)
    
    # Draw extra balls from multi-ball power-up
    for extra_ball in extra_balls:
        if extra_ball['active']:
            # Ensure ball coordinates are within screen bounds to prevent rendering glitches
            ball_x_pos = max(BALL_RADIUS, min(WIDTH - BALL_RADIUS, int(extra_ball['x'])))
            ball_y_pos = max(BALL_RADIUS + 50, min(HEIGHT - BALL_RADIUS, int(extra_ball['y'])))
            
            # Draw extra ball with subtle glow effect (reduced to prevent visual clutter)
            for offset in range(2, 0, -1):
                glow_alpha = 30 + 15 * offset
                pygame.draw.circle(screen, (255, 255, 100, glow_alpha), 
                                 (ball_x_pos, ball_y_pos), BALL_RADIUS + offset, 1)
            
            # Draw the extra ball
            pygame.draw.circle(screen, YELLOW, (ball_x_pos, ball_y_pos), BALL_RADIUS)
            
            # Add a small highlight to the extra ball for 3D effect
            pygame.draw.circle(screen, WHITE, 
                             (ball_x_pos - BALL_RADIUS//3, ball_y_pos - BALL_RADIUS//3), 
                             BALL_RADIUS//3)

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
        
        # Allow paddle movement before game starts with enhanced controls
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and paddle_x > 0:
            paddle_x -= paddle_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += paddle_speed
    else:
        # Only process game logic if not paused
        if not game_paused:
            # Paddle movement with enhanced controls
            keys = pygame.key.get_pressed()
            # Left movement with LEFT arrow or A key
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and paddle_x > 0:
                paddle_x -= paddle_speed
            # Right movement with RIGHT arrow or D key
            if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and paddle_x < WIDTH - PADDLE_WIDTH:
                paddle_x += paddle_speed

            # Ball movement
            if ball_dx != 0 or ball_dy != 0:  
                ball_x += ball_dx
                ball_y += ball_dy
                
                # Move extra balls if multi-ball power-up is active
                new_extra_balls = []
                
                # Process all balls but with controlled rendering and physics
                for extra_ball in extra_balls:
                    if extra_ball['active']:
                        # Move the extra ball with controlled speed
                        # Check if ball speed is too high and normalize it
                        current_speed = math.sqrt(extra_ball['dx']**2 + extra_ball['dy']**2)
                        if current_speed > 8:  # Reduced max speed for extra balls to prevent glitches
                            speed_factor = 8 / current_speed
                            extra_ball['dx'] *= speed_factor
                            extra_ball['dy'] *= speed_factor
                        
                        # Ensure minimum speed to prevent balls from getting stuck
                        if current_speed < 2:
                            speed_factor = 2 / current_speed if current_speed > 0 else 1
                            extra_ball['dx'] *= speed_factor
                            extra_ball['dy'] *= speed_factor
                            
                        # Apply movement
                        extra_ball['x'] += extra_ball['dx']
                        extra_ball['y'] += extra_ball['dy']
                        
                        # Handle collisions with screen borders for extra balls
                        if extra_ball['x'] - BALL_RADIUS <= 0:
                            extra_ball['x'] = BALL_RADIUS
                            extra_ball['dx'] = -extra_ball['dx']
                        elif extra_ball['x'] + BALL_RADIUS >= WIDTH:
                            extra_ball['x'] = WIDTH - BALL_RADIUS
                            extra_ball['dx'] = -extra_ball['dx']
                            
                        # Top border collision for extra balls
                        if extra_ball['y'] - BALL_RADIUS <= 50:
                            extra_ball['y'] = 50 + BALL_RADIUS
                            extra_ball['dy'] = -extra_ball['dy']
                            
                        # Create a rect for the extra ball for collision detection
                        extra_ball_rect = pygame.Rect(
                            extra_ball['x'] - BALL_RADIUS, 
                            extra_ball['y'] - BALL_RADIUS, 
                            BALL_RADIUS * 2, BALL_RADIUS * 2
                        )
                        
                        # Check paddle collision for extra balls
                        if extra_ball_rect.colliderect(paddle_rect) and extra_ball['dy'] > 0:
                            relative_intersect_x = (extra_ball['x'] - (paddle_x + PADDLE_WIDTH/2)) / (PADDLE_WIDTH/2)
                            bounce_angle = relative_intersect_x * 60
                            current_speed = math.sqrt(extra_ball['dx']**2 + extra_ball['dy']**2)
                            extra_ball['dx'] = current_speed * math.sin(math.radians(bounce_angle))
                            extra_ball['dy'] = -current_speed * math.cos(math.radians(bounce_angle))
                            # Add small offset to prevent sticking
                            extra_ball['y'] = paddle_y - BALL_RADIUS - 1
                        
                        # Check obstacle collision for extra balls
                        for obstacle, color in obstacles:
                            if extra_ball_rect.colliderect(obstacle):
                                # Calculate overlaps for precise collision direction
                                overlaps = {
                                    'left': obstacle.right - extra_ball_rect.left,
                                    'right': extra_ball_rect.right - obstacle.left,
                                    'top': obstacle.bottom - extra_ball_rect.top,
                                    'bottom': extra_ball_rect.bottom - obstacle.top
                                }
                                
                                # Find the smallest overlap to determine collision side
                                min_overlap_side = min(overlaps, key=overlaps.get)
                                
                                # Reflect ball based on collision side
                                if min_overlap_side in ['left', 'right']:
                                    # Horizontal collision (side hit)
                                    extra_ball['dx'] = -extra_ball['dx']
                                    # Add small offset to prevent sticking
                                    extra_ball['x'] = obstacle.right + BALL_RADIUS + 1 if min_overlap_side == 'left' else obstacle.left - BALL_RADIUS - 1
                                else:
                                    # Vertical collision (top/bottom hit)
                                    extra_ball['dy'] = -extra_ball['dy']
                                    # Add small offset to prevent sticking
                                    extra_ball['y'] = obstacle.bottom + BALL_RADIUS + 1 if min_overlap_side == 'top' else obstacle.top - BALL_RADIUS - 1
                        
                        # Check brick collision for extra balls
                        # Create a custom function to handle extra ball brick collisions
                        def check_extra_ball_brick_collision(ball_rect, extra_ball):
                            collision_occurred = False
                            score_increment = 0
                            spawn_power_up = False
                            power_up_position = (0, 0)
                            
                            for i, (brick, color, unbreakable) in enumerate(bricks[:]):
                                if ball_rect.colliderect(brick):
                                    collision_occurred = True
                                    
                                    if not unbreakable:
                                        # Store brick position for potential power-up spawn
                                        power_up_position = (brick.x + brick.width // 2, brick.y + brick.height // 2)
                                        
                                        # Remove brick and add score
                                        bricks.pop(i)
                                        score_increment = 10 * level
                                        
                                        # Chance to spawn a power-up (1 in power_up_spawn_chance)
                                        if random.randint(1, power_up_spawn_chance) == 1:
                                            spawn_power_up = True
                                    
                                    # Calculate overlaps for precise collision direction
                                    overlaps = {
                                        'left': brick.right - ball_rect.left,
                                        'right': ball_rect.right - brick.left,
                                        'top': brick.bottom - ball_rect.top,
                                        'bottom': ball_rect.bottom - brick.top
                                    }
                                    
                                    # Find the smallest overlap to determine collision side
                                    min_overlap_side = min(overlaps, key=overlaps.get)
                                    
                                    # Reflect ball based on collision side with small offset to prevent sticking
                                    if min_overlap_side in ['left', 'right']:
                                        # Horizontal collision (side hit)
                                        extra_ball['dx'] = -extra_ball['dx']
                                        # Add a small offset to prevent sticking
                                        extra_ball['x'] = brick.right + BALL_RADIUS + 1 if min_overlap_side == 'left' else brick.left - BALL_RADIUS - 1
                                    else:
                                        # Vertical collision (top/bottom hit)
                                        extra_ball['dy'] = -extra_ball['dy']
                                        # Add a small offset to prevent sticking
                                        extra_ball['y'] = brick.bottom + BALL_RADIUS + 1 if min_overlap_side == 'top' else brick.top - BALL_RADIUS - 1
                                    
                                    return collision_occurred, score_increment, spawn_power_up, power_up_position
                            
                            return False, 0, False, (0, 0)
                        
                        # Use the custom function for extra ball brick collisions
                        collision, score_bonus, spawn_power_up, power_up_position = check_extra_ball_brick_collision(extra_ball_rect, extra_ball)
                        if collision:
                            score += score_bonus
                            
                            # Create score popup at collision point
                            if score_bonus > 0:
                                active_score_popups.append(ScorePopup(score_bonus, extra_ball['x'], extra_ball['y']))
                        
                        # Check if extra ball falls below screen
                        if extra_ball['y'] + BALL_RADIUS < HEIGHT:
                            new_extra_balls.append(extra_ball)
                        # If an extra ball falls, we don't lose a life - it just disappears
                
                # Update the extra_balls list with only active balls
                extra_balls = new_extra_balls

        # Ball collision with screen borders
        if ball_x - BALL_RADIUS <= 0:  
            ball_x = BALL_RADIUS
            ball_dx = -ball_dx
        elif ball_x + BALL_RADIUS >= WIDTH:  
            ball_x = WIDTH - BALL_RADIUS
            ball_dx = -ball_dx

        if ball_y - BALL_RADIUS <= 50:  # Use 50 instead of 0 to account for the top UI panel
            ball_y = 50 + BALL_RADIUS
            ball_dy = -ball_dy

        # Create a ball rect for collision detection
        ball_rect = pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

        # Ball collision with paddle
        paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
        if ball_rect.colliderect(paddle_rect) and ball_dy > 0:
            relative_intersect_x = (ball_x - (paddle_x + PADDLE_WIDTH/2)) / (PADDLE_WIDTH/2)
            bounce_angle = relative_intersect_x * 60
            current_speed = math.sqrt(ball_dx**2 + ball_dy**2)
            ball_dx = current_speed * math.sin(math.radians(bounce_angle))
            ball_dy = -current_speed * math.cos(math.radians(bounce_angle))
            # Add small offset to prevent sticking
            ball_y = paddle_y - BALL_RADIUS - 1

        # Ball collision with obstacles
        check_obstacle_collision(ball_rect)

        # Ball collision with bricks
        collision, bricks, score_bonus, ball_dx, ball_dy, spawn_power_up, power_up_position = check_brick_collision(ball_rect, bricks)
        if collision:
            # If ghost ball is active, don't break the brick but still bounce
            if not ball_is_ghost or power_up_effects['ghost']['active'] == False:
                score += score_bonus
                active_score_popups.append(ScorePopup(score_bonus, power_up_position[0], power_up_position[1]))
                
                if spawn_power_up:
                    # Randomly choose a power-up type with weighted probabilities
                    power_up_types = ['extend', 'speed', 'life', 'multi', 'slow', 'ghost', 'magnet']
                    weights = [20, 20, 10, 15, 15, 10, 10]  # Adjust these weights to balance gameplay
                    power_up_type = random.choices(
                        population=power_up_types,
                        weights=weights,
                        k=1
                    )[0]
                    
                    # Create and add the power-up
                    new_power_up = PowerUp(power_up_position[0], power_up_position[1], power_up_type)
                    active_power_ups.append(new_power_up)
                
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
            # Check if there are any active extra balls from multi-ball power-up
            if extra_balls:
                # If we have extra balls, make one of them the main ball
                # Find the ball that's most centered on the screen to make it the main ball
                center_x = WIDTH / 2
                closest_ball_idx = 0
                closest_distance = abs(extra_balls[0]['x'] - center_x)
                
                for i in range(1, len(extra_balls)):
                    distance = abs(extra_balls[i]['x'] - center_x)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_ball_idx = i
                
                # Take the selected ball and make it the main ball
                new_main_ball = extra_balls.pop(closest_ball_idx)
                ball_x = new_main_ball['x']
                ball_y = new_main_ball['y']
                ball_dx = new_main_ball['dx']
                ball_dy = new_main_ball['dy']
                
                # Ensure the ball speed is reasonable
                current_speed = math.sqrt(ball_dx**2 + ball_dy**2)
                if current_speed > 10:
                    speed_factor = 10 / current_speed
                    ball_dx *= speed_factor
                    ball_dy *= speed_factor
                
                # Remove the multi-ball power-up effect but keep the balls
                for power_up in active_power_ups:
                    if power_up.type == 'multi' and power_up.active:
                        power_up.active = False
                        power_up_effects['multi']['active'] = False
            else:
                # No extra balls, lose a life
                lives -= 1
                # Remove all power-ups (both falling and active ones)
                for power_up in active_power_ups:
                    if power_up.active and power_up.duration > 0:
                        # Remove effect of active power-ups
                        remove_power_up_effect(power_up.type)
                
                # Clear all power-ups
                active_power_ups.clear()
                
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

    # Draw and update all active score popups
    if not game_paused:
        # Update and draw particles
        new_particles = []
        for particle in particles:
            # Update position
            particle['x'] += particle['velocity'][0]
            particle['y'] += particle['velocity'][1]
            
            # Decrease lifetime
            particle['lifetime'] -= 1
            
            # Keep particle if it's still alive
            if particle['lifetime'] > 0:
                # Calculate alpha based on remaining lifetime
                alpha = int(255 * (particle['lifetime'] / 40))
                
                # Draw particle based on its shape
                if particle['shape'] == 'circle':
                    pygame.draw.circle(screen, (*particle['color'], alpha), (int(particle['x']), int(particle['y'])), particle['size'])
                elif particle['shape'] == 'heart':
                    # Draw a simple heart shape
                    size = particle['size']
                    x, y = int(particle['x']), int(particle['y'])
                    pygame.draw.circle(screen, (*particle['color'], alpha), (x - size//2, y - size//2), size//2)
                    pygame.draw.circle(screen, (*particle['color'], alpha), (x + size//2, y - size//2), size//2)
                    points = [(x - size, y - size//2), (x + size, y - size//2), (x, y + size)]
                    pygame.draw.polygon(screen, (*particle['color'], alpha), points)
                elif particle['shape'] == 'ghost':
                    # Draw a simple ghost shape
                    size = particle['size']
                    pygame.draw.circle(screen, (*particle['color'], alpha), (int(particle['x']), int(particle['y'])), size)
                    pygame.draw.rect(screen, (*particle['color'], alpha), (int(particle['x']) - size, int(particle['y']), size*2, size))
                elif particle['shape'] == 'clock':
                    # Draw a clock shape
                    pygame.draw.circle(screen, (*particle['color'], alpha), (int(particle['x']), int(particle['y'])), particle['size'])
                    # Draw clock hands
                    center_x, center_y = int(particle['x']), int(particle['y'])
                    hand_length = particle['size'] * 0.7
                    pygame.draw.line(screen, (255, 255, 255, alpha), (center_x, center_y), 
                                    (center_x + hand_length * math.cos(particle['lifetime'] * 0.2), 
                                     center_y + hand_length * math.sin(particle['lifetime'] * 0.2)), 1)
                elif particle['shape'] == 'magnet':
                    # Draw a magnet shape
                    size = particle['size']
                    pygame.draw.rect(screen, (*particle['color'], alpha), (int(particle['x']) - size//2, int(particle['y']) - size, size, size*2))
                else:  # Default to square
                    pygame.draw.rect(screen, (*particle['color'], alpha), 
                                    (int(particle['x']) - particle['size']//2, 
                                     int(particle['y']) - particle['size']//2, 
                                     particle['size'], particle['size']))
                
                new_particles.append(particle)
        
        # Update particles list
        particles[:] = new_particles
        
        # Update and draw score popups
        new_active_popups = []
        for popup in active_score_popups:
            if popup.update():  # Returns False when popup expires
                popup.draw(screen)
                new_active_popups.append(popup)
        active_score_popups = new_active_popups
        
        # Draw and update power-ups
        current_time = pygame.time.get_ticks()
        new_active_power_ups = []
        
        for power_up in active_power_ups:
            if not power_up.collected:
                # Draw falling power-up
                power_up.y += 2  # Power-up falls down
                power_up.draw(screen)
                
                # Check if power-up is collected
                if pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT).colliderect(power_up.get_rect()):
                    power_up.collected = True
                    power_up.active = True
                    power_up.start_time = current_time
                    
                    # Apply power-up effect
                    apply_power_up_effect(power_up.type)
                
                # Remove power-ups that fall off screen
                if power_up.y < HEIGHT:
                    new_active_power_ups.append(power_up)
            else:
                # Update active power-up duration
                if power_up.update(current_time):
                    new_active_power_ups.append(power_up)
                else:
                    # Power-up expired, remove its effect
                    remove_power_up_effect(power_up.type)
        
        active_power_ups = new_active_power_ups
        
        # Draw active power-up timers at the bottom of the screen
        x_offset = 50
        for power_up in active_power_ups:
            if power_up.active and power_up.duration > 0:
                remaining = max(0, (power_up.duration - (current_time - power_up.start_time)) / 1000)
                if remaining > 0:
                    # Draw power-up icon
                    pygame.draw.rect(screen, power_up.color, (x_offset, HEIGHT - 30, 15, 15))
                    
                    # Draw timer text
                    timer_text = REGULAR_FONT.render(f"{remaining:.1f}s", True, WHITE)
                    screen.blit(timer_text, (x_offset + 20, HEIGHT - 28))
                    
                    x_offset += 80  # Space between power-up timers
    
    # Apply scanlines for retro effect
    screen.blit(scanlines, (0, 0))
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()