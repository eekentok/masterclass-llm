import json
import os

MODELS_FILE = "./data/models.json"

def load_models():
    if not os.path.exists(MODELS_FILE):
        with open(MODELS_FILE, "w") as f:
            json.dump([], f)
    with open(MODELS_FILE, "r") as f:
        return json.load(f)

def save_models(models):
    with open(MODELS_FILE, "w") as f:
        json.dump(models, f, indent=4)

def generate_new_id(models):
    if not models:
        return 1
    return max(model["model_id"] for model in models) + 1

def add_model(model_name, model_title, model_category):
    if model_category not in ["normal", "experimental","default"]:
        print("❌ model_category sadece 'normal', 'experimental' veya 'default' olabilir.")
        return

    models = load_models()
    new_id = generate_new_id(models)

    new_model = {
        "model_id": new_id,
        "model_name": model_name,
        "model_title": model_title,
        "model_category": model_category
    }

    models.append(new_model)
    save_models(models)
    print(f"✅ Model eklendi: {model_title} (ID: {new_id})")

def edit_model(model_id, new_name=None, new_title=None, new_category=None):
    models = load_models()
    found = False
    for model in models:
        if model["model_id"] == model_id:
            if new_name:
                model["model_name"] = new_name
            if new_title:
                model["model_title"] = new_title
            if new_category:
                if new_category not in ["normal", "experimental","default"]:
                    print("❌ model_category sadece 'normal', 'experimental' veya 'default' olabilir.")
                    return
                model["model_category"] = new_category
            found = True
            break

    if found:
        save_models(models)
        print(f"✅ Model ID {model_id} güncellendi.")
    else:
        print(f"❌ Model ID {model_id} bulunamadı.")

def delete_model(model_id):
    models = load_models()
    for model in models:
        if model["model_id"] == model_id:
            confirm = input(f"⚠️ Modeli silmek istediğinize emin misiniz? ({model['model_title']}) [y/n]: ")
            if confirm.lower() == "y":
                models.remove(model)
                save_models(models)
                print(f"🗑️ Model ID {model_id} silindi.")
            else:
                print("❎ Silme işlemi iptal edildi.")
            return
    print(f"❌ Model ID {model_id} bulunamadı.")

def list_models():
    models = load_models()
    if not models:
        print("📂 Hiç model bulunamadı.")
        return

    print("📂 Mevcut Modeller:")
    for model in models:
        print(f"---------------------------------\nID: {model['model_id']}\n Ad: {model['model_name']}\n Başlık: {model['model_title']}\n Kategori: {model['model_category']}\n---------------------------------")


def main():
    while True:
        print("\nModel Yönetimi")
        print("1. Model Ekle")
        print("2. Model Düzenle")
        print("3. Model Sil")
        print("4. Modelleri Listele")
        print("-q: Çıkış")

        choice = input("Seçiminizi yapın: ")
        
        if choice == "1":
            name = input("Model Adı: ")
            title = input("Model Başlığı: ")
            category = input("Model Kategorisi (normal/experimental): ")
            add_model(name, title, category)
        elif choice == "2":
            model_id = int(input("Düzenlenecek Model ID: "))
            new_name = input("Yeni Model Adı (boş bırakmak için Enter): ") or None
            new_title = input("Yeni Model Başlığı (boş bırakmak için Enter): ") or None
            new_category = input("Yeni Model Kategorisi (normal/experimental/default, boş bırakmak için Enter): ") or None
            edit_model(model_id, new_name, new_title, new_category)
        elif choice == "3":
            model_id = int(input("Silinecek Model ID: "))
            delete_model(model_id)
        elif choice == "4":
            list_models()
        elif choice == "-q" or choice == "--quit":
            print("Çıkılıyor...")
            break
        else:
            print("❌ Geçersiz seçim, lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()