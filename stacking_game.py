### STACKING GAME

## Variables that you can change are below:
# If you want to remove this section, make sure to edit the following variables yourself in the main code
game_title = "Stacking Game"
screen_size = (600,800)
screen_color = (135,206,235)
ground_color = (124,252,0)
ground_height = 100
pause_color = (0,0,0)
frame_rate = 120
start_speed = 100 # pixels per second
speed_increase = 20 # added to the speed after each block is placed
high_score_file = "highscore.txt" # saved in the same folder as this script

## Modules
import os
import pygame

## Functions

# Score Function
def show_score(score):
    scoreCenter = (screen_size[0]//2,57)
    # Dark shadow underneath keeps the score readable on light backgrounds
    shadowText = scoreFont.render(str(score),True,(0,0,0))
    screen.blit(shadowText,shadowText.get_rect(center=(scoreCenter[0]+3,scoreCenter[1]+3)))
    scoreText = scoreFont.render(str(score),True,(255,255,255))
    screen.blit(scoreText,scoreText.get_rect(center=scoreCenter))

# Block Drawing Function (outlined so blocks stand out on any background)
def draw_block(block,x,y):
    screen.blit(block,(x,y))
    pygame.draw.rect(screen,(40,40,40),block.get_rect(topleft=(x,y)),2)

# High Score Functions (a missing or unreadable file just means no high score yet)
def load_high_score():
    try:
        with open(high_score_path) as file:
            return max(int(file.read().strip()),0)
    except (OSError,ValueError):
        return 0

def save_high_score(score):
    try:
        with open(high_score_path,"w") as file:
            file.write(str(score))
    except OSError:
        pass

# High Score Line Function (progress below 1 draws the line partway across, for the sweep animation)
def draw_best_line(y,label,progress=1):
    lineEnd = screen_size[0]*progress
    # Dark edge keeps the red line visible on the red background
    pygame.draw.line(screen,(0,0,0),(0,y),(lineEnd,y),8)
    pygame.draw.line(screen,(255,0,0),(0,y),(lineEnd,y),4)
    if progress >= 1:
        shadowText = labelFont.render(label,True,(0,0,0))
        screen.blit(shadowText,shadowText.get_rect(bottomright=(screen_size[0]-6,y-4)))
        labelText = labelFont.render(label,True,(255,0,0))
        screen.blit(labelText,labelText.get_rect(bottomright=(screen_size[0]-8,y-6)))

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
def play_again(score,highScore,newBest):
    playAgain = "not picked"
    centerX = screen_size[0]//2
    titleFont = pygame.font.Font("freesansbold.ttf",64)
    scoreFont = pygame.font.Font("freesansbold.ttf",48)
    bestFont = pygame.font.Font("freesansbold.ttf",32)
    buttonFont = pygame.font.Font("freesansbold.ttf",32)
    tryAgainButton = pygame.Rect(0,0,220,80)
    tryAgainButton.center = (centerX,450)
    quitButton = pygame.Rect(0,0,220,80)
    quitButton.center = (centerX,570)

    screen.fill((0,0,0))
    titleText = titleFont.render("GAME OVER",True,(255,255,255))
    screen.blit(titleText,titleText.get_rect(center=(centerX,150)))
    scoreText = scoreFont.render("Score: "+str(score),True,(255,255,255))
    screen.blit(scoreText,scoreText.get_rect(center=(centerX,270)))
    if newBest:
        bestText = bestFont.render("New best!",True,(255,0,0))
    else:
        bestText = bestFont.render("Best: "+str(highScore),True,(255,255,255))
    screen.blit(bestText,bestText.get_rect(center=(centerX,330)))
    for button,color,label in ((tryAgainButton,(0,255,0),"Try Again"),(quitButton,(255,0,0),"Quit")):
        pygame.draw.rect(screen,color,button)
        labelText = buttonFont.render(label,True,(0,0,0))
        screen.blit(labelText,labelText.get_rect(center=button.center))
    pygame.display.update()
    while playAgain == "not picked":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playAgain = "picked"
                gameStatus = "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tryAgainButton.collidepoint(event.pos):
                    playAgain = "picked"
                    gameStatus = "ongoing"
                if quitButton.collidepoint(event.pos):
                    playAgain = "picked"
                    gameStatus = "quit"
        clock.tick(30)
    return gameStatus

# Title Screen Function
def title_screen(highScore):
    picked = False
    centerX = screen_size[0]//2
    # Shrink the title until it fits inside the screen with some margin
    titleSize = 64
    titleFont = pygame.font.Font("freesansbold.ttf",titleSize)
    while titleFont.size(game_title.upper())[0] > screen_size[0]-100:
        titleSize -= 4
        titleFont = pygame.font.Font("freesansbold.ttf",titleSize)
    buttonFont = pygame.font.Font("freesansbold.ttf",32)
    playButton = pygame.Rect(0,0,220,80)
    playButton.center = (centerX,350)
    quitButton = pygame.Rect(0,0,220,80)
    quitButton.center = (centerX,460)

    screen.fill(screen_color)
    screen.blit(ground,(0,screen_size[1]-ground_height))
    # A small stack of blocks sitting on the ground
    for i,width in enumerate((360,300,240)):
        block = pygame.Surface((width,50))
        block.fill((255,255,255))
        draw_block(block,centerX-width//2,screen_size[1]-ground_height-50*(i+1))
    shadowText = titleFont.render(game_title.upper(),True,(0,0,0))
    screen.blit(shadowText,shadowText.get_rect(center=(centerX+3,153)))
    titleText = titleFont.render(game_title.upper(),True,(255,255,255))
    screen.blit(titleText,titleText.get_rect(center=(centerX,150)))
    if highScore > 0:
        bestFont = pygame.font.Font("freesansbold.ttf",32)
        shadowText = bestFont.render("Best: "+str(highScore),True,(0,0,0))
        screen.blit(shadowText,shadowText.get_rect(center=(centerX+2,232)))
        bestText = bestFont.render("Best: "+str(highScore),True,(255,255,255))
        screen.blit(bestText,bestText.get_rect(center=(centerX,230)))
    for button,color,label in ((playButton,(0,255,0),"Play"),(quitButton,(255,0,0),"Quit")):
        pygame.draw.rect(screen,color,button)
        labelText = buttonFont.render(label,True,(0,0,0))
        screen.blit(labelText,labelText.get_rect(center=button.center))
    pygame.display.update()
    while not picked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                picked = True
                gameStatus = "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.collidepoint(event.pos):
                    picked = True
                    gameStatus = "ongoing"
                if quitButton.collidepoint(event.pos):
                    picked = True
                    gameStatus = "quit"
        clock.tick(30)
    return gameStatus

# Initialization
pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption(game_title)
clock = pygame.time.Clock()
scoreFont = pygame.font.Font("freesansbold.ttf",64)
labelFont = pygame.font.Font("freesansbold.ttf",20)
high_score_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),high_score_file)
ground = pygame.Surface((screen_size[0],ground_height))
ground.fill(ground_color)

