from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from googlesearch import search
import uvicorn

app = FastAPI()

# Set up CORS middleware options
origins = [
    "*",
    "https://begzesyud7.us-east-2.awsapprunner.com/"
    "https://jrhkpcmcz5.us-east-2.awsapprunner.com/",
    "http://localhost:80",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins that are allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

#get links 
def google_search_new(search_query, result_n):
    try:
        links = []
        for url in search(search_query, num_results=result_n):
            links.append(url)
        return links
    except Exception as e:
        print(f"Error during Google search: {e}")
        return []

class SearchQuery(BaseModel):
    query: str
    result_n: int

@app.post("/search", response_model=List[str])
def search_google(query: SearchQuery):
    try:
        results = google_search_new(query.query, query.result_n)
        if not results:
            raise HTTPException(status_code=404, detail="No results found")
        print(f'search api{results = }')
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Health Check Endpoint
@app.get("/health")
def read_health():
    return {"status": "healthy"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))