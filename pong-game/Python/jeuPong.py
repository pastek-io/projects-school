import pygame
import time
import os

pygame.init()

#Constantes

WIDTH, HEIGHT = 700, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GRAY = (180, 180, 180)

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 75
BALL_RADIUS = 7

SCORE_FONT = pygame.font.SysFont('Trebuchet MS', 50)

# Classe pour le paddle
class Paddle:
    # Constante de la classe
    COLOR = WHITE
    VELOCITY = 5

    # Constructeur de la classe
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    # Méthode pour déssiner le paddle
    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    # Méthode pour bouger le paddle
    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

# Classe pour la ball
class Ball:
    # Constante de la classe
    MIN_VELOCITY = 5
    MAX_VELOCITY = 7
    COLOR = WHITE

    # Constructeur de la classe
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VELOCITY
        self.y_vel = 0

    # Méthode augmentant la vitesse de déplacement
    def speedChange(self):
        for i in range(10):
            self.MAX_VELOCITY += 1
            self.x_vel = self.MAX_VELOCITY
            time.wait(2)

    # Méthode pour déssiner la ball
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    # Méthode pour bouger la ball
    def move(self, right_paddle, left_paddle):
        if self.x == self.original_x and self.y == self.original_y:
            if right_paddle.y == right_paddle.original_y and left_paddle.y == left_paddle.original_y and self.y_vel == 0:
                time.sleep(1.0)
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self, right_paddle, left_paddle):
        self.x = self.original_x
        self.y = self.original_y
        right_paddle.y = right_paddle.original_y
        left_paddle.y = left_paddle.original_y
        self.y_vel = 0
        self.x_vel *= -1

# Fonction déssiner les deux paddle et la ball
def drawGame(win, paddles, ball, left_score, right_score):
    win.fill(BLACK)

    left_score_text = SCORE_FONT.render(f"{left_score}", 1, WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}", 1, WHITE)
    win.blit(left_score_text, (WIDTH//4 - left_score_text.get_width()//2, 20))
    win.blit(right_score_text, (WIDTH * (3/4) - right_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)

    for i in range(10, HEIGHT, HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, LIGHT_GRAY, (WIDTH//2, i, 5, HEIGHT//20))

    ball.draw(win)
    pygame.display.update()

# Fonction pour bouger son paddle
def handle_paddle_movemement(keys, left_paddle, right_paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY >= 0.5:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT - 0.5:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY >= 0.5:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT - 0.5:
        right_paddle.move(up=False)

# Fonction pour créer les collisions de la ball
def handle_collision(ball, left_paddle, right_paddle):
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                # change dirrection id Mathematics
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VELOCITY
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                # change dirrection id Mathematics
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VELOCITY
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

# Fonction principal du jeu
def main():
    run = True
    clock = pygame.time.Clock()

    left_paddle = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = Ball(WIDTH // 2 + BALL_RADIUS // 2, HEIGHT // 2 - BALL_RADIUS // 2, BALL_RADIUS)

    left_score = 0
    right_score = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        clock.tick(FPS)
        drawGame(WIN, [left_paddle, right_paddle], ball, left_score ,right_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        handle_paddle_movemement(keys, left_paddle, right_paddle)

        ball.move(right_paddle, left_paddle)
        handle_collision(ball, left_paddle, right_paddle)

        if ball.x < 0:
            right_score += 1
            ball.reset(right_paddle ,left_paddle)
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset(right_paddle ,left_paddle)

    pygame.quit()

# Lance le jeu en continu
if __name__ == '__main__':
    main()