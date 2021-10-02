import pygame
import math

pygame.init()

# Screen
WIDTH = 600
ROWS = 3
win = pygame.display.set_mode((WIDTH, WIDTH))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Images
X_IMAGE = pygame.transform.scale(pygame.image.load("images/x.png"), (80, 80))
O_IMAGE = pygame.transform.scale(pygame.image.load("images/o.png"), (80, 80))

x_won = 0
o_won = 0

# Fonts
END_FONT = pygame.font.SysFont('Ink Free', 50)

# basic font for user typed
base_font = pygame.font.Font(None, 32)

# color_active stores color(lightskyblue3) which
# gets active when input box is clicked by user
color_active = pygame.Color('lightskyblue3')

# color_passive store color(chartreuse4) which is
# color of input box.
color_passive = pygame.Color('chartreuse4')


class Textbox:
    def __init__(self, screen, X, Y):
        self.input_rect = pygame.Rect(X, Y, 140, 32)
        self.color = color_passive
        self.user_text = ""
        self.active = False
        self.text_surface = base_font.render(self.user_text, True, (255, 255, 255))
        self.screen = screen
        pygame.draw.rect(self.screen, self.color, self.input_rect)
        self.change_mode()


    def update_for_event(self, event):
        """
        This function should be called for each event that is happening with Event as parameter.
        :param event: Event which is happened.
        :type event:
        :return:
        :rtype:None
        """

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect.collidepoint(event.pos):
                if not self.active:
                    self.active = True
                    self.change_mode()
            else:
                if self.active:
                    self.active = False
                    self.change_mode()

        if self.active:
            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    self.user_text = self.user_text[:-1]

                # Unicode standard is used for string
                # formation
                else:
                    self.user_text += event.unicode
                self.update_text()

    def change_mode(self):
        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(self.screen, self.color, self.input_rect)
        self.update_text()

    def update_text(self):
        self.text_surface = base_font.render(self.user_text, True, (255, 255, 255))
        # render at position stated in arguments
        self.screen.blit(self.text_surface, (self.input_rect.x + 5, self.input_rect.y + 5))

        # set width of textfield so that text cannot get
        # outside of user's text input
        self.input_rect.w = max(100, self.text_surface.get_width() + 10)

def draw_grid():
    gap = WIDTH // ROWS

    # Starting points
    x = 0
    y = 0

    for i in range(ROWS):
        x = i * gap

        pygame.draw.line(win, GRAY, (x, 0), (x, WIDTH), 3)
        pygame.draw.line(win, GRAY, (0, x), (WIDTH, x), 3)


def show_login(input_name):

    clock = pygame.time.Clock()

    # it will display on screen
    login_screen = pygame.display.set_mode([600, 500])

    xlogin = Textbox(login_screen, 200, 200)

    ologin = Textbox(login_screen, 200, 300)

    # display.flip() will update only a portion of the
    # screen to updated, not full area
    pygame.display.flip()

    # clock.tick(60) means that for every second at most
    # 60 frames should be passed.
    clock.tick(60)

    while True:
        for event in pygame.event.get():
            # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if pygame.MOUSEBUTTONDOWN == event.type or pygame.KEYDOWN == event.type:
                xlogin.update_for_event(event)
                ologin.update_for_event(event)
                # display.flip() will update only a portion of the
                # screen to updated, not full area
                pygame.display.flip()







def initialize_grid():
    dis_to_cen = WIDTH // ROWS // 2

    # Initializing the array
    game_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x = dis_to_cen * (2 * j + 1)
            y = dis_to_cen * (2 * i + 1)

            # Adding centre coordinates
            game_array[i][j] = (x, y, "", True)

    return game_array


def click(game_array):
    global x_turn, o_turn, images

    # Mouse position
    m_x, m_y = pygame.mouse.get_pos()

    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            x, y, char, can_play = game_array[i][j]

            # Distance between mouse and the centre of the square
            dis = math.sqrt((x - m_x) ** 2 + (y - m_y) ** 2)

            # If it's inside the square
            if dis < WIDTH // ROWS // 2 and can_play:
                if x_turn:  # If it's X's turn
                    images.append((x, y, X_IMAGE))
                    x_turn = False
                    o_turn = True
                    game_array[i][j] = (x, y, 'x', False)

                elif o_turn:  # If it's O's turn
                    images.append((x, y, O_IMAGE))
                    x_turn = True
                    o_turn = False
                    game_array[i][j] = (x, y, 'o', False)


# Checking if someone has won
def has_won(game_array):
    global x_won, o_won
    # Checking rows

    for row in range(len(game_array)):
        if (game_array[row][0][2] == game_array[row][1][2] == game_array[row][2][2]) and game_array[row][0][2] != "":
            display_message(game_array[row][0][2].upper() + " has won!")
            if game_array[row][0][2].upper() == 'X':
                x_won = x_won + 1
            else:
                o_won = o_won + 1
            return True

    # Checking columns
    for col in range(len(game_array)):
        if (game_array[0][col][2] == game_array[1][col][2] == game_array[2][col][2]) and game_array[0][col][2] != "":
            display_message(game_array[0][col][2].upper() + " has won!")
            if game_array[row][0][2].upper() == 'X':
                x_won = x_won + 1
            else:
                o_won = o_won + 1
            return True

    # Checking main diagonal
    if (game_array[0][0][2] == game_array[1][1][2] == game_array[2][2][2]) and game_array[0][0][2] != "":
        display_message(game_array[0][0][2].upper() + " has won!")
        if game_array[row][0][2].upper() == 'X':
            x_won = x_won + 1
        else:
            o_won = o_won + 1
        return True

    # Checking reverse diagonal
    if (game_array[0][2][2] == game_array[1][1][2] == game_array[2][0][2]) and game_array[0][2][2] != "":
        display_message(game_array[0][2][2].upper() + " has won!")
        if game_array[row][0][2].upper() == 'X':
            x_won = x_won + 1
        else:
            o_won = o_won + 1
        return True

    return False


def has_drawn(game_array):
    # TODO:logic can be improved to draw earlier
    for i in range(len(game_array)):
        for j in range(len(game_array[i])):
            if game_array[i][j][2] == "":
                return False

    display_message("It's a draw!")
    return True


def display_message(content):
    pygame.time.delay(500)
    win.fill(WHITE)
    end_text = END_FONT.render(content, 1, BLACK)
    win.blit(end_text, ((WIDTH - end_text.get_width()) // 2, (WIDTH - end_text.get_height()) // 2))
    pygame.display.update()
    pygame.time.delay(3000)


def render():
    win.fill(WHITE)
    draw_grid()

    # Drawing X's and O's
    for image in images:
        x, y, IMAGE = image
        win.blit(IMAGE, (x - IMAGE.get_width() // 2, y - IMAGE.get_height() // 2))

    pygame.display.update()


def main():
    global x_turn, o_turn, images, draw

    images = []
    draw = False

    run = True

    x_turn = True
    o_turn = False

    show_login("X USER")
    pygame.display.update()

    game_array = initialize_grid()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                click(game_array)

        render()

        if has_won(game_array) or has_drawn(game_array):
            run = False


while True:
    if __name__ == '__main__':
        pygame.display.set_caption("TicTacToe  X-{}  O-{}".format(x_won, o_won))
        main()
