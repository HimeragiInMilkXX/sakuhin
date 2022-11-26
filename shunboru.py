import pygame, sys, os, webbrowser
from random import randint
from PIL import Image

pygame.init()

screenWidth = 750
screenHeight = 750

win = pygame.display.set_mode( ( screenWidth, screenHeight ) )
pygame.display.set_caption( "瞬ボール" )

icon = pygame.image.load( 'icon.png' )
pygame.display.set_icon( icon )

fps = 120
clock = pygame.time.Clock()

playerimgleft = [ pygame.image.load( 'Spaceman_Sprite\L1.png' ), pygame.image.load( 'Spaceman_Sprite\L2.png' ), pygame.image.load( 'Spaceman_Sprite\L3.png' ),
                  pygame.image.load( 'Spaceman_Sprite\L4.png' ), pygame.image.load( 'Spaceman_Sprite\L5.png' ), pygame.image.load( 'Spaceman_Sprite\L6.png' ),
                  pygame.image.load( 'Spaceman_Sprite\L7.png' ), pygame.image.load( 'Spaceman_Sprite\L8.png' ) ]
playerimgright = [ pygame.image.load( 'Spaceman_Sprite\R1.png' ), pygame.image.load( 'Spaceman_Sprite\R2.png' ), pygame.image.load( 'Spaceman_Sprite\R3.png' ),
                   pygame.image.load( 'Spaceman_Sprite\R4.png' ), pygame.image.load( 'Spaceman_Sprite\R5.png' ), pygame.image.load( 'Spaceman_Sprite\R6.png' ),
                   pygame.image.load( 'Spaceman_Sprite\R7.png' ), pygame.image.load( 'Spaceman_Sprite\R8.png' ) ]
asteroidimg = [ pygame.image.load( 'Asteroid_Sprite\A1.png' ), pygame.image.load( 'Asteroid_Sprite\A2.png' ), pygame.image.load( 'Asteroid_Sprite\A3.png' ), pygame.image.load( 'Asteroid_Sprite\A4.png' ),
                pygame.image.load( 'Asteroid_Sprite\A5.png' ), pygame.image.load( 'Asteroid_Sprite\A6.png' ), pygame.image.load( 'Asteroid_Sprite\A7.png' ), pygame.image.load( 'Asteroid_Sprite\A8.png' ),
                pygame.image.load( 'Asteroid_Sprite\A9.png' ), pygame.image.load( 'Asteroid_Sprite\A10.png' ), pygame.image.load( 'Asteroid_Sprite\A11.png' ), pygame.image.load( 'Asteroid_Sprite\A12.png' ),
                pygame.image.load( 'Asteroid_Sprite\A13.png' ), pygame.image.load( 'Asteroid_Sprite\A14.png' ), pygame.image.load( 'Asteroid_Sprite\A15.png' ), pygame.image.load( 'Asteroid_Sprite\A16.png' ),
                pygame.image.load( 'Asteroid_Sprite\A17.png' ), pygame.image.load( 'Asteroid_Sprite\A18.png' ), pygame.image.load( 'Asteroid_Sprite\A19.png' ), pygame.image.load( 'Asteroid_Sprite\A20.png' ) ]                
backgroundimg = pygame.image.load( 'background.png' )
menuimg = pygame.image.load( 'menu.png' )
howtoimg = pygame.image.load( 'howto.png' )

#-Player Data-#
score = 0
txt = "Score: {:.0f}/{:.0f}"
pb = 0

# Check if not exist or empty
if( not os.path.exists( "record.txt" ) or os.path.getsize('record.txt') == 0 ):
    file = open( "record.txt", 'w' )
    file.write( "0" )
else:
    file = open( "record.txt", 'r' )
    pb = int( file.read() )

file.close()

# Getter of PB
def personalBest():

    global pb

    if( round(score) > pb ):
        pb = score
        file = open( "record.txt", 'w' )
        file.write( "{:.0f}".format( score ) )
        file.close()
        return True

    return False

