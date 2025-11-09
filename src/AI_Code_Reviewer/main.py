from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


@app.post("/debug")
async def test(request: Request):
    print("========== New Request ==========")
    
    # 1. Print Basic Info
    print(f"Method: {request.method}")
    print(f"URL: {request.url}")
    print(f"Client: {request.client.host}:{request.client.port}")

    # 2. Print Headers
    print("\n--- Headers ---")
    for name, value in request.headers.items():
        print(f"{name}: {value}")

    # 3. Print Query Parameters
    if request.query_params:
        print("\n--- Query Params ---")
        for name, value in request.query_params.items():
            print(f"{name}: {value}")
            
    # 4. Print Path Parameters (if any, e.g., /debug/{item_id})
    if request.path_params:
        print("\n--- Path Params ---")
        for name, value in request.path_params.items():
            print(f"{name}: {value}")

    # 5. Print Raw Body
    print("\n--- Body (raw) ---")
    body = await request.body()
    if body:
        try:
            # Try to decode as UTF-8 text (e.g., for JSON, form data)
            print(body.decode('utf-8'))
        except UnicodeDecodeError:
            # If it's binary data (e.g., an image), just show length
            print(f"[Binary data: {len(body)} bytes]")
    else:
        print("[No body]")
    
    print("=================================\n")

    # Return a confirmation response
    return {"message": "Request details printed to server console"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)