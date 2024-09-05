import re
import time

import pandas as pd
import streamlit as st
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
industry_lookup = pd.read_excel("D:\Industries.xlsx", "Sheet1")


def check_value_in_lookup(value):
    freq = len(industry_lookup[industry_lookup["Ingustry_classification"].str.lower() == value.lower()])
    return freq > 0


def detect_country_name(answer):
    print("detect_country_name")
    nlp = pipeline("ner", model=model, tokenizer=tokenizer)
    example = "My name is Wolfgang and I live in Berlin"
    print(answer)
    ner_results = nlp(answer)
    return ner_results


# Streamed response emulator
questionsDic = {
    1: "Welcome to Skilled! I'm ALI, your digital sales colleague. I'm here to make your sales journey smoother. Would you like to hear more about what I can do or just dive right in with the onboarding process?",
    2: "Could you please specify the job title of the customer you are targeting? For example, are you focusing on roles such as Chief Executive Officer (CEO), Marketing Manager, or IT Director? This will help me tailor our approach to the appropriate decision-makers or influencers in their role.",
    3: "To further refine your target customer, could you specify the job seniority level you're aiming for? Please provide one or a range of seniority levels, such as entry-level, mid-level, senior, or executive.",
    4: "Cool! could you identify the department or departments you want to target? Please provide one or a list of departments relevant to your ideal customer profiles.",
    5: "To help me better understand your target market, could you please specify the country where your ideal companies are located? For example, the United States, UAE, or Saudi Arabia.",
    6: "Could you also provide the city or cities within that country where you'd like to focus your outreach efforts? For instance, New York City, Dubai, or Riyadh.",
    7: "Which industry or industries are you interested in targeting? Examples might include technology, healthcare, finance, or manufacturing.",
    8: "Can you describe the main activities or business functions of the companies you want to target? For example, are they involved in software development, retail, consulting, or logistics",
    9: "What is the ideal employee size range of the companies you're interested in? You might consider small businesses (1-50 employees), mid-sized companies (51-500 employees), or large enterprises (501+ employees).",
    10: "Finally, could you share the revenue range of the companies you wish to target? Examples include companies with revenues of $1 million to $10 million, $10 million to $100 million, or $100 million and above"
}


# handle user respones
def handle_usesr_responese(question_index, answer):
    answerDict = st.session_state["answerDict"]
    print(f"answers: {answerDict}, question index: {question_index}")
    if question_index == 2:
        # this question for detect Customer job title
        # ustomer_job_title = detect_customer_job(answer)
        answerDict["customer_job_title"] = answer
        return True
    if question_index == 3:
        # this question for detect Job Seniority
        print(f" handle_usesr_responese", question_index)
        # country_name = detect_country_name(answer)
        answerDict["job_seniority"] = answer
        return True
    elif question_index == 4:
        # this question for detect Department
        print(f" handle_usesr_responese", question_index)
        # country_name = detect_country_name(answer)
        answerDict["department"] = answer
        return True
    elif question_index == 5:
        # this question for detect Country
        print(f" handle_usesr_responese", question_index)
        country_name = detect_country_name(answer)
        answerDict["country"] = country_name[0]["word"]
        return True
    elif question_index == 6:
        # detect city
        city_name = detect_country_name(answer)
        answerDict["city"] = city_name[0]["word"]
        return True
    elif question_index == 7:
        # detect industry
        exist = check_value_in_lookup(answer)
        if exist:
            answerDict["industry"] = answer
            return True
        else:
            return False
    elif question_index == 8:
        # detect activities
        answerDict["company_activities"] = answer
        return True
    elif question_index == 9:
        # detect company size
        company_size = detect_company_size(answer)
        answerDict["company_employee_size"] = company_size[0]
        return True
    elif question_index == 10:
        # detect company revenue
        answerDict["company_revenue"] = answer
        return True
    else:
        return True


# def detect_country_name(answer):
# nlp = spacy.load("en_core_web_sm")
# nlp.pipe_names
# doc = nlp(answer)
# for ent in doc.ents:
#     print(ent.text, "|", ent.label_, "|", spacy.explain(ent.label_))

def detect_company_size(answer):
    x = re.findall("[0-9]*-[0-9]*", answer)
    print(f"in company size function :{x}")
    return x


def response_generator(question_index):
    question = questionsDic[question_index]
    for word in question.split():
        yield word + " "
        time.sleep(0.08)


st.title("ALI Skilled Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
if "questionIndex" not in st.session_state:
    st.session_state["questionIndex"] = 1

if "answerDict" not in st.session_state:
    st.session_state["answerDict"] = {}

# dispaly the welcome msg for the assistant
questionIndex = int(st.session_state["questionIndex"])
if questionIndex == 1:
    welcome = questionsDic[questionIndex]
    with st.chat_message("assistant"):
        response = st.write(welcome)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # print(message["content"])
        if message["content"] != None:
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("waiting for your response"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # handle user respones
    # first get the index of the current question
    questionIndex = int(st.session_state.get("questionIndex"))
    questionIndex += 1
    st.session_state["questionIndex"] = questionIndex

    if questionIndex in questionsDic.keys():
        success = handle_usesr_responese(questionIndex, prompt)
        if not success:
            questionIndex -= 1
            st.session_state["questionIndex"] = questionIndex

        with st.chat_message("assistant"):
            response = st.write_stream(response_generator(questionIndex))

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