def pB():

    global pb
    file = open( "record.txt", 'r' )
    pb = int( file.read() )
    file.close()

scoreFactor = 0.01
def updateScore():

    global score
    score += scoreFactor

#-Player Sprite-#
class Player( pygame.sprite.Sprite ):

    def __init__( self, vel ): 
        pygame.sprite.Sprite.__init__( self )
        self.count = 0
        self.image = playerimgright[ int( self.count ) ]
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y = 300
        self.vel = vel
        self.left = False

    def update( self ):

        if self.left:
            self.image = playerimgleft[ int( self.count ) ]
        else:
            self.image = playerimgright[ int( self.count ) ]

        keys = pygame.key.get_pressed()

        if keys[ pygame.K_UP ] and self.rect.y > self.vel:
            self.rect.y -= self.vel
            background.y -= 0.2
        if keys[ pygame.K_DOWN ] and self.rect.y < screenHeight - self.rect.height - self.vel:
            self.rect.y += self.vel
            background.y += 0.2
        if keys[ pygame.K_LEFT ] and self.rect.x > self.vel:
            self.rect.x -= self.vel
            background.x -= 0.2
            self.left = True
        if keys[ pygame.K_RIGHT ] and self.rect.x < screenWidth - self.rect.width - self.vel:
            self.rect.x += self.vel
            background.x += 0.2
            self.left = False

        if keys[ pygame.K_LEFT ] or keys[ pygame.K_RIGHT ]:
            self.count += 0.1
            if( self.count > 7 ): self.count = 0

player_sprites = pygame.sprite.Group()
player = Player( 2 )
player_sprites.add( player )


#-Ball Sprite-#
class Ball( pygame.sprite.Sprite ):

    def __init__( self, vel ):
        pygame.sprite.Sprite.__init__( self )
        self.count = randint( 0, 19 )
        self.image = asteroidimg[ self.count ]
        self.rect = self.image.get_rect()
        # Vertical(y as main axis)? TopDown(go down)? LeftRight(go right)?
        self.directionSet = [ False, False, False ]

        # Determine Whole Movement
        self.direction()
        self.start_end = self.generatePosition()
        self.mainVel = vel
        self.subVel = self.subAxisVel()

    def direction( self ):
        # Vertical Indicator
        if( randint( 0, 1 ) == 1 ): self.directionSet[0] = True
        # TopDown Indicator
        if( randint( 0, 1 ) == 1 ): self.directionSet[1] = True
        # LeftRight Indicator
        if( randint( 0, 1 ) == 1 ): self.directionSet[2] = True

    def generatePosition( self ):
        # [x, y], [x, y] Start, End
        result = [ [ 0, 0 ], [ 0, 0 ] ]
        temp = 0

        # All base on topdown leftright
        # Y as main
        if( self.directionSet[0] ):
            result[0][1] = -30
            result[1][1] = 780
            result[0][0] = randint( -15, 765 )
            result[1][0] = randint( -15, 765 )
        # X as main
        else:
            result[0][0] = -15
            result[1][0] = 765
            result[0][1] = randint( -30, 780 )
            result[1][1] = randint( -30, 780 )

        if( not self.directionSet[1] ):
            temp = result[0][1]
            result[0][1] = result[1][1]
            result[1][1] = temp
        if( not self.directionSet[2] ):
            temp = result[0][0]
            result[0][0] = result[1][0]
            result[1][0] = temp

        return result

    def subAxisVel( self ):
        # Y as main
        if( self.directionSet[0] ):
            return abs( ( self.start_end[0][0] - self.start_end[1][0] ) / ( self.start_end[0][1] - self.start_end[1][1] ) ) + self.mainVel
        # X as main
        else:
            return abs( ( self.start_end[0][1] - self.start_end[1][1] ) / ( self.start_end[0][0] - self.start_end[1][0] ) ) + self.mainVel

    # True if end, False if moving
    def update( self ):

        self.rect.x = self.start_end[0][0]
        self.rect.y = self.start_end[0][1]

        # Change Image
        self.count += 0.2
        if( self.count > 19 ): self.count = 0
        self.image = asteroidimg[ int( self.count ) ]
        # Movement
        # X as main, TopDown, LeftRight
        if( not self.directionSet[0] ):

            if( self.directionSet[1] ):
                self.start_end[0][1] += self.subVel
            else:
                self.start_end[0][1] -= self.subVel

            if( self.directionSet[2] ):
                self.start_end[0][0] += self.mainVel
            else:
                self.start_end[0][0] -= self.mainVel

        # Y as main, TopDown, LeftRight
        elif( self.directionSet[0] ):
            if( self.directionSet[1] ):
                self.start_end[0][1] += self.mainVel
            else:
                self.start_end[0][1] -= self.mainVel

            if( self.directionSet[2] ):
                self.start_end[0][0] += self.subVel
            else:
                self.start_end[0][0] -= self.subVel

    def checkLeave( self ):

        if( self.directionSet[0] ):
            if( self.directionSet[1] ):
                if( self.start_end[0][1] >= self.start_end[1][1] ): return True
            else:
                if( self.start_end[0][1] <= self.start_end[1][1] ): return True
        else:
            if( self.directionSet[2] ):
                if( self.start_end[0][0] >= self.start_end[1][0] ): return True
            else:
                if( self.start_end[0][0] <= self.start_end[1][0] ): return True

        return False

    def debugConsole( self ):
        print( "TopDown: " + str( self.directionSet[1] ) )
        print( "LeftRight: " + str( self.directionSet[2] ) )

        if( self.directionSet[0] ): print( "Y Main" )
        else: print( "X Main" )

        print( "[ " + str( self.start_end[0][0] ) + ", " + str( self.start_end[0][1] ) + " ]")


