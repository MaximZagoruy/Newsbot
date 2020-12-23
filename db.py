from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_LINK)
db = client[settings.MONGO_DB]

def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "first_name": effective_user.first_name,
            "last_name": effective_user.last_name,
            "username": effective_user.username,
            "chat_id": chat_id,
            "last_seen": 0
        }
        db.users.insert_one(user)
    return user

def create_news_items(items):
    first_doc = db.news.find_one()
    text = 'updating'
    if db.news.count() == 0:
        docs = [{'id': item['id'], 'date': item['date'], 'text': item['text']} for item in items]
        db.news.insert_many(docs, ordered=True)
    else:
        from_index = list(db.news.find()).index(first_doc)
        if from_index == 0:
            text = 'all up to date'
            return text
        docs = [{'id': item['id'], 'date': item['date'], 'text': item['text']} for item in items[:from_index]]
        db.news.insert_many(docs, ordered=True)
    return text
