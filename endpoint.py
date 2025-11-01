import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import duckdb

app = FastAPI(title="Egypt API", description="Simple API responding with تحيا مصر")
DB_PATH = "my_database.duckdb"

class TaskInput(BaseModel):
    query: str

class TaskResponse(BaseModel):
    message: str

@app.get("/")
async def root():
    return {"message": "تحيا مصر"}

@app.post("/ask_db")
async def process_task(task: TaskInput):
    try:
        sql_query = ""
        print(task.query)
        con = duckdb.connect(DB_PATH)
        print("Successfully connected to db.")
        df = con.execute(task.query).fetchdf()
        con.close()
        # Convert to readable string (limit rows)
        db_response = df.head(1000).to_markdown(index=False)
        return TaskResponse(message="تحيا مصر")
    except Exception as e:        
        raise HTTPException(status_code=400, detail=f"SQL syntax error (Not valid SQL Statement): {e}")
    except duckdb.CatalogException as e:
        raise HTTPException(status_code=404, detail=f"Table or column not found: {e}")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        # Log full traceback for debugging
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    finally:
        if con:
            con.close()
@app.get("/task")
async def get_task():
    return {"message": "تحيا مصر"}

# To run locally: uvicorn main:app --reload