asteroid_sprites = pygame.sprite.Group()
asteroids = 5
added = [ False, False, False, False ]
ballVel = 2
level = 1

best = False
def checkCollision():

    global crashed, best

    if len( pygame.sprite.spritecollide( player, asteroid_sprites, False ) ) > 0:
        for ball in asteroid_sprites: asteroid_sprites.remove( ball )
        crashed = True

    if( personalBest() ): best = True

EndFont = pygame.font.Font( 'Pixel Font\ARCADECLASSIC.TTF', 70 )
EndSurf = EndFont.render( 'Game Over', False, 'White' )
EndRect = EndSurf.get_rect( center = ( 387, 300 ) )
SpaceFont = pygame.font.Font( 'Pixel Font\ARCADECLASSIC.TTF', 30 )
SpaceSurf = SpaceFont.render( 'Press SPACE to restart', False, ( 255, 250, 250 ) )
SpaceRect = SpaceSurf.get_rect( center = ( 387, 355 ) )
BSurf = SpaceFont.render( 'Press B to menu', False, ( 255, 250, 250 ) )
BRect = BSurf.get_rect( center = ( 387, 390 ) )
def drawEndMessage():

    win.blit( EndSurf, EndRect )
    win.blit( SpaceSurf, SpaceRect )
    win.blit( BSurf, BRect )

ScoreFont = pygame.font.Font( 'Pixel Font\ARCADECLASSIC.TTF', 40 )
ScoreMessage = ScoreFont.render( txt.format( score, pb ), 1, 'white' )
def drawScoreMessage():

    global scoreMessage
    if best and crashed:
        ScoreMessage = ScoreFont.render( "New Personal Best! {:.0f}".format( score ), 1, 'white' )
    else:
        ScoreMessage = ScoreFont.render( txt.format( score, pb ), 1, 'white' )

    win.blit( ScoreMessage, ( 20, 15 ) )

StartFont = pygame.font.Font( 'Pixel Font\ARCADECLASSIC.TTF', 50 )
StartSurf = StartFont.render( 'Press SPACE to start', False, 'White' )
StartRect = StartSurf.get_rect( center = ( 375, 600 ) )
def drawStartMessage():

    win.blit( StartSurf, StartRect )

