from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os, random

'''
For this to work u must have downloaded the chrome webdriver

sendMessage() takes a contact and delivers any message passed into the function
note: the contact name cannot contain a non character such as an emoji

findMeme() locates a random file in a specified local directory and returns its path
note: The directory path to get to a meme in my case was Folder -> Folder -> Meme
This meant I had to go into the main folder, choose a random folder in that folder, then from that folder a random meme

'''

def sendMessage(user, msg):
    contact = driver.find_element_by_xpath('//span[@title="{}"]'.format(user))
    contact.click()
    #print(contact)
    class_name = "_3FRCZ copyable-text selectable-text" # msg box path//*[@id="main"]/footer/div[1]/div[2]/div/div[1]/div/div[2]
    msgBox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[1]/div/div[2]')
    msgBox.send_keys("Hello {}, I am a meme bot created by Joel Brown. ".format(user))
    time.sleep(1)
    msgBox.send_keys(Keys.ENTER)
    msgBox.send_keys(msg)
    time.sleep(1)
    msgBox.send_keys(Keys.ENTER)
    # msgBox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[3]/button')
    # msgBox.click()

    print("Sent message to: ",user)

def findMeme():
    memeFolders = 'C:\\Users\\Joel\\Desktop\\Memes'
    allFolders = os.listdir(memeFolders)
    folder = random.choice(allFolders)
    memes = memeFolders + '\\{}'.format(folder)
    allMemes = os.listdir(memes) 
    #path = memes + '\\{}'.format(meme)
    meme = random.choice(allMemes)
    path = memes + '\\{}'.format(meme)
    print(path)
    return path


PATH = "C:\Program Files (x86)\chromedriver.exe"
argumentPath = "C:\\Users\\Joel\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
options = webdriver.ChromeOptions()
options.add_argument(argumentPath)
#options.add_argument("data\\Default")

driver = webdriver.Chrome(executable_path=PATH, options=options)
driver.get("https://web.whatsapp.com")
input("Press enter in console once QR is scanned")
print("all good")

response = "It appears you are trying to receive a meme. If it is an image, reply 'img' to the meme directly. If it is video, reply 'vid' "

time.sleep(2)
contact_list = []
msg_list = []
failed_divs = []
    
while True:
    for x in range(0, 16):
        try:
            user_msg = driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[{}]/div/div/div[2]/div[2]/div[1]/span/span'.format(x)).text
            user_msg = str.casefold(user_msg)
            user_name = driver.find_element_by_xpath('//*[@id="pane-side"]/div[1]/div/div/div[{}]/div/div/div[2]/div[1]/div[1]/span/span'.format(x)).text
            msg_list.append(user_msg)
            if user_msg == 'send':
                contact_list.append(user_name)
                sendMessage(user_name, response)
                #getImg()
            if user_msg == 'memebot':
                sendMessage(user_name, "If you want a meme from status reply 'send', if you want a random meme from my insta archives, reply 'memepls'")
            if user_msg == 'vid':
                sendMessage(user_name, "Unfortunately, I cannot send videos. I would need to request it directly from Whatsapp's servers and I'm not going to do that. However, it would be remiss of me to not mention the shear power of your own phone and that in fact you do not need to rely on mine.\n There are several 3rd party options [apps and mods] both on iOS and Android (especially) to download statuses for your own.")
            if user_msg == 'img':
                #press button, copy specific xfile (will be same for all images), get src from xfile, open in new tab, 
                try:
                    sendMessage(user_name, "please wait")
                    button = driver.find_element_by_xpath('//*[@id="main"]/div[3]/div/div/div[3]/div[8]/div/div/div/div[1]/div[1]/div/div')
                    button.click()
                except:
                    #sendMessage(user_name, "Meme not found. Error code: f\{\}")
                    print("Could not find button")
            if user_msg == 'memepls':
                sendMessage(user_name, "You will now receive a random meme:")
                paperclip = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/div')
                paperclip.click()
                memepath = findMeme() #old 
                paperclip = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/div[2]/div/span/div[1]/div/ul/li[1]/button/input') #old //*[@id="main"]/header/div[3]/div/div[2]/span/div/div/ul/li[1]/button/input
                paperclip.send_keys(memepath)
                time.sleep(3)
                paperclip = driver.find_element_by_xpath('//*[@id="app"]/div[1]/div[1]/div[2]/div[2]/span/div[1]/span/div[1]/div/div[2]/div/div[2]/div[2]/div/div')
                paperclip.click()
                # paperclip.send_keys(Keys.ENTER)

        except:
            failed_divs.append(x) #groups or chats that dont exist div's are shown here
    #print(contact_list)
    # print(msg_list)
    #print(failed_divs) 
    contact_list.clear()
    msg_list.clear()
    time.sleep(3)

driver.quit()
