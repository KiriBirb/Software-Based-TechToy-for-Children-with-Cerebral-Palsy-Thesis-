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

    pygame.mixer.music.stop()

    # Create window/display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Thesis Project Game")
    imgBackground = pygame.image.load("Resources/Food/Kitchenbg.png").convert_alpha()
    imgGameOver = pygame.image.load("Resources/Food/GameOver.png").convert_alpha()
    imgOpen = pygame.image.load("Resources/Food/DogOpen.png").convert_alpha()
    imgClose = pygame.image.load("Resources/Food/DogClose.png").convert_alpha()
    imgYum = pygame.image.load("Resources/Food/DogYum.png").convert_alpha()
    imgYuck = pygame.image.load("Resources/Food/DogYuck.png").convert_alpha()
    imgBarOutline = pygame.image.load("Resources/Food/barOutline.png").convert_alpha()
    buttonMenu = ButtonImg((800, 290), "Resources/Buttons/ButtonMenu.png",
                           pathSoundClick="Resources/MenuClick.wav",
                           pathSoundHover="Resources/Hover.wav")
    buttonPlayAgain = ButtonImg((200, 290), "Resources/Buttons/PlayAgain.png",
                           pathSoundClick="Resources/GameClick.wav",
                           pathSoundHover="Resources/Hover.wav")
    buttonTryAgain = ButtonImg((200, 290), "Resources/Buttons/TryAgain.png",
                           pathSoundClick="Resources/GameClick.wav",
                           pathSoundHover="Resources/Hover.wav")
    heartR = pygame.image.load("Resources/Food/HeartRed.png").convert_alpha()
    heartG = pygame.image.load("Resources/Food/HeartGrey.png").convert_alpha()

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
    GOsound = True

    # Set font
    font = pygame.font.Font(f"Resources/FredokaOne-Regular.ttf", 55)

    detector = FaceMeshDetector(maxFaces=1)

    idList = [0, 17, 78, 292]

    global ratio

    def get_frame(cap):
        global ratio
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

    startTime = pygame.time.get_ticks()
    maxTime = 120

    # Main loop
    while running:
        for event in pygame.event.get():
            if event.dict.get('key') == 27:
                gameOver = True

        img, ratio = get_frame(cap)

        window.blit(window, (0, 0))
        window.blit(imgBackground, (0, 0))
        window.blit(heartR, (width - 150, 10))
        window.blit(heartR, (width - 200, 10))
        window.blit(heartR, (width - 250, 10))

        if ratio > 50:
            mouthStatus = "Open"

        if ratio < 50:
            mouthStatus = "Closed"

        if mouthStatus == "Open":
            window.blit(imgOpen, (0, -75))
        else:
            window.blit(imgClose, (0, -75))

        if countdown > 0:
            countdownText = font.render(f'Get Ready!', True, (59, 108, 234), None)
            window.blit(countdownText, (510, 260))
            counting = font.render(f'{countdown}', True, (59, 108, 234), None)
            window.blit(counting, (625, 320))
            count_timer = pygame.time.get_ticks()
            if count_timer - lastCount > 1000:
                countdown -= 1
                lastCount = count_timer

        if not gameOver and countdown == 0:
            currentTime = pygame.time.get_ticks()

            time_text = font.render(f'time:{maxTime}', True, (214, 72, 111), None)
            window.blit(time_text, (width//2 + 10, 20))

            if currentTime - startTime > 1000:
                maxTime -= 1
                startTime = currentTime

            window.blit(currentObject, pos)
            pos[1] += speed

            if pos[1] > 330 and mouthStatus == "Open":
                if isEatable:
                    currentObject = resetObject()
                    Score += 1
                    pygame.mixer.Sound(f"Resources/Food/Correct.mp3").play().set_volume(0.5)
                    percent = Score/maxScore * 100
                else:
                    currentObject = resetObject()
                    pygame.mixer.Sound(f"Resources/Food/Incorrect.mp3").play().set_volume(0.5)
                    badScore -= 1

            if pos[1] > 500:
                currentObject = resetObject()

        if badScore == 2:
            window.blit(heartG, (width - 250, 10))

        if badScore == 1:
            window.blit(heartG, (width - 200, 10))
            window.blit(heartG, (width - 250, 10))

        if badScore == 0:
            window.blit(heartG, (width - 150, 10))
            window.blit(heartG, (width - 200, 10))
            window.blit(heartG, (width - 250, 10))

        progressBar(percent)
        window.blit(imgBarOutline, (0, -20))

        if Score == maxScore or badScore == 0:
            gameOver = True

        if gameOver and Score == maxScore:
            if GOsound:
                GOsound = False
                pygame.mixer.Sound(f"Resources/gameOverSound.wav").play().set_volume(0.5)
            window.blit(imgGameOver, (0, 0))
            scoreText = font.render(f'{Score}', True, (59, 108, 234), None)
            window.blit(scoreText, (620, 230))
            buttonMenu.draw(window)
            buttonPlayAgain.draw(window)
            if buttonMenu.state == "clicked":
                SceneManager.OpenScene("Menu")
            if buttonPlayAgain.state == "clicked":
                SceneManager.OpenScene("GameFood")
            window.blit(imgYum, (0, -75))

        if gameOver and maxTime <= 0:
            if GOsound:
                GOsound = False
                pygame.mixer.Sound(f"Resources/gameOverSound.wav").play().set_volume(0.5)
            window.blit(imgGameOver, (0, 0))
            scoreText = font.render(f'{Score}', True, (59, 108, 234), None)
            window.blit(scoreText, (620, 230))
            buttonMenu.draw(window)
            buttonPlayAgain.draw(window)
            if buttonMenu.state == "clicked":
                SceneManager.OpenScene("Menu")
            if buttonPlayAgain.state == "clicked":
                SceneManager.OpenScene("GameFood")
            window.blit(imgYum, (0, -75))

        if gameOver and badScore == 0:
            window.blit(imgGameOver, (0, 0))
            scoreText = font.render(f'{Score}', True, (59, 108, 234), None)
            window.blit(scoreText, (620, 230))
            buttonMenu.draw(window)
            buttonTryAgain.draw(window)

            if GOsound:
                GOsound = False
                pygame.mixer.Sound(f"Resources/gameOverSound.wav").play()

            if buttonMenu.state == "clicked":
                SceneManager.OpenScene("Menu")
            if buttonTryAgain.state == "clicked":
                SceneManager.OpenScene("GameFood")
            window.blit(imgYuck, (0, -75))

        # Update display
        pygame.display.update()
        # Set FPS
        clock.tick(fps)

if __name__ == "__main__":
    Game()