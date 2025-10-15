# import mysql.connector
# # !pip install googletrans==4.0.0-rc1
# from googletrans import Translator
# from transformers import pipeline
# import pandas as pd

# def translate_russian_to_english(text):
#     translator = Translator()
#     try:
#         # Split the text into smaller chunks (e.g., 500 characters each)
#         chunk_size = 500
#         chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
#         # Translate each chunk and join the results
#         translated_text = ""
#         for chunk in chunks:
#             translated_chunk = translator.translate(chunk, src='ru', dest='en').text
#             translated_text += translated_chunk
            
#         return translated_text
        
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None


# host = '144.167.34.17'
# port = 3306
# database = 'telegram'
# user = 'ckongala'
# password = 'C@DbConnect@1'

# try:
#     conn = mysql.connector.connect(host=host, port=port, database=database, user=user, password=password)

#     if conn.is_connected():
#         print('Connected to MySQL database')
        
#         cursor = conn.cursor()

#         sql_query = 'select posts.id, posts.message from telegram.posts limit 3'

#         cursor.execute(sql_query)

#         data = cursor.fetchall()
#         li = []

#         for row in data:
#             li.append(row)
#         cursor.close()
#         conn.close()
#         for i in range(len(li)):
#             print("id", li[i][0])
#             print("russian language", li[i][1])
#             print("#" * 100)
#             russian_text = li[i][1]
#             translated_text = translate_russian_to_english(russian_text)
#             model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
#             sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
#             if translated_text:
#                 print("@" * 100)
#                 print("Translated text in English:", translated_text)
#                 print("@" * 100)
#                 print("!" * 200)
#                 sent = sentiment_task(translated_text)
#                 print(sent, "sentttttttttttttttttttttt")
#                 sent_lab = sent[0]["label"]
#                 sent_score = sent[0]["score"]
#                 print(sent_lab)
#                 print("!" * 200)
#             else:
#                 print("Translation failed.")
#                 print("@" * 100)

# except mysql.connector.Error as err:
#     print(f"Error: {err}")
#################################################################################################################################################################################


# import mysql.connector
# import pandas as pd
# from googletrans import Translator
# from transformers import pipeline


# def translate_russian_to_english(text):
#     translator = Translator()
#     try:
#         # Split the text into smaller chunks (e.g., 500 characters each)
#         chunk_size = 500
#         chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
#         # Translate each chunk and join the results
#         translated_text = ""
#         for chunk in chunks:
#             translated_chunk = translator.translate(chunk, src='ru', dest='en').text
#             translated_text += translated_chunk
            
#         return translated_text
        
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# host = '144.167.34.17'
# port = 3306
# database = 'telegram'
# user = 'ckongala'
# password = 'C@DbConnect@1'

# try:
#     conn = mysql.connector.connect(host=host, port=port, database=database, user=user, password=password)

#     if conn.is_connected():
#         print('Connected to MySQL database')
        
#         cursor = conn.cursor()

#         sql_query = 'select id, reply_msg_id, reply_msg, user_id, reply_to_msg_id, original_post_id, reply_datetime, data_tag from telegram.temp_reply_messages where id > 200 and id <= 350'
#         cursor.execute(sql_query)

#         data = cursor.fetchall()
#         cursor.close()
#         conn.close()

#         df = pd.DataFrame(columns=['id', 'reply_msg_id', 'reply_msg', 'user_id', 'reply_to_msg_id', "original_post_id", "reply_datetime", "data_tag", 'sentiment_label', "sentiment_score"])

#         for row in data:
#             russian_text = row[2]
#             translated_text = translate_russian_to_english(russian_text)
#             model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
#             sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
            
#             if translated_text:
#                 sentiment = sentiment_task(translated_text)
#                 df = df.append({'id': row[0],"reply_msg_id": row[1], "reply_msg": row[2], "user_id": row[3], "reply_to_msg_id": row[4], "original_post_id":row[5], "reply_datetime":row[6], 'data_tag': row[7],  'translated_text': translated_text, 'sentiment_label': sentiment[0]["label"], "sentiment_score": sentiment[0]["score"]},ignore_index=True)
#             else:
#                 print("Translation failed.")

#         # Export DataFrame to Excel
#         df.to_excel('output.xlsx', index=False)
#         print("Data exported to Excel successfully.")

# except mysql.connector.Error as err:
#     print(f"Error: {err}")
####################################################################################################################################################################################################################################################################################################################################################################################


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

host = '144.167.34.17'
port = 3306
database = 'telegram'
user = 'ckongala'
password = 'C@DbConnect@1'

try:
    conn = mysql.connector.connect(host=host, port=port, database=database, user=user, password=password)

    if conn.is_connected():
        print('Connected to MySQL database')
        
        cursor = conn.cursor()

        sql_query = 'select id, reply_msg_id, reply_msg, user_id, reply_to_msg_id, original_post_id, reply_datetime, data_tag from telegram.temp_reply_messages where id > 200 and id <= 2000'
        cursor.execute(sql_query)

        df = pd.DataFrame(columns=['id', 'reply_msg_id', 'reply_msg', 'user_id', 'reply_to_msg_id', "original_post_id", "reply_datetime", "data_tag", 'sentiment_label', "sentiment_score"])

        for row in cursor.fetchall():
            russian_text = row[2]
            translated_text = translate_russian_to_english(russian_text)
            model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
            sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)
            
            if translated_text:
                sentiment = sentiment_task(translated_text)
                df = df.append({'id': row[0], "reply_msg_id": row[1], "reply_msg": row[2], "user_id": row[3], "reply_to_msg_id": row[4], "original_post_id": row[5], "reply_datetime": row[6], 'data_tag': row[7],  'translated_text': translated_text, 'sentiment_label': sentiment[0]["label"], "sentiment_score": sentiment[0]["score"]}, ignore_index=True)
                # Export DataFrame to Excel after processing each record
                df.to_excel('output.xlsx', index=False)
                print(f"Record {row[0]} exported to Excel successfully.")
            else:
                print(f"Translation failed for record {row[0]}.")

        cursor.close()
        conn.close()

except mysql.connector.Error as err:
    print(f"Error: {err}")
