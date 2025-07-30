import pygame
import os
pygame.font.init()
pygame.mixer.init()

win = pygame.display.set_mode((800,500))
pygame.display.set_caption("First Game")

yellow = pygame.image.load(os.path.join('Assets','spaceship_yellow.png')) #OneDrive\Desktop\all code types\C for uni\
re_yellow = pygame.transform.rotate(pygame.transform.scale(yellow,(55,40)),90)

red = pygame.image.load(os.path.join('Assets','spaceship_red.png'))
re_red = pygame.transform.rotate(pygame.transform.scale(red,(55,40)),270)

background = pygame.image.load(os.path.join('Assets','space.png'))
re_background = pygame.transform.scale(background,(800,500))

bullet_sound = pygame.mixer.Sound(os.path.join('Assets','Grenade+1.mp3'))
bullet_sound2 = pygame.mixer.Sound(os.path.join('Assets','Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)
MAX_BULLETS = 3
VEL = 5
BORDER = pygame.Rect(800//2 - 5,0,10,500)
BULLETS_SPEED = 10
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def draw_window(red,yellow,red_buttels,yellow_buttels,red_health,yellow_health):
    win.blit(re_background, (0,0))
    pygame.draw.rect(win, (0,0,0), BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, (255,255,255))
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, (255,255,255))
    win.blit(red_health_text, (800 - red_health_text.get_width() - 10,10))
    win.blit(yellow_health_text, (10,10))
    win.blit(re_yellow, (yellow.x,yellow.y))
    win.blit(re_red, (red.x,red.y))
    
    for bullet in red_buttels:
        pygame.draw.rect(win, (255,0,0), bullet)
    for bullet in yellow_buttels:
        pygame.draw.rect(win, (255,255,0), bullet)
    pygame.display.update()

def yellow_handle_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
            yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
            yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < 500 - 15:
            yellow.y += VEL
            
def red_handle_movement(keys_pressed,red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < 800:
            red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
            red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < 500 - 15:
            red.y += VEL
            
def handle_bullets(yellow_buttels,red_buttels,yellow,red):
    for bullet in yellow_buttels:
        bullet.x += BULLETS_SPEED
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_buttels.remove(bullet)
        elif bullet.x > 800:
            yellow_buttels.remove(bullet)
    for bullet in red_buttels:
        bullet.x -= BULLETS_SPEED
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_buttels.remove(bullet)
        elif bullet.x < 0:
            red_buttels.remove(bullet)
def draw_winner(text):
    draw_text = WINNER_FONT.render(text,1,(255,255,255))
    win.blit(draw_text,(win.get_width()/2 - draw_text.get_width()/2,win.get_height()/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    
    
def main():
    red_health = 10
    yellow_health = 10    
    red = pygame.Rect(700,100,55,40)
    yellow = pygame.Rect(100,100,55,40)
    
    red_buttels = []
    yellow_buttels = []
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_buttels) < MAX_BULLETS:
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                        yellow_buttels.append(bullet)
                        bullet_sound2.play()
                if event.key == pygame.K_RCTRL and len(red_buttels) < MAX_BULLETS:
                        bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                        red_buttels.append(bullet)
                        bullet_sound2.play()
            if event.type == RED_HIT:
                red_health -= 1
                bullet_sound.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1  
                bullet_sound.play()
        
        win=""
        if red_health == 0 :
            win = "Yellow Wins"
        if yellow_health == 0:
            win = "Red Wins"
        if win != "":   
                draw_winner(win)
                pygame.event.clear()
                break
        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed,yellow)
        red_handle_movement(keys_pressed,red)
        handle_bullets(yellow_buttels,red_buttels,yellow,red)
        draw_window(red,yellow,red_buttels,yellow_buttels,red_health,yellow_health)


if __name__ == "__main__":
    while True:
        main()
        pygame.event.clear
