
import argparse
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit


load_dotenv()

model=ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.4,
)

def demo_db_creation(db_path:str):
    "Creates a demo e-commerce SQLite database for testing."

    conn=sqlite3.connect(db_path)
    cur=conn.cursor()

    cur.executescript("""
            CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            country TEXT,
            created_at DATE DEFAULT CURRENT_DATE
        );


            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT,
                price REAL NOT NULL,
                stock INTEGER DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customers(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            order_date DATE DEFAULT CURRENT_DATE
        );
        INSERT OR IGNORE INTO customers VALUES
            (1,'Alice Johnson','alice@example.com','USA','2024-01-15'),
            (2,'Bob Smith','bob@example.com','UK','2024-02-20'),
            (3,'Carlos Lima','carlos@example.com','Brazil','2024-03-10'),
            (4,'Diana Prince','diana@example.com','USA','2024-01-05');
        INSERT OR IGNORE INTO products VALUES
            (1,'Laptop Pro','Electronics',1299.99,45),
            (2,'Wireless Mouse','Electronics',29.99,200),
            (3,'Python Book','Books',49.99,120),
            (4,'Standing Desk','Furniture',599.99,15);
        INSERT OR IGNORE INTO orders VALUES
            (1,1,1,1,1299.99,'2024-04-01'),
            (2,1,2,2,59.98,'2024-04-01'),
            (3,2,3,1,49.99,'2024-04-05'),
            (4,3,4,1,599.99,'2024-04-10'),
            (5,4,1,1,1299.99,'2024-04-12'),
            (6,2,2,3,89.97,'2024-04-15');
        """)

    conn.commit()
    conn.close()


def sql_uri(db_path:str,read_only: bool =True):
    absolute_path=Path(db_path).expanduser().resolve()
    if read_only:
        return f"sqlite:///file:{absolute_path.as_posix()}?mode=ro&uri=true"
    return f"sqlite:///{absolute_path.as_posix()}"



def build_agent(db_path:str ,read_only:bool =True):
    db=SQLDatabase.from_uri(sql_uri(db_path,read_only=read_only))
    toolkit=SQLDatabaseToolkit(db=db,llm=model)

    agent = create_sql_agent(
        llm=model,
        toolkit=toolkit,
        agent_type="zero-shot-react-description",
        verbose=False,
)

    return agent,db


def main():
    parser = argparse.ArgumentParser(description="SQL Query Agent")
    parser.add_argument("--db", default="demo.sqlite", help="SQLite database path")
    parser.add_argument("--question", help="Natural language question (omit for interactive)")
    parser.add_argument("--allow-write", action="store_true", help="Open the SQLite database read-write instead of read-only")
    args = parser.parse_args()

    if args.db == "demo.sqlite" and not os.path.exists("demo.sqlite"):
        print("Creating demo e-commerce database...")
        demo_db_creation("demo.sqlite")


    agent,db=build_agent(args.db,read_only=not args.allow_write)
    print(f"\nConnected to: {args.db}")
    print(f"Mode: {'read-write' if args.allow_write else 'read-only'}")
    print(f"Tables: {', '.join(db.get_usable_table_names())}\n")

    if args.question:
        print(f"Question: {args.question}")
        res=agent.invoke({"input":args.question})
        print(f"\nAnswer: {res['output']}")


    else:
        print("SQL Agent ready. Ask questions. Type 'quit' to exit.\n")

        while True:
            question=input("YOU: ").strip()
            if question.lower() in  ("quit", "exit", "q"):
                break
            if not question:
                continue
            res=agent.invoke({'input': question})
            print(f"\nAgent: {res['output']}\n")


if __name__ == "__main__":
    main()
