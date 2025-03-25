import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Параметры игры
CELL_SIZE = 20
PACMAN_SPEED = 2
GHOST_SPEED = 1

# Создание лабиринта (упрощенный вариант)
maze = [
    "#######################",
    "#........#........#...#",
    "#.###.##.#.##.###.#.###",
    "#....................#",
    "#.##.#.#####.#.##.#.###",
    "#....#...#...#....#...#",
    "####.### # ###.#### # #",
    "#......# # #......# # #",
    "#.####.# # #.####.# # #",
    "#....................#",
    "#######################"
]

class Pacman:
    def __init__(self):
        self.x = CELL_SIZE * 1.5
        self.y = CELL_SIZE * 1.5
        self.radius = CELL_SIZE // 2
        self.speed = PACMAN_SPEED
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.mouth_angle = 0
        self.mouth_change = 5
        self.mouth_max = 45
        
    def move(self):
        # Проверка следующего направления
        new_x = self.x + self.next_direction[0] * self.speed
        new_y = self.y + self.next_direction[1] * self.speed
        if self.can_move(new_x, new_y):
            self.direction = self.next_direction
        else:
            self.next_direction = self.direction
            
        # Движение
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        if self.can_move(new_x, new_y):
            self.x = new_x
            self.y = new_y
            
        # Анимация рта
        self.mouth_angle += self.mouth_change
        if abs(self.mouth_angle) > self.mouth_max:
            self.mouth_change *= -1
            
    def can_move(self, x, y):
        # Проверка столкновений со стенами
        row = int(y // CELL_SIZE)
        col = int(x // CELL_SIZE)
        
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]):
            if maze[row][col] != '#':
                return True
        return False
        
    def draw(self):
        # Рисуем Pac-Man
        if self.direction == (0, -1):  # Вверх
            start_angle = 180 + self.mouth_angle
            end_angle = 180 - self.mouth_angle
        elif self.direction == (0, 1):  # Вниз
            start_angle = 0 + self.mouth_angle
            end_angle = 0 - self.mouth_angle
        elif self.direction == (-1, 0):  # Влево
            start_angle = 90 + self.mouth_angle
            end_angle = 90 - self.mouth_angle
        elif self.direction == (1, 0):  # Вправо
            start_angle = 270 + self.mouth_angle
            end_angle = 270 - self.mouth_angle
        else:
            start_angle = 45
            end_angle = 315
            
        pygame.draw.arc(screen, YELLOW, 
                       (self.x - self.radius, self.y - self.radius, 
                        self.radius * 2, self.radius * 2),
                       start_angle * 3.14 / 180, end_angle * 3.14 / 180, self.radius)
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

class Ghost:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color
        self.speed = GHOST_SPEED
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.radius = CELL_SIZE // 2
        
    def move(self):
        # Простое ИИ для призраков
        if random.random() < 0.02:  # 2% шанс изменить направление
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        
        # Проверка столкновений
        if not self.can_move(new_x, new_y):
            self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        else:
            self.x = new_x
            self.y = new_y
            
    def can_move(self, x, y):
        # Аналогично Pac-Man
        row = int(y // CELL_SIZE)
        col = int(x // CELL_SIZE)
        
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]):
            if maze[row][col] != '#':
                return True
        return False
        
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        # Глаза
        pygame.draw.circle(screen, WHITE, (int(self.x - 5), int(self.y - 5)), 5)
        pygame.draw.circle(screen, WHITE, (int(self.x + 5), int(self.y - 5)), 5)
        pygame.draw.circle(screen, BLACK, (int(self.x - 5), int(self.y - 5)), 2)
        pygame.draw.circle(screen, BLACK, (int(self.x + 5), int(self.y - 5)), 2)

class Pellet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 3
        self.eaten = False
        
    def draw(self):
        if not self.eaten:
            pygame.draw.circle(screen, WHITE, (self.x, self.y), self.radius)

def create_pellets():
    pellets = []
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == '.':
                x = col * CELL_SIZE + CELL_SIZE // 2
                y = row * CELL_SIZE + CELL_SIZE // 2
                pellets.append(Pellet(x, y))
    return pellets

def draw_maze():
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == '#':
                pygame.draw.rect(screen, BLUE, 
                                (col * CELL_SIZE, row * CELL_SIZE, 
                                 CELL_SIZE, CELL_SIZE))

def main():
    clock = pygame.time.Clock()
    pacman = Pacman()
    ghosts = [
        Ghost(RED, CELL_SIZE * 9.5, CELL_SIZE * 7.5),
        Ghost(WHITE, CELL_SIZE * 10.5, CELL_SIZE * 7.5),
        Ghost((255, 192, 203), CELL_SIZE * 11.5, CELL_SIZE * 7.5)  # Розовый
    ]
    pellets = create_pellets()
    score = 0
    font = pygame.font.SysFont(None, 36)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pacman.next_direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    pacman.next_direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    pacman.next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    pacman.next_direction = (1, 0)
                    
        # Обновление объектов
        pacman.move()
        for ghost in ghosts:
            ghost.move()
            
        # Проверка столкновений с точками
        for pellet in pellets:
            if not pellet.eaten:
                dist = ((pacman.x - pellet.x) ** 2 + (pacman.y - pellet.y) ** 2) ** 0.5
                if dist < pacman.radius + pellet.radius:
                    pellet.eaten = True
                    score += 10
                    
        # Проверка столкновений с призраками
        for ghost in ghosts:
            dist = ((pacman.x - ghost.x) ** 2 + (pacman.y - ghost.y) ** 2) ** 0.5
            if dist < pacman.radius + ghost.radius:
                print("Game Over! Score:", score)
                running = False
                
        # Проверка победы
        if all(pellet.eaten for pellet in pellets):
            print("You Win! Score:", score)
            running = False
            
        # Отрисовка
        screen.fill(BLACK)
        draw_maze()
        for pellet in pellets:
            pellet.draw()
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()
            
        # Отрисовка счета
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()