LevelFont =  pygame.font.Font( 'Pixel Font\ARCADECLASSIC.TTF', 40 )
LevelMessage = LevelFont.render( 'Level ' + str(level), 1, 'white' )
def drawLevelMessage():

    global LevelMessage
    LevelMessage = LevelFont.render( 'Level ' + str(level), 1, 'white' )
    win.blit( LevelMessage, ( 625, 15 ) )

# Stage, Record, Howto
selectList = [ True, False, False ]
SelectFont = pygame.font.Font( 'Pixel Font\ARCADECLASSIC.TTF', 70 )
SelectSurf = [ SelectFont.render( '> Start <', False, 'White' ), SelectFont.render( 'Start', False, 'White' ), SelectFont.render( '> ' + str(pb) + ' <', False, 'White' ), SelectFont.render( 'Personal Best', False, 'White' ), SelectFont.render( '> HowTo <', False, 'White' ), SelectFont.render( 'HowTo', False, 'White' ) ]
SelectRect = [ SelectSurf[0].get_rect( center = ( 375, 200 ) ), SelectSurf[1].get_rect( center = ( 375, 200 ) ), SelectSurf[2].get_rect( center = ( 375, 400 ) ), SelectSurf[3].get_rect( center = ( 375, 400 ) ), SelectSurf[4].get_rect( center = ( 375, 600 ) ), SelectSurf[5].get_rect( center = ( 375, 600 ) ) ]
def drawSelectWindow():

    SelectSurf[2] = SelectFont.render( '> ' + str(pb) + ' <', False, 'White' )
    SelectRect[2] = SelectSurf[2].get_rect( center = ( 375, 400 ) )

    if( selectList[0] and not selectList[1] and not selectList[2] ): # Stage
        win.blit( SelectSurf[0], SelectRect[0] )
        win.blit( SelectSurf[3], SelectRect[3] )
        win.blit( SelectSurf[5], SelectRect[5] )
    elif( not selectList[0] and selectList[1] and not selectList[2] ): # Record
        win.blit( SelectSurf[1], SelectRect[1] )
        win.blit( SelectSurf[2], SelectRect[2] )
        win.blit( SelectSurf[5], SelectRect[5] )
    elif( not selectList[0] and not selectList[1] and selectList[2] ): # Howto
        win.blit( SelectSurf[1], SelectRect[1] )
        win.blit( SelectSurf[3], SelectRect[3] )
        win.blit( SelectSurf[4], SelectRect[4] )


def restart():

    for stone in asteroid_sprites:
        asteroid_sprites.remove( stone )

    global crashed
    crashed = False

    global best
    best = False

    global menu, game, select, howto
    menu = False
    select = False
    game = True

    global ballVel, scoreFactor, asteroids, added, level
    ballVel = 2
    scoreFactor = 0.01
    asteroids = 8
    added = [ False, False, False, False ]
    level = 1

    global player
    player.rect.x = 300
    player.rect.y = 300

    for i in range ( asteroids ):
        asteroid_sprites.add( Ball( ballVel ) )

    global score
    score = 0

#-Background Class-#
class Background():

    def __init__( self ):
        self.x = -150
        self.y = -150

background = Background()

