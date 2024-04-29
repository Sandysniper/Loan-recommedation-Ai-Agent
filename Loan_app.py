import streamlit as st
from crewai import Agent, Task, Crew
import os
# ... (Import other necessary libraries) ...
from langchain_groq import ChatGroq


model_agent=ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="llama3-8b-8192"
)
os.environ ["SERPER_API_KEY"] = "018591824635f940322a07169b38956fa75da3e7"

# Serperapi commands
from langchain.agents import load_tools


# Title and Introduction
st.title("Personalized Loan Recommendation Agent")
st.write("Discover the best Loans tailored to your needs!")

# Streamlit User Inputs
st.sidebar.header("Tell us about yourself:")

age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30)

loan_purpose = st.sidebar.selectbox(
    "Loan Purpose", 
    options=["Home Purchase", "Auto Loan", "Personal Loan", "Business loan", "Educational loan", "Debt Consolidation", "Other"]
)

loan_amount = st.sidebar.number_input("Loan Amount", min_value=1000)

loan_term = st.sidebar.selectbox(
    "Desired Loan Term",
    options=["Short-term (< 5 years)", "Medium-term (5-10 years)", "Long-term (> 10 years)"]
)

credit_score = st.sidebar.number_input("Credit Score", min_value=300, max_value=850)

income = st.sidebar.number_input("Annual Income", value=50000)

employment_length = st.sidebar.selectbox(
    "Employment Length",
    options=["< 1 year", "1-3 years", "3-5 years", "5+ years"]
)

debt_to_income_ratio = st.sidebar.number_input("Debt-to-Income Ratio (DTI)", min_value=0.0, format="%.2f")

has_coi = st.sidebar.checkbox("Do you have a co-signer?")

has_collateral = st.sidebar.checkbox("Do you have collateral?")

has_employment_guarantee = st.sidebar.checkbox("Do you have an employment guarantee?")

# Create User Input Dictionary
user_inputs = {
    "loan_purpose":loan_purpose,
    "loan_amount": loan_amount,
    "loan_term": loan_term,
    "credit_score": credit_score,
    "income": income,
    "employment_length": employment_length,
    "debt_to_income_ratio": debt_to_income_ratio,
    "has_coi": has_coi,
    "has_collateral": has_collateral,
    "has_employment_guarantee": has_employment_guarantee
}



    

                # Agent Backstory and Role

loan_expert_backstory = """
You are a loan specialist with extensive knowledge of various loan products, interest rates, and lending criteria. 
You can access and analyze data from multiple lenders to identify the most suitable loan options for borrowers based on their financial situation, creditworthiness, and loan requirements.
"""

loan_analyst_backstory = """
You are a financial analyst specializing in risk assessment and loan analysis. 
You can evaluate borrower information, assess their creditworthiness, and analyze the potential risks associated with different loan options.
"""

report_generator_backstory = """
You are a skilled report writer with expertise in presenting complex financial information in a clear, concise, and easy-to-understand format. 
You can tailor your reports to specific audiences, highlighting key insights and recommendations.
"""

# Implementation of Agents

loan_recommender = Agent(
    role="Loan Recommendation Expert",
    goal="Analyze borrower information and recommend suitable loan options in India",
    backstory=loan_expert_backstory,
    verbose=True,
    allow_delegation=False,
    tools=load_tools(["google-serper"]), 
    llm=model_agent
)

loan_analyst = Agent(
    role="Loan Risk Analyst",
    goal="Assess borrower creditworthiness and analyze potential loan risks", 
    backstory=loan_analyst_backstory,
    verbose=True,
    allow_delegation=False,
    llm=model_agent
)

report_generator = Agent(
    role="Financial Report Writer",
    goal="Generate clear and concise reports on loan options and recommendations",
    backstory=report_generator_backstory,
    verbose=True,
    allow_delegation=False, 
    llm=model_agent
)



# ... (Streamlit User Input code as before) ...

# Tasks
task1 = Task(
    description=f"""
    Analyze the loan request based on the following user information: {user_inputs}. 
    Research and identify potential loan options from various lenders.
    """,
    expected_output="List of potential loan options with key details (lender, interest rate, term, etc.)",
    agent=loan_recommender,
    async_execution=True
)

task2 = Task(
    description="""
    Evaluate the borrower's creditworthiness and assess the potential risks associated with each loan option identified in the previous task.
    Consider factors such as credit score, debt-to-income ratio, employment history, and collateral. 
    """,
    expected_output="Analysis of borrower's creditworthiness and risk assessment for each loan option available in only India ",
    agent=loan_analyst,
    async_execution=True
)

task3 = Task(
    description="""
    Based on the loan options and risk assessments, generate a comprehensive report for the user. 
    Clearly present the most suitable loan options, highlighting their terms, interest rates, potential risks, and benefits.
    Explain the rationale behind the recommendations and provide additional insights to guide the user's decision-making process.
    """,
    expected_output="Comprehensive report with clear highlighted loan recommendations and explanations and give the numerical data of loan options with Lender,Interest Rate, Loan Type, Loan Term, Monthly Payments in a different Tables so,the user can compare & choose the right one easily",
    agent=report_generator,
    context=[task1,task2]
  
)



# Crew
crew = Crew(
    agents=[loan_recommender, loan_analyst, report_generator,],
    tasks=[task1,task2,task3],
    verbose=1   
)

# Recommendation Button
if st.sidebar.button("Get Recommendations"):
    # Placeholder for Recommendation Logic
    st.header("Recommended Products for You:")
    # ... display recommended products based on user input ... 
    # ... you can use st.write() or other Streamlit components ...

    
    with st.spinner("Analyzing your request and generating recommendations...\n It Will take 2-3 Minutes So,Please Wait Patiently"):
     result = crew.kickoff()
     
   
     # Returns a TaskOutput object with the description and results of the task
    st.write(f"""
             Task : {task3.output.raw_output}""")
    
    
     # Assuming the agent provides a dictionary with "loan_options" key

