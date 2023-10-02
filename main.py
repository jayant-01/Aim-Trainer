import pygame
import time
import random
import math
pygame.init()

width,height = 800, 600
top_bar_height = 50

win =  pygame.display.set_mode((width, height))
pygame.display.set_caption("Aim Trainer")

target_increment = 400
target_event =pygame.USEREVENT
target_padding = 30
lives = 5

label_font = pygame.font.SysFont("comicsans",24)


class Target:
    MAX_SIZE = 30
    growth_rate = 0.2
    COLOR = 'red'
    SEC_COLOR = 'white'

    def __init__(self,x,y):
        self.x = x
        self.y =y
        self.size = 0
        self.grow = True
    def update(self):
        if(self.size + self.growth_rate >= self.MAX_SIZE):
            self.grow = False
        if self.grow:
            self.size += self.growth_rate
        else:
            self.size -= self.growth_rate
    def draw(self, win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.size)
        pygame.draw.circle(win, self.SEC_COLOR, (self.x, self.y), self.size*0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size*0.6)
        pygame.draw.circle(win, self.SEC_COLOR, (self.x, self.y), self.size*0.4)

    def collide(self,x,y):
        dis = math.sqrt((self.x-x)**2+(self.y-y)**2)
        return dis<=self.size



def draw(win,targets):
    win.fill((0,40,80))

    for target in targets:
        target.draw(win)

    pygame.display.update()



def format_time(secs):
    milli = math.floor(int(secs*1000%1000)/100)
    seconds = int(round(secs %60,1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_top_bar(win, elapsed_time,targets_pressed,misses):
    pygame.draw.rect(win,"cyan",(0,0,width,top_bar_height))
    time_label = label_font.render(f"Time: {format_time(elapsed_time)}",1,"black")

    speed = round(targets_pressed / elapsed_time,1)
    speed_label = label_font.render(f"speed: {speed} t/s",1,"black")
    hits_label = label_font.render(f"hits: {targets_pressed} ", 1, "black")

    lives_label = label_font.render(f"lives: {lives - misses} ", 1, "black")


    win.blit(time_label,(5,5))
    win.blit(speed_label, (200, 5))
    win.blit(hits_label, (450, 5))
    win.blit(lives_label, (600, 5))

def end_screen(win,elapsed_time,targets_pressed,clicks):
    win.fill((0,40,80))

    time_label = label_font.render(f"Time: {format_time(elapsed_time)}", 1, "white")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = label_font.render(f"speed: {speed} t/s", 1, "white")
    hits_label = label_font.render(f"hits: {targets_pressed} ", 1, "white")

    win.blit(time_label, (get_middle(time_label), 100))
    win.blit(speed_label, (get_middle(speed_label), 300))
    win.blit(hits_label, (get_middle(hits_label), 500))

    pygame.display.update()

    run =True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()
def get_middle(surface):
    return width/2 - surface.get_width()/2


def main():
    run = True
    targets=[]
    clock = pygame.time.Clock()
    pygame.time.set_timer(target_event, target_increment)

    targets_pressed=0
    clicks=0
    misses=0
    start_time = time.time()

    while run:
        clock.tick(60)
        click =False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time =time.time()-start_time


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run =False
                break

            if event.type == target_event:
                x = random.randint(target_padding,width-target_padding)
                y = random.randint(target_padding+top_bar_height,height-target_padding)
                target = Target(x,y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks+=1
        for target in targets:
            target.update()

            if target.size <=0:
                targets.remove(target)
                misses+=1
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed+=1

        if misses>=lives:
            end_screen(win,elapsed_time,targets_pressed,clicks)

        draw(win,targets)
        draw_top_bar(win,elapsed_time,targets_pressed,misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()

