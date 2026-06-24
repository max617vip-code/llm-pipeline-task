import os
import json
import pandas as pd
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def process_data():
    file_path = 'data/input.csv'
    df = pd.read_csv(file_path)
    
    # ОТЛАДКА: Посмотрим, что реально внутри CSV
    print(f"Колонки в файле: {df.columns.tolist()}")
    print(df.head().to_string())

    results = []

    for index, row in df.iterrows():
        # СТРОГАЯ ПРОВЕРКА: Если row['id'] уже содержит "размер 42", 
        # значит CSV кривой, и никакой код не поможет!
        print(f"DEBUG: id={row['id']}, desc={row['description']}")
        
        system_instruction = "Нужно вернуть в файле output.json все данные, Например: Цвет: черный и т.д.'."
        prompt = f"Описание товара: {row['description']}"

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        item_data = json.loads(response.choices[0].message.content)
        
        # Перезаписываем ID строго из колонки CSV
        item_data['id'] = row['id']
        results.append(item_data)

    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print("Готово!")

if __name__ == "__main__":
    process_data()
