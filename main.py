import unittest
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.select import Select
from dotenv import load_dotenv
import smtplib, ssl

DATE_STRING = '08/06/2020'
load_dotenv()

def send_email(body, subject):
	port = 465  # For SSL
	# Create a secure SSL context
	context = ssl.create_default_context()

	try:
		with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
			server.login(os.getenv('ADMIN_EMAIL'), os.getenv("ADMIN_PASSWORD"))
			message = 'Subject: {}\n\n{}'.format(subject, body)

			server.sendmail('robot-greenriver', os.getenv('ADMIN_EMAIL'), message)
	except Exception as e:
		print('Error', e)



class DatePickerDateRangeTest(unittest.TestCase):

	def setUp(self):
		# define a driver instance, for example Chrome
		self.driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')

	def test_date_picker_date_range_(self):
		driver = self.driver
		driver.get('https://www.recreation.gov/camping/campgrounds/264411/availability')
		time.sleep(1)
		datepicker_input = driver.find_element_by_xpath("//input[@id='single-date-picker-1']")
		datepicker_input.click()
		datepicker_input.clear()
		datepicker_input.send_keys(DATE_STRING)
		time.sleep(1)
		date_blocks = driver.find_elements_by_class_name('rec-availability-date')
		time.sleep(1)

		# We only want to send email if at least one spot is free
		slots_available = 0
		for block in date_blocks:
			local_text = block.get_attribute("aria-label")
			if 'is available' in local_text.lower():
				slots_available += 1
				break
			# assert 'Not Available text' in aria_label
		if slots_available:
			send_email(body='Go to website and pick a spot! Quick', subject='Green River Cabin Is Available!')

		now = datetime.now()
		# Send confirmation email once a day at 8
		if now.hour == 8 and now.minute < 30:
			send_email(body='Still not available', subject='Green River Cabin Emails still working.')
			print('Still working!')

	def tearDown(self):
		self.driver.close()
		self.driver.quit()


if __name__ == "__main__":
	unittest.main()
