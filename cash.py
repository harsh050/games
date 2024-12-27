import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tactical Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Grid settings
GRID_SIZE = 5
CELL_SIZE = WIDTH // GRID_SIZE

# Game state
grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
turn = "Player1"  # Alternates between "Player1" and "Player2"

# Unit class
class Unit:
    def __init__(self, x, y, color, health=100, attack=20, range=1):
        self.x = x
        self.y = y
        self.color = color
        self.health = health
        self.attack = attack
        self.range = range

    def draw(self):
        pygame.draw.circle(
            screen,
            self.color,
            (self.x * CELL_SIZE + CELL_SIZE // 2, self.y * CELL_SIZE + CELL_SIZE // 2),
            CELL_SIZE // 3,
        )

    def move(self, new_x, new_y):
        self.x, self.y = new_x, new_y

    def attack_unit(self, target):
        target.health -= self.attack


# Initialize units
player1_unit = Unit(0, 0, BLUE)
player2_unit = Unit(GRID_SIZE - 1, GRID_SIZE - 1, RED)
grid[0][0] = player1_unit
grid[GRID_SIZE - 1][GRID_SIZE - 1] = player2_unit

# Game loop
clock = pygame.time.Clock()
running = True
selected_unit = None

while running:
    screen.fill(WHITE)

    # Draw grid
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)

    # Draw units
    for row in grid:
        for cell in row:
            if cell:
                cell.draw()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get clicked cell
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x, grid_y = mouse_x // CELL_SIZE, mouse_y // CELL_SIZE

            if selected_unit:
                # Move unit if the cell is empty
                if grid[grid_x][grid_y] is None:
                    grid[selected_unit.x][selected_unit.y] = None
                    selected_unit.move(grid_x, grid_y)
                    grid[grid_x][grid_y] = selected_unit
                    selected_unit = None
                    turn = "Player2" if turn == "Player1" else "Player1"

                # Attack if an opponent is in the cell
                elif grid[grid_x][grid_y] and grid[grid_x][grid_y].color != selected_unit.color:
                    selected_unit.attack_unit(grid[grid_x][grid_y])
                    if grid[grid_x][grid_y].health <= 0:
                        grid[grid_x][grid_y] = None
                    selected_unit = None
                    turn = "Player2" if turn == "Player1" else "Player1"

            else:
                # Select a unit if it's the player's turn
                if grid[grid_x][grid_y]:
                    if (turn == "Player1" and grid[grid_x][grid_y].color == BLUE) or \
                       (turn == "Player2" and grid[grid_x][grid_y].color == RED):
                        selected_unit = grid[grid_x][grid_y]

    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
