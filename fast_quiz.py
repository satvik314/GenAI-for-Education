import streamlit as st
import os
import time
from educhain import qna_engine
from langchain_openai import ChatOpenAI

# Custom template for initial question generation
custom_template = """
Generate {num} multiple-choice question (MCQ) based on the given topic and level.
Provide the question, four answer options, and the correct answer.

Topic: {topic}
Learning Objective: {learning_objective}
Difficulty Level: {difficulty_level}
"""

# Adaptive template for subsequent questions
adaptive_template = """
Based on the user's response to the previous question on {topic}, generate a new multiple-choice question (MCQ).
If the user's response is correct, output a harder question. Otherwise, output an easier question.
Provide the question, four answer options, and the correct answer.

Previous Question: {previous_question}
User's Response: {user_response}
Was the response correct?: {response_correct}
"""

@st.cache_resource
def get_llm(api_key):
    return ChatOpenAI(
        model="llama-3.1-8b-instant",
        openai_api_base="https://api.groq.com/openai/v1",
        openai_api_key=api_key
    )

def generate_initial_question(topic, llm):
    result = qna_engine.generate_mcq(
        topic=topic,
        num=1,
        learning_objective="General knowledge of " + topic,
        difficulty_level="Medium",
        llm=llm,
        prompt_template=custom_template,
    )
    return result.questions[0] if result and result.questions else None

def generate_next_question(previous_question, user_response, response_correct, topic, llm):
    result = qna_engine.generate_mcq(
        topic=topic,
        num=1,
        llm=llm,
        prompt_template=adaptive_template,
        previous_question=previous_question,
        user_response=user_response,
        response_correct=response_correct
    )
    return result.questions[0] if result and result.questions else None

def main():
    st.set_page_config(page_title="Fast Adaptive Quiz", layout="wide")

    # Move API Key input to sidebar with highlighted instructions
    with st.sidebar:
        st.title("Settings")
        st.markdown("### :red[Enter your GROQ API Key below]")
        api_key = st.text_input("GROQ API Key:", type="password")

    st.title("Fast Adaptive Quiz")

    if not api_key:
        st.markdown("""
        ## Welcome to the Fast Adaptive Quiz!
        
        This quiz app uses AI to generate personalized questions based on your chosen topic and adapts to your performance.
        
        To get started:
        1. :red[Enter your GROQ API Key in the sidebar.] ← Start here!
        2. Choose a topic you want to study.
        3. Answer 5 questions and see how you do!
        
        The quiz will adjust its difficulty based on your answers, providing a tailored learning experience.
        
        Ready to challenge yourself? Let's begin!
        """)
        # st.image("https://via.placeholder.com/600x300.png?text=Fast+Adaptive+Quiz", use_column_width=True)
        st.info("Enhance your learning with AI-powered quizzes!")
        st.stop()

    llm = get_llm(api_key)

    if 'question_number' not in st.session_state:
        st.session_state.question_number = 0
        st.session_state.score = 0
        st.session_state.current_question = None
        st.session_state.topic = None
        st.session_state.start_time = None
        st.session_state.total_time = 0

    if st.session_state.question_number == 0:
        st.markdown("""
        ## Instructions
        1. Enter a topic you want to be quizzed on. It can be any subject or area of interest.
        2. The quiz consists of 5 multiple-choice questions.
        3. The difficulty of each question adapts based on your previous answer.
        4. Try to answer all questions to the best of your ability.
        5. Your total time will be tracked, so try to be both accurate and quick!

        Good luck and enjoy learning!
        """)
        topic = st.text_input("Enter the topic you want to study:")
        if st.button("Start Quiz", key="start_button"):
            st.session_state.topic = topic
            st.session_state.current_question = generate_initial_question(topic, llm)
            st.session_state.question_number += 1
            st.session_state.start_time = time.time()
            st.rerun()

    elif st.session_state.question_number <= 5:
        if st.session_state.current_question:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(f"Question {st.session_state.question_number}")
                st.write(st.session_state.current_question.question)
                
                user_answer = st.radio("Choose your answer:", st.session_state.current_question.options, key=f"q{st.session_state.question_number}")
                
                if st.button("Submit Answer", key=f"submit{st.session_state.question_number}"):
                    correct_answer = st.session_state.current_question.answer
                    if user_answer == correct_answer:
                        st.success("Correct!")
                        st.session_state.score += 1
                        response_correct = "True"
                    else:
                        st.error(f"Incorrect. The correct answer was {correct_answer}.")
                        response_correct = "False"

                    if st.session_state.current_question.explanation:
                        st.info(f"Explanation: {st.session_state.current_question.explanation}")

                    st.session_state.question_number += 1

                    if st.session_state.question_number <= 5:
                        st.session_state.current_question = generate_next_question(
                            st.session_state.current_question.question,
                            user_answer,
                            response_correct,
                            st.session_state.topic,
                            llm
                        )
                    else:
                        st.session_state.total_time = time.time() - st.session_state.start_time
                    st.rerun()
            
            with col2:
                st.metric("Score", f"{st.session_state.score}/{st.session_state.question_number - 1}")
                st.progress(st.session_state.question_number / 5)
                elapsed_time = time.time() - st.session_state.start_time
                st.metric("Time", f"{elapsed_time:.2f} seconds")

    if st.session_state.question_number > 5:
        st.success("Quiz completed!")
        st.balloons()
        st.metric("Final Score", f"{st.session_state.score}/5")
        st.metric("Total Time", f"{st.session_state.total_time:.2f} seconds")
        if st.button("Restart Quiz"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()