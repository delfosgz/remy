from langgraph.graph import START, END, StateGraph, MessagesState
from langchain_openai import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

#llm
llm = ChatOpenAI(model='gpt-5.4-nano')

# state
class State(MessagesState):
    '''contains extendet state'''

# node
instruction_msg = '''
- Eres un chef personal
- siempre que entiendas una intruccion empieza tu mensaje con la palabra "Oido!"
- refierete a cualquier persona como Cheff
- Tus raices y conocimientos gastronomicos con Mexicanos
- Tu tareaes generar recetas unicamnet con los ingredientes mencionados por el usuario
- Si no se indica lo contrario, asume que se tienen ingredientes y herramientas basicas como [Agua,Sal,Etufa,Sarten,etc.]
'''
def chat(state:State) -> State:
    sys_msg = SystemMessage(content=instruction_msg)
    responce = llm.invoke([sys_msg] + state['messages'])
    return {'messages':[responce]}

# builder
builder = StateGraph(State)

builder.add_node('chat', chat)

builder.add_edge(START, 'chat')
builder.add_edge('chat', END)

app = builder.compile() #no-checkpointer