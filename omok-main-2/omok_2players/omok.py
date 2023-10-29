import pygame
import random
from pygame import QUIT, MOUSEBUTTONDOWN, MOUSEBUTTONUP

OMOK_NUM = 5
NO_DOL = 0
PLAYER = 1
AI = 2
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255,200,0)
pad = 40
cell_size = 50
dol_size = 40
board_width, board_height = 15, 15
w = cell_size * (board_width - 1) + pad * 2
h = cell_size * (board_height - 1) + pad * 2
board = []
dols_order = []
win = False

img_bg = pygame.image.load("wooden.png")
img_bg = pygame.transform.scale(img_bg, (w,h))

img_go_black = pygame.image.load("go_black.png")
img_go_black = pygame.transform.scale(img_go_black, (dol_size,dol_size))
img_go_white = pygame.image.load("go_white.png")
img_go_white = pygame.transform.scale(img_go_white, (dol_size,dol_size))

pygame.font.init()
font_size = 80
myfont = pygame.font.SysFont("nanumgothicbold", font_size)


for i in range(board_height):
	row = []
	for j in range(board_width):
		row.append(NO_DOL)
	board.append(row)

def printBoard():
	for row in board:
		print(row)
	print()

def draw_board(screen):
	screen.blit(img_bg, (0,0))
	for i in range(board_height):
		py = pad + i * cell_size
		px = pad + i * cell_size
		pygame.draw.line(screen, BLACK, (pad, py), (w-pad, py), 2)
		pygame.draw.line(screen, BLACK, (px, pad), (px, h-pad), 2)

def draw_dols_order(screen, bgn=0, end=len(dols_order)):
	for i in range(bgn, end):
		py = pad + dols_order[i][0] * cell_size - dol_size //2
		px = pad + dols_order[i][1] * cell_size - dol_size //2
		if dols_order[i][2] == PLAYER:
			screen.blit(img_go_black, (px,py))
		else:
			screen.blit(img_go_white, (px,py))


def checkValid(mouse_pos):
	mx = mouse_pos[0] - pad
	my = mouse_pos[1] - pad
	
	i_m = my / cell_size
	j_m = mx / cell_size

	i_ref = round(i_m)
	j_ref = round(j_m)
	if abs(i_m-i_ref) < 0.18 and abs(j_m-j_ref) < 0.18:
		return True, int(i_ref), int(j_ref)
	else:
		return False, -1, -1

def checkHorizontalOmok(new_i, new_j, bturn):
	count = 0
	for j in range(new_j, -1, -1):
		if j < 0:
			break
		if board[new_i][j] == (PLAYER if bturn else AI):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	for j in range(new_j+1, new_j + 1 + OMOK_NUM - count):
		if j > board_width - 1:
			break
		if board[new_i][j] == (PLAYER if bturn else AI):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	return False

def checkVerticalOmok(new_i, new_j, bturn):
	count = 0
	for i in range(new_i, -1, -1):
		if i < 0:
			break
		if board[i][new_j] == (PLAYER if bturn else AI):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	for i in range(new_i + 1, new_i + 1 + OMOK_NUM - count):
		if i > board_height - 1:
			break
		if board[i][new_j] == (PLAYER if bturn else AI):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	return False

def checkFirstDiagOmok(new_i, new_j, bturn):
	count = 0
	for d in range(0, OMOK_NUM):
		if new_i - d < 0 or new_j + d > board_width - 1:
			break
		if board[new_i - d][new_j + d] == (PLAYER if bturn else AI):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	for d in range(1, OMOK_NUM):
		if new_i + d > board_height - 1 or new_j - d < 0:
			break
		if board[new_i + d][new_j - d] == (PLAYER if bturn else AI):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	return False

def checkSecondDiagOmok(new_i, new_j, bturn):
	count = 0
	for d in range(0, OMOK_NUM):
		if new_i - d < 0 or new_j - d < 0:
			break
		if board[new_i - d][new_j - d] == (PLAYER if bturn else AI):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	for d in range(1, OMOK_NUM):
		if new_i + d > board_height - 1 or new_j + d > board_height - 1 :
			break
		if board[new_i + d][new_j + d] == (PLAYER if bturn else AI):
			count += 1
			if count == OMOK_NUM:
				return True
		else:
			break
	return False

def checkOmok(new_i, new_j, bturn):
	if checkHorizontalOmok(new_i, new_j, bturn):
		return True
	elif checkVerticalOmok(new_i, new_j, bturn):
		return True
	if checkFirstDiagOmok(new_i, new_j, bturn):
		return True
	elif checkSecondDiagOmok(new_i, new_j, bturn):
		return True
	else:
		return False

