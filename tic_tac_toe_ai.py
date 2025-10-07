import pygame
import sys
import random

pygame.init()

# 기본 설정
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe (Fixed)")
screen.fill(BG_COLOR)

board = [[0 for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 1:
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (int(col * SQUARE_SIZE + SQUARE_SIZE // 2),
                                    int(row * SQUARE_SIZE + SQUARE_SIZE // 2)),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 2:
                start1 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end1 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                start2 = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end2 = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start1, end1, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, start2, end2, CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full():
    return all(board[r][c] != 0 for r in range(BOARD_ROWS) for c in range(BOARD_COLS))

def check_win(player):
    # 가로
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            return ("row", row)
    # 세로
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            return ("col", col)
    # 대각선
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        return ("diag_desc", None)
    if all(board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)):
        return ("diag_asc", None)
    return None

def draw_winning_line(direction, index, player):
    color = CIRCLE_COLOR if player == 1 else CROSS_COLOR
    offset = SQUARE_SIZE // 2

    if direction == "row":
        y = index * SQUARE_SIZE + offset
        pygame.draw.line(screen, color, (15, y), (WIDTH - 15, y), 15)
    elif direction == "col":
        x = index * SQUARE_SIZE + offset
        pygame.draw.line(screen, color, (x, 15), (x, HEIGHT - 15), 15)
    elif direction == "diag_desc":
        pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)
    elif direction == "diag_asc":
        pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)

def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            board[r][c] = 0

# --- “적당히 똑똑한 AI” ---
def ai_move():
    # 1️⃣ 이길 수 있는 자리 있으면 이기기
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if available_square(r, c):
                board[r][c] = 2
                if check_win(2):
                    board[r][c] = 0
                    return (r, c)
                board[r][c] = 0
    # 2️⃣ 플레이어가 이길 수 있는 자리 막기
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if available_square(r, c):
                board[r][c] = 1
                if check_win(1):
                    board[r][c] = 0
                    return (r, c)
                board[r][c] = 0
    # 3️⃣ 랜덤
    empty = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if available_square(r, c)]
    return random.choice(empty) if empty else None

# 게임 루프
draw_lines()
player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = event.pos
            row, col = mouseY // SQUARE_SIZE, mouseX // SQUARE_SIZE

            if available_square(row, col):
                mark_square(row, col, 1)
                draw_figures()
                result = check_win(1)
                if result:
                    direction, idx = result
                    draw_winning_line(direction, idx, 1)
                    game_over = True

                if not game_over and not is_board_full():
                    ai_row, ai_col = ai_move()
                    mark_square(ai_row, ai_col, 2)
                    draw_figures()
                    result = check_win(2)
                    if result:
                        direction, idx = result
                        draw_winning_line(direction, idx, 2)
                        game_over = True

        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart()
            player = 1
            game_over = False

    pygame.display.update()