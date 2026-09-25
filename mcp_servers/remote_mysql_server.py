
from mcp.server.fastmcp import FastMCP
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv("mcp_servers/.env.remote")

mcp = FastMCP("Remote MySQL Database Server")


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("REMOTE_MYSQL_HOST"),
        user=os.getenv("REMOTE_MYSQL_USER"),
        password=os.getenv("REMOTE_MYSQL_PASSWORD"),
        database=os.getenv("REMOTE_MYSQL_DATABASE")
    )


@mcp.tool()
def remote_execute_query(query: str) -> str:
    """Execute a read-only SQL query on the remote MySQL database."""

    try:

        # Only allow read-only queries
        query = query.strip()

        if not query:
         return "Query rejected: empty SQL query."

# Block multiple SQL statements
        if query.rstrip().count(";") > 1:
         return "Query rejected: multiple SQL statements are not allowed."

     # Allow only read-only SQL commands
        allowed = (
           "select",
           "show",
           "describe",
           "desc"
      )

        first_word = query.lower().split()[0]

        if first_word not in allowed:
          return (
        "Query rejected: only read-only SQL queries are allowed. "
        "Allowed commands: SELECT, SHOW, DESCRIBE, DESC."
       )

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        if not rows:
            return "No records found."

        return "\n".join(str(row) for row in rows)

    except Exception as e:
        return f"Database error: {str(e)}"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        mcp.streamable_http_app,
        host="127.0.0.1",
        port=8001
    )