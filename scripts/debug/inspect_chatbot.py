
import inspect
from spoon_ai.chat import ChatBot

try:
    print(inspect.signature(ChatBot.__init__))
except Exception as e:
    print(e)
