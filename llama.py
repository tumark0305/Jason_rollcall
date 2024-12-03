import ollama

class chat_llama:
    def select_question_filler(_question:str , _select:str):
        _sele_text = ''
        for _counter in range(len(_select)):
            _sele_text = f'{_sele_text}    {_counter}:{_select[_counter]}'
        _output = ollama.chat(model='llama2:13b-chat', messages=[
            {'role':'system','content':'You have to choose answer most suitable with the asking question, reply questions using a single number (0,1,2,3).'},
            {    'role': 'assistant',    'content': 'answer:'},
            {
                'role': 'user',
                'content': f'{_question}? \n select from : {_sele_text}',
            },
        ])
        return _output
    def ask(_question:str , _select:str)->str:
        while True:
            _reply = chat_llama.select_question_filler(_question,_select)
            try:
                _ans = int(_reply['message']['content'][-1])
                break
            except:
                continue
        return _ans

if __name__ == '__main__':
    q0,s0 = '下列何者不是 Python 的特色？',['免費','移植性高','簡單易學','編譯式語言']
    q1,s1 = 'num = 96%5，num 的值為何？',['0','1','19','20']
    print(chat_llama.ask(q1,s1))






