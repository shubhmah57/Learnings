from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

# PLAN EXECUTE AND CONCLUDE PATTERN, first its planned to invoke which tool is called from the schema of that tool 
# using that schema actual python method is executed and the response message is again sent back to LLM to generate a human readable response.

@tool
def getSharePrice(symbol: str)->float:
        """Return the current share price for a given ticker symbol"""
        fake_prices = {"AAPL": 241.5, "GOOG": 168.2, "AMZN": 198.0}
        return fake_prices.get(symbol.upper(),0.0)
    
@tool
def getCityWeather(symbol: str)->float:
        """Return the weather for a given symbol for city"""
        fake_weather = {"GURGAON": 41, "NEW YORK":"37","NEW JERSEY":35}
        return fake_weather.get(symbol.upper(),0.0)

class Excersice:

    def invokeLLM(self):
        load_dotenv(override=True)
        open_router_key =  os.getenv('OPEN_ROUTER_API_KEY')
        open_router_base_url = os.getenv('OPEN_ROUTER_BASE_URL')
        open_router_lang_llm = ChatOpenAI(
            model = "openai/gpt-4o-mini",
            base_url=open_router_base_url,
            api_key=open_router_key,
            max_completion_tokens= 1000)
        open_router_lang_llm_with_tools = open_router_lang_llm.bind_tools([getSharePrice,getCityWeather])
        conversation = [HumanMessage("What is the share price of Amazon and weather of Gurgaon ? Also add in response the answer is fictional")]
        ai_message = open_router_lang_llm_with_tools.invoke(conversation)
        print(f"AI Message after first invoke: {ai_message.tool_calls}") # Added for debugging to see tool_calls
        conversation.append(ai_message) # AI messge will have tool_calls as a field in it from that field we can find out which tools needs to be called (Same done by tool_condition in lang)

        for call in ai_message.tool_calls:
            if call["name"] == "getSharePrice":
                result = getSharePrice.invoke(call["args"])
                conversation.append(ToolMessage(content=str(result),tool_call_id= call["id"]))
            if call["name"] == "getCityWeather":
                 result = getCityWeather.invoke(call["args"])
                 conversation.append(ToolMessage(content=str(result),tool_call_id = call["id"]))    
        final = open_router_lang_llm_with_tools.invoke(conversation)
        print(final.content)               


if __name__ == "__main__":
    obj = Excersice()
    obj.invokeLLM()
