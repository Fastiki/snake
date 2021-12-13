import pygame
import random
from typing import Optional, List, Tuple

TILE_SIZE = 40


# TODO: Spielklassen


class Item:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    def occupies(self, x: int, y: int) -> bool:
        if self._x == x and self._y == y:
            return True
        else:
            return False

    def get_position(self) -> tuple:
        return self._x, self._y


class Brick(Item):
    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(
            (0, 0, 150),
            pygame.Rect(
                self._x * TILE_SIZE,
                self._y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
        )


class Snake:
    def __init__(self, x: int, y: int) -> None:
        self._occupies = [(x, y)]
        self._direction = (1, 0)
        self._grow: int = 0
        self.grow(2)
        self._last_direction = self._direction

    def get_head(self) -> tuple:
        return self._occupies[0]

    def occupies(self, x: int, y: int):
        for a, b in self._occupies:
            if (a, b) == (x, y):
                return True
            else:
                return False

    def draw(self, surface: pygame.Surface) -> None:
        for a, b in self._occupies:
            pygame.draw.rect(
                surface,
                (0, 255, 0),
                pygame.Rect(
                    a * TILE_SIZE,
                    b * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                ),
                12,
                10,
            )

    def set_direction(self, direction: str) -> None:
        if direction == 'left':
            if not self._direction == (1, 0):
                self._direction = (-1, 0)

        elif direction == 'right':
            if not self._direction == (-1, 0):
                self._direction = (1, 0)

        elif direction == 'up':
            if not self._direction == (0, 1):
                self._direction = (0, -1)

        elif direction == 'down':
            if not self._direction == (0, -1):
                self._direction = (0, 1)

    def grow(self, grow: int) -> None:
        self._grow += grow

    def step(self, forbidden: list) -> bool:
        head = self.get_head()
        move_position = (head[0] + self._direction[0], head[1] + self._direction[1])

        # Checks if the field is allready occupied by items
        for i in forbidden:
            if move_position == i:
                return False

        # Checks if the field is allready occupied by itself
        for i in self._occupies:
            if move_position == i:
                return False

        # Adding new postion to snake
        self._occupies.insert(0, move_position)

        # Grow control
        if self._grow > 0:
            self._grow -= 1
        else:
            self._occupies.pop()

        return True


class Cherry(Item):
    def __init__(self):
        super().__init__(0, 0)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.ellipse(
            surface,
            (255, 0, 0),
            pygame.Rect(
                self._x * TILE_SIZE,
                self._y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            )
        )

    def move(self, forbidden: list, width: int, height: int, snake: Snake, surface: pygame.Surface) -> None:
        while True:
            field = (random.randrange(1, width - 1), random.randrange(1, height - 2))
            a = False
            b = False

            if snake.occupies(field[0], field[1]):
                a = True

            for i in forbidden:
                if field == i:
                    b = True

            if not (a or b):
                break

        self._x = field[0]
        self._y = field[1]

        self.draw(surface)


def main():
    width = 25
    height = 20
    speed = 7

    pygame.init()
    screen = pygame.display.set_mode((
        TILE_SIZE * width,
        TILE_SIZE * height
    ))

    clock = pygame.time.Clock()

    wall = []
    for x in range(width):
        wall.append((x, 0))

    for x in range(width):
        wall.append((x, height - 1))

    for x in range(height):
        wall.append((0, x))

    for x in range(height):
        wall.append((width - 1, x))

    # Initialise Snake
    snake = Snake(width // 2, height // 2)

    # Initialise Cherry
    cherry = Cherry()
    cherry.move(wall, width, height, snake, screen)
    cherry.move(wall, width, height, snake, screen)

    running = True
    while running:
        screen.fill((20, 20, 20))

        for a, b in wall:
            Brick(a, b).draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Spiel beenden
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake.set_direction('left')

                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake.set_direction('right')

                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake.set_direction('up')

                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake.set_direction('down')

                elif event.key == pygame.K_ESCAPE:
                    running = False

        if not running:
            break

        if not snake.step(wall):
            break

        snake.draw(screen)

        if snake.get_head() == cherry.get_position():
            cherry.move(wall, width, height, snake, screen)
            snake.grow(2)

        cherry.draw(screen)

        pygame.display.flip()
        clock.tick(speed)

    pygame.display.quit()
    pygame.quit()


if __name__ == '__main__':
    main()
