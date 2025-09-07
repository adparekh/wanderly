from utils.load_model import LoadModel
from prompts.prompt import SYSTEM_PROMPT
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

from tools.weather_info import WeatherInfo
from tools.place_search import PlacesSearch
from tools.calculator import ExpenseCalculator
from tools.currency_conversion import CurrencyConversion
    
class GraphBuilder():
    def __init__(self, model_provider: str = "openai"):
        self.load_model = LoadModel(model_provider=model_provider)
        self.llm = self.load_model.load_llm()

        self.tools = []

        self.weather_tools = WeatherInfo()
        self.places_search_tools = PlacesSearch()
        self.calculator_tools = ExpenseCalculator()
        self.currency_converter_tools = CurrencyConversion()

        self.tools.extend([
            * self.weather_tools.weather_tool_list, 
            * self.places_search_tools.places_search_tool_list,
            * self.calculator_tools.calculator_tool_list,
            * self.currency_converter_tools.currency_conversion_tool_list
        ])

        self.llm_with_tools = self.llm.bind_tools(tools=self.tools)

        self.graph = None

        self.system_prompt = SYSTEM_PROMPT

    def agent_function(self, state: MessagesState):
        """Main agent function"""
        user_question = state["messages"]
        input_question = [self.system_prompt] + user_question
        response = self.llm_with_tools.invoke(input_question)

        return {"messages" : [response]}

    def build_graph(self):
        graph_builder = StateGraph(MessagesState)

        graph_builder.add_node("agent", self.agent_function)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))
        graph_builder.add_edge(START, "agent")
        graph_builder.add_conditional_edges("agent", tools_condition)
        graph_builder.add_edge("tools", "agent")
        graph_builder.add_edge("agent", END)

        self.graph = graph_builder.compile()

        return self.graph

    def __call__(self):
        return self.build_graph()