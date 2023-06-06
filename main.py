from fastapi import FastAPI
app = FastAPI() #nom de variable

@app.get("/")
async def root():
    return {"message": "sheshhhhh"}