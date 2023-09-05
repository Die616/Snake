import os
import pygame
import random

# Iniciar pygame
pygame.init()

font = pygame.font.Font(None, 36)

# Configuración de la ventana
w_screen = 640
l_screen = 480
screen = pygame.display.set_mode((w_screen, l_screen))
pygame.display.set_caption("Snake")

tile = 20

speed_x = 0
speed_y = 0

clock = pygame.time.Clock()

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
data_folder_path = os.path.join(script_dir, "data", "score")


def play_music(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

# Grid para debug
def grid():
    for x in range(0, w_screen, tile):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, l_screen))
    for y in range(0, l_screen, tile):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (w_screen, y))

# Pantalla de inicio
def start_screen():
    play_music(start_music_path)
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return
        screen.blit(start_screen_path, (0,0))
        pygame.display.flip()
        clock.tick(10)

# Dibujar en pantalla
def draw_elements(screen, background_img, food_img, food_x, food_y, snake_coords, snake, font, score):
    screen.blit(background_img, (0, 0))
    screen.blit(food_img, (food_x, food_y))

    snake = [SnakeSegment(coord[0], coord[1], is_head=(i==0))for i, coord in enumerate(snake_coords)]
    for segment in snake:
        screen.blit(segment.image, segment.rect)

    # ***Funcion solamente para debug***
    #grid()        
    
    # Score Draw
    score_text = font.render("Score: {}".format(score), True, (255, 255, 255))
    high_score_text = font.render("High Score: {}".format(load_score()), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))

    pygame.display.flip()

# Detectar si comio
def handle_food_events(x, y, food_x, food_y, score, snake_coords):
    if x == food_x and y == food_y:
        score += 1
        food_x = round(random.randint(0, w_screen - tile) / tile) * tile
        food_y = round(random.randint(0, l_screen - tile) / tile) * tile
        eat_sound.play()
    else:
        snake_coords.pop()
    return food_x, food_y, score

# Detectar eventos
def handle_events():
    global speed_x, speed_y
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and speed_y != tile:
                    speed_x = 0
                    speed_y = -tile
                elif event.key == pygame.K_DOWN and speed_y != -tile:
                    speed_x = 0
                    speed_y = tile
                elif event.key == pygame.K_LEFT and speed_x != tile:
                    speed_x = -tile
                    speed_y = 0
                elif event.key == pygame.K_RIGHT and speed_x != -tile:
                    speed_x = tile
                    speed_y = 0
    return False

# Movimiento de la serpiente
def move_snake(x , y, speed_x, speed_y, snake_coords):
    x += speed_x
    y += speed_y
    snake_coords.insert(0, (x, y))
    return x, y, snake_coords

# Coliciones
def check_colitions(x, y, w_screen, l_screen, snake_coords, gameover_sound_played):
    end_game = False

    if x >= w_screen or x < 0 or y >= l_screen or y < 0:
            if not gameover_sound_played:
                pygame.mixer.music.stop()
                No_sound.play()
                pygame.time.delay(1000)
                gameover_sound.play()
                gameover_sound_played = True
                pygame.time.delay(6000)
            end_game = True

    if (x, y) in snake_coords[1:]:
            if not gameover_sound_played:
                pygame.mixer.music.stop()
                No_sound.play()
                pygame.time.delay(1000)
                gameover_sound.play()
                gameover_sound_played = True
                pygame.time.delay(6000)
            end_game = True
    return end_game, gameover_sound_played

# Snake
class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, x, y, is_head=False):
        super().__init__()
        if is_head:
            image_path = os.path.join("data", "img", "head.png")
        else:
            image_path = os.path.join("data", "img", "snake.png")
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tile, tile))
        self.rect = self.image.get_rect(topleft = (x, y))

# Crear documento score
def create_score_file():
    score_file_path = os.path.join(data_folder_path, "Score.txt")
    try:
        with open(score_file_path, "x") as file:
            file.write("0")
    except FileExistsError:
        pass

# Guarda el score mas alto
def save_score(score):
    high_score = load_score()
    if score > high_score:
        score_file_path = os.path.join(data_folder_path, "Score.txt")
        with open(score_file_path, "w") as file:
            file.write(str(score))

# Carga documento score
def load_score():
    score_file_path = os.path.join(data_folder_path, "Score.txt")
    try:
        with open(score_file_path, "r") as file:
            return int(file.read())
    except FileExistsError:
        return 0

# Creamos el documento
create_score_file()


# Start Screen
start_screen_path = os.path.join("data", "img", "start_screen.png")
start_screen_path = pygame.image.load(start_screen_path).convert()
start_screen_path = pygame.transform.scale(start_screen_path, (w_screen, l_screen))
start_music_path = os.path.join("data", "ost", "StartScreen.mp3")

# Background
background_path = os.path.join("data", "img", "background.png")
background_img = pygame.image.load(background_path).convert()
background_img = pygame.transform.scale(background_img, (w_screen, l_screen))

# Food image
food_img_path = os.path.join("data", "img", "rat.png")
food_img = pygame.image.load(food_img_path)
food_img = pygame.transform.scale(food_img, (tile, tile))

# Background music
music_path = os.path.join("data", "ost", "Bgm.mp3")
pygame.mixer.music.load(music_path)

# Sound coin
eat_sound_path = os.path.join("data", "ost", "Mlem.mp3")
eat_sound = pygame.mixer.Sound(eat_sound_path)

# Sound game over
gameover_sound_path = os.path.join("data", "ost", "GameOver.mp3")
gameover_sound = pygame.mixer.Sound(gameover_sound_path)

No_sound_path = os.path.join("data", "ost", "No.mp3")
No_sound = pygame.mixer.Sound(No_sound_path)


def game():
    play_music(music_path)

    x = w_screen // 2
    y = l_screen // 2

    snake_coords = [(x, y)]
    snake = [SnakeSegment(w_screen // 2, l_screen // 2)]
    snake_group = pygame.sprite.Group()
    snake_group.add(snake[0])

    food_x = round(random.randint(0, w_screen - tile) / tile) * tile
    food_y = round(random.randint(0, l_screen - tile) / tile) * tile

    score = 0

    end_game = False
    gameover_sound_played = False

    while not end_game:
        end_game, gameover_sound_played = check_colitions(x, y, w_screen, l_screen, snake_coords, gameover_sound_played)
        draw_elements(screen, background_img, food_img, food_x, food_y, snake_coords, snake, font, score)
        snake.insert(0, (x, y))
        clock.tick(10)
        
        if not end_game:
            handle_events()
            x, y, snake_coords = move_snake(x, y, speed_x, speed_y, snake_coords)
            food_x, food_y, score = handle_food_events(x, y, food_x, food_y, score, snake_coords)


    print("Game Over\nScore: {}".format(score))
    save_score(score)
    pygame.display.flip()
    pygame.time.delay(1000)



while True:
    start_screen()
    game()