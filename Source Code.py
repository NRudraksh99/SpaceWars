import pygame as py
import os
import sys

py.init()

py.font.init()
py.mixer.init()

W=py.display.set_mode((1200,900))
height,width=900,1200
py.display.set_caption("Space Wars")

black=(0,0,0)
green=(0,255,30)
Red=(255,0,0)
Yellow=(255,255,0)
bgi=py.transform.scale(py.image.load(os.path.join("Images","Background.jpg")),(width,height))

border=py.Rect(595,0,10,900)

HFont=py.font.Font(os.path.join("Fonts","pkmnrs.ttf"),40)

WinnerText=py.font.Font(os.path.join("Fonts","pkmnem.ttf"),100)

FPS=60
vel=5

Yhit=py.USEREVENT+1
Rhit=py.USEREVENT+2

Ybullet,Rbullet=[],[]
rb,yb=[],[]
b_vel=10
max_bullet=3

bulletHitSound=py.mixer.Sound(os.path.join("Audio","HitEnemy.wav"))
yShoot=py.mixer.Sound(os.path.join("Audio","Shoot.wav"))
rShoot=py.mixer.Sound(os.path.join("Audio","Shoot.wav"))

S1=py.image.load(os.path.join("Images","SpaceshipR.png"))
S1=py.transform.rotate((py.transform.scale(S1,(120,100))),90)

S2=py.image.load(os.path.join("Images","SpaceshipY.png"))
S2=py.transform.rotate((py.transform.scale(S2,(120,100))),270)

#Background Music
bgm=py.mixer.Sound(os.path.join("Audio","BGM.wav"))
bgm.play(-1)

def RedMove(key,red):
    if key[py.K_w] and red.y-vel>0: #LeftUP
        red.y-=vel
    if key[py.K_s] and red.y+vel+red.height<height-5: #LeftDOWN
        red.y+=vel
    if key[py.K_a] and red.x-vel>0: #LeftLEFT
        red.x-=vel
    if key[py.K_d] and red.x+vel+red.width<border.x: #LeftRIGHT
        red.x+=vel

def YellowMove(key,yellow):
    if key[py.K_UP] and yellow.y-vel>0: #RightUP
        yellow.y-=vel
    if key[py.K_DOWN] and yellow.y+vel+yellow.height<height-5: #RightDOWN
        yellow.y+=vel
    if key[py.K_LEFT] and yellow.x-vel>border.x+border.width: #RightLEFT
        yellow.x-=vel
    if key[py.K_RIGHT] and yellow.x+vel+yellow.width<width: #RightRIGHT
        yellow.x+=vel

def drawWindow(red,yellow,Rbullet,Ybullet,RHealth,YHealth):
    W.blit(bgi,(0,0))
    py.draw.rect(W,black,border)
    W.blit(S2,(yellow.x,yellow.y))
    W.blit(S1,(red.x,red.y))

    RHealthText=HFont.render("Health: "+str(RHealth),1,green)
    YHealthText=HFont.render("Health: "+str(YHealth),1,green)

    W.blit(YHealthText,(width-RHealthText.get_width()-15,10))
    W.blit(RHealthText,(5,10))
    
    for bullet in Rbullet:
        py.draw.rect(W,Red,bullet)
    for bullet in Ybullet:
        py.draw.rect(W,Yellow,bullet)

    
    py.display.update()

def MoveBullet(Ybullet,Rbullet,yellow,red):
    for i in Rbullet:
        i.x+=b_vel
        if yellow.colliderect(i):
            py.event.post(py.event.Event(Yhit))
            Rbullet.remove(i)
        if i.x>1200:
            Rbullet.remove(i)
    for i in Ybullet:
        i.x-=b_vel
        if red.colliderect(i):
            py.event.post(py.event.Event(Rhit))
            Ybullet.remove(i)
        if i.x<0:
            Ybullet.remove(i)

def Winner(t):
    draw=WinnerText.render(t,1,(191,170,29))
    W.blit(draw,(250,470))
    py.display.update()
    bgm.stop()
    py.time.delay(5000)
    
def main():
    RHealth,YHealth=225,225
    red=py.Rect(100,350,120,100)
    yellow=py.Rect(950,350,120,100)
    c=py.time.Clock()
    r=True
    while r:
        c.tick(FPS)
        for i in py.event.get():
            if i.type==py.QUIT:
                r=False
                py.quit()
                sys.exit()
            if i.type==py.KEYDOWN:
                if i.key==py.K_LCTRL and len(Rbullet)<max_bullet:
                    bullet=py.Rect(red.x+red.width,red.y+red.height//2-2,10,5)
                    Rbullet.append(bullet)
                    rShoot.play()
                if i.key==py.K_RCTRL and len(Ybullet)<max_bullet:
                    bullet=py.Rect(yellow.x,yellow.y+yellow.height//2-2,10,5)
                    Ybullet.append(bullet)
                    yShoot.play()
            if i.type==Rhit:
                RHealth-=15
                bulletHitSound.play()
            if i.type==Yhit:
                YHealth-=15
                bulletHitSound.play()
        Text=""
        if RHealth<=0:
            Text="Yellow Player Wins!"
            Winner(Text)
            py.quit()
        if YHealth<=0:
            Text="Red player Wins!"
            Winner(Text)
            py.quit()
        if Text!="":
            break
        key=py.key.get_pressed()
        RedMove(key,red)
        YellowMove(key,yellow)

        MoveBullet(Ybullet,Rbullet,yellow,red)
        drawWindow(red,yellow,Rbullet,Ybullet,RHealth,YHealth)
    py.quit()
    sys.exit()
if __name__=="__main__":
    main()
