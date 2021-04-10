
from chess import Game, Color, display_board
from test import Screen
import pygame

game = Game()
screen = Screen()

while not any(event.type == pygame.QUIT for event in pygame.event.get()) and not game.over():
    screen.update(game.board)
    game.take_turn()
    game.player.swap_color()

display_board(game.board)

if game.check_mate():
    opposing_player_color = Color.get_opposing_color(game.player.color)
    print("%s in check mate. %s wins!" % (str(game.player.color.name).capitalize(
    ), str(opposing_player_color.name).capitalize()) + "\n")

elif game.stale_mate():
    print("%s in stale mate. It's a draw!" %
          str(game.player.color.name).capitalize() + "\n")

pygame.quit()
quit()
