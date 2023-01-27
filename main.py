import pygame
import os
import random
import time
#op

game_over = False
win, lose = False, False
last_right = True
cnt = 0
def load_image(name, colorkey=None):
    image = pygame.image.load(os.path.join('data', name))
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

if __name__ == '__main__':
    pygame.init()
    size = width, height = 480, 1000
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    gm_st = pygame.sprite.Sprite()
    image = load_image('start.png')
    pygame.mixer.music.load("data/Splash Reverb Version.mp3")
    pygame.mixer.music.play(0)
    gm_st.image = image
    gm_st.rect = gm_st.image.get_rect()
    gm_st.rect.x, gm_st.rect.y = 0, 0
    all_sprites.add(gm_st)
    pygame.display.flip()
    # ожидание закрытия окна:
    clock = pygame.time.Clock()
    fps = 40
    v = 5
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)



class cadre(pygame.sprite.Sprite):
    image = load_image("cadre.png")

    def __init__(self):
        super().__init__(stabel_group)
        self.image = cadre.image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)



player = None
stabel_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
win_group = pygame.sprite.Group()
player_image = load_image('chel.png', -1)


class door(pygame.sprite.Sprite):
    image = load_image('escape.png', -1)

    def __init__(self):
        super().__init__(win_group)
        self.image = door.image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(135, 200)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        for i in stabel_group:
            if pygame.sprite.collide_mask(self, i):
                i.kill()
class knopki(pygame.sprite.Sprite):
    image = load_image('knopki.png', -1)

    def __init__(self):
        super().__init__(player_group)
        self.image = knopki.image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 850
        #self.mask = pygame.mask.from_surface(self.image)

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group)
        self.add(player_group)
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 600
        self.gravity = 0
        self.fall = False
        self.go_left = False
        self.go_right = False
        self.bumped_left = False
        self.bumped_right = False
        self.mask = pygame.mask.from_surface(self.image)
        self.c = 1
        self.alive = True
        self.win = False

    def collision(self, group):
        for i in group:
            if pygame.sprite.collide_mask(self, i):
                return True
        return False


    def update(self, *args):
        if self.alive:
            if self.collision(all_sprites):
                self.alive = False
            if pygame.sprite.collide_mask(self, dor):
                self.alive = False
                self.win = True
            self.rect = self.rect.move(0, self.gravity)
            if self.collision(stabel_group):
                self.rect = self.rect.move(0, -self.gravity)
                self.gravity = self.gravity // 2
                self.rect = self.rect.move(0, self.gravity)
                if self.collision(stabel_group):
                    self.rect = self.rect.move(0, -self.gravity)
                    self.gravity = self.gravity // 2
                    self.rect = self.rect.move(0, self.gravity)
                    if self.collision(stabel_group):
                        self.rect = self.rect.move(0, -self.gravity)
                self.fall = True
                self.gravity = 0
            else:
                self.gravity += 1


            if args:
                global last_right
                print(args)
                if args[0].type == pygame.KEYDOWN:
                    if args[0].key == 1073741906 and self.fall:
                        self.fall = False
                        self.bumped_right = False
                        self.bumped_left = False
                        self.gravity = -18
                    if args[0].key == 1073741903:
                        self.go_left = True
                        self.bumped_right = False
                        if not last_right:
                            self.image = pygame.transform.flip(self.image, True, False)
                            last_right = not last_right
                    if args[0].key == 1073741904:
                        self.go_right = True
                        self.bumped_left = False
                        if last_right:
                            self.image = pygame.transform.flip(self.image, True, False)
                            last_right = not last_right
                if args[0].type == pygame.KEYUP:
                    print(1)
                    if args[0].key == 1073741903:
                        self.go_left = False
                    if args[0].key == 1073741904:
                        self.go_right = False
            if self.go_left and not self.bumped_left:
                self.rect = self.rect.move(6, 0)
                if self.collision(stabel_group):
                    self.rect = self.rect.move(-3, 0)
                    if self.collision(stabel_group):
                        self.rect = self.rect.move(-2, 0)
                        if self.collision(stabel_group):
                            self.rect = self.rect.move(-1, 0)
                    self.bumped_left = True
            if self.go_right and not self.bumped_right:
                self.rect = self.rect.move(-6, 0)
                if self.collision(stabel_group):
                    self.rect = self.rect.move(3, 0)
                    if self.collision(stabel_group):
                        self.rect = self.rect.move(2, 0)
                        if self.collision(stabel_group):
                            self.rect = self.rect.move(1, 0)
                    self.bumped_right = True
        else:
            global game_over, win, lose
            if self.win:
                self.image = load_image('chel_win.png', -1)
                win = True
            else:
                self.image = load_image('chel_ded.png', -1)
                lose = True
            game_over = True






