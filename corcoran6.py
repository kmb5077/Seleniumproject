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

csv_file = open('apts2.csv', 'w', encoding='utf-8')#this is the csv file to be created 
writer = csv.writer(csv_file)
driver = webdriver.Chrome()#this opens the chrome and populates the website


#do i want to use data comprehension to get a list of all the urls 
start_urls = ["https://www.corcoran.com/nyc-real-estate/for-sale/search/manhattan?SaleType=Sale&Count=36&SearchingFrom=%2Fnyc-real-estate%2Ffor-sale%2Fsearch%2Fmanhattan&IsNewDev=false&OnlyExclusives=False&Price.Minimum=0&Price.Maximum=1000000000&Bedrooms.SearchValue=-0.5&Bathrooms.SearchValue=0.5&Borough=Manhattan&NeighborhoodID=5&NeighborhoodID=8&NeighborhoodID=94&NeighborhoodID=21&NeighborhoodID=22&NeighborhoodID=24&NeighborhoodID=34&NeighborhoodID=36&NeighborhoodID=37&NeighborhoodID=39&NeighborhoodID=44&NeighborhoodID=47&NeighborhoodID=49&NeighborhoodID=50&NeighborhoodID=51&NeighborhoodID=57&NeighborhoodID=62&NeighborhoodID=63&NeighborhoodID=66&NeighborhoodID=67&NeighborhoodID=524&NeighborhoodID=73&NeighborhoodID=76&NeighborhoodID=83&NeighborhoodID=85&NeighborhoodID=86&NeighborhoodID=87&NeighborhoodID=89&NeighborhoodID=91"]


#driver.find_element_by_xpath('//span[@data-bind"text: Total"]').text /36
start_urls.extend(["https://www.corcoran.com/nyc-real-estate/for-sale/search/manhattan?SaleType=Sale&Count=36&SearchingFrom=%2Fnyc-real-estate%2Ffor-sale%2Fsearch%2Fmanhattan&IsNewDev=false&OnlyExclusives=False&Price.Minimum=0&Price.Maximum=1000000000&Bedrooms.SearchValue=-0.5&Bathrooms.SearchValue=0.5&Borough=Manhattan&NeighborhoodID=5&NeighborhoodID=8&NeighborhoodID=94&NeighborhoodID=21&NeighborhoodID=22&NeighborhoodID=24&NeighborhoodID=34&NeighborhoodID=36&NeighborhoodID=37&NeighborhoodID=39&NeighborhoodID=44&NeighborhoodID=47&NeighborhoodID=49&NeighborhoodID=50&NeighborhoodID=51&NeighborhoodID=57&NeighborhoodID=62&NeighborhoodID=63&NeighborhoodID=66&NeighborhoodID=67&NeighborhoodID=524&NeighborhoodID=73&NeighborhoodID=76&NeighborhoodID=83&NeighborhoodID=85&NeighborhoodID=86&NeighborhoodID=87&NeighborhoodID=89&NeighborhoodID=91&Page=" + str(x) for x in range(1,38)])



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

