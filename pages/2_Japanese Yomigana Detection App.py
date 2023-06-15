import streamlit as st
from kana_convert.main_jp3 import kana_converter

st.set_page_config(
    page_title="braille-app (JP)",
    page_icon="👋",
)

st.title('Japanese Yomigana Detection App (Yomigana GPT)')


def main():
    st.write("Find Pronunciation for Character")
    sentence = st.text_area('Enter Japanese sentence here')
    convert_button = st.button("Detect")
    if sentence and convert_button:
        try:
            # avoid consume token
            # result = sentence
            prompt, result = kana_converter(sentence)
            st.write('Result:')
            st.write(result)

            st.write('Prompt:')
            st.write(prompt)
        except ValueError:
            st.write("Please enter only Japanese characters")


if __name__ == '__main__':
    main()
