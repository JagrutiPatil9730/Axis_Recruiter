from langchain import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import os
os.environ["OPENAI_API_KEY"] = "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"

from langchain.document_loaders import YoutubeLoader
# !pip install youtube-transcript-api

# Environment Variables


def pull_from_website(url):
    
    # Doing a try in case it doesn't work
    try:
        response = requests.get(url)
            # Put your response in a beautiful soup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get your text
        text = soup.get_text()
    
        # Convert your html to markdown. This reduces tokens and noise
        text = md(text)
         
        return text
    except:
        # In case it doesn't work
        print ("Whoops, error")
        return None

# I'm going to store my website data in a simple string.
# There is likely optimization to make this better but it's a solid 80% solution


    website_data = ""
    urls = ['https://engineeringinterviewquestions.com/axis-bank-interview-questions-and-answers-pdf/']

    for url in urls:
        text = '''   EXPERIENCE
    EDUCATION
    POSITIONS OF RESPONSIBILITY:
    PROJECTS
    SKILLS SUMMARY
    Firebase
    Kivy Python
    Mysql
    Django
    LANGUAGE
    English Japanese Marathi
    TRAINING AND WORKSHOPS
    Hindi
    C++
    TCP/IP
    Java
    C
    JavaScript
    PHP
    Linux/Windows
    HTML/CSS
    ACHIEVEMENTS:
    Data Structure And Algorithms
    Network Programming Vice President of CESA (Computer Engineering Student Association) in R.
    C. Patel Polytechnic college.
    Led a team of 8 members in organizing technical events, resulting in a
    30% increase in student participation.
    Group Leader of Capstone Project PBM App. and Medsync App.
    Coordinated a team of 5 members in the development of two mobile
    applications, achieving a 40% reduction in paperwork and improving
    parent engagement by 25%.
    JAGRUTI
    As a motivated and enthusiastic individual, I am
    eager to utilize the skills and knowledge gained
    from my internship and projects to contribute to
    an organization in the field. I am particularly
    interested in opportunities that allow me to work
    on innovative technologies and apply my
    engineering skills.
    About Me
    linkedin.com/in//ms-jagruti-patil
    9970923077
    Sumago Infotech Pvt. Ltd. [Internship]
    Year: 2023 (Pursuing)
    Performance: Recent CGPA 7.73
    44, Shiv Darshan Rd, Parvati, Nirmal Baug
    Colony, Parvati Paytha, Pune, 411009
    Period: Feb 2021 to June 2022
    Collaborated with a team of 5 members to solve problems and develop
    innovative software solutions.
    Demonstrated proficiency in programming and implementing objectoriented languages, completing 3 projects.
    Applied engineering principles to creatively solve complex problems,
    resulting in a 25% improvement in project efficiency.
    Adapted to new technologies, tools, and processes to enhance solutions,
    increasing productivity by 15%.
    Successfully completed 4 software projects in a cooperative team
    environment, meeting all project deadlines.
    Pursuing Bachelor of Engineering in Computer Science
    [Currently Pursuing 3rd Year]
    PBM Android App [Sponcered Project]
    Platform Used: Python, Kivy, KivyMD, Firebase, Ubuntu-buildozer
    Developed a school management app with automatic timetable
    builder, attendance sheet generator, and progress tracker.
    Increased operational efficiency by 40% and improved parent
    engagement by 25%.
    Completed the project within a team of 4 members in 9 months.
    B-E: Pune Vidyarthi Griha College of Engineering, Pune (SPPU)
    Year: August 2022
    Performance: 91.83%
    Diploma: R. C. Patel Polytechnic, Shirpur (MSBTE)
    PATIL
    jagrutipatil5433@gmail.com
    Year: March 2019
    Performance: 93.40%
    S.S.C: H. R. Patel Secondary School, Shirpur (MSBSHSE)
    Med-Sync AI Based Health Manager
    Platform Used: Python, Django, PostgreSQL
    Currently working on the development of a secure and user-friendly
    healthcare app.
    Implementing features such as appointment scheduling, electronic
    medical records, medication tracking, AI consultant, and remote
    consultation.
    Leading a team of 4 members in the ongoing development process.
    First Prize in Project Competition at R.C Patel
    College, competing against 10 teams.
    Winner of Blog Making Competition, with over 50
    participants.
    Participated in Pradnya at PICT Pune, a nationallevel tech fest.
    Completed a 3-month training program on AI Development, Machine
    Learning, and Ethical Hacking at IIT Bombay, acquiring practical knowledge
    in cutting-edge technologies.
    Training on Bootstrap, WordPress, and Blogger by R.C Patel College,
    expanding web development skills.
    github.com/JagrutiPatil9730
    https://jagruti.vercel.app/
    '''
        text+=pull_from_website(url) 
        website_data += text

    user_information = website_data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=20000, chunk_overlap=2000)
    docs = text_splitter.create_documents([user_information])
    print(len(docs))
    map_prompt=''' You are a helpful AI bot that takes the banking interview of the user .give list to interview question by analysing given resume  information by using this data as % START OF INFORMATION ABOUT {job}:
    {text}
    % END OF INFORMATION ABOUT {job}:'''
    # map_prompt = """You are a helpful AI bot that takes the banking interview of the user by of a {job} asking relevant questions from the provided data set.
    # Below is information about the banking questions and answers which are usually asked in the interview.
    # Information will include interview transcripts about the {job}
    # Your goal is to generate logical interview questions about {job} which can be answered by the user
    # Use specifics from the research when possible

    # % START OF INFORMATION ABOUT {job}:
    # {text}
    # % END OF INFORMATION ABOUT {job}:
    # Please respond with list of a few interview questions based on the topics above
    # YOUR RESPONSE:"""
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text", "job"])

    combine_prompt = """
    You are a helpful AI bot that is an interviewer which takes the banking interview of the user and takes the input from the user for the answer.
    You will be given a list of potential interview questions that we can ask to the user related to the {job}.

    Please consolidate the questions and return set of questions 

    % INTERVIEW QUESTIONS
    {text}
    """
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text", "job"])
    llm = ChatOpenAI(temperature=.25, model_name='gpt-3.5-turbo')

    chain = load_summarize_chain(llm,chain_type="map_reduce",map_prompt=map_prompt_template,combine_prompt=combine_prompt_template
    #,verbose=True
    )

    output = chain({"input_documents": docs, # The seven docs that were created before
                    "job": "cleark"
                })
    print (output['output_text'])