def gameLevel():

    global ballVel, scoreFactor, asteroids, added, level

    # 1. 10 asteroids
    # 2. + floating (30)
    # 3. + faster asteroids(50)
    # 4. + slower score increment + faster asteroids(70)
    # 5. + 2,1,1,1 asteroids(100, 110, 120, 130)

    for stone in asteroid_sprites:
        if( stone.checkLeave() ):
            asteroid_sprites.remove( stone )
            asteroid_sprites.add( Ball( ballVel ) )

    asteroid_sprites.update()
    asteroid_sprites.draw( win )

    if( level == 1 ):

        if( randint( 0, 1 ) == 0 ): # UP
            player.rect.y -= 1
            background.y -= 0.1
        if( randint( 0, 1 ) == 0 ): # DOWN
            player.rect.y += 1
            background.y += 0.1
        if( randint( 0, 3 ) == 0 ): # LEFT
            player.rect.x -= 1
            background.x -= 0.1
        if( randint( 0, 3 ) == 0 ): # RIGHT
            player.rect.x += 1
            background.x += 0.1


    if( score >= 30 ):

        level = 2

        if( randint( 0, 1 ) == 0 ):

            if( randint( 0, 1 ) == 0 ): # UP
                if player.rect.y > 5:
                    for i in range(5):
                        player.rect.y -= 1
                        background.y -= 0.1
            if( randint( 0, 1 ) == 0 ): # DOWN
                if player.rect.y < screenHeight - player.rect.height - 3:
                    for i in range(5):
                        player.rect.y += 1
                        background.y += 0.1
            if( randint( 0, 3 ) == 0 ): # LEFT
                if player.rect.x > 10:
                    for i in range(10):
                        player.rect.x -= 1
                        background.x -= 0.1
            if( randint( 0, 3 ) == 0 ): # RIGHT
                if player.rect.x < screenWidth - player.rect.width - 10:
                    for i in range(10):
                        player.rect.x += 1
                        background.x += 0.1

    if( score >= 40 ):
        level = 3
        ballVel = 3

    if( score >= 50 ):
        level = 4
        scoreFactor = 0.005
        ballVel = 4

    if( score >= 70 and not added[0] ):
        level = 5
        asteroid_sprites.add( Ball( ballVel ) )
        asteroid_sprites.add( Ball( ballVel ) )
        added[0] = True

    if( score >= 75 and not added[1] ):
        asteroid_sprites.add( Ball( ballVel ) )
        added[1] = True

    if( score >= 80 and not added[2] ):
        asteroid_sprites.add( Ball( ballVel ) )
        added[2] = True

    if( score >= 85 and not added[3] ):
        asteroid_sprites.add( Ball( ballVel ) )
        added[3] = True


crashed = False
run = True
messageCount = 3
game = False
menu = True
select = False
pressed = False
while run:

    clock.tick( fps )

    pB()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            sys.exit()

    win.fill( ( 0, 0, 0 ) )
    win.blit( backgroundimg, ( background.x, background.y ) )

    if( game ):

        gameLevel()

        checkCollision()

        if( not crashed ):
            player_sprites.draw( win )
            player_sprites.update()
            updateScore()

        else:
            if( messageCount == 3 ):
                drawEndMessage()
                messageCount = 0
            messageCount += 1

            if( pygame.key.get_pressed()[pygame.K_b] ):
                menu = True
                game = False
                select = False

        if( pygame.key.get_pressed()[pygame.K_SPACE] ):
            pressed = True
        else:
            if( pressed ):
                restart()

            pressed = False

        drawScoreMessage()
        drawLevelMessage()

    elif( menu ):

        menuRect = menuimg.get_rect( center = ( 375, 300 ) )
        win.blit( menuimg, menuRect )

        if( messageCount == 3 ):
            drawStartMessage()
            messageCount = 0
        messageCount += 1

        if( pygame.key.get_pressed()[pygame.K_SPACE] ):
            pressed = True
        else:
            if( pressed ):
                menu = False
                game = False
                select = True

            pressed = False

    elif( select ):

        if( pygame.key.get_pressed()[pygame.K_RETURN] ):

            if( selectList[0] and not selectList[1] and not selectList[2] ): # Stage
                restart()
            elif( not selectList[0] and not selectList[1] and selectList[2] ): # Howto
                os.system( 'howto.png' )

        else:

            if( pygame.key.get_pressed()[pygame.K_SPACE] ):
                pressed = True
            else:
                if( pressed ):
                    if( selectList[0] and not selectList[1] and not selectList[2] ): # Stage
                        selectList = [ False, True, False ]
                    elif( not selectList[0] and selectList[1] and not selectList[2] ): # Record
                        selectList = [ False, False, True ]
                    elif( not selectList[0] and not selectList[1] and selectList[2] ):
                        selectList = [ True, False, False ]

                pressed = False

        drawSelectWindow()

    pygame.display.update()

pygame.quit()
