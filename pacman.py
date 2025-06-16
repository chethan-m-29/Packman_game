import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Colors
black = (0, 0, 0)
blue = (0, 0, 255)  # Changed yellow to blue
white = (255, 255, 255)
red = (255, 0, 0)

# Pac-Man settings
pacman_radius = 20
pacman_speed = 5
mouth_angle = 30
mouth_opening = True
lives = 3
score = 0

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pac-Man Game')

# Initial position and direction
pacman_x = screen_width // 2
pacman_y = screen_height // 2
direction = 'RIGHT'

# Food settings
food_radius = 5
food_spacing = 50
food_positions = [(x, y) for x in range(food_spacing // 2, screen_width, food_spacing) 
                         for y in range(food_spacing // 2, screen_height, food_spacing)]

# Font for score and lives
font = pygame.font.Font(None, 36)

# Function to display the game over screen
def game_over_screen():
    game_over_font = pygame.font.Font(None, 74)
    game_over_text = game_over_font.render('GAME OVER', True, red)
    score_text = font.render(f'Final Score: {score}', True, white)

    screen.fill(black)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + game_over_text.get_height()))

    pygame.display.flip()

    pygame.time.wait(3000)  # Wait for 3 seconds before closing

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        direction = 'LEFT'
        pacman_x -= pacman_speed
    if keys[pygame.K_RIGHT]:
        direction = 'RIGHT'
        pacman_x += pacman_speed
    if keys[pygame.K_UP]:
        direction = 'UP'
        pacman_y -= pacman_speed
    if keys[pygame.K_DOWN]:
        direction = 'DOWN'
        pacman_y += pacman_speed

    # Check for border collision
    if pacman_x - pacman_radius < 0 or pacman_x + pacman_radius > screen_width or pacman_y - pacman_radius < 0 or pacman_y + pacman_radius > screen_height:
        lives -= 1
        # Reset Pac-Man position to center
        pacman_x = screen_width // 2
        pacman_y = screen_height // 2
        if lives <= 0:
            running = False

    # Check for collisions with food
    pacman_rect = pygame.Rect(pacman_x - pacman_radius, pacman_y - pacman_radius, pacman_radius * 2, pacman_radius * 2)
    new_food_positions = []
    for pos in food_positions:
        if not pacman_rect.collidepoint(pos):
            new_food_positions.append(pos)
        else:
            score += 10
    food_positions = new_food_positions

    # Clear the screen
    screen.fill(black)

    # Draw Pac-Man with chomping effect
    if mouth_opening:
        mouth_angle += 1
        if mouth_angle >= 45:
            mouth_opening = False
    else:
        mouth_angle -= 1
        if mouth_angle <= 0:
            mouth_opening = True

    if direction == 'RIGHT':
        pacman_mouth_pos = [(pacman_x, pacman_y), (pacman_x + pacman_radius, pacman_y - mouth_angle), (pacman_x + pacman_radius, pacman_y + mouth_angle)]
    elif direction == 'LEFT':
        pacman_mouth_pos = [(pacman_x, pacman_y), (pacman_x - pacman_radius, pacman_y - mouth_angle), (pacman_x - pacman_radius, pacman_y + mouth_angle)]
    elif direction == 'UP':
        pacman_mouth_pos = [(pacman_x, pacman_y), (pacman_x - mouth_angle, pacman_y - pacman_radius), (pacman_x + mouth_angle, pacman_y - pacman_radius)]
    else:  # DOWN
        pacman_mouth_pos = [(pacman_x, pacman_y), (pacman_x - mouth_angle, pacman_y + pacman_radius), (pacman_x + mouth_angle, pacman_y + pacman_radius)]

    pygame.draw.circle(screen, blue, (pacman_x, pacman_y), pacman_radius)  # Changed to blue
    pygame.draw.polygon(screen, black, pacman_mouth_pos)

    # Draw food
    for food_pos in food_positions:
        pygame.draw.circle(screen, white, food_pos, food_radius)
   
    # Draw score and lives
    score_text = font.render(f'Score: {score}', True, white)
    lives_text = font.render(f'Lives: {lives}', True, white)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (screen_width - 120, 10))

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(30)

# Display game over screen
game_over_screen()

# Quit pygame
pygame.quit()
sys.exit()
