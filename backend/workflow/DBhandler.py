import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Any
import os
from core.config import DATABASE_URL



class DBHandler:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL)

    def get_schema(self, table_name: str) -> str:
        """Retrieve the schema (columns & types) for a specific table."""
        try:
            with self.conn.cursor() as cur:
                cur.execute("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    AND table_name = %s
                    ORDER BY ordinal_position;
                """, (table_name,))
                
                rows = cur.fetchall()
                
                if not rows:
                    return f"No table found with name '{table_name}'"
                
                schema = "\n".join([f"{table_name}: {col} ({dtype})" for col, dtype in rows])
                return schema
        except Exception as e:
            raise Exception(f"Error fetching schema for {table_name}: {str(e)}")

    def execute_query(self, table_name: str, query: str, isParamertized: bool = True) -> List[Any]:
        """Execute SQL query on the given table and return results."""
        try:

            print(f"Executing query on {table_name}: {query}")
            with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Ensure table_name is safely injected (avoid SQL injection by quoting)
                from psycopg2 import sql
                formatted_query = sql.SQL(query).format(
                    table=sql.Identifier(table_name)
                )
                if isParamertized:
                    cur.execute(formatted_query)
                else:
                    print("Executing non-parametrized query")
                    cur.execute(query)
                    print("After executing non-parametrized query")
                
                print(f"Query executed successfully on {table_name}")
                
                if cur.description:  # SELECT
                    return cur.fetchall()
                else:  # INSERT / UPDATE / DELETE
                    return []
        except Exception as e:
            self.conn.rollback()
            print(f"Failed executing query on {table_name}: {str(e)}")
            raise Exception(f"Error executing query on {table_name}: {str(e)}")
