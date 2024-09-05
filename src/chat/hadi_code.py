import spacy

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define questions
questions = [
    {"field": None,
     "question": "Welcome to Skilled! I'm ALI, your digital sales colleague. I'm here to make your sales journey smoother. Would you like to hear more about what I can do or just dive right in with the onboarding process?"},
    {"field": "Customer job title",
     "question": "Could you please specify the job title of the customer you are targeting? For example, are you focusing on roles such as Chief Executive Officer (CEO), Marketing Manager, or IT Director? This will help me tailor our approach to the appropriate decision-makers or influencers in their role."},
    {"field": "Job Seniority",
     "question": "To further refine your target customer, could you specify the job seniority level you're aiming for? Please provide one or a range of seniority levels, such as entry-level, mid-level, senior, or executive."},
    {"field": "Department",
     "question": "Cool! Could you identify the department or departments you want to target? Please provide one or a list of departments relevant to your ideal customer profiles."}
]

# Dictionary to store the detected values as lists
user_info = {
    "Customer job title": [],
    "Job Seniority": [],
    "Department": []
}


def aggressive_detection(field, text):
    """
    Perform aggressive detection of fields, allowing broad matching.
    This approach may increase false positives.
    """
    doc = nlp(text)
    possibilities = []

    # Aggressive detection for job titles, companies, or departments
    if field == "Customer job title":
        # Capture all noun phrases and entities that might represent a job title
        for chunk in doc.noun_chunks:
            possibilities.append(chunk.text)

        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "TITLE", "PRODUCT", "WORK_OF_ART", "GPE", "LOC", "NORP"]:
                possibilities.append(ent.text)

        # Capture verbs that might be followed by roles
        for token in doc:
            if token.pos_ == "VERB" and token.dep_ == "ROOT":
                job_title_phrase = ' '.join([child.text for child in token.subtree])
                possibilities.append(job_title_phrase)

    elif field == "Job Seniority":
        # Broadly capture adjectives and nouns that might indicate seniority
        for token in doc:
            if token.pos_ in ["ADJ", "NOUN"] and token.dep_ in ["amod", "attr", "advmod", "compound"]:
                possibilities.append(token.text)

    elif field == "Department":
        # Capture broader entity types and noun phrases that could indicate departments
        for chunk in doc.noun_chunks:
            possibilities.append(chunk.text)

        for ent in doc.ents:
            if ent.label_ in ["ORG", "GPE", "LOC", "NORP", "FAC"]:
                possibilities.append(ent.text)

    # Consider all noun chunks if no entities are detected
    if not possibilities:
        possibilities = [chunk.text for chunk in doc.noun_chunks]

    return possibilities if possibilities else None


def ask_question(question_data):
    """
    Asks the user a question and stores all possible values in a list for the specified field.
    No feedback is provided to the user during the interaction.
    """
    while True:
        user_input = input(question_data["question"] + "\n")

        # Skip detection if no field is defined (e.g., for greeting)
        if question_data["field"] is None:
            break  # Move to the next question after the greeting

        detected_values = aggressive_detection(user_input, question_data["field"])

        if detected_values:
            # Store all detected values in a list for the corresponding field
            user_info[question_data["field"]].extend(detected_values)
            break
        else:
            print(f"Sorry, I couldn't detect the {question_data['field']}. Please try again, or clarify your input.\n")


# # Start the interaction
# for question_data in questions:
#     ask_question(question_data)
#
# # Show the collected information (multiple values stored for each field)
# print("Here's the collected information:")
# for key, values in user_info.items():
#     print(f"{key}: {values}")
