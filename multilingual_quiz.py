import os
from educhain import qna_engine
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

custom_template = """
दिए गए विषय और स्तर के आधार पर {num} बहुविकल्पीय प्रश्न (MCQ) उत्पन्न करें। प्रश्न, चार उत्तर विकल्प और सही उत्तर प्रदान करें।
विषय: {topic}

Generate questions in hindi.
"""

gpt_4o_mini = ChatOpenAI(model= "gpt-4o-mini")
llama3_405b = ChatOpenAI(model = "accounts/fireworks/models/llama-v3p1-405b-instruct",
                      openai_api_key = os.environ["FIREWORKS_API_KEY"],
                      openai_api_base = "https://api.fireworks.ai/inference/v1"
)


## Generate questions in Hindi
result = qna_engine.generate_mcq(
                                  topic="भारतीय भूगोल",
                                  num=3,
                                  llm = gpt_4o_mini,
                                  prompt_template=custom_template
                                  )

result.show()
     

custom_template = """
ఇచ్చిన అంశం మరియు స్థాయిని బట్టి {num} బహుళ ఎంపిక ప్రశ్నలు (MCQ) రూపొందించండి. ప్రశ్న, నాలుగు సమాధాన ఎంపికలు మరియు సరైన సమాధానాన్ని అందించండి.
అంశం: {topic}
ప్రశ్నలను తెలుగులో రూపొందించండి.
"""

result = qna_engine.generate_mcq(
                                  topic="భారతదేశ భౌగోళికం",
                                  num=3,
                                  llm = gpt_4o_mini,
                                  prompt_template=custom_template,
                                  )

result.show()