from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import glob
import os
import pathlib


class Crawler:
    def __init__(self, report_type, date, download_path, driver_path):
        self.__download_path = download_path
        self.__date = list(date)
        self.__driver_path = driver_path
        self.__report_type = report_type
        pathlib.Path(self.__download_path).mkdir(parents=True, exist_ok=True)
        self.__column_list = 'stationCounty', 'station', 'dataclass', 'datatype', 'datepicker', 'doquery', 'downloadCSV'
        self.__open_browser()
        time.sleep(2)
        self.__crawl()

    def __preprocess(self, id_string):
        self.__id_list = []
        self.__string_list = id_string.split('\n')
        for string in self.__string_list:
            if string.find('撤銷') == -1 and string.strip() != '':
                self.__id_list.append(string.split('(')[0].strip())
        return range(len(self.__id_list))

    def __open_browser(self):
        self.__options = webdriver.ChromeOptions()
        self.__prefs = {'download.default_directory': self.__download_path,
                        "profile.default_content_settings.popups": 0}
        self.__options.add_experimental_option('prefs', self.__prefs)
        self.chrome = webdriver.Chrome(
            executable_path=self.__driver_path, options=self.__options)
        self.chrome.get(
            'https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp')

    def __crawl(self):
        for d in range(len(self.__date)):
            self.__path = os.path.join(
                self.__download_path, self.__report_type, self.__date[d].replace('-', ''))
            pathlib.Path(os.path.realpath(self.__path)).mkdir(
                parents=True, exist_ok=True)
            for i in self.__preprocess(self.chrome.find_element_by_id(self.__column_list[0]).text):
                Select(self.chrome.find_element_by_id(
                    self.__column_list[0])).select_by_index(i)
                time.sleep(.5)
                for k in self.__preprocess(self.chrome.find_element_by_id(self.__column_list[1]).text):
                    Select(self.chrome.find_element_by_id(
                        self.__column_list[1])).select_by_index(k)
                    Select(self.chrome.find_element_by_id(
                        self.__column_list[2])).select_by_index(0)
                    Select(self.chrome.find_element_by_id(
                        self.__column_list[3])).select_by_index((1 if self.__report_type == 'monthly' else 0))
                    self.chrome.find_element_by_id(
                        self.__column_list[4]).clear()
                    self.chrome.find_element_by_id(
                        self.__column_list[4]).send_keys(self.__date[d])
                    self.chrome.find_element_by_id(
                        self.__column_list[5]).click()
                    self.chrome.switch_to.window(self.chrome.window_handles[1])
                    self.chrome.find_element_by_id(
                        self.__column_list[6]).click()
                    self.chrome.close()
                    self.chrome.switch_to.window(self.chrome.window_handles[0])
                    time.sleep(.5)
                    file = max(glob.glob(os.path.join(
                        self.__download_path, '*.csv')), key=os.path.getmtime)
                    os.rename(
                        file,
                        os.path.join(
                            self.__path, f'{os.path.split(file)[1][:6]}-{"".join((s for s in self.__date[d].split("-")))}.csv')
                    )
        self.chrome.close()
