import re

from transformers import pipeline

from src.chat.hadi_code import aggressive_detection


# industry_lookup = pd.read_excel("D:\Industries.xlsx", "Sheet1")
#
#
# def check_value_in_lookup(value):
#     freq = len(industry_lookup[industry_lookup["Ingustry_classification"].str.lower() == value.lower()])
#     return freq > 0


def detect_country_name(pipe: pipeline, answer):
    ner_results = pipe(answer)
    return ner_results


def detect_company_size(answer):
    x = re.findall("[0-9]*-[0-9]*", answer)
    print(f"in company size function :{x}")
    return x


def handle_user_response(pipe: pipeline, question_id: int, answer: str):
    # this question for detect Customer job title
    if question_id == 2:
        field = "Customer job title"
        title = aggressive_detection(field, answer)
        if title and len(title) > 0:
            return title[0], True
        return answer, False

    elif question_id == 3:
        # this question for detect Job Seniority
        field = "Job Seniority"
        seniority = aggressive_detection(field, answer)
        if seniority and len(seniority) > 0:
            return seniority[0], True
        return answer, False

    elif question_id == 4:
        # this question for detect Department
        field = "Department"
        department = aggressive_detection(field, answer)
        if department and len(department) > 0:
            return department, True
        return answer, False

    elif question_id == 5:
        # this question for detect
        countries = detect_country_name(pipe, answer)
        if not countries or len(countries) == 0:
            return answer, False
        else:
            return countries[0]["word"], True

    elif question_id == 6:
        # detect city
        cities = detect_country_name(pipe, answer)
        if not cities or len(cities) == 0:
            return answer, False
        else:
            return cities[0]["word"], True

    elif question_id == 7:
        # detect industry
        # exist = check_value_in_lookup(answer)
        exist = False
        if exist:
            return answer, True
        return answer, False

    elif question_id == 8:
        # detect activities
        return answer, True

    elif question_id == 9:
        # detect company size
        company_size = detect_company_size(answer)
        if len(company_size) == 0:
            return answer, False
        return company_size[0], True

    elif question_id == 10:
        # detect company revenue
        return answer, True

    else:
        return answer, False
