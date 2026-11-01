### STACKING GAME

## Variables that you can change are below:
# If you want to remove this section, make sure to edit the following variables yourself in the main code
global game_title, screen_size, screen_color, ground_color, ground_height, pause_color
game_title = "Stacking Game"
screen_size = (600,800)
screen_color = (135,206,235)
ground_color = (124,252,0)
ground_height = 100
pause_color = (0,0,0)

## Modules
import pygame
from time import sleep

## Functions

# Score Function
def show_score(score):
    scoreFont = pygame.font.Font("freesansbold.ttf",64)
    scoreText = scoreFont.render(str(score),True,(255,255,255))
    if score < 10:
        screen.blit(scoreText,(290,25))
    else:
        screen.blit(scoreText,(270,25))

# Click Function
def get_latest_click():
  if pygame.mouse.get_pressed():
    mouseClickX,mouseClickY = pygame.mouse.get_pos()
    return mouseClickX, mouseClickY

# Pausing (returns False if the window was closed while paused)
def pause_game():
    unpaused = False
    cover = pygame.Surface(screen_size)
    cover.fill(pause_color)
    cover.set_alpha(128)
    screen.blit(cover,(0,0))
    pygame.display.update()
    while not unpaused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    unpaused = True
        clock.tick(30)
    return True

# Play Again Function
def play_again():
    playAgain = "not picked"
    tryAgainCoords = (100,100)
    quitCoords = (screen_size[0]-200,100)
    screen.fill((0,0,0))
    pygame.draw.rect(screen,(0,255,0),pygame.Rect(tryAgainCoords[0],tryAgainCoords[1],100,100))
    pygame.draw.rect(screen,(255,0,0),pygame.Rect(quitCoords[0],quitCoords[1],100,100))
    pygame.display.update()
    while playAgain == "not picked":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playAgain = "picked"
                gameStatus = "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseClickX,mouseClickY = get_latest_click()
                if mouseClickX >= tryAgainCoords[0] and mouseClickX <= tryAgainCoords[0]+100 and mouseClickY >= tryAgainCoords[1] and mouseClickY <= tryAgainCoords[1] + 100:
                    playAgain = "picked"
                    gameStatus = "ongoing"
                if mouseClickX >= quitCoords[0] and mouseClickX <= quitCoords[0]+100 and mouseClickY >= quitCoords[1] and mouseClickY <= quitCoords[1] + 100:
                    playAgain = "picked"
                    gameStatus = "quit"
        clock.tick(30)
    return gameStatus

# Initialization
pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption(game_title)
clock = pygame.time.Clock()
ground = pygame.Surface((screen_size[0],ground_height))
ground.fill(ground_color)

def game():
    gameStatus = "ongoing"
    pause = False

    score = 1
    block = pygame.Surface((400,50))
    block.fill((255,255,255))
    speed = 0.5
    height = 600
    direction = 1
    movingXL = 0
    movingXR = movingXL+400
    placedBlocks = [block]
    placedXL = [100]
    placedXR = [placedXL[0]+400]
    placedY = [650]
    groundDist = 0
    blockWidth = 400
    numBlocks = 1
    newBlock = True
    fade = 255
    greenFade = False
    faded = True
    background_color = screen_color

    # Game Loop
    running = True
    while running:

        # Background
        screen.fill(background_color)
        screen.blit(ground,(0,screen_size[1]-ground_height+groundDist))

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                gameStatus = "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    if movingXL > placedXR[-1] or movingXR < placedXL[-1]:
                        running = False
                        gameStatus = "over"
                    else:
                        if movingXL > placedXL[-1] and movingXL < placedXR[-1]:
                            placedXL.append(movingXL)
                            placedXR.append(placedXR[-1])
                            blockWidth -= movingXR - placedXR[-1]
                        elif movingXL < placedXL[-1] and movingXR > placedXL[-1]:
                            placedXL.append(placedXL[-1])
                            placedXR.append(movingXR)
                            blockWidth -= placedXL[-1] - movingXL
                        elif movingXL == placedXL[-1]:
                            placedXL.append(movingXL)
                            placedXL.append(movingXR)
                        score += 1
                        numBlocks += 1
                        speed += 0.1
                        placedBlocks.append(pygame.Surface((blockWidth,50)))
                        block = pygame.Surface((blockWidth,50))
                        block.fill((255,255,255))
                        faded = False
                        fade = 0
                        if abs(placedXL[-1]-movingXL) <= 0.025*blockWidth:
                            placedBlocks[-1].fill((fade,255,fade))
                            greenFade = True
                        else:
                            placedBlocks[-1].fill((255,255,fade))
                            greenFade = False
                        placedY.append(height)
                        height -= 50
                        direction *= -1
                        moving = False
                        newBlock = True

                # Pausing
                if event.key == pygame.K_p:
                    pause = True
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseClickX,mouseClickY = get_latest_click()
            

        # Check height
        if height < 100:
            height = 100
            groundDist += 50
            for i in range(numBlocks):
                placedY[i] += 50

        # Spawn new block
        if newBlock:
            if direction == 1:
                movingXL = -blockWidth
            elif direction == -1:
                movingXL = screen_size[0]
            movingXR = movingXL+blockWidth
            moving = True
            newBlock = False
        if moving:
            movingXL += speed*direction
            movingXR = movingXL+blockWidth
            if (direction == 1 and movingXR > screen_size[0]) or (direction == -1 and movingXL < 0):
                direction *= -1
            screen.blit(block,(movingXL,height))

        # Blocks
        for i in range(numBlocks):
            screen.blit(placedBlocks[i],(placedXL[i],placedY[i]))

        # Color fading
        if not faded:
            fade += 4
            if fade >= 255:
                fade = 255
                faded = True
                greenFade = False
            if greenFade:
                placedBlocks[-1].fill((fade,255,fade))
            else:
                placedBlocks[-1].fill((255,255,fade))

        # Score
        show_score(score)

        # Background change based on score
        if score >= 10 and score < 20:
            background_color = (66,105,47)
        elif score >= 20 and score < 30:
            background_color = (255,220,0)
        elif score >= 30 and score < 40:
            background_color = (255,94,5)
        elif score >= 40 and score < 50:
            background_color = (250,10,0)
        elif score >= 50:
            background_color = (255,0,255)

        if pause and running:
            if not pause_game():
                running = False
                gameStatus = "quit"
            pause = False

        sleep(0.005)
        pygame.display.update()
    return gameStatus
        

        
# Main Function
def main():
    gameStatus = "ongoing"
    while gameStatus == "ongoing":
        gameStatus = game()
        if gameStatus == "over":
            gameStatus = play_again()
    pygame.quit()


if __name__ == "__main__":
    main()