import pygame

pygame.init()

board_size = 8

horizontal_border = 20  # px
vertical_border = 20  # px

square_width = 60  # px
square_height = 60  # px


def get_square_parameters(row_number: int, column_number: int) -> tuple[int, int, int, int]:
    left_margin = horizontal_border + square_width * column_number
    top_margin = vertical_border + square_height * row_number

    return (left_margin, top_margin, square_width, square_height)


white, black, brown = (255, 255, 255), (0, 0, 0), (187, 129, 65)

screen_width = horizontal_border * 2 + square_width * board_size
screen_height = vertical_border * 2 + square_height * board_size

game_display = pygame.display.set_mode((screen_width, screen_height))
game_display.fill(brown)

pygame.display.set_caption("ChessBoard")

icon = pygame.image.load("assets/game_icon.png")
pygame.display.set_icon(icon)

for row_number in range(8):
    for column_number in range(8):
        square_color = white if (
            row_number + column_number) % 2 == 0 else black
        pygame.draw.rect(game_display, square_color,
                         get_square_parameters(row_number, column_number))

pygame.display.update()

gameExit = False

while not gameExit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True

pygame.quit()
quit()
