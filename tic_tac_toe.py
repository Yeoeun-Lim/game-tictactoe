import pygame
import sys

# 초기 설정
pygame.init()
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
# 색상
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# 창 설정
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# 보드 상태 (0=빈칸, 1=O, 2=X)
board = [[0]*BOARD_COLS for _ in range(BOARD_ROWS)]

# 선 그리기 함수
def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2*SQUARE_SIZE), (WIDTH, 2*SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2*SQUARE_SIZE, 0), (2*SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col*SQUARE_SIZE+SQUARE_SIZE//2), int(row*SQUARE_SIZE+SQUARE_SIZE//2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col*SQUARE_SIZE+SPACE, row*SQUARE_SIZE+SQUARE_SIZE-SPACE), 
                                 (col*SQUARE_SIZE+SQUARE_SIZE-SPACE, row*SQUARE_SIZE+SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, 
                                 (col*SQUARE_SIZE+SPACE, row*SQUARE_SIZE+SPACE), 
                                 (col*SQUARE_SIZE+SQUARE_SIZE-SPACE, row*SQUARE_SIZE+SQUARE_SIZE-SPACE), CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    return all(board[row][col] != 0 for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

def check_win(player):
    # 가로
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            draw_horizontal_winning_line(row, player)
            return True
    # 세로
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            draw_vertical_winning_line(col, player)
            return True
    # 대각선
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        draw_desc_diagonal(player)
        return True
    if all(board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)):
        draw_asc_diagonal(player)
        return True
    return False

def draw_vertical_winning_line(col, player):
    posX = col * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (posX, 15), (posX, HEIGHT - 15), 15)

def draw_horizontal_winning_line(row, player):
    posY = row * SQUARE_SIZE + SQUARE_SIZE // 2
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, posY), (WIDTH - 15, posY), 15)

def draw_asc_diagonal(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)

def draw_desc_diagonal(player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            board[row][col] = 0

draw_lines()

player = 1
game_over = False

# 메인 루프
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE

            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player):
                    game_over = True
                player = 2 if player == 1 else 1
                draw_figures()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                player = 1
                game_over = False

    pygame.display.update()