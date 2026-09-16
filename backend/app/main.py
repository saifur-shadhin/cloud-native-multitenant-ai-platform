from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Cloud-Native Multi-Tenant AI Platform is running!"}
