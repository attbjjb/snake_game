import pygame
import random
import sys

pygame.init()

CELL_SIZE = 20
GRID_WIDTH = 32
GRID_HEIGHT = 24
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
BACKGROUND_COLOR = (0, 0, 0)

SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class GameObject:
    def __init__(self, position=None, body_color=None):
        self.position = position or (0, 0)
        self.body_color = body_color or (255, 255, 255)
    
    def draw(self, surface):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()
    
    def randomize_position(self):
        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)
    
    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0],
            self.position[1],
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()
    
    def reset(self):
        start_x = (GRID_WIDTH // 2) * CELL_SIZE
        start_y = (GRID_HEIGHT // 2) * CELL_SIZE
        self.positions = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.length = 1
    
    def update_direction(self):
        if self.next_direction:
            opposite = [
                (UP, DOWN), (DOWN, UP),
                (LEFT, RIGHT), (RIGHT, LEFT)
            ]
            can_change = True
            for dir1, dir2 in opposite:
                if self.direction == dir1 and self.next_direction == dir2:
                    can_change = False
                    break
            if can_change:
                self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_x = (head_x + dir_x * CELL_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dir_y * CELL_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def get_head_position(self):
        return self.positions[0]
    
    def grow(self):
        self.length += 1
    
    def check_self_collision(self):
        head = self.get_head_position()
        return head in self.positions[1:]
    
    def draw(self, surface):
        for x, y in self.positions:
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)


def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона")
    snake = Snake()
    apple = Apple()
    clock = pygame.time.Clock()
    
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        
        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()
        
        if snake.check_self_collision():
            snake.reset()
        
        screen.fill(BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.flip()
        clock.tick(20)


if __name__ == "__main__":
    main()
