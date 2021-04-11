
from chess import Game, Color, display_board
import pygame

game = Game()

while not game.over():
    game.update_display()
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
