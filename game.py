import pygame
import sys
import time
from PIL import Image, ImageSequence

# Inicializar Pygame
pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
TRACK_COLOR = (139, 69, 19)
LINE_COLOR = (129, 59, 9)
FINISH_LINE_COLOR = (0, 255, 0)  # Verde para la línea de meta

# Configuración de la pantalla
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH + 50, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de carrera simple")

# Cargar imágenes
athlete_images = [
    pygame.image.load('athlete2.png').convert_alpha(),
    pygame.image.load('athlete3.png').convert_alpha(),
]

# Cargar el GIF y convertirlo en una lista de cuadros de imágenes
gif_path = 'athlete9.gif'
im = Image.open(gif_path)
frames = [pygame.image.fromstring(frame.convert("RGBA").tobytes(), frame.size, "RGBA") for frame in ImageSequence.Iterator(im)]
frame_count = len(frames)

# Configuración del personaje
player_size = 100
player_initial_pos = 5
player_pos = [player_initial_pos, SCREEN_HEIGHT // 2 - player_size // 2]
player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size * 1.3, player_size)

# Variables del juego
steps = 0
goal = 100  # Número de pasos necesarios para ganar
start_time = None
end_time = None
current_image = 0
current_frame = 0
expecting_right = True  # Empezar esperando la tecla derecha
frame_duration = im.info['duration'] / 1000  # Duración de cada cuadro en segundos

# Fuente para el texto
font = pygame.font.SysFont(None, 48)

# Configuración del reloj
clock = pygame.time.Clock()

# Tiempo para controlar la animación del GIF
last_frame_time = time.time()

# Bucle principal del juego
running = True
while running:
    current_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and expecting_right:
                expecting_right = False
                if start_time is None:  # Comenzar el cronómetro
                    start_time = time.time()
                player_pos[0] += player_size
                steps += 1
                current_image = (current_image + 1) % len(athlete_images)
            elif event.key == pygame.K_LEFT and not expecting_right:
                expecting_right = True
                if start_time is None:  # Comenzar el cronómetro
                    start_time = time.time()
                player_pos[0] += player_size
                steps += 1
                current_image = (current_image + 1) % len(athlete_images)

    #if current_time - last_frame_time >= frame_duration:
    #    current_frame = (current_frame + 1) % frame_count
    #    last_frame_time = current_time
    current_frame = steps % frame_count

    # Verificar si se ha alcanzado la meta
    if steps >= goal:
        if end_time is None:
            end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"¡Has ganado! Tiempo transcurrido: {elapsed_time:.2f} segundos")
        running = False

    # Dibujar en la pantalla
    screen.fill(WHITE)

    # Dibujar pista de atletismo
    pygame.draw.rect(screen, TRACK_COLOR, (0, SCREEN_HEIGHT // 2 - 75, SCREEN_WIDTH, 150))
    for i in range(0, SCREEN_WIDTH, 50):
        pygame.draw.line(screen, LINE_COLOR, (i, SCREEN_HEIGHT // 2 - 75), (i, SCREEN_HEIGHT // 2 + 75), 2)
    
    # Dibujar línea de meta
    finish_line_x = goal * player_size
    # if player_pos[0] < SCREEN_WIDTH:
    #     offset = player_pos[0] % SCREEN_WIDTH
    #     pygame.draw.line(screen, FINISH_LINE_COLOR, (offset, SCREEN_HEIGHT // 2 - 75), 
    #                      (offset, SCREEN_HEIGHT // 2 + 75), 5)
    # else:
    #     pygame.draw.line(screen, FINISH_LINE_COLOR, (finish_line_x - player_pos[0] + SCREEN_WIDTH, SCREEN_HEIGHT // 2 - 75), 
    #                      (finish_line_x - player_pos[0] + SCREEN_WIDTH, SCREEN_HEIGHT // 2 + 75), 5)
        
    pygame.draw.line(screen, FINISH_LINE_COLOR, (SCREEN_WIDTH - 5, SCREEN_HEIGHT // 2 - 75),
                     (SCREEN_WIDTH - 5, SCREEN_HEIGHT // 2 + 75), 5)

    # Dibujar atleta
    player_draw_pos = (SCREEN_WIDTH * steps  ) / (goal )
    #screen.blit(pygame.transform.scale(athlete_images[current_image], (player_size, player_size)), (player_draw_pos, player_pos[1]))
    
    screen.blit(pygame.transform.scale(frames[current_frame], (player_size * 1.3, player_size)), (player_draw_pos, player_pos[1]))

    # Mostrar el tiempo transcurrido
    if start_time is not None:
        elapsed_time = time.time() - start_time
        time_text = font.render(f"Tiempo: {elapsed_time:.2f} segundos", True, BLACK)
        screen.blit(time_text, (10, 10))

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad del juego
    clock.tick(30)

# Salir del juego
#pygame.quit()
#sys.exit()
