from omok import *
import random
pygame.init()
SURFACE = pygame.display.set_mode((w, h))
clock = pygame.time.Clock()
player_turn = True
ai_turn = False
running = True
is_down = False
is_valid = False
new_pos = (0, 0)

while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
        elif e.type == MOUSEBUTTONDOWN:
            is_down = True
        elif e.type == MOUSEBUTTONUP:
            if is_down:
                is_valid, i_new, j_new = checkValid(pygame.mouse.get_pos())
                if is_valid:
                    is_down = False
                    if board[i_new][j_new] == NO_DOL:
                        if player_turn:
                            board[i_new][j_new] = PLAYER
                            dols_order.append((i_new, j_new, board[i_new][j_new]))
                            printBoard()
                            if checkOmok(i_new, j_new, player_turn):
                                running = False
                                win = board[i_new][j_new]
                            player_turn = not player_turn
                            ai_turn = not ai_turn
                            
    if ai_turn:
        if board[i_new][j_new] == NO_DOL:
            ai_move = find_best_move(board, AI) 
            i_new, j_new = ai_move[0], ai_move[1]
            board[i_new][j_new] = AI
            dols_order.append((i_new, j_new, board[i_new][j_new]))
            printBoard()
            if checkOmok(i_new, j_new, ai_turn):
                running = False
                win = board[i_new][j_new]
            ai_turn = not ai_turn
            player_turn = not player_turn

    SURFACE.fill(YELLOW)
    draw_board(SURFACE)
    draw_dols_order(SURFACE, 0, len(dols_order))
    pygame.display.update()
    clock.tick(30)

if win:
    win_text = "You win" if win == PLAYER else "AI WINS"
    text_surface = myfont.render(win_text, False, (0, 0, 255))
    SURFACE.blit(text_surface, (w//2 - 200, h//2 - font_size))
    pygame.display.update()
    for i in range(6):
        clock.tick(1)

pygame.quit()
