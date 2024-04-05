import streamlit as st
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent,Task
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
api = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Lyzr Code Convertor",
    layout="centered",  # or "wide"
    initial_sidebar_state="auto",
    page_icon="lyzr-logo-cut.png",
)

st.markdown(
    """
    <style>
    .app-header { visibility: hidden; }
    .css-18e3th9 { padding-top: 0; padding-bottom: 0; }
    .css-1d391kg { padding-top: 1rem; padding-right: 1rem; padding-bottom: 1rem; padding-left: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)

image = Image.open("lyzr-logo.png")
st.sidebar.image(image, width=150)

# App title and introduction
st.sidebar.title("Lyzr Lyzr Code Convertor")
st.sidebar.markdown("### Welcome to the Lyzr Code Convertor!")
st.sidebar.markdown("Upload Your Code and covert into any language!!!")

open_ai_text_completion_model = OpenAIModel(
    api_key=api,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)
languages=["Python","Javascript","Java","C","C++","C#","Ruby","Swift","Kotlin","PHP","TypeScript","Go,","Rust","Perl","R","Haskell","Scala"]
topic = st.sidebar.text_area("Enter Code Here",height=200,placeholder="print('Hello World!!')")
output_lang = st.sidebar.selectbox("Select Language",options=languages,index=None,placeholder="Programming Language")

if st.sidebar.button("Convert",type='primary'):
    developer_agent = Agent(
        role="Code expert",
        prompt_persona=f"You are an Expert developer in every language."
    )

    prompt=(f"Convert the below code snippet to {output_lang}: {topic}.[!IMPORTANT] only generate code nothing else."
            f"If code conversion is not possible then write code conversion not possible message in 20 words")

    code_conversion_task = Task(
        name="Code Conversion",
        model=open_ai_text_completion_model,
        agent=developer_agent,
        instructions=prompt,
    )

    output = LinearSyncPipeline(
            name="Code Conversion Pipeline",
            completion_message="Code Converted",
            tasks=[code_conversion_task],
    ).run()
    st.markdown(output[0]['task_output'])