import os,requests,pyperclip,cv2,pytesseract
import numpy as np
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime

from llama import chat_llama
silent_run = True
test_form_URL = f'https://docs.google.com/forms/d/e/1FAIpQLSdUTn-QCfLkyHBM9jQtuH0zJ9jpv-OSsZpCrNb8aSD_y1TYdQ/viewform?usp=sf_link'
URL = f'https://sites.google.com/view/jasontem/'
keyinID = 'b11007157'
keyinNAME = '我是機器人0'
target = 'LLaMA 2-13B'
class tool:
    def url_to_text(_url:str)->str:
        _save_path = f'{os.getcwd()}\\caches'
        _data = requests.get(_url).content
        _img_array = np.frombuffer(_data, dtype=np.uint8)
        _img = cv2.imdecode(_img_array, cv2.IMREAD_COLOR)
        _text = tool.img_to_text(_img)
        return _text
    def img_to_text(_img)->str:
        _net = cv2.dnn.readNet("frozen_east_text_detection.pb")
        _blob = cv2.dnn.blobFromImage(_img, 1.0, (320, 320), (123.68, 116.78, 103.94), True, crop=False)
        _net.setInput(_blob)
        _data = _net.getUnconnectedOutLayersNames()
        _net.forward()
        _text = pytesseract.image_to_string(_img)
        return _text
    def ask_llama(_data)->None:
        _q = _data.question
        _s = _data.select
        if _q == jason.ID_find:
            _output = keyinID
        elif _q == jason.NAME_find:
            _output = keyinNAME
        else:
            while True:
                _output = chat_llama.ask(_q,_s)
                if _output<len(_s):
                    break
        _data.answer = _output
        return None
