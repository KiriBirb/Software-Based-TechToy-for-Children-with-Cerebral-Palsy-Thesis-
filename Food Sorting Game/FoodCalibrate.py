import pygame
import SceneManager
from Button import ButtonImg
import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np
import random

def Game():
    # Initialize
    pygame.init()
    pygame.event.clear()

    # Create window/display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Thesis Project Game")
    imgBackground = pygame.image.load("Resources/Food/Kitchenbg.png").convert_alpha()
    imgOpen = pygame.image.load("Resources/Food/DogOpen.png").convert_alpha()
    imgClose = pygame.image.load("Resources/Food/DogClose.png").convert_alpha()
    imgBarOutline = pygame.image.load("Resources/Food/barOutline.png").convert_alpha()
    buttonStart = ButtonImg((520, height - 160), "Resources/Buttons/Start.png",
                           pathSoundClick="Resources/GameClick.wav",
                           pathSoundHover="Resources/Hover.wav")

    # All the food sprites
    Carrot = pygame.image.load("Resources/Food/Carrot.png").convert_alpha()
    Carrot = pygame.transform.scale(Carrot, (200, 200))
    Chicken = pygame.image.load("Resources/Food/Chicken.png").convert_alpha()
    Chicken = pygame.transform.scale(Chicken, (200, 200))
    Fishbone = pygame.image.load("Resources/Food/Fishbone.png").convert_alpha()
    Fishbone = pygame.transform.scale(Fishbone, (200, 200))
    Strawberry = pygame.image.load("Resources/Food/Strawberry.png").convert_alpha()
    Strawberry = pygame.transform.scale(Strawberry, (200, 200))
    Sandal = pygame.image.load("Resources/Food/Sandal.png").convert_alpha()
    Sandal = pygame.transform.scale(Sandal, (200, 200))

    eatList = [Carrot, Chicken, Strawberry]
    noneatList = [Fishbone, Sandal, Fishbone]
    currentObject = eatList[random.randint(0, 2)]
    pos = [width/2 - 100, 0]
    speed = 3

    # Initialize for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Set font
    font = pygame.font.Font(f"Resources/FredokaOne-Regular.ttf", 55)

    detector = FaceMeshDetector(maxFaces=1)

    idList = [0, 17, 78, 292]

    ratio = 1

    def get_frame(cap):
        _, img = cap.read()
        img = cv2.resize(img, (width, height))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img, faces = detector.findFaceMesh(img, draw=False)

        if faces:
            face = faces[0]
            for id in idList:
                cv2.circle(img, face[id], 5, (255, 0, 255), 5)
            cv2.line(img, face[idList[0]], face[idList[1]], (0,255,0), 3)
            cv2.line(img, face[idList[2]], face[idList[3]], (0, 255, 0), 3)

            vertical, _ = detector.findDistance(face[idList[0]], face[idList[1]])
            horizontal, _ = detector.findDistance(face[idList[2]], face[idList[3]])

            ratio = int((vertical/horizontal) * 100)

        img = np.rot90(img)
        img = pygame.surfarray.make_surface(img)
        return img, ratio

    running = True
    gameOver = False
    Score = 0
    maxScore = 10
    badScore = 3
    countdown = 4
    lastCount = pygame.time.get_ticks()

    cap = cv2.VideoCapture(0)

    global isEatable
    isEatable = True

    def resetObject():
        global isEatable

        pos[0] = width/2 - 100
        pos[1] = 0
        randNo = random.randint(0, 2)

        if randNo == 0:
            currentObject = noneatList[random.randint(0, 2)]
            isEatable = False
        else:
            currentObject = eatList[random.randint(0, 2)]
            isEatable = True
        return currentObject

    percent = 0

    def progressBar(percent):
        progress = percent/100 * 600
        pygame.draw.rect(window, (0, 255, 0), (20, 30, progress, 50))

    # Main loop
    while running:
        for event in pygame.event.get():
            if event.dict.get('key') == 27:
                gameOver = True

        img, Ratio = get_frame(cap)

        window.blit(window, (0, 0))
        window.blit(imgBackground, (0, 0))

        if Ratio > 50:
            mouthStatus = "Open"

        if Ratio < 50:
            mouthStatus = "Closed"

        if mouthStatus == "Open":
            window.blit(imgOpen, (0, -75))
        else:
            window.blit(imgClose, (0, -75))

        window.blit(imgBarOutline, (0, -20))
        Status = font.render(f'{mouthStatus}', True, (59, 108, 234), None)
        window.blit(Status, (550, 100))
        buttonStart.draw(window)

        if buttonStart.state == "clicked":
            SceneManager.OpenScene("GameFood")


        # Update display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)

if __name__ == "__main__":
    Game()