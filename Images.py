import pygame
from PIL import Image
import numpy as np
import requests
from io import BytesIO

def GetImage(filename, url, **options):
  try:
    if options.get("raw") or False == True:
      img = Image.open(filename)
    else:
      img = pygame.image.load(filename)
  except:
    print("%s not cached, requesting %s" % (filename, url))
    response = requests.get(url)
    if response.status_code != requests.codes.ok:
      print("HTTP request for %s returned %s" % (url, response.status_code))
      return
    
    img = Image.open(BytesIO(response.content))
    size = options.get("size")
    if type(size) != None:
      img.thumbnail(size)
    try:
      img.save(filename)
      print("Successfully cached", filename)
    except:
      print("Exception occured saving %s" % filename)
    else:
      if options.get("raw") or False == True:
        img = Image.open(filename)
      else:
        img = pygame.image.load(filename)
      
  return img


def GetIconImage():
  filename = "icon.png"
  url = "https://image.flaticon.com/icons/png/128/706/706026.png"
  size = 32, 32
  return GetImage(filename, url, size=size)
  
  
def GetShipImage():
  filename = "ship.png"
  url = "https://image.flaticon.com/icons/png/128/706/706026.png"
  size = 64, 64
  return GetImage(filename, url, size=size)
  
  
def GetAlienSprite(alien_sprites, alien):
  import spritesheet
  ss = spritesheet.spritesheet(alien_sprites)
  aliens = []
  aliens.append([(0, 94, 110, 94), (111, 94, 110, 94)])
  aliens.append([(224, 94, 99, 94), (320, 94, 99, 94)])
  aliens.append([(175, 0, 100, 94), (295, 0, 100, 94)])
  aliens.append([(10, 0, 160, 84), (10, 10, 160, 84)])
  
  images = ss.images_at(aliens[alien], colorkey=(0, 0, 0))
  # Sprite is 16x16 pixels at location 0,0 in the file...
  #image = ss.image_at((0, 0, 16, 16))
  #images = []
  # Load two images into an array, their transparent bit is (255, 255, 255)
  #images = ss.images_at((0, 0, 16, 16),(17, 0, 16,16), colorkey=(255, 255, 255))
  return images

def ResizeAlienImages(img):
  basewidth = 64
  for i in range(2):
    wpercent = (basewidth/float(img[i].get_size()[0]))
    hsize = int((float(img[i].get_size()[1])*float(wpercent)))
    img[i] = pygame.transform.scale(img[i], (basewidth,hsize))
  return img


def GetAlienImage(alien):
  filename = "aliens.png"
  url = "https://vignette.wikia.nocookie.net/villains/images/9/9b/Spaceinvaders.png/revision/latest?cb=20130815215326"
  size = 420, 188
  sprites = GetImage(filename, url, size=size, raw=True)
  images = GetAlienSprite(filename, alien)
  images = ResizeAlienImages(images)
  return images
  
  
def CreateLocalImage(pixels, filename):
  # Convert the pixels into an array using numpy
  array = np.array(pixels, dtype=np.uint8)
  
  # Use PIL to create an image from the new array of pixels
  new_image = Image.fromarray(array)
  new_image.save(filename)
  
  
def GetShipBulletImage():
  filename = "ship_bullet.png"
  try:
    img = pygame.image.load(filename)
  except:
    print("Could not load %s, creating new image" % filename)
    pixels = [
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)],
      [(255,255,255),(255,255,255),(255,255,255),(255,255,255)]
    ]
    CreateLocalImage(pixels, filename)
    img = pygame.image.load(filename)
  return img
