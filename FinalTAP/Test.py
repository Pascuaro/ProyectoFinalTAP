import pygame

pygame.init()

screen = pygame.display.set_mode((500, 480)) #Creamos una ventana
pygame.display.set_caption("Juego final") #Ponemos un titulo a la ventana
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()
score = 0
#bulletSound = pygame.mixer.Sound('bullet.wav')
#hitSound = pygame.mixer.Sound('hit.wav')
music = pygame.mixer.music.load("oldtown.mp3")
pygame.mixer.music.play(-1)

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.Jump = False
        self.jumpCount = 10
        self.left = True
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

    def draw(self, screen):

        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing): #Checamos que el personaje no este parado, si no lo esta, se esta moviendo hacia uno de los dos lados
            if self.left:
                screen.blit(walkLeft[self.walkCount // 3], (self.x, self.y)) #Dividimos sobre 3 porque es el numero de sprites disponibles
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))

        self.hitbox = (self.x + 17, self.y + 11, 29, 52) #Modificamos la hitbox porque si usamos el 64x64 era mas grande que el modelo del personaje
        #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.x = 60
        self.x = 410
        self.walkCount = 0
        font1 = pygame.font.SysFont('comicsans', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        screen.blit(text, (250 - (text.get_width()/2),200))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()

class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

class enemies(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'),
                 pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'),
                 pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'),
                 pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'),
                pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'),
                pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'),
                pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0 :
                screen.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                screen.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(screen, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
            #Si el personaje es visible, o sea si esta vivo, se le da una velocidad, una direccion, un punto inicial y final, y esta sera la ruta que va a seguir

    def move(self):
        if self.vel > 0:
            if self.x + self.vel< self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        #Multiplicamos el movimiento por un -1 para cambiar de direccion del enemigo
    def hit(self):
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
            #print('Hit')
        #Mientras el personaje tenga vida con cada "hit" perdera vida hasta llegar a 0 y desaparecer

def redrawGameWindow():
    screen.blit(bg, (0, 0))
    #text = font.render('Score ' + str(score), 1, (0, 0, 0))
    #screen.blit(text, (390, 10))
    Jugador.draw(screen)
    Enemigo.draw(screen)
    for bullet in bullets:
        bullet.draw(screen)

    pygame.display.update()
    #pygame.display.flip()

#font = pygame.font.SysFont('comicsans', 30, True, True)
Jugador = player(300, 410, 64, 64)
Enemigo = enemies(100, 415, 64, 64, 450)
shootLoop = 0
bullets = []
run = True
while run:
    clock.tick(27) #FPS's

    if Jugador.hitbox[1] < Enemigo.hitbox[1] + Enemigo.hitbox[3] and Jugador.hitbox[1] + Jugador.hitbox[3] > Enemigo.hitbox[1]:
        if Jugador.hitbox[0] + Jugador.hitbox[2] > Enemigo.hitbox[0] and Jugador.hitbox[0]  < Enemigo.hitbox[0] + Enemigo.hitbox[2]:
            Jugador.hit()
            score += 5


    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0
    #Este es nuestro timer para los projectiles, sin el las balas salen en "burst" al presionar la tecla de disparo

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False #Validacion para cerrar el juego

    for bullet in bullets:
        if bullet.y - bullet.radius < Enemigo.hitbox[1] + Enemigo.hitbox[3] and bullet.y + bullet.radius > Enemigo.hitbox[1]:
            if bullet.x + bullet.radius > Enemigo.hitbox[0] and bullet.x - bullet.radius < Enemigo.hitbox[0] + Enemigo.hitbox[2]:
                #Es nuestra validacion de que la bala tuvo colision con el modelo del enemigo
                #hitSound.play()
                Enemigo.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
                #La bala al tener contacto con el enemigo hace pop de la lista de balas y desaparecer de la ventana

        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            #Si la bala esta en la ventana se le da su velocidad, de lo contrario se le hace pop de la lista

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE] and shootLoop == 0:
        #bulletSound.play()
        if Jugador.left:
            facing = -1
        else:
            facing = 1
        if len(bullets) < 3:
            bullets.append(projectile(round(Jugador.x + Jugador.width // 2), round(Jugador.y + Jugador.height // 2), 6, (0, 0, 0), facing))
        shootLoop = 1

    if keys[pygame.K_LEFT] and Jugador.x > Jugador.vel:
        Jugador.x -= Jugador.vel
        Jugador.left = True
        Jugador.right = False
        Jugador.standing = False

    elif keys[pygame.K_RIGHT] and Jugador.x < 500 - Jugador.width - Jugador.vel:
        Jugador.x += Jugador.vel
        Jugador.left = False
        Jugador.right = True
        Jugador.standing = False

    else:
        Jugador.standing = True
        Jugador.walkCount = 0
    #Checamos la tecla presionada y checando el valor de "x" verificamos que nuestro objeto/personaje no pueda salirse
    #de la ventana que creamos
    if not(Jugador.Jump):
        if keys[pygame.K_UP]:
            Jugador.Jump = True
            Jugador.right = False
            Jugador.left = False
            Jugador.walkCount = 0
    #Si estamos saltando se "lockean" las teclas up & down para no tener anormalidades
    else:
        if Jugador.jumpCount >= -10:
            neg = 1

            if Jugador.jumpCount < 0:
                neg = -1

            Jugador.y -= (Jugador.jumpCount ** 2) * 0.185 * neg
            Jugador.jumpCount -= 1

        else:
            Jugador.Jump = False
            Jugador.jumpCount = 10
    #Usamos una funcion cuadratica para calcular el salto, se inicia en cierta velocidad y disminuye hasta llegar a 0
    #Despues de 0 acelera hasta la velocidad inicial, la tenemos decrementada con el * 0.5 porque era muy rapida

    redrawGameWindow()
