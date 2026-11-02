from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio
from datetime import date
import asyncio
import sys
from utils.modelconfig import ModelConfig

class ExpenseManagement(ModelConfig):
    def __init__(self):
        super().__init__()
    INSTRUCTIONS = """"""
    async def main(self)-> "None":
        expense_server_file = Path(__file__).with_name("expenseServer.py").resolve()

        async with MCPServerStdio(name = "Expense Management",params = {"command" : sys.executable,"args" : [str(expense_server_file)]},cache_tools_list=True) as expense_server:
            agent = Agent(name = "Expense Assistant", model= self.model,instructions=(
             f"Today's local date is {date.today().isoformat()}. "
                "For spending questions, call expense_summary with YYYY-MM. "
                "Use the tool result only. Reply briefly in Hinglish. "
                "Show the month, total INR, category totals, and top categories. "
                "These figures cover only the supplied CSV, not all bank spending. "
                "If no categories are returned, say no records were found for "
                "that month. If the tool fails, explain without inventing amounts."
        ),mcp_servers=[expense_server],model_settings=self.model_settings)
            question = "October month kitna kharacha hua ?"
            result = await Runner.run(agent,question,max_turns=3)
            print(f"Answer is {result.final_output}")

if __name__=="__main__":
    asyncio.run(ExpenseManagement().main())
