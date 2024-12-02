import os,requests,pyperclip,cv2,pytesseract
import numpy as np
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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
class jason:
    class define:
        def __init__(self, _data):
            self.source = _data
            self.question = jason.define.get_question(_data)
            self.answer = None
            self.error = False
            return None
        @staticmethod
        def get_question(_input_driver)->str:
            _data = _input_driver.find_elements(By.CSS_SELECTOR, 'span.M7eMe')[0].text
            try:
                _text = _data
                _img_element = _input_driver.find_element(By.CLASS_NAME, "y6GzNb")
                _img_url = _img_element.find_element(By.TAG_NAME,"img").get_attribute("src")
                _output = f'{_text}\n\n{tool.url_to_text(_img_url)}'
            except:
                _output = _data
            return _output
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
            for _i ,_cell in enumerate(_urls):
                _text = f'{_text}{_i}.   {_cell}\nTitle : {get_title(_cell)}\n\n'
            print(_text)
            os.system('cls' if os.name=='nt' else 'clear')
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
    def write_form(_url:str)->None:
        driver = webdriver.Chrome()
        driver.get(_url)
        _page_source = driver.page_source
        _questions = driver.find_elements(By.CSS_SELECTOR, 'div.Qr7Oae[role="listitem"]')
        _all_questions = []
        for _quest in _questions:
            _all_questions.append(jason.define(_quest))
        return None
    def main():
        #_url = jason.find_sign_url()
        jason.write_form(test_form_URL)


if __name__ == '__main__':
    jason.main()




