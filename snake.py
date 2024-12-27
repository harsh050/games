import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Snake settings
snake_block = 20
snake_speed = 15
snake = [(100, 50), (90, 50), (80, 50)]  # Initial snake body

# Food settings
food_x = random.randint(0, (WIDTH - snake_block) // snake_block) * snake_block
food_y = random.randint(0, (HEIGHT - snake_block) // snake_block) * snake_block

# Direction
direction = "RIGHT"
change_to = direction

# Score
score = 0


def draw_snake(snake_list):
    """Draw the snake on the screen."""
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], snake_block, snake_block])


def show_score():
    """Display the score on the screen."""
    font = pygame.font.SysFont("comicsansms", 20)
    value = font.render(f"Score: {score}", True, WHITE)
    screen.blit(value, [10, 10])


def game_over():
    """Display game over and exit."""
    font = pygame.font.SysFont("comicsansms", 35)
    message = font.render("Game Over!", True, RED)
    screen.fill(BLACK)
    screen.blit(message, [WIDTH // 3, HEIGHT // 3])
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()


# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Control snake with arrow keys
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                change_to = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                change_to = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                change_to = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                change_to = "RIGHT"

    direction = change_to

    # Update the snake's position
    head_x = snake[0][0]
    head_y = snake[0][1]

    if direction == "UP":
        head_y -= snake_block
    if direction == "DOWN":
        head_y += snake_block
    if direction == "LEFT":
        head_x -= snake_block
    if direction == "RIGHT":
        head_x += snake_block

    # Snake movement
    snake.insert(0, (head_x, head_y))

    # Check if the snake eats food
    if head_x == food_x and head_y == food_y:
        score += 10
        food_x = random.randint(0, (WIDTH - snake_block) // snake_block) * snake_block
        food_y = random.randint(0, (HEIGHT - snake_block) // snake_block) * snake_block
    else:
        snake.pop()  # Remove the last block if no food is eaten

    # Check for collisions
    if (
        head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT
        or (head_x, head_y) in snake[1:]
    ):
        game_over()

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, RED, [food_x, food_y, snake_block, snake_block])
    draw_snake(snake)
    show_score()

    # Update the screen
    pygame.display.flip()

    # Control the frame rate
    clock.tick(snake_speed)

pygame.quit()
sys.exit()
