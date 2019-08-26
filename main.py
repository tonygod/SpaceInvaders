# <div>Icons made by <a href="https://www.flaticon.com/authors/smashicons" title="Smashicons">Smashicons</a> from <a href="https://www.flaticon.com/"         title="Flaticon">www.flaticon.com</a> is licensed by <a href="http://creativecommons.org/licenses/by/3.0/"         title="Creative Commons BY 3.0" target="_blank">CC 3.0 BY</a></div>

import pygame
import Images
import time
import math


# globals
running = True
gameOver = True
score = 0
alien_cols = 7
alien_rows = 5
shipSpeed = 0.3
alienSpeed = 32
minX = 0
maxX = 740
print("globals init")

# initialization
pygame.init()
pygame.display.set_caption("Space_Invaders")
icon = Images.GetIconImage()
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((800,800)) # w=800, h=800
print("screen init")

# player ship
playerImg = Images.GetShipImage()
playerX = 370
playerY = 725
playerX_change = 0
bulletImg = Images.GetShipBulletImage()
bulletX = 0
bulletY = 0
bulletY_change = -1
bulletReady = True
bulletTimer = time.time()
fireRate = 3.0
print("player init")

aliens = []
alienInfo = [
  [2, 50], # row 0
  [1, 25], # row 1
  [0, 10], # row 2
  [0, 10], # row 3
  [0, 10] # row 4
  ]
alienX_change = 0
alienTimer = time.time()

def init_aliens():
  global aliens
  alienX = 0
  alienY = 50
  for row in range(alien_rows):
    for i in range(alien_cols):
      alienX = i * 74 # 64 + 10
      alienY = row * 55 + 50
      alien = { "image" : Images.GetAlienImage(alienInfo[row][0]), "x" : alienX, "y" : alienY, "score" : alienInfo[row][1] }
      aliens.append(alien)
  print("alien init")
  # end init_aliens
  
  
font = pygame.font.Font("freesansbold.ttf", 32)
scoreTextX = 10
scoreTextY = 10
gameOverTextX = 300
gameOverTextY = 400
winlose = ""
winloseTextX = 310
winloseTextY = 500
startTextX = 290
startTextY = 600
print("text init")


def start_game():
  global score
  global gameOver
  print("START GAME")
  init_aliens()
  score = 0
  gameOver = False
  # end start_game
  

def bulletHit(alien):
  if bulletReady == True:
    return False
  distance = math.sqrt(abs(math.pow(alien["x"] - bulletX, 2) + math.pow(alien["y"] - bulletY, 2)))
  if distance < 27:
    return True
  #end bulletHit

def update_text():
  scoreText = font.render("SCORE: " + str(score), True, (255, 255, 255))
  screen.blit(scoreText, (scoreTextX, scoreTextY))
  if gameOver:
    gameOverText = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameOverText, (gameOverTextX, gameOverTextY))
    winloseText = font.render(winlose, True, (255, 255, 255))
    screen.blit(winloseText, (winloseTextX, winloseTextY))
    startText = font.render("TAP TO START", True, (255, 255, 255))
    screen.blit(startText, (startTextX, startTextY))
  # end update_text

def update_player():
  global playerX
  if playerX_change != 0:
    playerX += playerX_change
  if playerX < minX:
    playerX = minX
  elif playerX > maxX:
    playerX = maxX
    
  screen.blit(playerImg, (playerX, playerY))
  # end update_player
  
def update_bullet():
  screen.blit(bulletImg, (bulletX, bulletY))
  # end update_bullet
  
def update_alien():
  secs = int(time.time())
  global bulletReady
  global score
  global winlose
  global gameOver
  for alien in aliens:
    if bulletHit(alien):
      bulletReady = True
      #print("hit: aX=%f, aY=%f, bX=%f, bY=%f" % (alien["x"], alien["y"], bulletX, bulletY))
      score += alien["score"]
      #print("SCORE:", score)
      # remove alien from aliens
      aliens.remove(alien)
      if len(aliens) == 0:
        print("YOU WIN! GAME OVER")
        winlose = "YOU WIN!"
        gameOver = True
    else:
      if secs % 2 == 0:
        screen.blit(alien["image"][1], (alien["x"], alien["y"]))
      else:
        screen.blit(alien["image"][0], (alien["x"], alien["y"]))
      if alien["y"] >= playerY:
        print("YOU LOSE! GAME OVER")
        winlose = "YOU LOSE!"
        gameOver = True
  # end update_alien
  
  
def fire_bullet():
  global bulletX
  global bulletY
  global bulletTimer
  global bulletReady
  bulletReady = False
  bulletX = playerX + 30
  bulletY = playerY - 5
  bulletTimer = time.time()
  # end fire_bullet

# begin game loop
while running:
  # events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
      
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_q:
        running = False
        
      if event.key == pygame.K_a:
        playerX_change = -shipSpeed
          
      elif event.key == pygame.K_d:
        playerX_change = shipSpeed
        
    elif event.type == pygame.KEYUP:
      if event.key == pygame.K_a or event.key == pygame.K_d:
        playerX_change = 0
        
    elif event.type == pygame.MOUSEBUTTONDOWN:
      tapStart = time.time()
      mousePosX, mousePosY = pygame.mouse.get_pos()
      if mousePosX < 400:
        playerX_change = -shipSpeed
      else:
        playerX_change = shipSpeed
        
    elif event.type == pygame.MOUSEBUTTONUP:
      if gameOver:
        if time.time() - tapStart < 0.4:
          start_game()
      playerX_change = 0
        

  # alien movement
  if gameOver == False:
    if time.time() - alienTimer >= 1:
      alienX_change = alienSpeed
      moveDown = False
      for i in range(len(aliens)):
        aliens[i]["x"] += alienX_change
        if aliens[i]["x"] >= maxX or aliens[i]["x"] < minX:
          moveDown = True
      if moveDown:
        alienSpeed = -alienSpeed
        for i in range(len(aliens)):
          aliens[i]["y"] += 32
      alienTimer = time.time()
    elif alienX_change != 0:
      alienX_change = 0
  # end alien movement

  # check bullet status
  if gameOver == False:
    if bulletReady == False:
      bulletY += bulletY_change
      if bulletY < -10:
        bulletReady = True

    # bullet auto-fire
    if time.time() - bulletTimer >= fireRate:
      if bulletReady:
        fire_bullet()
    
  # render
  screen.fill((0, 0, 0))
  if gameOver == False:
    update_player()
    update_alien()
    if bulletReady == False:
      update_bullet()
  update_text()
  pygame.display.update()
# end game loop
  
      