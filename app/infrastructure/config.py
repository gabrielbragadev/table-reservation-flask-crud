class Config:
    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:admin123@127.0.0.1:3306/table-reservation"
    )
