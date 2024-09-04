from pymongo import MongoClient
from bson.objectid import ObjectId

# Підключення до MongoDB
client = MongoClient("mongodb+srv://anastasyavasilievna:NbveH_2012@cluster0.knirp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['cat_database']
collection = db['cats']

# Створення (Create)
def create_cat(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    result = collection.insert_one(cat)
    print(f"Кота додано з id: {result.inserted_id}")

# Читання (Read)
def get_all_cats():
    cats = collection.find()
    for cat in cats:
        print(cat)

def get_cat_by_name(name):
    cat = collection.find_one({"name": name})
    if cat:
        print(cat)
    else:
        print("Кота з таким ім'ям не знайдено")

# Оновлення (Update)
def update_cat_age(name, new_age):
    result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
    if result.matched_count > 0:
        print(f"Вік кота '{name}' оновлено")
    else:
        print("Кота з таким ім'ям не знайдено")

def add_feature_to_cat(name, feature):
    result = collection.update_one({"name": name}, {"$push": {"features": feature}})
    if result.matched_count > 0:
        print(f"Характеристику додано коту '{name}'")
    else:
        print("Кота з таким ім'ям не знайдено")

# Видалення (Delete)
def delete_cat_by_name(name):
    result = collection.delete_one({"name": name})
    if result.deleted_count > 0:
        print(f"Кота з ім'ям '{name}' видалено")
    else:
        print("Кота з таким ім'ям не знайдено")

def delete_all_cats():
    result = collection.delete_many({})
    print(f"Видалено {result.deleted_count} котів")

# Приклад використання функцій
if __name__ == "__main__":
    # Додати кота
    create_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])

    # Отримати всіх котів
    print("\nВсі коти:")
    get_all_cats()

    # Отримати кота за ім'ям
    print("\nКіт з ім'ям 'barsik':")
    get_cat_by_name("barsik")

    # Оновити вік кота
    update_cat_age("barsik", 4)

    # Додати нову характеристику
    add_feature_to_cat("barsik", "любить гратися з м'ячем")

    # Видалити кота
    delete_cat_by_name("barsik")

    # Видалити всіх котів
    delete_all_cats()