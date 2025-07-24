# scripts/clean.py

#!/usr/bin/env python3

"""
clean.py

Amaç:
- HTML ve gereksiz karakterleri temizle
- Lower-case
"""

import pandas as pd
import numpy as np
import os
import random as rand
import string
from difflib import get_close_matches
import re

def clean_navigation_text(text):
    # Temizlenecek yaygın kelime ve kalıpların listesi
    # Her kelimeyi veya ifadeyi arama deseni olarak tanımlayın.
    # r'\b...\b' kelimenin tam eşleşmesini sağlar (kelime sınırı).
    # re.IGNORECASE büyük/küçük harf duyarsızlığı sağlar.
    
    patterns = [
        r'\bana sayfa\b',
        r'\banasayfa\b'
        r'\boturum aç\b',
        r'\bkayıt ol\b',
        r'\bbize ulaşın\b',
        r'\bgizlilik politikası\b',
        r'\bhakkımızda\b',
        r'\bşartlar ve koşullar\b',
        r'\bsepetim\b',
        r'\bara\b',
        r'\btelif hakkı\b.*?\d{4}',
        r'\bgeri dön\b',
        r'\btüm hakları saklıdır\b',
        r'\bgiriş yap\b',
        r'\byardım merkezi\b',
        r'\bsitemap\b',
        r'\biletişim\b',
        r'\byakınımdakiler\b',
        r'\bayarlar\b'
        r'\bbağış yapın eğer vikipedi sizin için yararlıysa lütfen bugün bağış yapın.\b'
        r'\bvikipedi hakkında sorumluluk reddi ara\b'
        r'\bdil i̇zle değiştir\b'
        r'\(.*? sayfasından yönlendirildi\)'
        r'(?:diller|\d+\s*dil)\s*(.*?)(?:\s*sayfa en son\.{3}|\s*\n\n|\s*\Z|$)'
        r'sayfa en son\s*(.*?)\s*tarihinde değiştirildi\.\s*(?:aksi belirtilmedikçe içeriğin kullanımı)?\s*(.*?)\s*lisansı kapsamında uygundur\.\s*(.*)'
        r'"\s*https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*?)?"\s*sayfasından alınmıştır\s*son düzenleme\s*(.*?)\s*tarihinde yapıldı'
        r'\bmobil görünüm\b'
        r'\bi̇çeriğe atla\b'
        r'\bana menü\b'
        r'\bkenar çubuğuna taşı\b'
        r'\b\b'
        r'\b\b'
        r'\b\b'
        r'\b\b'
        #Sayısal navigasyonlar (örn: [1] [2] [3]), eğer varsa:
        r'\[\d+\]'
    ]

    for pattern in patterns:
        print(f'{pattern} temizleniyor...')
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
    return text.strip() # Baştaki ve sondaki boşlukları temizle

#A custom function to replace special characters with corresponding letters
def replaceSpecialChars(text):
    # Define character replacements
    char_replacements = {
        '@': 'a',
        '3': 'e',
        '1': 'i',
        '0': 'o',
        '!': 'i',
        '#': 'h',
        '$': 's',
        '5': 's',
        '7': 't',
        '9': 'g'
    }
    # If the input is not a string, return it as-is
    if not isinstance(text, str):
        return text
    # remove empty spaces
    text = text.strip()
    # Replace each special character in the text
    for char, replacement in char_replacements.items():
        text = text.replace(char, replacement)
    
    return text
        

# A function that manipulates strings in columns.
def str_basicclean(df,column ='',style = 'cap',sp_char = string.whitespace, sp_replace = False): # capitalizes strings and strips whitespaces by default, it can strip anything if provided as argument.
    try:
        if df[column].dtype == 'object':
            print('✅ Data type is object')
            if type(sp_char) == str:
                try:
                    df[column] = df[column].str.strip()
                    df[column] = df[column].str.strip(sp_char)
                    print('✅ The string has been stripped')
                except:
                    print('ERROR: Strip function did not work properly')
            else:
                df[column] = df[column].str.strip()
                print('✅ The string has been stripped')
            if style == 'up':
                df[column] = df[column].str.upper()
                print('✅ String has been changed to upper case')
            elif style == 'low':
                df[column] = df[column].str.lower()
                print('✅ String has been changed to lower case')
            elif style == 'cap':
                df[column] = df[column].str.capitalize()
                print('✅ String has been changed to camel case')
        
            if sp_replace == True:
                df[column] = df[column].apply(replaceSpecialChars)
                print('✅ Special characters has been changed')
    except:
        print(f'ERROR: Data Type of the {column} is not object.')
        return 0
    
    print(f'✅✅ The {column} column has been cleaned successfully!')
    return df[column]

def main():
    df = pd.read_csv('./data/traf_data.csv')
    #df['cleaned_content'] = df['content'].apply(clean_text)
    str_basicclean(df, 'content', 'low')
    df.to_csv('./data/cleaned_traf_data.csv', index=False)
    
    #print(df[df['content'].isna()])

    '''
    print("Navigasyon metinleri temizliği başlıyor...")
    df['content'] = df['content'].fillna('')
    df['content']=df['content'].apply(clean_navigation_text)
    '''
    print("✅ Temizleme tamamlandı.")

if __name__ == "__main__":
    main()
