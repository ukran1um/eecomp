import streamlit as st
import pandas as pd
import random
import os
import numpy as np


def load_poem(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_random_poem_path(poem_type, num_poems):
    poem_number = random.randint(1, num_poems)
    st.session_state.poem_number = poem_number
    return f'./{poem_type}_poems/{poem_number}.txt'

    
def display_poem(num_real_poems, num_fake_poems):
    if np.random.rand() > 0.5:
        poem_path = get_random_poem_path("real", num_real_poems)
        st.session_state.poem_source = "Human"
    else:
        poem_path = get_random_poem_path("fake", num_fake_poems)
        st.session_state.poem_source = "AI"
    poem = load_poem(poem_path)
    formatted_poem = poem.replace('\n', '<br>')  # Replace newlines with HTML line breaks
    st.session_state.poem = formatted_poem
    st.session_state.poem_path = poem_path
    st.markdown(f"<div style='background-color:darkgrey;padding:5px;'>{formatted_poem}</div>", unsafe_allow_html=True)
    print(poem_path)

def save_results(source, rating, guess, path):
    new_data = pd.DataFrame({'Source': [source], 'Rating': [rating], 'Guess': [guess], 'Path': [path]})
    if not os.path.isfile('results.csv') or os.path.getsize('results.csv') == 0:
        # Create a new file or overwrite an empty file with headers
        new_data.to_csv('results.csv', index=False)
    else:
        # Append to the existing file without adding the header
        new_data.to_csv('results.csv', mode='a', header=False, index=False)

def calculate_poem_stats(poem_path):
    # Check if the results file exists and is not empty
    if os.path.isfile('results.csv') and os.path.getsize('results.csv') > 0:
        df = pd.read_csv('results.csv')
        poem_df = df[df['Path'] == poem_path]
        if not poem_df.empty:
            avg_rating = poem_df['Rating'].mean()
            correct_guesses = (poem_df['Guess'] == poem_df['Source']).sum()
            total_guesses = len(poem_df)
            accuracy = (correct_guesses / total_guesses) * 100 if total_guesses > 0 else 0
            return avg_rating, accuracy
    else:
        # Handle the case where there are no existing results
        return None, None

def get_author_by_poem_number(poem_number):
    if 1 <= poem_number <= 20:
        return "E.E. Cummings"
    elif 21 <= poem_number <= 40:
        return "Pablo Neruda"
    elif 41 <= poem_number <= 50:
        return "T.S. Eliot"
    elif 51 <= poem_number <= 60:
        return "Ralph Waldo Emerson"
    elif 61 <= poem_number <= 80:
        return "Emily Dickinson"
    elif 81 <= poem_number <= 90:
        return "Oscar Wilde"
    elif 91 <= poem_number <= 100:
        return "Sylvia Plath"
    else:
        return "Unknown"

def main():
    # Display a logo
    st.image("logo/logo2.png", width=300)  # Adjust the path and size as needed

    num_real_poems = 100  
    num_fake_poems = 100  

    if 'poem_displayed' not in st.session_state or st.button("Show new poem"):
        display_poem(num_real_poems, num_fake_poems)
        st.session_state.poem_displayed = True
    elif 'poem' in st.session_state:
        # Display the stored poem
        st.markdown(f"<div style='background-color:darkgrey;padding:5px;'>{st.session_state.poem}</div>", unsafe_allow_html=True)
        avg_rating, accuracy = calculate_poem_stats(st.session_state.poem_path)
        if avg_rating is not None:
            st.write(f"Average Rating for this Poem: {avg_rating:.2f}/10")
            st.write(f"Accuracy of Guesses: {accuracy:.2f}%")

    rating = st.slider("Rate the quality of this poem from 1-10", 1, 10)
    guess = st.radio("Was this poem written by a human or AI?", ('Human', 'AI'))
    if st.button("Submit"):
        guess_result = "Correct" if guess == st.session_state.poem_source else "Incorrect"
        save_results(st.session_state.poem_source, rating, guess, st.session_state.poem_path)
        st.session_state.poem_displayed = False
        st.success(f"Thank you for your feedback! Your guess was {guess_result}.")
        if st.session_state.poem_source == "Human":
            author = get_author_by_poem_number(st.session_state.poem_number)
            st.write(f"Author of the Poem: {author}")

if __name__ == "__main__":
    main()
