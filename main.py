import streamlit as st
import pandas as pd
import random

def read_words(file):
    with open(file,'r') as f:
        words = f.readlines()
    words = [word.strip().upper() for word in words]
    return words

def check_guess(guess,answer):
    points = [0,0,0,0,0]
    for i,letter in enumerate(guess):
        if letter == answer[i]:
            points[i] = 2
            answer = answer.replace(letter,'-',1)
        elif letter in answer:
            points[i] = 1
            answer = answer.replace(letter,'-',1)
    return points

def valid_guess(guess):
    if len(guess) == 5 and guess in ALLOWED:
        return True
    else:
        return False

def list_to_df(alist):
    list_of_lists = []
    for item in alist:
        list_of_lists.append([i for i in item])
    df = pd.DataFrame(list_of_lists)
    df = df.reindex(list(range(0, 6))).reset_index(drop=True)
    return df

def colormap(x):
    if x == 2:
        return 'background-color: green; font-size: 24pt; text-align: center'
    elif x == 1:
        return 'background-color: yellow; font-size: 24pt; text-align: center'
    elif x ==0:
        return 'background-color: grey; font-size: 24pt; text-align: center'
    else:
        return 'background-color: white; color: white'

# initialize state
ANSWERS = read_words('wordle-answers-alphabetical.txt')
ALLOWED = read_words('wordle-allowed-guesses.txt')
ALLOWED = ALLOWED + ANSWERS

if 'ANSWER' not in st.session_state:
    st.session_state['ANSWER'] = random.choice(ANSWERS)
ANSWER = st.session_state['ANSWER']

if 'guesses' not in st.session_state:
    st.session_state['guesses'] = []
if 'points' not in st.session_state:
    st.session_state['points'] = []


st.title('Guess the word!')
st.write('Guess the 5-letter word in as few guesses as possible.')
# st.write('Answer: ',ANSWER)

with st.form(key='my_form',clear_on_submit=True):
    guess = st.text_input('Enter a guess').upper()
    submit = st.form_submit_button(label='Submit guess' )
if len(st.session_state['guesses'])<6: 
    if submit and valid_guess(guess):
        st.session_state['guesses'].append(guess)
        st.session_state['points'].append(check_guess(guess,ANSWER))
    else:
        st.write('Invalid guess')

# show results
if len(st.session_state['guesses']) == 0:
    st.markdown('# Submit your first guess!')
else:
    df = list_to_df(st.session_state['guesses'])
    df_points = list_to_df(st.session_state['points'])
    df = df.style.apply(lambda x: df_points.applymap(colormap), axis=None)
    st.dataframe(df, width=1600)
    if st.session_state['guesses'][-1] == ANSWER:
        st.markdown('# You Win! \nRefresh page to start over')
        st.balloons()
    elif len(st.session_state['guesses']) == 6:
        st.markdown('# You Lose!\nRefresh page to start over')

