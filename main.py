import uvicorn
from core.interceptor import app

if __name__ == "__main__":
    # Boot server locally on your HP Laptop natively using strict loopback mappings
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
