import os, time, random, spintax, requests, config
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from random import randint, randrange
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

PROXY = "3.88.169.225:80"

def stop(n):
	time.sleep(randint(2, n))

#login bot===================================================================================================
def youtube_login(email,password):

	op = webdriver.ChromeOptions()
	# op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
	# op.add_argument('--headless')
	op.add_argument('--disable-dev-shm-usage')
	# op.add_argument('--no-sandbox')
	op.add_argument('--disable-gpu')
	# op.add_argument("--window-size=1920,1080")
	op.add_argument("disable-infobars")
	op.add_argument("--disable-extensions")
	# op.add_argument('--proxy-server=%s' % PROXY)
	# op.add_argument("--proxy-bypass-list=*")
	driver = webdriver.Chrome(options=op, executable_path= 'chromedriver.exe')
	driver.execute_script("document.body.style.zoom='80%'")
	driver.get('https://accounts.google.com/ServiceLogin?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620')

	print("=============================================================================================================")
	print("Google Login")

	#finding email field and putting our email on it
	email_field = driver.find_element_by_xpath('//*[@id="identifierId"]')
	email_field.send_keys(email)
	driver.find_element_by_id("identifierNext").click()
	stop(5)
	print("email - done")

	#finding pass field and putting our pass on it
	find_pass_field = (By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')
	WebDriverWait(driver, 50).until(EC.presence_of_element_located(find_pass_field))
	pass_field = driver.find_element(*find_pass_field)
	WebDriverWait(driver, 50).until(EC.element_to_be_clickable(find_pass_field))
	pass_field.send_keys(password)
	driver.find_element_by_id("passwordNext").click()
	stop(5)
	print("password - done")
	WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-masthead button#avatar-btn")))
	print("Successfully login")
	print("============================================================================================================")

	return driver
#==============================================================================================================



#comment bot===================================================================================================
def comment_page(driver,urls,comment):

	if len( urls ) == 0:
		print("============================================================================================================")
		print ('Finished keyword jumping to next one...')
		return []
	
	#gettin a video link from the list
	url = urls[0]
	
	driver.get(url)
	print("Video url:" + url)
	driver.implicitly_wait(1)

	#checking if video is unavailable
	if not check_exists_by_xpath(driver,'//*[@id="movie_player"]'):
		print("skiped")
		return comment_page(driver, urls, random_comment())


	
	time.sleep(2)
	# You can add like function by uncommenting 4 lines below
	# like_button = EC.presence_of_element_located(By.XPATH, '/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-icon-button/button/yt-icon')
	# WebDriverWait(driver, 50).until(EC.element_to_be_clickable(like_button)).click()
	# print('Liked')
	# time.sleep(1)
	driver.execute_script("window.scrollTo(0, window.scrollY + 500)")
	time.sleep(1)

	#checking if comments are disabled
	if not check_exists_by_xpath(driver,'//*[@id="simple-box"]/ytd-comment-simplebox-renderer'):
		print("skiped")
		return comment_page(driver, urls, random_comment())

	#checking if video is a livestream
	if check_exists_by_xpath(driver,'//*[@id="contents"]/ytd-message-renderer'):
		print("skiped")
		return comment_page(driver, urls, random_comment())

	#finding comment box and submiting our comment on it
	comment_box = EC.presence_of_element_located((By.CSS_SELECTOR, '#placeholder-area'))
	WebDriverWait(driver, 4).until(comment_box)
	comment_box1 = driver.find_element_by_css_selector('#placeholder-area')
	ActionChains(driver).move_to_element(comment_box1).click(comment_box1).perform()
	add_comment_onit = driver.find_element_by_css_selector('#contenteditable-root')
	add_comment_onit.send_keys(comment)
	time.sleep(2) 
	driver.find_element_by_css_selector('#submit-button').click()
	print("done")

	stop(5)

	return comment_page(driver, urls, random_comment())
#==============================================================================================================


#comment section
def random_comment():
# You can edit these lines if you want to add more comments===================================
	comments = [
		"Huge thanks for hosting this amazing giveaway!",
		"This laptop would be a game-changer, and I'm so grateful for the chance to win. ",
		"Your generosity is incredible, and I'm crossing my fingers for everyone! ",
		"Just entered the giveaway, and wanted to say thank you for spreading holiday cheer! ",
		"Seriously, you rock! This giveaway is the best Christmas present ever. ",
		"Winning this laptop would change my life! Goodbye, slow desktop! ",
		"Online classes and work would be a breeze with this beauty. ",
		"Finally, I could edit my videos like a pro! ",
		"Laptop envy? Gone. Thanks to this giveaway! ",
		"New year, new laptop? Let's make it happen! ",
		"Wishing everyone a Merry Christmas filled with joy and (maybe) a new laptop! ",
		"May the spirit of Christmas bring good luck to everyone in this giveaway!",
		"Sending warm wishes and holiday cheer to all the laptop hopefuls!",
		"Let's spread some festive cheer and positive vibes! Merry Christmas! ",
		"Santa better be bringing laptops this year, because I'm ready! ",
		"May the luck of the draw be with you all! Good luck in the giveaway! ",
		"Sending positive vibes to everyone! May the best comment win! ",
		"Go get 'em, everyone! May the most passionate laptop lover win! ",
		"Don't give up, dreamers! This laptop could be yours! ",
		"Merry Christmas and good luck to all! May the odds be ever in your favor! ",
		"Feeling festive and optimistic! Let's do this! "
	]
	for i in range(1000000000):
		b=str(a)
		comment="Feeling festive and optimistic! Let's do this! "
		comment1="Merry Christmas and good luck to all! May the odds be ever in your favor! "
		comment2="Santa better be bringing laptops this year, because I'm ready! "
		comment3="Finally, I could edit my videos like a pro! "
		comments.append(comment)
		comments.append(comment1)
		comments.append(comment2)
		comments.append(comment3)
		comment="Huge thanks for hosting this amazing giveaway!"
		comment1="Merry Christmas and good luck to all! May the odds be ever in your favor! "
		comment2="Santa better be bringing laptops this year, because I'm ready! "
		comment3="Finally, I could edit my videos like a pro! "
		comments.append(comment)
		comments.append(comment1)
		comments.append(comment2)
		comments.append(comment3)
		comment="Feeling festive and optimistic! Let's do this! "
		comment1="Your generosity is incredible, and I'm crossing my fingers for everyone! "
		comment2="Santa better be bringing laptops this year, because I'm ready! "
		comment3="Finally, I could edit my videos like a pro! "
		comments.append(comment)
		comments.append(comment1)
		comments.append(comment2)
		comments.append(comment3)
		comment="Feeling festive and optimistic! Let's do this! "
		comment1="Merry Christmas and good luck to all! May the odds be ever in your favor! "
		comment2="Winning this laptop would change my life! Goodbye, slow desktop! "
		comment3="Just entered the giveaway, and wanted to say thank you for spreading holiday cheer! "
		comments.append(comment)
		comments.append(comment1)
		comments.append(comment2)
		comments.append(comment3)
# =============================================================================================
	r = np.random.randint(0, len(comments))

	return comments[r]
 
def check_exists_by_xpath(driver,xpath):
	try:
		driver.find_element_by_xpath(xpath)
	except NoSuchElementException:
		return False

	return True


#running bot------------------------------------------------------------------------------------
if __name__ == '__main__':
	email = config.email
	password = config.password

	driver = youtube_login(email, password)
	driver.maximize_window()
	while True:
		key = driver.find_element_by_name('search_query')

		key.send_keys(Keys.CONTROL,"a")
		key.send_keys(Keys.DELETE)

		#get keyword list and extract each key
		with open('gaming_keywords.txt', 'r') as f:
			keywords = [line.strip() for line in f]
			random_keyword = random.choice(keywords)
			keys = spintax.spin(random_keyword)

			#send keyword in the search box
			for char in keys:
				key.send_keys(char)
		
		time.sleep(1)


		#click search icon
		driver.find_element_by_css_selector('#search-icon-legacy > yt-icon').click()
		time.sleep(3)
		#click filter button to filter the videos for the recently uploaded, you can remove or edit this option
		driver.find_element_by_css_selector('#container > ytd-toggle-button-renderer > a').click()
		time.sleep(3)

		#filtering for this week
		driver.find_element_by_xpath("(//yt-formatted-string[@class='style-scope ytd-search-filter-renderer'])[3]").click()
		time.sleep(3)
		
		#grabbing videos titles
		for i in range(5):
			ActionChains(driver).send_keys(Keys.END).perform()
			time.sleep(3)
		titles = driver.find_elements_by_xpath('//*[@id="video-title"]')

		urls = []

		#getting url from href attribute in title
		for i in titles:
			if i.get_attribute('href') != None:
				urls.append(i.get_attribute('href'))
			else:
				continue
	
		#checking if we have links or not
		if urls == []:
			print("There is no videos for this keyword at the moment")
		else:
			for i in range(100000000000000000000000):
				comment_page(driver,urls,random_comment())
