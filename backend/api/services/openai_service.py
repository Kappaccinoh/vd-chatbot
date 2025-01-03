from openai import OpenAI
from django.conf import settings
from typing import List, Dict
import json

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-3.5-turbo"
    
    def generate_response(self, user_message: str) -> str:
        """Generate a response using OpenAI's API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant having a conversation with a user."},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            raise Exception("Failed to generate response")

    def extract_topics(self, text: str) -> List[Dict]:
        """Extract topics and their relationships from text"""
        try:
            prompt = """
            Analyze this text and extract key topics and their relationships.
            Format the response EXACTLY as a JSON array of objects with this structure:
            [
                {
                    "topic": "main topic",
                    "related_topics": ["related topic 1", "related topic 2"],
                    "relationship_type": "describes/contains/relates to"
                }
            ]

            Text to analyze:
            {text}

            Remember: Response must be valid JSON array only, no other text.
            """.format(text=text)

            print(f"\nExtracting topics from: {text}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a topic extraction specialist. Return only valid JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            topics_str = response.choices[0].message.content.strip()
            print(f"OpenAI response: {topics_str}")
            
            topics = json.loads(topics_str)
            print(f"Parsed topics: {topics}")
            
            if not topics:  # If empty array
                print("⚠️ No topics extracted")
                return []
                
            return topics
                
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            print(f"Raw response: {topics_str}")
            return []
        except Exception as e:
            print(f"❌ Topic extraction error: {str(e)}")
            return []

    def summarize_conversation(self, transcript: str) -> str:
        """Generate a summary of the conversation"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Summarize the following conversation concisely:"},
                    {"role": "user", "content": transcript}
                ],
                temperature=0.5,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Summarization error: {str(e)}")
            return "Failed to generate summary"

    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze the sentiment of the conversation"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Analyze the sentiment of this text and return a JSON object with 'sentiment' (positive/negative/neutral) and 'confidence' (0-1):"},
                    {"role": "user", "content": text}
                ],
                temperature=0.3,
                max_tokens=50
            )
            
            return json.loads(response.choices[0].message.content.strip())
            
        except json.JSONDecodeError:
            return {"sentiment": "neutral", "confidence": 0}
        except Exception as e:
            print(f"Sentiment analysis error: {str(e)}")
            return {"sentiment": "neutral", "confidence": 0}