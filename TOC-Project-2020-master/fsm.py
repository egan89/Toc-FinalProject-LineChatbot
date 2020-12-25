from transitions.extensions import GraphMachine
from utils import send_text_message
from currency import *

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)
        self.currency = []
        self.number = ''
    
    #input_2currency state
    def is_going_to_input_2currency(self, event):
        text = event.message.text
        self.currency = separate(text)
        return ifLegal(self.currency[0], self.currency[1])
        
    def on_enter_input_2currency(self, event):
        send_text_message(event.reply_token, "輸入 check or calculate")
    
    #check state
    def is_going_to_check(self, event):
        text = event.message.text
        return text.lower() == "check"
    
    def on_enter_check(self, event):
        send_text_message(event.reply_token, exRate(self.currency[0], self.currency[1]))
        self.go_back()
  
    #calculate state
    def is_going_to_calculate(self, event):
        text = event.message.text
        return text.lower() == "calculate"

    def on_enter_calculate(self, event):
        send_text_message(event.reply_token, "輸入一個金額")
   
    #input_number state
    def is_going_to_input_number(self, event):
        text = event.message.text
        self.number = text
        return text.isnumeric()
        
    def on_enter_input_number(self, event):
        send_text_message(event.reply_token, exchange(self.currency[0], self.currency[1], self.number))
        self.go_back()
    
