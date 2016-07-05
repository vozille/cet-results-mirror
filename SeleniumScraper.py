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

    def find_by_xpath(self, driver, locator, timeout=2):
        element = WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located((By.XPATH, locator))
        )
        return element

    def run(self):
        global cnt
        driver = webdriver.Chrome()
        driver.get(self.url)
        mybirthday = self.birthday.strftime("%d/%m/%Y")
        self.find_by_xpath(driver, '//*[@id="dpStudentdob_dateInput"]').send_keys(mybirthday)
        for roll_num in range(self.start_roll, self.end_roll):
            result_link = [
                '//*[@id="gvResultSummary_ctl02_lnkViewResult"]',
                '//*[@id="gvResultSummary_ctl03_lnkViewResult"]',
                '//*[@id="gvResultSummary_ctl04_lnkViewResult"]',
                '//*[@id="gvResultSummary_ctl05_lnkViewResult"]',
                '//*[@id="gvResultSummary_ctl06_lnkViewResult"]',
                '//*[@id="gvResultSummary_ctl07_lnkViewResult"]',
                '//*[@id="gvResultSummary_ctl08_lnkViewResult"]',
                '//*[@id="gvResultSummary_ctl09_lnkViewResult"]',
                '//*[@id="gvResultSummary_ctl10_lnkViewResult"]'
            ]

            try:
                self.find_by_xpath(driver, '//*[@id="txtRegNo"]').clear()
                self.find_by_xpath(driver, '//*[@id="txtRegNo"]').send_keys(str(roll_num))
                self.find_by_xpath(driver, '//*[@id="btnView"]').click()
                # print self.find_by_xpath(driver, '', 1)
                try:
                    try:
                        list_links = driver.find_elements_by_xpath("//*[contains(text(), 'View Result')]")
                        result_link = list_links[-1].get_attribute('href')[25:60]
                        result_link = result_link.replace("$", "_")
                    except:
                        continue
                    """
                    The webpage has been loaded, do anything you want
                    """
                    self.find_by_xpath(driver, '//*[@id="'+result_link+'"]').click()
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
                except:
                    pass
            except:
                pass
        driver.close()


def main():
    # dont know why this date works for everyone
    bday = date(1995, 6, 1)
    # start roll
    i = 1201106000
    threads = []
    while i < 1201106400:
        t = Webscraper(i, i + 80, bday, 'http://www.bputexam.in/StudentSection/ResultPublished/StudentResult.aspx')
        threads.append(t)
        i += 80

    for i in threads:
        i.start()
        # well, opening web browsers takes time
        time.sleep(6)
    for i in threads:
        i.join()
    print "Done "


if __name__ == '__main__':
    main()
