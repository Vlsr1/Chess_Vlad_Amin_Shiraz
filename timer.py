import pygame
import sys

# Инициализация pygame
pygame.init()

# Константы
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 48
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50

# Создание окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess Timer")

# Шрифт
font = pygame.font.Font(None, FONT_SIZE)

# Время игроков (в секундах)
time_player1 = 900  # 15 минут
time_player2 = 900  # 15 минут

# Текущий игрок и состояние таймера
current_player = 1
running = False

# Тип добавления времени
increment_type = "none"  # "none", "fischer", "bronstein"
increment_value = 0  # Время добавления в секундах

# Функция для форматирования времени
def format_time(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02}:{seconds:02}"

# Ввод настроек через консоль
print("Enter the increment type (none, fischer, bronstein):")
increment_type = input().strip().lower()
print("Enter the increment value (in seconds):")
increment_value = int(input().strip())

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if 50 <= mouse_x <= 50 + BUTTON_WIDTH and 200 <= mouse_y <= 200 + BUTTON_HEIGHT:
                if current_player != 1:
                    current_player = 1
                    running = True
                    if increment_type == "fischer":
                        time_player1 += increment_value
                    elif increment_type == "bronstein":
                        time_player1 += increment_value // 2
            elif 450 <= mouse_x <= 450 + BUTTON_WIDTH and 200 <= mouse_y <= 200 + BUTTON_HEIGHT:
                if current_player != 2:
                    current_player = 2
                    running = True
                    if increment_type == "fischer":
                        time_player2 += increment_value
                    elif increment_type == "bronstein":
                        time_player2 += increment_value // 2

    if running:
        if current_player == 1:
            time_player1 -= 1
            if time_player1 <= 0:
                time_player1 = 0
                running = False
        else:
            time_player2 -= 1
            if time_player2 <= 0:
                time_player2 = 0
                running = False

        pygame.time.delay(1000)  # Задержка в 1 секунду

    # Очистка экрана
    screen.fill(WHITE)

    # Отображение времени
    text_player1 = font.render(f"Player 1: {format_time(time_player1)}", True, BLACK)
    text_player2 = font.render(f"Player 2: {format_time(time_player2)}", True, BLACK)
    screen.blit(text_player1, (50, 50))
    screen.blit(text_player2, (350, 50))

    # Отображение кнопок
    pygame.draw.rect(screen, BLACK, (50, 200, BUTTON_WIDTH, BUTTON_HEIGHT))
    pygame.draw.rect(screen, BLACK, (450, 200, BUTTON_WIDTH, BUTTON_HEIGHT))
    button_text1 = font.render("Player 1", True, WHITE)
    button_text2 = font.render("Player 2", True, WHITE)
    screen.blit(button_text1, (50 + (BUTTON_WIDTH - button_text1.get_width()) // 2, 200 + (BUTTON_HEIGHT - button_text1.get_height()) // 2))
    screen.blit(button_text2, (450 + (BUTTON_WIDTH - button_text2.get_width()) // 2, 200 + (BUTTON_HEIGHT - button_text2.get_height()) // 2))

    # Обновление экрана
    pygame.display.flip()