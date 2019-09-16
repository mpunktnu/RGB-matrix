#!/usr/bin/env python
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time, os, requests, csv, math, sys, random
from lxml import html, etree
from datetime import datetime

def getOrders():
  #This function crawls a webpage and finds whatever. In our case it returns how many orders we have shipped and how many are left
  with requests.Session() as s:
    r = s.get("http://anyWebpageWithYourOrders")

    tree = html.fromstring(r.content)

    allTds = tree.xpath("//xpathToFindYourOrders")

    incomming = allTds[0].xpath("span")[0].text[:-3].strip()
    done = allTds[1].xpath("span")[0].text[:-3].strip()

    return incomming, done

def showOrders(canvas, font, color):
  #Print how many orders we still have to pack
  incomming, done = getOrders()
  graphics.DrawText(canvas, font, 6, 13, color, "Kvar")
  graphics.DrawText(canvas, font, 39, 13, color, "Klar")
  graphics.DrawLine(canvas, 32, 32, 32, 0, color)
  graphics.DrawText(canvas, font, 12, 27, color, incomming)
  graphics.DrawText(canvas, font, 43, 27, color, done)

def showStatistics(canvas, font, color):
  #Shows how many orders we have gotten today vs yeserday
  today = ""
  yesterday = ""

  with requests.Session() as s:
    r = s.get("http://anyWebpageWithYourOrders")

    tree = html.fromstring(r.content)

    allTds = tree.xpath("//xpathToFindYourOrders")

    today = allTds[4].xpath("span")[0].text[:-3].strip()
    yesterday = allTds[5].xpath("span")[0].text[:-3].strip()

  graphics.DrawText(canvas, font, 6, 13, color, "Idag")
  graphics.DrawText(canvas, font, 39, 13, color, "Ig"+unichr(229)+"r") #get å to work
  graphics.DrawLine(canvas, 32, 32, 32, 0, color)
  graphics.DrawText(canvas, font, 12, 27, color, today)
  graphics.DrawText(canvas, font, 44, 27, color, yesterday)

def welcomeToM(canvas, font, color, delay):
  #Shows Welcome to m! and changes the heart to different colors
  blue = graphics.Color(0, 0, 255)
  red = graphics.Color(255, 0, 0)
  green = graphics.Color(0, 255, 0)
  annaEBFavo = graphics.Color(60, 50, 100)

  colors = [blue, red, green, annaEBFavo]
  graphics.DrawText(canvas, font, 3, 13, color, "V"+unichr(228)+"lkommen" + unichr(9829)) #get ä to work and a heart
  graphics.DrawText(canvas, font, 1, 26, color, "till")
  graphics.DrawText(canvas, font, 1, 26, red, "     m.nu!")

  sec = 0
  while sec < delay:
    time.sleep(0.2)
    graphics.DrawText(canvas, font, 3, 13, random.choice(colors), "         " + unichr(9829)) #change color of the heart
    sec += 0.2

def showTime(canvas, font, color, delay):
  #Shows the time
  font.LoadFont("../../../fonts/7x14.bdf")
  sec = 0
  while sec < delay:
    graphics.DrawText(canvas, font, 5, 20, color, datetime.now().strftime('%H:%M:%S'))
    sec += 1
    time.sleep(1)
    canvas.Clear()

def scrollaText(canvas, font, color, text):
  #Scroll text
  pos = canvas.width - 1
  font.LoadFont("../../../fonts/7x14.bdf")

  while pos < 64:
    canvas.Clear()
    len = graphics.DrawText(canvas, font, pos, 20, color, text)
    pos -= 1
    if (pos + len < 0):
      pos = canvas.width

    time.sleep(0.03)

def getGuldkorn(canvas, font, color):
  #help function to get the text to print in "scrollaText"
  with requests.Session() as s:
    r = s.get("http://anyPageWithYourText")

    text = random.choice(r.text.split("\r\n"))

    text = text.split(";")[1]

    scrollaText(canvas, font, color, text)

def birthdays(canvas, font, color):
  #If it is a special day, print a message that day
  today = datetime.now().strftime('%m-%d')

  if today == "03-14":
    text = "Pi party! Wohooooooo!!"

    scrollaText(canvas, font, color, text)

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

#Some variables to play with
fontToUse = "../../../fonts/6x13.bdf"
delayInSec = 5
color = graphics.Color(0, 0, 255) #just temporary color. Will change each loop

canvas = matrix
font = graphics.Font()
font.LoadFont(fontToUse)
#Loop FOREVER and EVER!
try:
    print("Press CTRL-C to stop.")
    while True:
        hour = datetime.now().strftime('%H')
        minute = datetime.now().strftime('%M')

        today = datetime.today().weekday()

        if int(hour) > 7 and int(hour) < 18 and int(today) < 5: #If we are at work, use the display. Otherwise nothing happens
          color = graphics.Color(random.randrange(0,256,1), random.randrange(0,256,1), random.randrange(0,256,1)) #Pick a random color each time

          #Display welcome to m message
          welcomeToM(canvas, font, color, delayInSec)
          canvas.Clear()

          #Display how many orders we have packed
          showOrders(canvas, font, color)
          time.sleep(delayInSec)
          canvas.Clear()

          #Display how many orders we have gotten today/yesterday
          showStatistics(canvas, font, color)
          time.sleep(delayInSec)
          canvas.Clear()

          #Show the time
          showTime(canvas, font, color, delayInSec)
          font.LoadFont(fontToUse)
          canvas.Clear()

          #Show a random praise we have gotten over the years
          getGuldkorn(canvas, font, color)
          canvas.Clear()
          font.LoadFont(fontToUse)

          #Show a message on special days
          birthdays(canvas, font, color)
          canvas.Clear()
          font.LoadFont(fontToUse)
except KeyboardInterrupt:
    sys.exit(0)
  
