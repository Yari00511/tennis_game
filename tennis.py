import pygame
import math
import time


class Background(pygame.sprite.Sprite):

    '''Background class.'''

    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


pygame.mixer.init()
class Ball(pygame.sprite.Sprite):

    '''Ball class.'''

    def __init__(self, image_file, location, speed, increment_x, increment_y, sound):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.speed = speed
        self.increment_x = increment_x
        self.increment_y = increment_y
        self.sound = sound

    def move(self, increment_x, increment_y):

        '''Moving the ball.'''

        self.rect.move_ip(-1*self.increment_x*self.speed, 0)
        self.rect.move_ip(0, 1*self.increment_y*(speed//3))

    def collision_left(self, object):

        '''Ball hitting racket of Player 1.'''

        if (self.rect.left  <= object.rect.right) and (self.rect.top < object.rect.bottom) and (self.rect.bottom > object.rect.top):
            return True

    def collision_right(self, object):

        '''Ball hitting racket of Palyer 2.'''

        if (self.rect.right  >= object.rect.left) and (self.rect.top < object.rect.bottom) and (self.rect.bottom > object.rect.top):
            return True

    def change_angle(self, object):
        
        '''Change the ball's angle depending on how far from the center it hits the racket.'''

        a = self.rect.center[1]  - object.rect.top
        b = object.rect.bottom - self.rect.center[1]
        angle = (object.rect.center[1]-object.rect.top)/(9000)*(b-a)
        return angle

    def out_left(self, field):

        '''Check if the ball is out of the field and the point goes to player1.'''

        if ((self.rect.left > 1497) or (((self.rect.bottom < 156) or (self.rect.top > 700)) and (self.rect.left > field.rect.center[0]))):
            return True

    def out_right(self, field):

        '''Check if the ball is out of the field and the point goes to player2.'''

        if ((self.rect.right < 297) or (((self.rect.bottom < 156) or (self.rect.top > 700)) and (self.rect.right < field.rect.center[0]))):
            return True

    def reset_pos(self, new_loc):

        '''Reset the ball's position to center and increment y to 0.'''

        self.rect.center = new_loc
        self.increment_y = 0

    def hit_sound(self):

        '''Sound of hitting the ball with a racket.'''

        pygame.mixer.music.load(self.sound)
        pygame.mixer.music.play(0)


class Player(pygame.sprite.Sprite):

    '''Player class.'''

    def __init__(self, image_file, location, speed, up_key, down_key):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location
        self.speed = speed
        self.up_key = up_key
        self.down_key = down_key

    def handle_keys(self):

        '''Moving rackets when user presses the button.'''

        key = pygame.key.get_pressed()
        if key[self.up_key]:
            if self.rect.top >= 156:
                self.rect.move_ip(0, -1*self.speed)
        if key[self.down_key]:
            if self.rect.bottom <= 700:
                self.rect.move_ip(0, 1*self.speed)

    def reset_pos(self, loc_x, loc_y):

        '''Reset the racket's position to the initial one.'''

        self.rect.center = (loc_x, loc_y)


pygame.font.init()
class Score(pygame.sprite.Sprite):

    '''Score class.'''

    def __init__(self, points1=0, points2=0):
        pygame.sprite.Sprite.__init__(self)
        self.myfont = pygame.font.SysFont('Liberation Sans', 30)
        self.points1 = points1
        self.points2 = points2
        
    def refresh(self, screen):

        '''Refreshing the score with the Players' points.'''

        self.textsurface = self.myfont.render('Player 1 points: {}     Player 2 points: {}'.format(self.points1, self.points2), False, (255, 255, 255))
        screen.blit(self.textsurface, (20, 20))


def display_message(msg, screen, background, score, player_numb, waiting, dist):

    '''Displaying the add points and victory messages.'''
    
    msg_font = pygame.font.SysFont('Liberation Sans', 30)
    msg_textsurface = msg_font.render(msg.format(player_numb), False, (255, 255, 255))
    
    screen.blit(msg_textsurface, (background.rect.center[0]-dist, 50))
    score.refresh(screen)
    pygame.display.update()
    time.sleep(waiting)

def reset_positions(ball, player1, player2):

        '''Reset the positions of the rackets and the ball.'''

        ball.reset_pos(background.rect.center)
        player1.reset_pos(297, background.rect.center[1])
        player2.reset_pos(1497, background.rect.center[1])

def congrats_song(song):

    '''Playing a congratulations song.'''

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(0)

def display_objects(screen, background, ball, player1, player2):

    '''Displaying all objects on the screen.'''

    screen.blit(background.image, background.rect)
    screen.blit(ball.image, ball.rect)
    screen.blit(player1.image, player1.rect)
    screen.blit(player2.image, player2.rect)


speed = 10
background = Background('court.png', [0, 0])
ball = Ball('ball.png', background.rect.center, speed, 1, 0, 'ball_hit.wav')
player1 = Player('racket1.png', [297, background.rect.center[1]], speed, pygame.K_w, pygame.K_s)
player2 = Player('racket2.png', [1497, background.rect.center[1]], speed, pygame.K_UP, pygame.K_DOWN)
score = Score()

plus_point_msg = 'One point for Player {}.'
won_msg = 'Congratualtions, Player {}! You won the game.'

screen = pygame.display.set_mode(background.rect.size)
pygame.display.set_caption('Tennis Game')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    display_objects(screen, background, ball, player1, player2)
    
    player1.handle_keys()
    player2.handle_keys()
    
    if ball.collision_left(player1):
        ball.hit_sound()
        ball.increment_x *= -1
        ball.increment_y = ball.change_angle(player1)
    
    if ball.collision_right(player2):
        ball.hit_sound()
        ball.increment_x *= -1
        ball.increment_y = ball.change_angle(player2)
    
    ball.move(ball.increment_x, ball.increment_y)

    if ball.out_left(background):
        score.points1 += 1
        reset_positions(ball, player1, player2)

        if score.points1 == 6:
            congrats_song('tina_turner_the_best_cut.wav')
            display_message(won_msg, screen, background, score, 1, 20, 300)
            running = False
        else:
            display_message(plus_point_msg, screen, background, score, 1, 4, 150)

    if ball.out_right(background):
        score.points2 += 1
        reset_positions(ball, player1, player2)

        if score.points2 == 6:
            congrats_song('tina_turner_the_best_cut.wav')
            display_message(won_msg, screen, background, score, 2, 20, 300)
            running = False
        else:
            display_message(plus_point_msg, screen, background, score, 2, 4, 150)

    score.refresh(screen)
    pygame.display.update()
