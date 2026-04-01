from langgraph.graph import START, END, StateGraph, MessagesState
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_mcp_adapters.client import MultiServerMCPClient     
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from typing import TypedDict, Optional

load_dotenv()

#llm
llm = ChatOpenAI(model='gpt-4o-mini')

# state
class State(MessagesState):
    pass

# schemas
class diner_name_schema(BaseModel):
    diner_name: str = Field('nombre del comensal')

    @field_validator('diner_name', mode='before')
    @classmethod
    def lower_name(cls, value: Optional[str]) -> str:
        if value:
            return value.lower()
        return value
    
    
# in code tools
@tool(args_schema=diner_name_schema)
def get_diners_preferences(diner_name :str) -> str:
    """Útil para obtener las restricciones alimenticias o preferencias de un comensal a partir de su nombre.
    DEBES usar esta herramienta SIEMPRE antes de crear o sugerir una receta para una persona específica."""
    print(f"DEBUG: diner_name recibido -> {diner_name}")
    diners = {
        'camila' : 'sin picante',
        'mama' : 'sin gluten',
        'papa' : 'con picante' 
    }

    if diner_name in diners:
        return f"preference: {diners[diner_name]}"
    else:
        return 'no preferences'

# # ── Conexión al MCP Server ─────────────────────────────────────────────────────
# from langchain_mcp_adapters.client import MultiServerMCPClient

# client = MultiServerMCPClient(
#     {
#         'Cocina_Tools':{
#             'transport':'stdio',
#             'command':'python',
#             'args':['mcp_server.py']
#         }
#     }
# )
# tools = await client.get_tools()
# reso



# tools
tools = [get_diners_preferences] #+ mcp_tools
tool_node = ToolNode(tools)

# node
instruction_msg = '''
- Eres un chef personal
- siempre que entiendas una intruccion empieza tu mensaje con la palabra "Oido!"
- refierete a cualquier persona como Cheff
- Tus raices y conocimientos gastronomicos con Mexicanos
- Tu tarea es generar recetas unicamente con los ingredientes mencionados por el usuario
- Si no se indica lo contrario, asume que se tienen ingredientes y herramientas basicas como [Agua,Sal,Etufa,Sarten,etc.]
- REGLA CRÍTICA: Antes de generar cualquier receta para una persona, DEBES usar la herramienta disponible para verificar si ese comensal tiene preferencias o restricciones alimenticias. No asumas nada sin verificar primero.
'''
def chat(state:State) -> State:
    sys_msg = SystemMessage(content=instruction_msg)
    llm_with_tools = llm.bind_tools(tools)
    responce = llm_with_tools.invoke([sys_msg] + state['messages'])
    return {'messages':[responce]}

# builder
builder = StateGraph(State)

builder.add_node('chat', chat)
builder.add_node('tools', tool_node)

builder.add_edge(START, 'chat')
builder.add_conditional_edges(
    'chat',
    tools_condition,
    {
        'tools' : 'tools',   
        END : END
    }
)
builder.add_edge('tools', 'chat')
app = builder.compile()