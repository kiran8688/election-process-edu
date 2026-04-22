from pydantic import BaseModel, Field

class ChatbotQuery(BaseModel):
    query: str = Field(..., min_length=1, description="A natural language query for the chatbot")

class PollingLocator(BaseModel):
    zip_code: str = Field(..., pattern=r"^\d{5}$", description="A 5-digit US zip code")
