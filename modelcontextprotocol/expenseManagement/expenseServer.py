from mcp.server.fastmcp import FastMCP
import csv
from pathlib import Path
from datetime import date

ExpenseFile = Path(__file__).with_name("expenses.csv")
mcp = FastMCP("Expense Tools")

@mcp.tool()
def expenseSummary(month: str) -> dict:
    """Calculate spending for a month in YYYY-MM format from the demo CSV.
    Amounts are whole INR rupees. Return category totals and all top categories.
    Only includes rows in this file; this is not a bank connection.
    """
    #date.fromisoformat(month + "-01")
    categories: dict[str, int] = {}

    with ExpenseFile.open(newline="",encoding="UTF-8") as file:
        for row in csv.DictReader(file):
            if date.fromisoformat(row["date"]).strftime("%Y-%m") != month:
                continue
            category = row["category"]
            amount = int(row["amount"])
            categories[category] = categories.get(category, 0) + amount
    highest = max(categories.values(), default=0)
    return {
        "month":month,
        "currency": "INR",
        "total": sum(categories.values()),
        "by_category": categories,
        "top_categories":[
            key for key, value in categories.items() if value == highest
        ]
    }

if __name__ == "__main__":
    mcp.run()

