from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date
import time
import re
import csv
import caffeine


caffeine.on

csv_file = open('aptsbk.csv', 'w', encoding='utf-8')#this is the csv file to be created 
writer = csv.writer(csv_file)
driver = webdriver.Chrome()#this opens the chrome and populates the website


#do i want to use data comprehension to get a list of all the urls 
start_urls = ["https://www.corcoran.com/nyc-real-estate/for-sale/search/brooklyn?SaleType=Sale&Count=36&SearchingFrom=%2Fnyc-real-estate%2Ffor-sale%2Fsearch%2Fbrooklyn&IsNewDev=false&OnlyExclusives=False&Price.Minimum=0&Price.Maximum=1000000000&Bedrooms.SearchValue=-0.5&Bathrooms.SearchValue=0.5&Borough=Brooklyn&NeighborhoodID=6&NeighborhoodID=7&NeighborhoodID=4&NeighborhoodID=11&NeighborhoodID=12&NeighborhoodID=13&NeighborhoodID=16&NeighborhoodID=17&NeighborhoodID=18&NeighborhoodID=19&NeighborhoodID=20&NeighborhoodID=25&NeighborhoodID=26&NeighborhoodID=27&NeighborhoodID=28&NeighborhoodID=30&NeighborhoodID=31&NeighborhoodID=88&NeighborhoodID=33&NeighborhoodID=35&NeighborhoodID=38&NeighborhoodID=40&NeighborhoodID=42&NeighborhoodID=43&NeighborhoodID=45&NeighborhoodID=46&NeighborhoodID=48&NeighborhoodID=53&NeighborhoodID=55&NeighborhoodID=59&NeighborhoodID=64&NeighborhoodID=65&NeighborhoodID=15&NeighborhoodID=69&NeighborhoodID=70&NeighborhoodID=71&NeighborhoodID=72&NeighborhoodID=75&NeighborhoodID=82&NeighborhoodID=92&NeighborhoodID=93&NewSearchName=&SearchName=&TypeOfHome=homes+for+sale&SortBySimplified=Price"]


#driver.find_element_by_xpath('//span[@data-bind"text: Total"]').text /36
start_urls.extend(["https://www.corcoran.com/nyc-real-estate/for-sale/search/brooklyn?SaleType=Sale&Count=36&SearchingFrom=%2Fnyc-real-estate%2Ffor-sale%2Fsearch%2Fbrooklyn&IsNewDev=false&OnlyExclusives=False&Price.Minimum=0&Price.Maximum=1000000000&Bedrooms.SearchValue=-0.5&Bathrooms.SearchValue=0.5&Borough=Brooklyn&NeighborhoodID=6&NeighborhoodID=7&NeighborhoodID=4&NeighborhoodID=11&NeighborhoodID=12&NeighborhoodID=13&NeighborhoodID=16&NeighborhoodID=17&NeighborhoodID=18&NeighborhoodID=19&NeighborhoodID=20&NeighborhoodID=25&NeighborhoodID=26&NeighborhoodID=27&NeighborhoodID=28&NeighborhoodID=30&NeighborhoodID=31&NeighborhoodID=88&NeighborhoodID=33&NeighborhoodID=35&NeighborhoodID=38&NeighborhoodID=40&NeighborhoodID=42&NeighborhoodID=43&NeighborhoodID=45&NeighborhoodID=46&NeighborhoodID=48&NeighborhoodID=53&NeighborhoodID=55&NeighborhoodID=59&NeighborhoodID=64&NeighborhoodID=65&NeighborhoodID=15&NeighborhoodID=69&NeighborhoodID=70&NeighborhoodID=71&NeighborhoodID=72&NeighborhoodID=75&NeighborhoodID=82&NeighborhoodID=92&NeighborhoodID=93&NewSearchName=&SearchName=&TypeOfHome=homes+for+sale&SortBySimplified=Price&Page=" + str(x) for x in range(1,17)])



for url in start_urls:
	driver.get(url)

	page_links = driver.find_elements_by_xpath('//div[@class="Search-Results-Block"]//div[@class="img-wrapper pic Exclusive"]//a[@href]')
	page_links = list(map(lambda x: x.get_attribute('href'), page_links))
	print(len(page_links))

	for page in page_links:
		driver.get(page)
		#driver.find_element_by_xpath('//div[@class="Search-Results-Block"]//a[@href]').get_attribute()

		#review_button=driver.find_element_by_xpath('//*[@id="main"]/div[2]/div/div[1]/div[1]/div/div/div[1]/a/img')
			#review_button.click()#clicks on first link in list of manhattan listings

		print('$'*50)
		apts_dict = {}
		element_dict={}

		# while driver.find_element_by_xpath('//a[@class="NextHomeInSearch"]')==True:
		time.sleep(2)
		try:
			driver.find_element_by_xpath('//div[@class="address-info"]/h1[@class="title"]').text
			address=driver.find_element_by_xpath('//div[@class="address-info"]/h1[@class="title"]').text
		except:
			address='na'
			continue

		try:
			neighborhood=driver.find_element_by_xpath('//a[@class="hood"]').text
		except:
			neighborhood=driver.find_element_by_xpath('//div[@class="bold "]').text

		essentials=driver.find_elements_by_xpath('//div[@class="essential-item"]/span[@class]')
		essentials_lst=list(map(lambda x: x.text,essentials))

		for ele in range(len(essentials_lst)//2):
			element_dict[essentials_lst[ele*2]] = essentials_lst[(ele*2)+1]


		driver.find_element_by_xpath('//div[@class="description NudgeDown"]').text
		description=driver.find_element_by_xpath('//div[@class="description NudgeDown"]').text

		apts_dict['address'] = address
		apts_dict['neighborhood'] = neighborhood
		apts_dict['price'] = element_dict.get('Price')
		apts_dict['apttype'] = element_dict.get('Type')
		apts_dict['bedrooms'] = element_dict.get('Bedrooms')
		apts_dict['bathrooms'] = element_dict.get('Bathrooms')
		apts_dict['rooms'] = element_dict.get('Rooms')
		apts_dict['sqft'] = element_dict.get('Approx. Sq. Ft.')
		apts_dict['description'] = description
		print(apts_dict)
		writer.writerow(apts_dict.values())

		
			#CLICK BUTTON TO NEXT PAGE
		#driver.execute_script("window.history.go(-1)")

