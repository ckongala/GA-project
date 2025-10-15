import mysql.connector
import pandas as pd
from googletrans import Translator
from transformers import pipeline

def translate_russian_to_english(text):
    translator = Translator()
    try:
        # Split the text into smaller chunks (e.g., 500 characters each)
        chunk_size = 500
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        # Translate each chunk and join the results
        translated_text = ""
        for chunk in chunks:
            translated_chunk = translator.translate(chunk, src='ru', dest='en').text
            translated_text += translated_chunk
            
        return translated_text
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

host = 'ipppppppppp'
port = 3306
database = 'aaaaaaaaaa'
user = 'ccccccccccc'
password = 'zzzzzzzzzz'

try:
    conn = mysql.connector.connect(host=host, port=port, database=database, user=user, password=password)

    if conn.is_connected():
        print('Connected to MySQL database')
        
        cursor = conn.cursor()

        sql_query = 'select id, reply_msg_id, reply_msg, user_id, reply_to_msg_id, original_post_id, reply_datetime, data_tag from telegram.temp_reply_messages where id > 6983 and id <= 10000'
        cursor.execute(sql_query)

        df = pd.DataFrame(columns=['id', 'reply_msg_id', 'reply_msg', 'user_id', 'reply_to_msg_id', "original_post_id", "reply_datetime", "data_tag", 'sentiment_label', "sentiment_score"])

        for row in cursor.fetchall():
            russian_text = row[2]
            translated_text = translate_russian_to_english(russian_text)
            model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
            sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
            
            if translated_text:
                max_seq_length = 512  # Adjust this value based on your model's maximum sequence length
                truncated_text = translated_text[:max_seq_length]
                sentiment = sentiment_task(truncated_text)
                # sentiment = sentiment_task(translated_text)
                df = df.append({'id': row[0], "reply_msg_id": row[1], "reply_msg": row[2], "user_id": row[3], "reply_to_msg_id": row[4], "original_post_id": row[5], "reply_datetime": row[6], 'data_tag': row[7],  'translated_text': truncated_text, 'sentiment_label': sentiment[0]["label"], "sentiment_score": sentiment[0]["score"]}, ignore_index=True)
                # Export DataFrame to Excel after processing each record
                df.to_excel('output2.xlsx', index=False)
                print(f"Record {row[0]} exported to Excel successfully.")
            else:
                print(f"Translation failed for record {row[0]}.")

        cursor.close()
        conn.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")