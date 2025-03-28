class Config:
  SECRET_KEY = 'simple_secret_key'  # Replace with a secure key in production
  SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz.db'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
