# Import
import pygame

# Initialize
pygame.init()
pygame.mixer.pre_init()

class ButtonImg:
    def __init__(self, pos, pathing, scale=0.8, pathSoundHover=None, pathSoundClick=None):
        # Loading Main Image
        img = pygame.image.load(pathing).convert_alpha()
        width, height = img.get_size()
        img = pygame.transform.smoothscale(img, (int(width * scale), int(height * scale)))

        # Split image to get all frames
        width, height = img.get_size()
        heightSingleFrame = int(height/3)
        self.imgList = []

        for i in range(3):
            imgCrop = img.subsurface((0, i * heightSingleFrame, width, heightSingleFrame))
            self.imgList.append(imgCrop)

        self.pos = pos
        self.state = None
        self.img = self.imgList[0]
        self.rectImg = self.imgList[0].get_rect()
        self.rectImg.topleft = self.pos
        self.pathSoundClick = pathSoundClick
        self.pathSoundHover = pathSoundHover
        if self.pathSoundHover is not None:
            self.pathSoundHover = pygame.mixer.Sound(self.pathSoundHover)
        if self.pathSoundClick is not None:
            self.pathSoundClick = pygame.mixer.Sound(self.pathSoundClick)

    def draw(self, window):
        # Get mouse position ot check if inside button
        posMouse = pygame.mouse.get_pos()
        self.img = self.imgList[0]
        if self.rectImg.collidepoint(posMouse):

            if pygame.mouse.get_pressed()[0]:
                self.img = self.imgList[2]  # Clicked
                if self.pathSoundClick is not None and self.state != "clicked":
                    self.pathSoundClick.play().set_volume(0.5)
                self.state = 'clicked'
            else:
                self.img = self.imgList[1]  # Hovering
                if self.pathSoundHover is not None and self.state != "hover" and self.state !="clicked":
                    self.pathSoundHover.play().set_volume(0.5)
                self.state = 'hover'
        else:
            self.state = None

        window.blit(self.img, self.rectImg)

if __name__ == "__main__":

    # Create window/display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Thesis Project Game")

    # Initialize clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    # Create buttons
    button1 = ButtonImg((100, 100), "Resources/Buttons/ButtonPlay.jpg", scale=0.5,
                        pathSoundClick="Resources/MenuClick.wav",
                        pathSoundHover="Resources/Hover.wav")
    # Main Loop
    start = True
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()

        # Apply logic
        window.fill((255, 255, 255))
        button1.draw(window)
        # Update display
        pygame.display.update()
