import pygame
from pygame.locals import *
import time
import random

#block size
SIZE = 40
#background color
BACKGOUND_COLOR = (14,212,105)


class Apple:
    def __init__(self,parent_screen):
        #creating a surface
        self.parent_screen = parent_screen
        #load a apple image
        self.image = pygame.image.load("resources/apple.jpg").convert()
        #Apple co-ordinate on window in multiple of 40(block size)
        self.x = 120
        self.y = 120

    def draw(self):
        #draw the Apple on surface
        self.parent_screen.blit(self.image,(self.x,self.y))
        #Update surface
        pygame.display.flip()

    def move(self):
        #change the apple position randomaly
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,16)*SIZE


class Snake:
    def __init__(self,parent_screen,length):
        self.length = length
        #creating a surface
        self.parent_screen = parent_screen
        #load a block image
        self.block = pygame.image.load("resources/block.jpg").convert()
        #block co-ordinate on window
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        #inital direction
        self.direction = "down"

    #move the block in specifying direction
    def move_left(self):
        self.direction = "left"
 
    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    #walk Automatically in previous direction
    def walk(self):
        #update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        #update head
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    def draw(self):
        #draw the block on surface
        for i in range(self.length):
            self.parent_screen.blit(self.block,(self.x[i],self.y[i]))
        #Update surface
        pygame.display.flip()


class Game:
    def __init__(self):
        #initialize pygame Module
        pygame.init()
        pygame.display.set_caption("Pankaj: Snake And Apple Game")
        
        #start background music
        pygame.mixer.init()
        self.play_background_music()

        #initialize game window or creating a surface
        self.surface = pygame.display.set_mode((1000,680))
        #creating snake object
        self.snake = Snake(self.surface,1)
        #draw this snake on the window or surface
        self.snake.draw()
        #creating Apple Object
        self.apple = Apple(self.surface)
        #draw this apple on the window or surface
        self.apple.draw()

    #play background music
    def play_background_music(self):
        #Sound is for just once Music is for long
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1, 0)

    #play sound
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    #when game Over Reset the score
    def reset(self):
        self.snake = Snake(self.surface,1)
        self.apple = Apple(self.surface)

    #check there is collision or not to the apple and snake
    def is_collision(self,x1,y1,x2,y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    #add background music
    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0,0))

    def play(self):
        #render bacground image
        self.render_background()
        self.snake.walk()
        #since surface will update every time so draw the image every time
        self.apple.draw()
        #display Score
        self.display_score()
        #update Screen
        pygame.display.flip()

        #snake eating apple
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[0],self.snake.y[0],self.apple.x,self.apple.y):
                #add eating music
                self.play_sound("ding")
                #increase snake length
                self.snake.increase_length()
                #if collision occur move apple to random position
                self.apple.move()

        #check for snake collision with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i],self.snake.y[i]):
                #add crasg music
                self.play_sound("crash")
                raise "Game over"

        # snake colliding with the boundries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 680):
            self.play_sound('crash')
            raise "Hit the boundry error"

    #display the score
    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(255,255,255))
        self.surface.blit(score, (700,10))

    #show game Over Text
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}",True,(255,255,255))
        self.surface.blit(line1, (200,330))
        line2 = font.render(f"To play again press Enter. To exit press Escape!",True,(255,255,255))
        self.surface.blit(line2, (200,360))
        #when game over pause the music
        pygame.mixer.music.pause()
        pygame.display.flip()
    
    def run(self):
        #event loop : waiting for user input, event is fumdamental of UI
        running = True
        pause = False
        while running:
            #get all the type of event from user, module is pyagame.locals
            for event in pygame.event.get():
                #event when pressing key
                if event.type == KEYDOWN:
                    #when user click esc key event will be end
                    if event.key == K_ESCAPE:
                        running = False
                    #when user press enter pause will be false
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    
                    if not pause:
                        #when user click UP,DOWN,LEFT,RIGHT key 
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                #even click on cross(X) event will be end
                elif event.type == QUIT:
                    running = False

            #when user not chhose any event snake will move automatically
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            time.sleep(.1)


if __name__ == "__main__":
    game = Game()
    game.run()
