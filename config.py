import os
from dotenv import load_dotenv
import cloudinary

load_dotenv()


cloudinary.config(
  cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
  api_key=os.getenv('CLOUDINARY_API_KEY'),
  api_secret=os.getenv('CLOUDINARY_SECRET_KEY')
)

class Config:
  DEBUG=True
  SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JWT_SECRET_KEY = os.getenv('JWT_SECRET')

config=Config()