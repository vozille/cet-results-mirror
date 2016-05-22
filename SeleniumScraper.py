import threading
import time
from datetime import date

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

cnt = 0
class Webscraper(threading.Thread):
    def __init__(self, start, end, birthday, url):
        threading.Thread.__init__(self)
        self.start_roll = start
        self.end_roll = end
        self.birthday = birthday
        self.url = url

    def find_by_xpath(self, driver, locator, timeout=3):
        element = WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located((By.XPATH, locator))
        )
        return element

    def run(self):
        global cnt
        driver = webdriver.Firefox()
        driver.get(self.url)
        mybirthday = self.birthday.strftime("%d/%m/%Y")
        self.find_by_xpath(driver, '//*[@id="dpStudentdob_dateInput"]').send_keys(mybirthday)
        for roll_num in range(self.start_roll, self.end_roll):
            try:
                self.find_by_xpath(driver, '//*[@id="txtRegNo"]').clear()
                self.find_by_xpath(driver, '//*[@id="txtRegNo"]').send_keys(str(roll_num))
                self.find_by_xpath(driver, '//*[@id="btnView"]').click()
                try:
                    """
                    The webpage has been loaded, do anything you want
                    """
                    self.find_by_xpath(driver, '//*[@id="gvResultSummary_ctl02_lnkViewResult"]').click()
                    name = self.find_by_xpath(driver, '//*[@id="lblName"]').text
                    branch = self.find_by_xpath(driver, '//*[@id="lblResultName"]').text
                    subjects = self.find_by_xpath(driver, '//*[@id="tblBasicDetail"]/table/tbody/tr[7]/td').text
                    cnt += 1
                    """
                    What I am doing here is printing data so that i can save it later in a csv file
                    And upload it later to a database
                    """
                    print str(cnt) + ', ' + name + ' ,' + branch + ' ,' + str(roll_num) + ' ,',
                    subjects = subjects.split('\n')
                    for k in subjects:
                        print k + ',',
                    print
                except TimeoutException:
                    pass
            except TimeoutException:
                pass
        driver.close()


def main():
    # dont know why this date works for everyone
    bday = date(1995, 6, 1)
    # start roll
    i = 1501106100
    threads = []
    while i < 1501106105:
        t = Webscraper(i, i + 1, bday, 'http://www.bputexam.in/StudentSection/ResultPublished/StudentResult.aspx')
        threads.append(t)
        i += 1

    for i in threads:
        i.start()
        # well, opening web browsers takes time
        time.sleep(6)
    for i in threads:
        i.join()
    print "Done"
    
if __name__ == '__main__':
    main()
