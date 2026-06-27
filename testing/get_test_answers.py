from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings , ChatGoogleGenerativeAI
from time import sleep
import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from pydantic import BaseModel
import json
#=======================================
class Answer(BaseModel):
    answer: str
@tool 
def get_documents_from_vector_db(query:str)->str:
    """tool that retrieve answers from vetor db"""
    retrieved = ''
    docs = vectorstore.similarity_search(query, k=3)
    for doc in docs:
        retrieved+=doc.page_content
    return retrieved
#=======================================================
load_dotenv()
key = os.environ.get("GOOGLE_API_KEY")
embed_key = os.environ.get("EMBEDDING")
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview" , 
    output_dimensionality = 500 ,
    task_type = "RETRIEVAL_DOCUMENT" , 
    api_key = embed_key)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash" , api_key =key , temperature=0.2 ,  max_retries=2)
system_prompt = """
 you are a hepful assistant that takes the docs found , and query of the user , summarize the docs
 and give answer for the query as human , answer should be meduim , understandable
"""
agent = create_agent(model = llm  , system_prompt= system_prompt , tools=[get_documents_from_vector_db], response_format=Answer)
vectorstore = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings,
    collection_name="english_learning_platform"
)
questions = [
  { "question": "What score is needed to pass an exam?", "expected_answer": "Students must achieve at least 70% to pass the exam." },
  { "question": "Can I retake a failed exam?", "expected_answer": "Yes, students can retake a failed exam after a waiting period of 14 days." },
  { "question": "How are students graded?", "expected_answer": "Students are graded based on exams, quizzes, assignments, and participation activities." },
  { "question": "What is included in the exam?", "expected_answer": "Exams include multiple choice questions, writing tasks, listening comprehension, and oral evaluation." },
  { "question": "How do I get a certificate?", "expected_answer": "Certificates are awarded after completing all courses and passing the final exam." },
  { "question": "What is the refund policy?", "expected_answer": "Refunds are available within 14 days if less than 20 percent of course content has been accessed." },
  { "question": "Can I share my account?", "expected_answer": "No, each user is allowed one account only and sharing accounts is strictly prohibited." },
  { "question": "What happens if I cheat in exams?", "expected_answer": "Cheating during exams or quizzes will result in penalties or account suspension." },
  { "question": "How does the platform track progress?", "expected_answer": "The platform tracks progress using completed lessons, quiz scores, and exam results." },
  { "question": "What are the four skills in each level?", "expected_answer": "Each level includes Reading, Writing, Listening, and Speaking courses." },

  { "question": "What does reading course focus on?", "expected_answer": "Reading courses focus on comprehension, vocabulary expansion, and understanding written texts." },
  { "question": "What does writing course teach?", "expected_answer": "Writing courses develop grammar, sentence structure, paragraph writing, and essay writing." },
  { "question": "What does listening course include?", "expected_answer": "Listening courses train learners to understand spoken conversations, lectures, and real-life speech." },
  { "question": "What does speaking course focus on?", "expected_answer": "Speaking courses focus on fluency, pronunciation, vocabulary, and communication skills." },

  { "question": "What is A1 level?", "expected_answer": "A1 is beginner level where learners understand basic expressions and simple sentences." },
  { "question": "What is A2 level?", "expected_answer": "A2 is elementary level where learners handle simple everyday communication." },
  { "question": "What is B1 level?", "expected_answer": "B1 is intermediate level where learners can handle everyday situations and express opinions." },
  { "question": "What is B2 level?", "expected_answer": "B2 is upper-intermediate level where learners can communicate fluently and in detail." },
  { "question": "What is C1 level?", "expected_answer": "C1 is advanced level where learners understand complex texts and express ideas clearly." },
  { "question": "What is C2 level?", "expected_answer": "C2 is proficiency level where learners can understand and express like native speakers." },

  { "question": "Do I need all courses before next level?", "expected_answer": "Yes, students must complete all four skill courses before progressing." },
  { "question": "What is learning path rule?", "expected_answer": "Students must complete all required courses in a level before moving to the next level." },
  { "question": "What are community rules?", "expected_answer": "Users must be respectful and avoid harassment, spam, or offensive behavior." },
  { "question": "What are security guidelines?", "expected_answer": "Users must use strong passwords and avoid sharing login credentials." },
  { "question": "How is data protected?", "expected_answer": "User data is encrypted and only shared when required by law." },
  { "question": "Is the platform always available?", "expected_answer": "Yes, the platform is available 24/7 except during maintenance." },
  { "question": "What devices are supported?", "expected_answer": "The platform supports mobile, tablet, and desktop devices." },
  { "question": "What is lesson format?", "expected_answer": "Lessons include videos, quizzes, and practice exercises." },
  { "question": "What is adaptive learning?", "expected_answer": "Adaptive learning adjusts difficulty based on student performance." },
  { "question": "How does recommendation system work?", "expected_answer": "It recommends lessons based on student weaknesses and progress." },

  { "question": "What is course completion rule?", "expected_answer": "A course is completed when all lessons and assessments are finished." },
  { "question": "What is vocabulary policy?", "expected_answer": "Vocabulary is introduced progressively across all levels." },
  { "question": "What is grammar learning policy?", "expected_answer": "Grammar is taught from simple to advanced structures across levels." },
  { "question": "How is speaking practiced?", "expected_answer": "Speaking practice includes pronunciation exercises and conversation simulations." },
  { "question": "How is listening practiced?", "expected_answer": "Listening exercises include real-life conversations and academic lectures." },
  { "question": "How is writing practiced?", "expected_answer": "Writing tasks include essays, summaries, and structured paragraphs." },
  { "question": "How is reading practiced?", "expected_answer": "Reading exercises include articles, stories, and comprehension tests." },

  { "question": "What is platform overview?", "expected_answer": "The platform is an AI-powered English learning system from A1 to C2." },
  { "question": "What is course structure?", "expected_answer": "Each level contains four courses: Reading, Writing, Listening, Speaking." },
  { "question": "What is exam structure?", "expected_answer": "Exams include multiple choice, writing, listening, and speaking evaluation." },
  { "question": "What is passing criteria?", "expected_answer": "Students must score at least 70% to pass." },
  { "question": "What happens after passing?", "expected_answer": "Students receive a certificate after passing the exam." },
  { "question": "What happens if I fail?", "expected_answer": "Students can retake the exam after 14 days." },

  { "question": "What is instructor responsibility?", "expected_answer": "Instructors must provide accurate content and support students professionally." },
  { "question": "How do instructors communicate?", "expected_answer": "Communication is done through official platform channels only." },
  { "question": "How are instructors evaluated?", "expected_answer": "They are evaluated based on student feedback and engagement." },
  { "question": "What are student guidelines?", "expected_answer": "Students must complete lessons in order and follow platform rules." },

  { "question": "What is attendance policy?", "expected_answer": "Consistent participation improves learning outcomes." },
  { "question": "What is skill balance?", "expected_answer": "Students should balance reading, writing, listening, and speaking." },
  { "question": "What is progress tracking?", "expected_answer": "Progress is measured by lessons completed and exam results." },
  { "question": "What is learning analytics?", "expected_answer": "The system analyzes student performance across all skills." },
  { "question": "What is certification policy?", "expected_answer": "Certificates are given after completing all courses and passing exams." },

  { "question": "What is payment policy?", "expected_answer": "All courses must be paid before access is granted." },
  { "question": "What is subscription model?", "expected_answer": "Users can subscribe monthly or annually." },
  { "question": "What is platform availability policy?", "expected_answer": "The platform is available 24/7 except maintenance periods." },
  { "question": "What is mobile access policy?", "expected_answer": "The platform supports mobile, tablet, and desktop devices." },
  { "question": "What is exercise system?", "expected_answer": "Each lesson includes interactive exercises." },

  { "question": "What is reading policy?", "expected_answer": "Reading includes articles, stories, and comprehension tasks." },
  { "question": "What is writing policy?", "expected_answer": "Writing includes essays, summaries, and structured texts." },
  { "question": "What is listening policy?", "expected_answer": "Listening includes conversations and lectures." },
  { "question": "What is speaking policy?", "expected_answer": "Speaking includes pronunciation and communication practice." },

  { "question": "What is anti cheating policy?", "expected_answer": "Cheating results in penalties or account suspension." },
  { "question": "What is content protection policy?", "expected_answer": "All content is protected and cannot be redistributed." },
  { "question": "What is technical support policy?", "expected_answer": "Users can contact support for technical issues." },
  { "question": "What is privacy policy?", "expected_answer": "User data is protected and not shared without legal requirement." },

  { "question": "What is platform goal?", "expected_answer": "The platform aims to provide structured AI-powered English learning from A1 to C2." }
]

answers = json.load(open("testing/answers.json",'r',encoding='utf-8'))
start = json.load(open("testing/index.json",'r',encoding='utf-8'))['idx']
n = len(questions)
for i in range( start , n):
    question = questions[i]
    try:
        answer = agent.invoke({"messages":[{'role' : "user" , 'content' : question['question']}]})['structured_response'].answer
        answers.append({
            "rag" : answer, "expected" : question['expected_answer']})
        print(f'SUCSESS {i+1} / {n}')
        sleep(40)
        print('passing rate limit')
    except Exception as e:
        print(e)
        with open("testing/index.json", "w") as f:
            json.dump({'idx'  : i}, f, indent=2)
        break
with open("testing/answers.json", "w") as f:
    json.dump(answers, f, indent=2)
#py testing\get_test_answers.py