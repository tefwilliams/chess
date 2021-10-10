
from chess import Game, Color

game = Game()

while not game.over():
    game.take_turn()

if game.check_mate():
    opposing_player_color = Color.get_opposing_color(game.player_color.color)

    losing_player = game.player_color.color.name.capitalize()
    winning_player = opposing_player_color.name.capitalize()

    print(f"{losing_player} in check mate. {winning_player} wins!" + "\n")

elif game.stale_mate():
    current_player = game.player_color.color.name.capitalize()

    print(f"{current_player} in stale mate. It's a draw!" + "\n")

Game.quit()
