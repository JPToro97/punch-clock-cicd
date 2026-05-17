from fastapi import FastAPI

app = FastAPI(title="Punch-Clock CI/CD Project")

@app.get("/")
def read_root():
    return {"message": "Punch-Clock API is online!", "stage": 1}

@app.get("/health")
def health_check():
    return {"status": "healthy", "containers_communicating": True}