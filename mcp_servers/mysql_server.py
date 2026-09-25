from dotenv import load_dotenv
import os
load_dotenv()
from mcp.server.fastmcp import FastMCP
import mysql.connector

mcp = FastMCP("MySQL Database Server")


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )


@mcp.tool()
def local_execute_query(query: str) -> str:
    """Execute a read-only SQL query on the local MySQL database."""

    try:
        query = query.strip()

        # Empty query
        if not query:
            return "Query rejected: empty SQL query."

        # ------------------------------------------
        # Check for multiple SQL statements
        # ------------------------------------------

        # Remove one optional trailing semicolon first
        query_without_semicolon = query.rstrip(";").strip()

        # Check for multiple SQL statements
        in_single_quote = False
        in_double_quote = False

        for char in query_without_semicolon:

            if char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote

            elif char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote

            elif char == ";" and not in_single_quote and not in_double_quote:
               return "Query rejected: multiple SQL statements are not allowed."

        if not query_without_semicolon:
            return "Query rejected: empty SQL query."

        # ------------------------------------------
        # Allowed SQL commands
        # ------------------------------------------

        allowed_commands = (
            "select",
            "show",
            "describe",
            "desc"
        )

        first_word = query_without_semicolon.lower().split()[0]

        if first_word not in allowed_commands:
            return (
                "Query rejected: only read-only SQL queries are allowed. "
                "Allowed commands: SELECT, SHOW, DESCRIBE, DESC."
            )

        # ------------------------------------------
        # Execute query
        # ------------------------------------------

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(query_without_semicolon)

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        if not rows:
            return "No records found."

        return "\n".join(str(row) for row in rows)

    except Exception as e:
        return f"Database error: {str(e)}"


if __name__ == "__main__":
    mcp.run()