def game(highScore):
    gameStatus = "ongoing"
    pause = False

    score = 1
    block = pygame.Surface((400,50))
    block.fill((255,255,255))
    speed = start_speed
    height = 600
    direction = 1
    movingXL = -400
    movingXR = movingXL+400
    placedBlocks = [block]
    placedXL = [100]
    placedXR = [placedXL[0]+400]
    placedY = [650]
    groundDist = 0
    blockWidth = 400
    newBlock = True
    falling = False
    fallSpeed = 0
    fallTime = 0
    fade = 255
    greenFade = False
    faded = True
    background_color = screen_color

    # Game Loop
    running = True
    while running:
        # Seconds since the last frame, capped so the block doesn't jump after a stall (e.g. dragging the window)
        dt = min(clock.tick(frame_rate)/1000,0.05)

        # Background
        screen.fill(background_color)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                gameStatus = "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and not falling:
                    # Snap to whole pixels so the drawn block matches the one used for the overlap
                    droppedXL = round(movingXL)
                    droppedXR = droppedXL+blockWidth
                    overlapXL = max(droppedXL,placedXL[-1])
                    overlapXR = min(droppedXR,placedXR[-1])
                    if overlapXR <= overlapXL:
                        # Missed: let the block fall off the screen before ending the game
                        falling = True
                        movingXL = droppedXL
                    else:
                        perfect = abs(droppedXL-placedXL[-1]) <= 0.025*blockWidth
                        placedXL.append(overlapXL)
                        placedXR.append(overlapXR)
                        blockWidth = overlapXR-overlapXL
                        score += 1
                        speed += speed_increase
                        placedBlocks.append(pygame.Surface((blockWidth,50)))
                        block = pygame.Surface((blockWidth,50))
                        block.fill((255,255,255))
                        faded = False
                        fade = 0
                        if perfect:
                            placedBlocks[-1].fill((fade,255,fade))
                            greenFade = True
                        else:
                            placedBlocks[-1].fill((255,255,fade))
                            greenFade = False
                        placedY.append(height)
                        height -= 50
                        direction *= -1
                        newBlock = True

                # Pausing
                if event.key == pygame.K_p:
                    pause = True

        # Check height
        if height < 100:
            height = 100
            groundDist += 50
            for i in range(len(placedY)):
                placedY[i] += 50

        # Spawn new block
        if newBlock:
            if direction == 1:
                movingXL = -blockWidth
            elif direction == -1:
                movingXL = screen_size[0]
            movingXR = movingXL+blockWidth
            newBlock = False
        if falling:
            fallTime += dt
            fallSpeed += 2000*dt
            height += fallSpeed*dt
            # On a new best, also wait for the new high score line to finish drawing
            if height > screen_size[1] and (score <= highScore or fallTime >= 1.2):
                running = False
                gameStatus = "over"
        else:
            movingXL += speed*direction*dt
            movingXR = movingXL+blockWidth
            if (direction == 1 and movingXR > screen_size[0]) or (direction == -1 and movingXL < 0):
                direction *= -1
        draw_block(block,movingXL,height)

        # Ground (drawn after the moving block so a missed block falls behind it)
        screen.blit(ground,(0,screen_size[1]-ground_height+groundDist))

        # Blocks
        for placedBlock,x,y in zip(placedBlocks,placedXL,placedY):
            draw_block(placedBlock,x,y)

        # Color fading
        if not faded:
            fade += 800*dt
            if fade >= 255:
                fade = 255
                faded = True
                greenFade = False
            if greenFade:
                placedBlocks[-1].fill((fade,255,fade))
            else:
                placedBlocks[-1].fill((255,255,fade))

        # High score lines (at the top of the block that would match the high score)
        if highScore > 0:
            draw_best_line(placedY[0]-50*(highScore-1),"BEST")
        if falling and score > highScore:
            draw_best_line(placedY[-1],"NEW BEST",min(fallTime/0.6,1))

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

        pygame.display.update()
    return gameStatus, score
        

        
# Main Function
def main():
    highScore = load_high_score()
    gameStatus = title_screen(highScore)
    while gameStatus == "ongoing":
        gameStatus, score = game(highScore)
        newBest = score > highScore
        if newBest:
            highScore = score
            save_high_score(highScore)
        if gameStatus == "over":
            gameStatus = play_again(score,highScore,newBest)
    pygame.quit()


if __name__ == "__main__":
    main()