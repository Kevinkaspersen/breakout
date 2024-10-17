from queue import Empty
import pygame
from pygame.locals import *

pygame.init()


#Clock
clock = pygame.time.Clock()
FPS = 50

#Screen size
screen_width = 800
screen_height = 700

#Rows and colums (Decide how many blocks you want)
rows = 2
colums = 2

#Colors
background = ('light blue')
color = (0, 0, 0)

#Text variables
font = pygame.font.SysFont('Calibri', 30)
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Breakout')
    

class paddle():
    def __init__(self):
        self.reset()
    #Reset function for the paddle
    def reset(self):
        self.height = 10
        self.width  = 150
        self.x = ((screen_width / 2) - (self.width / 2))
        self.y = (screen_height)  -  (self.height + 100)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)


    def move(self):
        #Makes the player paddel move
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, 'black', self.rect)


class blocks():
    def __init__(self):
        self.width = screen_width // colums
        self.height = 50

    #Creates the blocks and put them in a list
    def make_blocks(self):
        self.block_list = []

        for row in range(rows):
            for col in range(colums):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                self.block = [rect]
                #Assign each brick to heir respected rows
                self.block_list.append(self.block)
            
        
    def draw(self):
        for block in self.block_list: 
            pygame.draw.rect(screen, 'yellow', block[0])
            pygame.draw.rect(screen, background, (block[0]), 3)
        

class ball():
    def __init__(self, x ,y):
        self.reset(x, y)

    #Reset function for the ball
    def reset(self,x, y):
        self.ball_radius = 10
        self.x = x - self.ball_radius
        self.y = y 
        self.speed_x = 7
        self.speed_y = -7
        self.rect = Rect(self.x, self.y, self.ball_radius * 2, self.ball_radius * 2)

    #Makes the ball move
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


        #Checks if it hits the screen borders
        
        #Left
        if self.rect.x - self.ball_radius < 0:
            self.speed_x = abs(self.speed_x)
        #Top
        if self.rect.y - self.ball_radius < 0:
            self.speed_y = abs(self.speed_y)
        #Right
        if self.rect.x + self.ball_radius  > screen_width:
            self.speed_x = -abs(self.speed_x)
       
    def draw(self):
        pygame.draw.circle(screen, 'black', (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius), self.ball_radius)



class main():
    def __init__(self):
        #Game variables to control the game
        self.live_ball = False
        self.game_over = 0
    
    
    #Player paddle
        self.player_paddle = paddle()

    #Ball
        self.player_ball = ball(self.player_paddle.x + (self.player_paddle.width // 2), self.player_paddle.y - self.player_paddle.height - 10)

    #Brick wall
        self.player_blocks = blocks()
        self.player_blocks.make_blocks()
        self.loop()

        
    def collision(self):
        #Check if it hits the player paddle
        if self.player_ball.rect.colliderect(self.player_paddle):
            self.player_ball.speed_y *= -1 
        #Checks for collision with the blocks and removes them
        for block in self.player_blocks.block_list:
            if self.player_ball.rect.colliderect(block[0]):
                self.player_ball.speed_y *= -1 
                self.player_blocks.block_list.remove(block)

    #Reset the game if you lose
    def reset(self):
            #Clears the list with the blocks
            self.player_blocks.block_list.clear()
            #Generate new blocks
            self.player_blocks.make_blocks()
            #Resets the player ball
            self.player_ball.reset(self.player_paddle.x + (self.player_paddle.width // 2), self.player_paddle.y - self.player_paddle.height - 10)
            #Reset the paddle
            self.player_paddle.reset()
                
        
    #Game loop
    def loop(self):
        run = True
        while run:
            
            clock.tick(FPS)
            screen.fill(background)

            #Calling the draw functions from each class
            self.player_ball.draw()
            self.player_paddle.draw()
            self.player_blocks.draw()
        
            
           
            #Controls the moving objects
            if self.live_ball:
                self.player_paddle.move()
                self.player_ball.move()
                self.collision()

                if self.game_over != 0:
                    self.live_ball = False

            #Prints messages on the screen based on which conditions that are met
            if not self.live_ball:
                if self.game_over == 0:
                    draw_text('Click anywhere in the window to start', font, 'black', screen_width // 2 - 225 , screen_height // 2 + 100)
                elif self.game_over == 1:
                    draw_text('You Won', font, 'black', screen_width // 2 - 50, screen_height // 2 + 50)
                    draw_text('Click anywhere in the window to start', font, 'black', screen_width // 2 - 225, screen_height // 2 + 100)
                elif self.game_over == -1:
                    draw_text('You lost', font, 'black', screen_width // 2 - 50  , screen_height // 2 + 50)
                    draw_text('Click anywhere in the window to start', font, 'black', screen_width // 2 - 225, screen_height // 2 + 100) 

            #Reset functions

            #Checks if you lose the game
            if self.player_ball.rect.y + self.player_ball.ball_radius  > screen_height:
                self.game_over = -1
                
                    
            #Checks if you win the game
            if len(self.player_blocks.block_list) == 0:
                self.game_over = 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.live_ball == False:
                    self.live_ball = True
                    self.reset()
                    self.game_over = 0
                    

            pygame.display.update()

if __name__== "__main__":
    game = main()


