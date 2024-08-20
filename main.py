import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from googlesearch import search
import uvicorn
import httpx
import asyncio

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

# #get links 
# def google_search_new(search_query, result_n):
#     try:
#         links = []
#         for url in search(search_query, num_results=result_n):
#             links.append(url)
#         return links
#     except Exception as e:
#         print(f"Error during Google search: {e}")
#         return []

#test new logic
# Function to select a random user agent
def select_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
    ]
    return random.choice(user_agents)

# Get links with user-agent rotation
def google_search_new(search_query, result_n):
    try:
        links = []
        user_agent = select_random_user_agent()
        headers = {"User-Agent": user_agent}
        
        for url in search(search_query, num_results=result_n, extra_params=None, headers=headers):
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
            print(f"No results found")
            results = []
        print(f'search api{results = }')
        return results
    except Exception as e:
        print(f"Error during search process: {e}")
        return []
    
#Health Check Endpoint
@app.get("/health")
def read_health():
    print('server awake')
    return {"status": "healthy"}

async def keep_awake():
    while True:
        try:
            async with httpx.AsyncClient() as client:
                await client.get("https://search-res-microservice.onrender.com/health")
            await asyncio.sleep(600)  # Sleep for 10 minutes
        except Exception as e:
            print(f"Error keeping the service awake: {e}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(keep_awake())



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))