def alpha_beta_pruning(depth, board, alpha, beta, is_maximizing_player):
    dir_x = [-1, 1, -1, 1, 0, 0, 1, -1]
    dir_y = [0, 0, -1, 1, -1, 1, -1, 1]
    
    max_depth = max((-depth // 30 + 3), 1)
    if depth == max_depth:
        return evaluate_board(board, AI)

    if is_maximizing_player:
        v = float("-inf")
        pruning = False

        for x in range(15):
            for y in range(15):
                cur_stone = board[y][x]
                flag = False

                if cur_stone == NO_DOL:
                    for k in range(8):
                        nx = x + dir_x[k]
                        ny = y + dir_y[k]

                        if nx < 0 or ny < 0 or nx >= 15 or ny >= 15:
                            continue
                        if board[ny][nx] != NO_DOL:
                            flag = True
                            break

                    if flag:
                        board[y][x] = AI
                        temp = alpha_beta_pruning(depth + 1, alpha, beta, board, False)

                        if v < temp or (v == temp and random.choice([0, 1]) == 0):
                            v = temp
                            if depth == 0:
                                aiX = x
                                aiY = y
                        board[y][x] = NO_DOL

                        alpha = max(alpha, v)

                        if beta <= alpha:
                            pruning = True
                            break
                if pruning:
                    break
            if pruning:
                break
        return v
    else:
        v = float("inf")
        pruning = False

        for x in range(15):
            for y in range(15):
                curStone = board[y][x]
                flag = False

                if curStone == NO_DOL:
                    for k in range(8):
                        nx = x + dir_x[k]
                        ny = y + dir_y[k]
                        if nx < 0 or ny < 0 or nx >= 15 or ny >= 15:
                            continue
                        if board[ny][nx] != NO_DOL:
                            flag = True
                            break
                    if flag:
                        board[y][x] = PLAYER
                        v = min(v, alpha_beta_pruning(depth + 1, alpha, beta, board, True))
                        board[y][x] = NO_DOL

                        beta = min(beta, v)

                        if beta <= alpha:
                            pruning = True
                            break
                if pruning:
                    break
            if pruning:
                break
        return v

def check_fit_five(x, y, direction):
    stone = board[y][x]
    
    for _ in range(5):
        if x < 0 or x >= board_width or y < 0 or y >= board_height or board[y][x] != stone:
            return False
        x, y = x + dir_x[direction], y + dir_y[direction]
    
    return True



def evaluate_board(board, player):
    dir_x = [-1, 1, -1, 1, 0, 0, 1, -1]
    dir_y = [0, 0, -1, 1, -1, 1, -1, 1]
    ai_weight = 0
    player_weight = 0

    for x in range(15):
        for y in range(15):
            if board[y][x] == NO_DOL:
                continue

            cur_stone = board[y][x]

            for k in range(0, 8, 2):
                if check_fit_five(x, y, k):
                    continue

                nx, ny = x, y
                stone_cnt = 1
                flag = False
                is_one_space = False

                is_one_side_block = False

                if x == 0 or y == 0 or x == 14 or y == 14:
                    is_one_side_block = True

                for i in range(4):
                    nx += dir_x[k]
                    ny += dir_y[k]

                    if nx < 0 or ny < 0 or nx >= 15 or ny >= 15:
                        break

                    if board[ny][nx] == NO_DOL and is_one_space:
                        break
                    if board[ny][nx] == cur_stone:
                        stone_cnt += 1
                        if flag:
                            is_one_space = True
                            flag = False
                        if nx == 0 or ny == 0 or nx == 14 or ny == 14:
                            is_one_side_block = True
                    elif board[ny][nx] == NO_DOL and not flag:
                        flag = True
                    else:
                        if not flag:
                            is_one_side_block = True
                        break

                nx, ny = x, y
                flag = False

                for i in range(4):
                    nx += dir_x[k + 1]
                    ny += dir_y[k + 1]

                    if nx < 0 or ny < 0 or nx >= 15 or ny >= 15:
                        break

                    if board[ny][nx] == NO_DOL and is_one_space:
                        break

                    if board[ny][nx] == cur_stone:
                        stone_cnt += 1
                        if flag:
                            is_one_space = True
                            flag = False
                        if nx == 0 or ny == 0 or nx == 14 or ny == 14:
                            is_one_side_block = True
                    elif board[ny][nx] == NO_DOL and not flag:
                        flag = True
                    else:
                        if not flag:
                            is_one_side_block = True
                        break

                weight_sum = 0

                if stone_cnt == 1:
                    if is_one_side_block and not is_one_space:
                        weight_sum += 5
                    elif not is_one_side_block and not is_one_space:
                        weight_sum += 10
                elif stone_cnt == 2:
                    if is_one_side_block and not is_one_space:
                        weight_sum += 30
                    elif is_one_side_block and is_one_space:
                        weight_sum += 15
                    elif not is_one_side_block and not is_one_space:
                        weight_sum += 40
                    else:
                        weight_sum += 30
                elif stone_cnt == 3:
                    if is_one_side_block and not is_one_space:
                        weight_sum += 60
                    elif is_one_side_block and is_one_space:
                        weight_sum += 120
                    elif not is_one_side_block and not is_one_space:
                        weight_sum += 400
                    else:
                        weight_sum += 360
                elif stone_cnt == 4:
                    if is_one_side_block and not is_one_space:
                        weight_sum += 300
                    elif is_one_side_block and is_one_space:
                        weight_sum += 250
                    elif not is_one_side_block and not is_one_space:
                        weight_sum += 2200
                    else:
                        weight_sum += 660
                elif stone_cnt == 5 or stone_cnt == 6:
                    weight_sum += 4500

                if cur_stone == PLAYER:
                    player_weight += weight_sum
                else:
                    ai_weight += weight_sum
    return ai_weight - player_weight


def find_best_move(board, player):
    best_move = None
    best_value = float('-inf') if player == AI else float('inf')
    alpha = float('-inf')
    beta = float('inf')
    depth = 0  # You can set the desired search depth

    for i in range(board_height):
        for j in range(board_width):
            if board[i][j] == NO_DOL:
                board[i][j] = player
                value = alpha_beta_pruning(depth, board, alpha, beta, False)
                board[i][j] = NO_DOL

                if player == AI:
                    if value > best_value:
                        best_value = value
                        best_move = (i, j)
                    alpha = max(alpha, best_value)
                else:
                    if value < best_value:
                        best_value = value
                        best_move = (i, j)
                    beta = min(beta, best_value)

    return best_move