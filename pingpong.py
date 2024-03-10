# IMPORT
from pygame import *

# CLASSES
# GameSprite class
class GameSprite(sprite.Sprite):
    # Constructor Function
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height)) # Resizing the image
        self.speed = player_speed
        
        self.rect = self.image.get_rect()   # Hitbox
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Player Class
class Player(GameSprite):
    def update_l(self):
        keys = key.get_pressed()  # Gets the state of keys (are they pressed?)
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

    def update_r(self):
        keys = key.get_pressed()  # Gets the state of keys (are they pressed?)
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed

# Scene/Background
back = (200, 255, 255) # Background color
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
window.fill(back)

# Variables that determine the state of the game
isRunning = True # Is the program running?
isFinished = False  # Is the game over?
clock = time.Clock() # Timer (to set the FPS)
FPS = 60  # FPS value

# Ball and paddles
paddle1 = Player('racket.png', 30, 200, 4, 50, 150)
paddle2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

# PLAYER 1 LOSES / PLAYER 2 LOSES TEXT
font.init()  # initializes the font
lose1 = font.render('PLAYER 1 LOSE!', True, (180, 0, 0))
lose2 = font.render('PLAYER 2 LOSE!', True, (180, 0, 0))

# Speed of the ball
speed_x = 3
speed_y = 3

# GAME LOOP
while isRunning:
    # Exits the game if you click on the 'X' button on the window tab
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if isFinished != True: # While the game hasn't finished (no one has won)
        window.fill(back)  # Update window background
        paddle1.update_l() # Update paddle1's position
        paddle2.update_r() # Update paddle2's position
        ball.rect.x += speed_x # Update ball's horizontal position
        ball.rect.y += speed_y # Update ball's vertical position

        # If the ball hits one of the paddles
        if sprite.collide_rect(paddle1, ball) or sprite.collide_rect(paddle2, ball):
            speed_x *= -1  # Change the horizontal direction of the ball

        # If the ball reaches screen edges, change its movement direction
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1  # Change the vertical direction of the ball

        # If the ball hits the left edge of the screen, display 'PLAYER 1 LOSE!'
        if ball.rect.x < 0:
            isFinished = True
            window.blit(lose1, (200, 200))
            game_over = True

        # If the ball hits the right edge of the screen, display 'PLAYER 2 LOSE!'
        if ball.rect.x > win_width:
            isFinished = True
            window.blit(lose2, (200, 200))
            game_over = True

        # Updates position of sprites to the next frame
        paddle1.reset()
        paddle2.reset()
        ball.reset()
    
    # Displays the next frame
    display.update()
    clock.tick(FPS) # Sets FPS