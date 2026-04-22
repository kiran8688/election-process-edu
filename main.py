from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import ChatbotQuery, PollingLocator

app = FastAPI()

# Configure CORS for local testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:8080", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/educate")
async def educate(query: ChatbotQuery):
    # Mocked, sanitized JSON response
    return {"message": "This is a mocked response for the chatbot query.", "sanitized_query": query.query.strip()}

@app.post("/api/locate")
async def locate(locator: PollingLocator):
    # Mocked, sanitized JSON response
    return {"polling_place": "Mocked Polling Place at 123 Main St", "zip_code": locator.zip_code}
