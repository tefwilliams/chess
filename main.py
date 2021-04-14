
from chess import Game, Color

game = Game()

while not game.over():
    game.take_turn()

if game.check_mate():
    opposing_player_color = Color.get_opposing_color(game.player.color)
    print("%s in check mate. %s wins!" % (str(game.player.color.name).capitalize(
    ), str(opposing_player_color.name).capitalize()) + "\n")

elif game.stale_mate():
    print("%s in stale mate. It's a draw!" %
          str(game.player.color.name).capitalize() + "\n")

Game.quit()
