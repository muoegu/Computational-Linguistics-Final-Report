import streamlit as st
import pandas as pd

st.title('Japanese to Braille Converter')

st.write('Japanese Braille Data')
df = pd.read_csv('braille_jp.csv')

st.dataframe(df)

input_sentence = st.text_input('Please enter a Katakana string')

st.sidebar.write('Outout Type')

options = st.sidebar.multiselect(
    'Please Choose Output Options',
    ['Braille', 'Hiragana', 'Unicode', 'Number', 'Alphabet'],
    ['Braille']
)

converted_strings_braille = []
converted_strings_hira = []
converted_strings_unicode = []
converted_strings_number = []
converted_strings_alphabet = []

for char in input_sentence:
    matching_row = df[df['kana'] == char]

    if not matching_row.empty:
        if 'Braille' in options:
            converted_strings_braille.append(matching_row.iloc[0]['braille'])
        if 'Hiragana' in options:
            converted_strings_hira.append(matching_row.iloc[0]['hira'])
        if 'Unicode' in options:
            converted_strings_unicode.append(matching_row.iloc[0]['unicode'])
        if 'Number' in options:
            converted_strings_number.append(matching_row.iloc[0]['rep'])
        if 'Alphabet' in options:
            converted_strings_alphabet.append(
                matching_row.iloc[0]['letter_alphabet'])
    else:
        if 'Braille' in options:
            converted_strings_braille.append('N/A')
        if 'Hiragana' in options:
            converted_strings_hira.append('N/A')
        if 'Unicode' in options:
            converted_strings_unicode.append('N/A')
        if 'Number' in options:
            converted_strings_number.append('N/A')
        if 'Alphabet' in options:
            converted_strings_alphabet.append('N/A')

st.write('Katakana:')
st.write(input_sentence)

if 'Braille' in options:
    st.write('Braille:')
    st.write(' '.join(converted_strings_braille))

if 'Hiragana' in options:
    st.write('Hiragana:')
    st.write(' '.join(converted_strings_hira))

if 'Alphabet' in options:
    st.write('Alphabet:')
    st.write(' '.join(converted_strings_alphabet))

if 'Unicode' in options:
    st.write('Unicode:')
    st.write(' '.join(converted_strings_unicode))

if 'Number' in options:
    st.write('Number:')
    st.write(' '.join(converted_strings_number))