class jason:
    ID_find = '學號'
    NAME_find = '姓名'
    _log_path = f'{os.getcwd()}\\log'
    class define:
        def __init__(self,_main_driver , _data):
            self.driver = _main_driver
            self.source = _data
            self.question = None
            self.answer = None
            self.type = None
            self.error = False
            self.select = []
            self.select_check_box_loc = []
            jason.define.get_question(self ,_data)
            jason.define.get_selection(self ,_data)
            return None
        def get_question(self , _input_driver)->None:
            def test_if_isfill():
                _page_source = _input_driver.get_attribute("outerHTML")
                if 'AB7Lab Id5V1' in _page_source:
                    self.type = 'sele'
                else:
                    self.type = 'fill'
                return None
            test_if_isfill()
            _data = _input_driver.find_element(By.CSS_SELECTOR, 'span.M7eMe').text

            try:
                _text = _data
                _img_element = _input_driver.find_element(By.CLASS_NAME, "y6GzNb")
                _img_url = _img_element.find_element(By.TAG_NAME,"img").get_attribute("src")
                _output = f'{_text}\n\n{tool.url_to_text(_img_url)}'
            except:
                _output = _data
            self.question = _output
            return None
        def get_selection(self , _input_driver)->None:
            if self.type == 'sele':
                _selections = _input_driver.find_elements(By.CSS_SELECTOR, ".nWQGrd.zwllIb")
                for _statment in _selections:
                    self.select.append(_statment.text)
                    _page_source = _statment.get_attribute("outerHTML")
                    _find_button = _statment.find_element(By.CSS_SELECTOR, '[jscontroller="EcW08c"]')
                    _buttom = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable(_find_button)
                    )
                    self.select_check_box_loc.append(_buttom)
            elif self.type == 'fill':
                _fill_block = _input_driver.find_elements(By.CSS_SELECTOR, '[jsname="YPqjbf"]')[1]
                self.select_check_box_loc.append(_fill_block)
            return None

    def find_sign_url()->str:
        def get_possible_url()->list[str]:
            _text = requests.get(URL).text
            _list = _text.split('"')
            _new_list = []
            for _test in _list:
                if 'jasontem' in _test and  _test.startswith('/view/'):
                    _new_list.append(_test)
            _new_list = list(set(_new_list))
            _all_url_list = [URL]
            return [f'https://sites.google.com{_url}' for _url in _new_list]
        def find_google_doc(_all_url:list[str]):
            output = []
            for _url in tqdm(_all_url):
                _text = requests.get(_url).text
                for _soup in _text.split('"'):
                    if 'docs.google.com/forms' in _soup:
                        output.append(_soup)
            return output
        def ask_which(_urls:list[str]):
            def get_title(_input_url:str)->str:
                _url_data = requests.get(_input_url).text
                _output = []
                for _finder in _url_data.split('<'):
                    if 'F9yp7e' in _finder:
                        _output.append(_finder.split('>')[1])
                return _output[0]
            _text = 'which might be the right URL?\n'
            _urls.append(test_form_URL)
            for _i ,_cell in enumerate(_urls):
                _text = f'{_text}{_i}.   {_cell}\nTitle : {get_title(_cell)}\n\n'
            os.system('cls' if os.name=='nt' else 'clear')
            print(_text)
            while True:
                _input_data = input(f'>>>    ')
                try:
                    _selector = int(_input_data)
                except:
                    print('Unreconized number.')
                    continue
                finally:
                    if _selector <= len(_urls):
                        _output = _urls[_selector]
                        break
                    else:
                        print(f'Need number from 0 to {len(_urls)}')
                        continue
            os.system('cls' if os.name=='nt' else 'clear')
            return _output
        _all_urls = get_possible_url()
        _sus_urls = find_google_doc(_all_urls)
        _url = ask_which(_sus_urls)
        return _url
    def fill_answer(_all_data)->None:
        for _question in _all_data:
            if _question.type == 'fill':
                _question.select_check_box_loc[0].send_keys(_question.answer)
            elif _question.type == 'sele':
                _question.select_check_box_loc[_question.answer].click()
            pass
        return None
    def write_form(_url:str)->None:
        def press_send():
            _send_buttom = driver.find_element(By.CSS_SELECTOR, '.uArJ5e.UQuaGc.Y5sE8d.VkkpIf.QvWxOd')
            _buttom = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(_send_buttom)
            )
            _buttom.click()
            return None
        def write_log(_all):
            def form_txt():
                _output = ''
                for _qs in _all:
                    _local_text = ''
                    for _sele_num in range(len(_qs.select)):
                        _local_text = f'{_local_text}{_sele_num}:{_qs.select[_sele_num]}\n'
                    try:
                        _output = f'{_output}{_qs.question}\n{_local_text}ans:-->{_qs.answer}:{_qs.select[_qs.answer]}\n'
                    except:
                        _output = f'{_output}{_qs.question}\n{_local_text}ans:-->{_qs.answer}\n'
                return _output
            _date = str(datetime.now())[5:16].replace(':','').replace('-','').replace(' ','_')
            _path = f'{jason._log_path}\\{_date}.txt'
            _text = form_txt()
            _f = open(_path,'w')
            _f.write(_text)
            _f.close()
        def get_driver():
            if silent_run:
                options = Options()
                options.add_argument('--headless')
                options.add_argument('--disable-gpu')
                _output = webdriver.Chrome( options=options)
            else:
                _output = webdriver.Chrome()
            return _output
        driver = get_driver()
        driver.get(_url)
        _page_source = driver.page_source
        _questions = driver.find_elements(By.CSS_SELECTOR, 'div.Qr7Oae[role="listitem"]')
        _all_questions = []
        for _quest in _questions:
            _all_questions.append(jason.define(driver , _quest))
        #solve q
        for _cell in _all_questions:
            tool.ask_llama(_cell)
        write_log(_all_questions)
        jason.fill_answer(_all_questions)
        if silent_run:
            _input_data = 'y'
        else:
            _input_data = input('送出表單? y/N')
        if _input_data=='y':
            press_send()
        driver.quit()
        return None
    def main():
        if silent_run:
            jason.write_form(test_form_URL)
        else:
            _url = jason.find_sign_url()
            jason.write_form(test_form_URL)


if __name__ == '__main__':
    if silent_run:
        for i in range(100):
            jason.main()
    else:
        jason.main()
    




