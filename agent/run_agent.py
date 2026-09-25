import asyncio

from agent.graph import graph


async def main():

    question = input("\nAsk your database question: ")

    print("\nUser:")
    print(question)

    result = await graph.ainvoke(
        {
            "messages": [
                ("user", question)
            ]
        }
    )

    print("\nFinal Answer:")

    final_message = result["messages"][-1]

    print(final_message.content)


if __name__ == "__main__":
    asyncio.run(main())