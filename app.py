import random
import streamlit as st
import smtplib
import os
from email.message import EmailMessage

# Email credentials
EMAIL_ADDRESS = 'mirza.22sept@gmail.com'
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

# Medium difficulty level
MAX_ATTEMPTS = 15
BASE_POINTS = 10

# Initialize the game
def initialize_game():
    st.session_state.number = random.randint(0, 100)
    st.session_state.guesses = 0
    st.session_state.score = BASE_POINTS

# Send email notification
def send_email(user_name, attempts, correct_number):
    msg = EmailMessage()
    msg['Subject'] = 'Number Guessing Game Result'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg.set_content(
        f'User Name: {user_name}\n'
        f'Correct Number: {correct_number}\n'
        f'Number of Attempts: {attempts}'
    )

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        st.error(f'Failed to send email: {e}')

# Streamlit App
st.title("Number Guessing Game")
st.image("emoji_numbers.png", use_container_width=True)
st.write("---")

# Ask for user's name first
if 'user_name' not in st.session_state:
    st.session_state.user_name = st.text_input("Enter your full name:")
    if st.button("Next") and st.session_state.user_name.strip():
        st.session_state.name_entered = True
        initialize_game()
else:
    st.session_state.name_entered = True

# Game interface
if 'name_entered' in st.session_state and st.session_state.name_entered:
    st.write(f"Hello, **{st.session_state.user_name}**! Guess a number between 0 and 100.")

    if 'number' not in st.session_state or 'guesses' not in st.session_state:
        initialize_game()

    guess = st.number_input("Enter your guess:", min_value=0, max_value=100, key="number_guess")

    if st.button("Submit Guess"):
        st.session_state.guesses += 1

        if guess == st.session_state.number:
            st.success(f"Correct! You guessed the number in {st.session_state.guesses} attempt(s)!")

            # Send email
            send_email(st.session_state.user_name, st.session_state.guesses, st.session_state.number)

            initialize_game()  # Reset the game after a correct guess

        elif guess > st.session_state.number:
            st.warning(f"{guess} is too high!")
        else:
            st.warning(f"{guess} is too low!")

        if st.session_state.guesses >= MAX_ATTEMPTS:
            st.error(f"Game over! You've used all {MAX_ATTEMPTS} attempts. The number was {st.session_state.number}.")
            initialize_game()
