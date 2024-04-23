import streamlit as st
from textSFunctionality import generateText

st.set_page_config(page_title="Text Summarization", page_icon="😃") 

st.markdown("""
    <style>
        body {
            color: #ffffff;
            background-color: #191970;  /* Midnight blue background */
        }
        .stTextInput>div>div>input, .stTextInput>div>div>textarea {
            color: #333;
            background-color: #ffffff;
        }
        .css-2trqyj {
            background-color: #191970;
            color: #ffffff;
        }
        header, .css-1d391kg {
            background-color: #191970;
        }
        .stButton>button {
            color: #ffffff;
            background-color: #4b0082;  /* Indigo button */
        }
    </style>
    """, unsafe_allow_html=True)

st.title('Text Summarization App')
st.markdown("Enter the text you want to summarize in the box below and click summarize to see the output. Dialogues are preferable")


user_input = st.text_area("Enter Text", height=250)


if st.button('Summarize'):
    # Call the generate_text function
    summary = generateText(user_input)
    # Display the summarized text in a separate styled text box
    st.markdown(f"""
        <style>
            .summary_box {{
                border: 2px solid #4b0082;  /* Indigo border */
                border-radius: 10px;
                padding: 10px;
                margin: 10px;
                background-color: #000080;  /* Navy background for the output box */
                color: #ffffff;
            }}
        </style>
        <div class="summary_box">
            {summary}
        </div>
        """, unsafe_allow_html=True)
