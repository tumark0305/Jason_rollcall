import os,requests,pyperclip
from tqdm import tqdm
URL = f'https://sites.google.com/view/jasontem/'

class jason:
    class define:
        def __init__(self,_number:int,_question:str):
            self.order = _number
            self.question = _question
            self.answer = None
            self.error = False
            return None
        def do_the_question(self):
            self.answer = int(self.question)
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
            _text = 'which might be the right URL?\n'
            for _i ,_cell in enumerate(_urls):
                _text = f'{_text}{_i}.   {_cell}\n'
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
    def write_form()->None:
        return None
    def main():
        _url = jason.find_sign_url()


if __name__ == '__main__':
    jason.main()
    print('s')




