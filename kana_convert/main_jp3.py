import re
from jisho_api.sentence import Sentence
from jisho_api.word import Word
from janome.tokenizer import Tokenizer
from langchain import PromptTemplate
from langchain.llms import OpenAI

import os


os.environ["OPENAI_API_KEY"] = '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'

# analyze text with Janome


def analyze_text(input_text):
    t = Tokenizer()
    tokens = t.tokenize(input_text)
    analyzed_tokens = []
    for token in tokens:
        analyzed_tokens.append(
            [token.surface, token.part_of_speech, token.reading, token.phonetic])
    return analyzed_tokens


def check_kanji(string):
    kanji_pattern = re.compile(r"[\u4e00-\u9faf]")
    match = kanji_pattern.search(string)

    if match:
        return True
    else:
        return False


def convert_results_to_dictionary(result):
    dictionary = {}

    for sublist in result:
        word = sublist[0]
        pos = sublist[1]
        reading = sublist[2]
        phonetic = sublist[3]

        entry = {'pos': pos, 'reading': reading, 'phonetic': phonetic}

        if word in dictionary:
            dictionary[word].append(entry)
        else:
            dictionary[word] = [entry]

    return dictionary


def format_result(result):

    dictionary = convert_results_to_dictionary(result)

    formatted_result = []

    for word, entries in dictionary.items():
        if check_kanji(word):
            if len(entries) == 1:
                formatted_result.append(
                    word + '(' + entries[0]['reading'] + ') ')
            else:
                formatted_result.append(word + ' - ambiguous ')
        else:
            formatted_result.append(word + '(' + entries[0]['reading'] + ') ')

    return '\n'.join(formatted_result)


"""def filter_surface(word_list):
    surface = []
    for item in word_list:
        word = item[0]
        surface.append(word)
    return surface"""


def get_all_unknown_words_and_sentences(dictionary):
    return '\n'.join([get_dictionary_entries(word) for word, entries in dictionary.items() if len(entries) > 1 and check_kanji(word)])


def get_dictionary_entries(word):
    return_list = list()
    word_results = Word.request(word)
    if word_results.meta.status == 200 and word_results.data:

        return_list.append(f"Word information for '{word}'")

        word_results = Word.request(word)

        if word_results.meta.status == 200 and word_results.data:
            if len(word_results.data) == 1:
                for word_config in word_results.data:
                    return_list.append("reading must be: " +
                                       word_results.data[0].japanese[0].reading)

            else:
                for word_config in word_results.data:
                    slug = word_config.slug
                    japanese = word_config.japanese
                    senses = word_config.senses

                    return_list.append("Word:" + slug)
                    return_list.append(
                        "JP:" + word_results.data[0].japanese[0].reading)
                    return_list.append("meaning:")
                    for sense in senses:
                        english_definitions = sense.english_definitions
                        parts_of_speech = sense.parts_of_speech
                        return_list.append(
                            "- En:" + ', '.join(english_definitions))
                        return_list.append(
                            "  POS:" + ', '.join(parts_of_speech))

        else:
            return_list.append("No words found.")

        return_list.append(f"example sentences with'{word}'")

        sentence_results = Sentence.request(word)
        if sentence_results.meta.status == 200 and sentence_results.data:
            for sentence_config in sentence_results.data:
                japanese_sentence = sentence_config.japanese
                return_list.append("Example:" + japanese_sentence)

        else:
            return_list.append("There was no example sentence.")

    return '\n'.join(return_list)


template = """
How to read following Japanese sentence?  
Please answer in Katakana:

" {subject} "

I have already tokenized the sentence and found the following Katakana:
'''
{known} \n 
'''

Where the reading is unclear, it is marked as 'ambiguous'. With reference to the information in the dictionary data below, decide which is the appropriate reading and fill in the part and answer the reading in katakana for the subject.

'''
{dict_info}
'''

Please answer in Katakana:
" {subject} "

"""


prompt = PromptTemplate(
    template=template,
    input_variables=["subject", 'dict_info', 'known']
)

'''prompt_text = prompt.format(subject=input_text, content='生年月日, 月, 日, 日曜日, 祝日, 晴れ',
                            dict_info='dict_info', surface='1-unknown,日-ニチ,は-ハ,日曜日-ニチヨウビ')

'''


def kana_converter(input_text):
    result = analyze_text(input_text)
    known = format_result(result)

    dict_entries_for_unknown_words = get_all_unknown_words_and_sentences(
        convert_results_to_dictionary(result))
    # surface_only = filter_surface(formatted_result)
    # kanji_only = filter_words_with_kanji(formatted_result)

    prompt_text = prompt.format(subject=input_text,
                                dict_info=dict_entries_for_unknown_words, known=known)

    llm = OpenAI(model_name="text-davinci-003")

    # print(prompt_text)

    return prompt_text, llm(prompt_text)

    # return prompt_text
