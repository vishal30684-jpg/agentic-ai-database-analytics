
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import mysql.connector
import os

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from agent.graph import graph



# Load environment variables


load_dotenv()


# FastAPI application


app = FastAPI(
    title="Agentic AI Database Assistant",
    description="AI-powered MySQL database assistant",
    version="1.0.0"
)

app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)


# CORS


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Database connection


def get_db_connection():

    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )



# Request models


class QuestionRequest(BaseModel):
    question: str
    conversation_id: int | None = None


class ConversationRequest(BaseModel):
    title: str = "New Chat"


# Basic routes


from fastapi.responses import FileResponse

@app.get("/")
def root():
    return FileResponse("frontend/index.html")

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# Create new conversation


@app.post("/conversations")
def create_conversation(request: ConversationRequest):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO conversations (user_id, title)
        VALUES (1, %s)
        """,
        (request.title,)
    )

    conversation_id = cursor.lastrowid

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "conversation_id": conversation_id,
        "title": request.title
    }



# Get all conversations


@app.get("/conversations")
def get_conversations():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, title, created_at, updated_at
        FROM conversations
        WHERE user_id = 1
        ORDER BY updated_at DESC
        """
    )

    conversations = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "conversations": conversations
    }



# Get messages for one conversation


@app.get("/conversations/{conversation_id}/messages")
def get_conversation_messages(conversation_id: int):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, role, content, created_at
        FROM messages
        WHERE conversation_id = %s
        ORDER BY created_at ASC, id ASC
        """,
        (conversation_id,)
    )

    messages = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "conversation_id": conversation_id,
        "messages": messages
    }



# Ask AI


@app.post("/ask")
async def ask_database(request: QuestionRequest):

    conversation_id = request.conversation_id

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Create conversation if needed
 
    if conversation_id is None:

        cursor.execute(
            """
            INSERT INTO conversations (user_id, title)
            VALUES (1, %s)
            """,
            ("New Chat",)
        )

        conversation_id = cursor.lastrowid

        conn.commit()

  
    # Load previous conversation messages
   

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        WHERE conversation_id = %s
        ORDER BY created_at ASC, id ASC
        """,
        (conversation_id,)
    )

    previous_messages = cursor.fetchall()

    cursor.close()
    conn.close()

   
    # Build messages for LangGraph
   

    messages = []

    for message in previous_messages:

        if message["role"] == "user":

            messages.append(
                ("user", message["content"])
            )

        elif message["role"] == "assistant":

            messages.append(
                ("assistant", message["content"])
            )

    # Add current question
    messages.append(
        ("user", request.question)
    )

   
    # Run AI agent
  

    result = await graph.ainvoke(
        {
            "messages": messages
        }
    )

    final_message = result["messages"][-1]

    answer = final_message.content

   
    # Save messages
    

    conn = get_db_connection()
    cursor = conn.cursor()

    # Save user message
    cursor.execute(
        """
        INSERT INTO messages
        (conversation_id, role, content)
        VALUES (%s, %s, %s)
        """,
        (
            conversation_id,
            "user",
            request.question
        )
    )

    # Save AI response
    cursor.execute(
        """
        INSERT INTO messages
        (conversation_id, role, content)
        VALUES (%s, %s, %s)
        """,
        (
            conversation_id,
            "assistant",
            answer
        )
    )

    
    # Update conversation


    cursor.execute(
        """
        UPDATE conversations
        SET
            title = CASE
                WHEN title = 'New Chat'
                THEN %s
                ELSE title
            END,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = %s
        """,
        (
            request.question[:50],
            conversation_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "conversation_id": conversation_id,
        "question": request.question,
        "answer": answer
    }



# Get user memories


@app.get("/memory")
def get_memory():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT memory_key, memory_value
        FROM user_memory
        WHERE user_id = 1
        ORDER BY id ASC
        """
    )

    memories = cursor.fetchall()

    cursor.close()
    conn.close()

    return {
        "memories": memories
    }



# Delete a conversation


@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: int):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM conversations
        WHERE id = %s
        AND user_id = 1
        """,
        (conversation_id,)
    )

    deleted = cursor.rowcount

    conn.commit()

    cursor.close()
    conn.close()

    if deleted == 0:
        return {
            "message": "Conversation not found"
        }

    return {
        "message": "Conversation deleted successfully",
        "conversation_id": conversation_id
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)