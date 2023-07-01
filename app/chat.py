import sys
import numpy as np
from konlpy.tag import Kkma
from konlpy.tag import Okt
import openai
import googletrans
import re
import pandas as pd
import json
import time


kkma = Kkma()
okt = Okt()
translator = googletrans.Translator()

# Minsu's OpenAI Key!!!
# If you upload this code file at github, Please delete lower line.
openai.api_key = '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'

start_time = time.time()


def ChatGPT_JSON(field, script):
    message = []
    translator = googletrans.Translator()

    keyword_number = 8  # Setting Keyw"ord Number
    # keyword_number = input("keyword_nunber : ")

    while True:
        elapsed_time = time.time() - start_time
        prompt = []
        ChatGPT_Prompt_JSON(prompt, keyword_number, field, script)
        content = ' '.join(prompt)
        message.append({"role": "user", "content": content})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=message)
        chat_response = completion.choices[0].message.content
        message.append({"role": "assistant", "content": chat_response})
        # print('ChatGPT : ', chat_response)

        if (chat_response.find('{') == None) & (chat_response.find('}') == None):
            continue
        else:
            break
        if elapsed_time >= 30:
            print('ChatGPT Error!!! Time Over.')
            break

    dictionary = json.loads(chat_response)
    values_list = list(dictionary.values())[0]
    # print(values_list)

    keyword_count_chatgpt = {}
    for word in values_list:
        count = script.count(word)
        keyword_count_chatgpt[word] = count

    # print(keyword_count_chatgpt) # form : dictionary

    return keyword_count_chatgpt


def ChatGPT_Prompt_JSON(prompt, keyword_number, field, script):
    prompt.append('Field is {}.'.format(field))
    prompt.append('Script is {}.'.format(script))
    prompt.append(
        'Print out the Most Important Script Keyword for the field, in the form of json')
    prompt.append('The number of keyword words is {}.'.format(keyword_number))
    prompt.append('I will give you an example of the output')
    prompt.append('{\"Keywords\": [\"고양이\", \"강아지\"]}')
    # prompt.append('Keywords must be nouns, and verbs, adjectives, adverbs, and surveys should not be used.')


def ChatGPT_JSON_Question(field, script, values_list):
    message = []
    translator = googletrans.Translator()

    keyword_number = 8  # Setting Keyw"ord Number
    # keyword_number = input("keyword_nunber : ")

    prompt = []
    ChatGPT_Prompt_Question(prompt, field, script, values_list)
    content = ' '.join(prompt)
    message.append({"role": "user", "content": content})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=message)
    chat_response = completion.choices[0].message.content
    message.append({"role": "assistant", "content": chat_response})
    #print('ChatGPT : ', chat_response)

    # dictionary = json.loads(chat_response)
    # values_list = list(dictionary.values())[0]
    # print(values_list)
    # print(keyword_count_chatgpt) # form : dictionary

    return chat_response


def ChatGPT_Prompt_Question(prompt, field, script, values_list):
    prompt.append('Field is {}.'.format(field))
    prompt.append('Script is {}.'.format(script))
    prompt.append('Keyword is {}.'.format(values_list))
    prompt.append(
        'When you become an interviewer about a field and look at script, keyword, what is the question to ask the presenter?')
    prompt.append('You can ask up to 3 questions to the presenter.')
    prompt.append('The output is python list. and language is korean')


# if __name__ == '__main__':
#     keyword_dic = {}
# # field = input("My Field : ")
# # script = input("Script : ")

# # keyword_dic = ChatGPT_JSON(field, script)
# # sorted_keywords = sorted(keyword_dic, key=keyword_dic.get, reverse=True)[:5]

# field = "면접"
# script = "대본입니다."
# keyword_dic = {'목탁디자인학과': 2,
#                '목탁디자인': 5,
#                '목재': 1,
#                '디자인 트렌드': 1,
#                '시장 동향': 1,
#                '조화로운 관계': 1,
#                '협업 능력': 2,
#                '회사의 목표': 2}
# # sorted_keywords = sorted(keyword_dic, key=keyword_dic.get, reverse=True)[:5]
# sorted_keywords = sorted(keyword_dic, key=keyword_dic.get, reverse=True)[:5]
# return list(field, script, sorted_keywords)
# # print(sorted_keywords)

# #keyword_values_list = list(sorted_keywords.values())

# # question_list = ChatGPT_JSON_Question(field, script, keyword_values_list) # Question To Applicant, string
