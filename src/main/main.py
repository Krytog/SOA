from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/hello")
async def greet_user(username):
    print("Hello, dear", username)
    return JSONResponse(content={"message": "hello, dear " + username}, status_code=status.HTTP_200_OK);