class piece(pygame.sprite.Sprite):
    def __init__(self, group, x, y, active, *cur_frame):
        super().__init__(group)
        self.frames = []
        self.cut_sheet(load_image('ntnhbc.png', -1), 4, 7)
        if cur_frame:
            self.cur_frame = cur_frame[0]
        else:
            self.cur_frame = random.randint(0, 6) * 4
        self.figure = self.cur_frame
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)
        self.active = active
        self.count = 0
        self.wait = 60
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))


    def update(self, *args):
        if self.active:
            if self.count % 30 == 0:
                self.rect = self.rect.move(0, 40)
            if self.wait == 60:
                if args:
                    self.wait = 0
                    if args[0] == 97:
                        self.rect = self.rect.move(-40, 0)
                        for i in stabel_group:
                            if pygame.sprite.collide_mask(self, i):
                                self.rect = self.rect.move(40, 0)
                    if args[0] == 100:
                        self.rect = self.rect.move(40, 0)
                        for i in stabel_group:
                            if pygame.sprite.collide_mask(self, i):
                                self.rect = self.rect.move(-40, 0)
                    if args[0] == 101:
                        self.cur_frame += 1
                        if self.cur_frame - 4 == self.figure:
                            self.cur_frame -= 4
                        self.image = self.frames[self.cur_frame]
                        self.mask = pygame.mask.from_surface(self.image)
                        for i in stabel_group:
                            if pygame.sprite.collide_mask(self, i):
                                self.cur_frame -= 1
                                if self.cur_frame == self.figure - 1:
                                    self.cur_frame += 4
                                self.image = self.frames[self.cur_frame]
                                self.mask = pygame.mask.from_surface(self.image)
                    if args[0] == 113:
                        self.cur_frame -= 1
                        if self.cur_frame == self.figure - 1:
                            self.cur_frame += 4
                        self.image = self.frames[self.cur_frame]
                        self.mask = pygame.mask.from_surface(self.image)
                        for i in stabel_group:
                            if pygame.sprite.collide_mask(self, i):
                                self.cur_frame += 1
                                if self.cur_frame - 4 == self.figure:
                                    self.cur_frame -= 4
                                self.image = self.frames[self.cur_frame]
                                self.mask = pygame.mask.from_surface(self.image)
            else:
                self.wait += 1
            for i in stabel_group:
                global cnt
                if pygame.sprite.collide_mask(self, i):
                    s = [i for i in range(80, 400, 40)]
                    self.rect = self.rect.move(0, -40)
                    self.kill()
                    piece(stabel_group, self.rect.x, self.rect.y, False, self.cur_frame)
                    if player.alive:
                        piece(all_sprites, s[random.randint(0, len(s) - 1)], 40, True)
                        cnt += 1

                    break
            self.count += 1

def update_end(image, speed):
    if image.rect.x + image.rect.width > width:
        speed = 0
    image.rect.x = image.rect.x + speed
    return speed



if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('tetris')
    pygame.mixer.music.load("data/Missiya_Nevypolnima_-_Mission_Impossible_Theme_Ost_Missiya_nevypolnima_Plemya_izgoev_62673572.mp3")
    pygame.mixer.music.play(0)
    size = width, height = 480, 1000
    screen = pygame.display.set_mode(size)
    screen.fill([255, 255, 255])
    piece(all_sprites, 200, 40, True)
    cadre()
    player = Player(1, 2)
    dor = door()
    kn = knopki()
    running = True
    fps = 60
    v = 5
    Pause = False
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                print(event.key)
                all_sprites.update(event.key)
                player_group.update(event)
            if event.type == pygame.KEYUP:
                player_group.update(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    Pause = not Pause
                    if Pause:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
        all_sprites.update()
        win_group.update()
        player_group.update()
        screen.fill([255, 255, 255])
        win_group.draw(screen)
        all_sprites.draw(screen)
        stabel_group.draw(screen)
        player_group.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
        screen.blit(txxt, (20, 20))
        if game_over:
            pygame.mixer.music.stop()
            time.sleep(3)
            pygame.init()
            # размеры окна:
            #size = width, height = 480, 1000
            # screen — холст, на котором нужно рисовать:
            screen = pygame.display.set_mode(size)
            all_sprites = pygame.sprite.Group()
            gm_ov = pygame.sprite.Sprite()
            if lose:
                screen.fill((0, 0, 255))
                image = load_image('gameover_lose.png')
                pygame.mixer.music.load("data/Грустный тромбон.mp3")
                pygame.mixer.music.play(0)
            else:
                screen.fill((255, 255, 0))
                image = load_image('gameover_win.png')
                pygame.mixer.music.load("data/GTA_San_Andreas.mp3")
                pygame.mixer.music.play(0, 10)
            gm_ov.image = image
            gm_ov.rect = gm_ov.image.get_rect()
            gm_ov.rect.x, gm_ov.rect.y = -600, 0
            all_sprites.add(gm_ov)
            pygame.display.flip()
            # ожидание закрытия окна:
            clock = pygame.time.Clock()
            fps = 40
            v = 5
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                for sprite in all_sprites:
                    v = update_end(sprite, v)
                all_sprites.draw(screen)
                pygame.display.flip()
                clock.tick(fps)
    pygame.quit()