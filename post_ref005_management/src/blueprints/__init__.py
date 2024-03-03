import os

offer_url = os.getenv("OFFER_MS", 'http://localhost:3003')
route_url = os.getenv("ROUTE_MS", 'http://localhost:3002')
post_url = os.getenv("POST_MS", 'http://localhost:3001')
user_url = os.getenv("USER_MS", 'http://localhost:3000')
score_url = os.getenv("SCORE_MS", 'http://localhost:3020')
