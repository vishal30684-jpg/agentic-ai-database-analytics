import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    server_params = StdioServerParameters(
        command="python",
        args=["mcp_servers/mysql_server.py"],
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                "execute_query",
                {
                    "query": """
                        SELECT
                            c.name,
                            SUM(oi.quantity * oi.price) AS total_spending
                        FROM customers c
                        JOIN orders o
                            ON c.customer_id = o.customer_id
                        JOIN order_items oi
                            ON o.order_id = oi.order_id
                        GROUP BY c.customer_id, c.name
                        ORDER BY total_spending DESC;
                    """
                }
            )

            print("\nQuery Result:\n")

            for content in result.content:
                print(content.text)


if __name__ == "__main__":
    asyncio.run(main())