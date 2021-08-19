from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.common.exceptions import NoSuchElementException
from PIL import Image

username = input("Enter Your Username: ")
password = input('Enter Your Password: ')
targetUsername = input('Enter Your Target`s Username: ')

browser = webdriver.Chrome(ChromeDriverManager().install())


def login(username,password):
    browser.get("https://www.instagram.com")
    time.sleep(5)
    username_area = browser.find_element_by_xpath(
    '//*[@id="loginForm"]/div/div[1]/div/label/input')
    username_area.click()
    time.sleep(1)
    username_area.send_keys(username)
    password_area = browser.find_element_by_xpath(
    '//*[@id="loginForm"]/div/div[2]/div/label/input')
    password_area.click()
    time.sleep(1)
    password_area.send_keys(password)
    browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]').click()
    time.sleep(5)
    return print("Logged In")

def getProfile(targetUsername):
    browser.get(f'https://www.instagram.com/{targetUsername}/')
    time.sleep(3)
    numbers = browser.find_elements_by_css_selector('.g47SY')
    global postCount
    postCount = numbers[0].text.replace('.', '')
    time.sleep(2)
    return print(f'{targetUsername} Has {postCount} Posts')
   



def downloadPosts():
    browser.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div/div[1]/div[1]').click()
    time.sleep(5)
    for i in reversed(range(int(postCount)+1)):
        try:
            browser.find_element_by_css_selector('.coreSpriteRightChevron')
            if browser.find_element_by_css_selector('.coreSpriteRightChevron'):
                for j in range(10):
                    if browser.find_element_by_css_selector('.coreSpriteRightChevron'):

                        slideButton = browser.find_element_by_css_selector(
                        '.coreSpriteRightChevron')

                        post = browser.find_element_by_xpath(
                        '/html/body/div[6]/div[2]/div/article/div[2]/div/div/div[2]')
                        browser.save_screenshot(f"{i}.{j}.png")
                        location = post.location
                        size = post.size
                        x = location['x']
                        y = location['y']
                        width = location['x']+size['width']
                        height = location['y']+size['height']
                        img = Image.open(f'{i}.{j}.png')
                        img = img.crop((int(x), int(y), int(width), int(height)))
                        img.save(f'{i}.{j}.png')
                        print(f"saved {i}.{j}")
                        time.sleep(3)

                        slideButton.click()
                        time.sleep(2)
                    else:
                        break

        except NoSuchElementException:
            post = browser.find_element_by_xpath(
            '/html/body/div[6]/div[2]/div/article/div[2]/div/div/div[1]')
            # postLink = browser.find_element_by_xpath('/html/body/div[6]/div[2]/div/article/div[3]/section[2]/div/div[1]/a').get_attribute('href')
            # print(f'{postLink}')
            browser.save_screenshot(f'{i}.png')
            location = post.location
            size = post.size
            x = location['x']
            y = location['y']
            width = location['x']+size['width']
            height = location['y']+size['height']
            img = Image.open(f'{i}.png')
            img = img.crop((int(x), int(y), int(width), int(height)))
            img.save(f'{i}.png')
            print(f"saved {i}.png")
            try:
                nextPost = browser.find_element_by_xpath("//*[text()='Sonraki']")
                nextPost.click()
            except NoSuchElementException:
                break
            time.sleep(2)
    return print("Download Completed Successfully")

login(username,password)
getProfile(targetUsername)
downloadPosts()


time.sleep(4)
print("Goodbye")
browser.close()
