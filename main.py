from chess import Game

game = Game()

while not game.over():
    game.take_turn()

if game.in_check_mate():
    opposing_player_color = game.player_color.get_opposing_color()

    losing_player = game.player_color.name
    winning_player = opposing_player_color.name

    print(f"{losing_player} in check mate. {winning_player} wins!" + "\n")

elif game.in_stale_mate():
    current_player = game.player_color.name

    print(f"{current_player} in stale mate. It's a draw!" + "\n")
