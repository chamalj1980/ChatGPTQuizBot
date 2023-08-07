import streamlit as st
import openai
import configparser
import json
from langchain import PromptTemplate, OpenAI, LLMChain
from langchain.chat_models import ChatOpenAI
#from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts.chat import (SystemMessagePromptTemplate, HumanMessagePromptTemplate,
                                     ChatPromptTemplate,)

# Setting the API key
config = configparser.ConfigParser()
config.read('config.ini')
openai.api_key = config['SECRETS']['openai_api_key']

# Define the language model and creates the ChatOpenAI object to chain together LM and the Open AI APIs
MODEL = "gpt-3.5-turbo"
chat_llm = ChatOpenAI(model=MODEL, temperature=1, max_tokens=500, openai_api_key=openai.api_key)

#Python function to generate quesions, answer choices and correct answer given a topic.Returns a python dictionary
def generate_question_answer(subject):
    
    # System Prompt
    system_prompt_template = (
        #"You are a quizbot that generates 1 question on a given {topic} and must have 4 choices  as answers for each question. Only one answer choice must be correct. Answer choices must be numered from 1 to 4. Do not duplicate questions. You must return question , answer choices and correct answer as  JSON objects for all question. Output must be in JSON format (question 1, answer choice 1, correct answer 1,question 2, answer choice 2, correct answer 2,question 3, answer choice 3, correct answer 3)"
        #"You are a quizbot that generates 3 question on a given {topic} with 4 choices  as answers for each question. Only one answer choice must be correct. Answer choices must be numered from 1 to 4. Do not duplicate questions. You must return question , answer choices and correct answer as  python list objects one after the other for each question. Output must be as python list objects"
        "You are a quizbot that generates only 1 question on a given {topic} and must have 4 choices  as answers for each question. Only one answer choice must be correct. Answer choices must be numbered from 1 to 4. Do not duplicate questions. You must return question , answer choices and correct answer as  JSON objects for the question. Output must be in JSON format (question 1, answer choice 1, correct answer 1)"
        #"You are a quizbot that generates 5 question on a given {topic} and must have 4 choices  as answers for each question. Only one answer choice must be correct. Answer choices must be numered from 1 to 4. Do not duplicate questions. You must return question , answer choices and correct answer as  JSON objects for all question. Output must be in JSON format (question 1, answer choice 1, correct answer 1,question 2, answer choice 2, correct answer 2,question 3, answer choice 3, correct answer 3)"
    )
    system_message_prompt = SystemMessagePromptTemplate.from_template(system_prompt_template, input_variables=["topic"])

    # Human Prompt
    human_prompt_template = "{topic}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_prompt_template, input_variables=["topic"])

    # Final Prompt
    chat_llm_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    # Chains ChatOpenAI object and the final prompt
    chat_llm_chain = LLMChain(
        llm=chat_llm,
        prompt=chat_llm_prompt,
    )

    # Model output as a JSON object
    response = chat_llm_chain.predict(topic=subject)

    # Converts JSON object to a python dictionary
    dict_response = json.loads(response)

    return dict_response


# Define streamlit application
st.title("Streamlit Chat Bot Application")
subject = st.text_input("Enter the subject for the questions:", disabled=False)
questions = generate_question_answer(subject)

if subject:
    # Loop to present questions one after the other using st.form context manager
    count = 0
    current_question = list(questions.items())[count][1]
    current_choices = list(questions.items())[count + 1][1]
    st.write(current_question)
    st.write(current_choices)

    with st.form(key="quiz_form"):
            
        # Initialize question index
       
        # While there are more questions to display
        #for i in range(5):
            #question_name = "question_" + str(i)
        #st.write(questions)
        #user_answer = st.text_input(question_name)

        user_answer = st.selectbox(
                "user_answer:",
                (1,2,3,4),
                label_visibility="visible",
                index=3,
                disabled=False,
                key="user_answer"
            )
        submitted = st.form_submit_button("Submit")
        
        if submitted:
            
            correct_answer = int(list(questions.items())[count + 2][1])
            
            if user_answer == correct_answer:
               st.write("Your answer is correct.")
               subject = ""
            else:
                st.write("Your answer is incorrect.")
                st.write("The correct answer is:", list(questions.items())[count + 2][1])
                subject = ""
            
                #count += 3  # Increment count by 3 for the next iteration
