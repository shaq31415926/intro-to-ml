import streamlit as st
import pandas as pd
import numpy as np
import cv2
from get_recommendations import get_recommendations
import pandas as pd

# set the page config info
st.set_page_config(
    page_title="My Tinder App",
    page_icon="🔥",
    layout="wide"
)

if 'login_count' not in st.session_state:
    st.session_state.login_count = 0


def one_hot(df, categorical_cols):
    """
    @param df pandas DataFrame
    @param cols a list of columns to encode
    @return a DataFrame with one-hot encoding
    """

    for c in categorical_cols:
        dummies = pd.get_dummies(df[c], prefix=c)
        df = pd.concat([df, dummies], axis=1)
        df.drop(c, axis=1, inplace=True)

    return df

def increment_login_counter():
    st.session_state.login_count += 1


if st.session_state.login_count == 0:
    # create a placeholder variable, so I can delete the form widget after using it
    placeholder = st.empty()

    with placeholder.form("Login"):
        st.title("Welcome to 🔥")
        name = st.text_input("What is your name?")
        image_file = st.file_uploader("Upload Your Image",
                                          type=["jpg", "png", "jpeg"])
        st.write(f"Tell us about what you are looking for")
        gender = st.radio("Are you searching for a man or woman?",['🕺', '💃'])
        bio = st.text_area("Tell us about yourself in your own words:")
        age = st.number_input("How old are you?", 18, 50)
        height = st.slider("How tall are you (inches)?", min_value=40, max_value=100)
        education = st.select_slider("What is your level of education?",
                                 [1, 2, 3, "4 🤓"])
        drink = st.select_slider("Do you drink? 🍷", ['Not at all', 'Often', 'Rarely', 'Socially', 'Very often', 'Desperately'])
        smoke = st.select_slider("Do you smoke? 🚬", ['No', 'Sometimes', 'Trying to quit', 'When Drinking', 'Yes'])
        drugs = st.select_slider("Do you do drugs? 💉", ['Never', 'Sometimes', 'Often'])
        cats = st.radio("Do you like cats?", ["Yes", "No"])
        dogs = st.radio("Do you like dogs?", ["Yes", "No"])
        new_language = st.select_slider("How do you feel about learning a new language?", ['Not interested', 'Interested', 'Somewhat interested'])
        body_profile = st.radio("How would you define your body profile? 🏋️‍♂️", ['Average',
                                                                                     'Fit',
                                                                                     'Athletic',
                                                                                     'Curvy',
                                                                                     'Thin',
                                                                                     'A little extra',
                                                                                     'Skinny',
                                                                                     'Full figured',
                                                                                     'Used up',
                                                                                     'Overweight',
                                                                                     'Rather not say',
                                                                                     'Jacked'])
        job = st.radio("What job do you have?", ['Other',
                                     'Student',
                                     'Science / tech / engineering',
                                     'Sales / marketing / biz dev',
                                     'Artistic / musical / writer',
                                     'Computer / hardware / software',
                                     'Medicine / health',
                                     'Education / academia',
                                     'Banking / financial / real estate',
                                     'Entertainment / media',
                                     'Executive / management',
                                     'Law / legal services',
                                     'Construction / craftsmanship',
                                     'Hospitality / travel',
                                     'Political / government',
                                     'Clerical / administrative',
                                     'Transportation',
                                     'Rather not say',
                                     'Unemployed',
                                     'Military',
                                     'Retired'])

        login_button = st.form_submit_button("Click here for matches")
        if login_button:
            increment_login_counter()
            # create a dataframe of all the matches
            if education == 1:
                dropped_out = 1
            else:
                dropped_out = 0

            # code to take input from streamlit and convert to a dataframe so we can make predictions
            row = np.array([age, gender, height, education, dropped_out, drink, drugs, job, smoke, body_profile, new_language, dogs, cats])


            columns = ['age',
                       'sex',
                       'height',
                       'education_level',
                       'dropped_out',
                       'drinks',
                       'drugs',
                       'job',
                       'smokes',
                       'body_profile',
                       'new_languages',
                       'likes_dog',
                       'likes_cats',
                       ]
            user_data = pd.DataFrame([row], columns=columns)
            # user_data["user_id"] = "u1234" # hardcoded this value for now
            user_data["sex"] = user_data["sex"].apply(lambda x: 1 if x == '🕺' else 0)
            user_data["likes_cats"] = user_data["likes_cats"].apply(lambda x: 1 if x == "Yes" else 0)
            user_data["likes_dog"] = user_data["likes_dog"].apply(lambda x: 1 if x == "Yes" else 0)
            for col in ["drinks", 'drugs', 'job', 'smokes', 'body_profile', 'new_languages']:
                user_data[col] = user_data[col].apply(lambda x: x.lower())
            user_data = one_hot(user_data, ["drinks", 'drugs', 'job', 'smokes', 'body_profile', 'new_languages'])

            # store and manipulate user data
            col_order = pd.read_csv("data/col_names.csv")
            user_data_transformed = pd.concat([col_order, user_data], axis=0)
            # replace missing values with na
            user_data_transformed.fillna(0, inplace=True)
            user_data_transformed.to_csv("data/user_profile_data.csv", index=False)

if 'profile_number' not in st.session_state:
    st.session_state.profile_number = 0


def increase_profile_number():
    st.session_state.profile_number += 1


user_profile = pd.read_csv("data/user_profile_data.csv")
tinder_data = pd.read_csv("data/tinder_data_prepared.csv")
tinder_data_raw = pd.read_csv("data/tinder_data_filtered.csv")


def get_match_info(profile_ids, tinder_data_raw):
    match_profile = profile_ids[st.session_state.profile_number]
    match_name = tinder_data_raw[tinder_data_raw.user_id == match_profile].username
    match_age = tinder_data_raw[tinder_data_raw.user_id == match_profile].age
    match_bio = tinder_data_raw[tinder_data_raw.user_id == match_profile].bio
    st.write("Name:", list(match_name)[0])
    st.write("Age:", list(match_age)[0])
    st.write("Bio:\n", list(match_bio)[0])

def display_match_info():
    profile_ids = list(pd.read_csv("data/matches.csv")["0"])
    get_match_info(profile_ids, tinder_data_raw)

    # add button like or dislike
    c3, c4 = st.columns(2)

    with c3:
        st.button("❤️", on_click=increase_profile_number)
    with c4:
        st.button("❌", on_click=increase_profile_number)


if st.session_state.login_count == 1:
    increment_login_counter()

    # delete all the form widgets we created
    placeholder.empty()

    # create a page with column structure
    c1, c2 = st.columns(2)

    with c1:
        if image_file is not None:
            # annoying code to convert the uploaded qr code image into an image the decoder function can read
            file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
            opencv_image = cv2.imdecode(file_bytes, 1)
            # place the image on our app
            st.image(opencv_image,
                     caption=f"Hi {name}",
                     width=200)
    with c2:
        st.title("Your Matches Are...")

        profile_ids = get_recommendations(user_profile,
                                          tinder_data,
                                          number_recommendations=10)
        # dump this in a file
        pd.DataFrame(profile_ids).to_csv("data/matches.csv", index=False)

        get_match_info(profile_ids, tinder_data_raw)

        # add button like or dislike
        c3, c4 = st.columns(2)

        with c3:
            st.button("❤️", on_click=increase_profile_number)
        with c4:
            st.button("❌", on_click=increase_profile_number)

if st.session_state.profile_number >= 1 and st.session_state.profile_number < 10:
    display_match_info()

if st.session_state.profile_number >= 10:
    st.image("images/Screenshot 2024-06-24 at 23.06.53.png")