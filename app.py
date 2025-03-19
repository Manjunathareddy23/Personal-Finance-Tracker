import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json

# Firebase authentication setup (you need to set this up in Firebase)
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK (this will need a JSON file for Firebase)
if not firebase_admin._apps:
    cred = credentials.Certificate("financetracker-8bb74-firebase-adminsdk-fbsvc-44d0570416.json")
    firebase_admin.initialize_app(cred)

# Inject Tailwind CSS via CDN link
st.markdown(
    """
    <style>
        @import url('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css');
        .stTextInput, .stNumberInput, .stDateInput, .stTextArea {
            margin-bottom: 1rem;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.375rem;
            border: none;
            transition: background-color 0.3s;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stSuccess {
            color: #4CAF50;
        }
        .stError {
            color: #f44336;
        }
        .stRadio div {
            margin-bottom: 1rem;
        }
        .container {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 20px;
        }
        .form-section {
            flex: 1;
            max-width: 45%;
        }
        .section-header {
            font-size: 2rem;
            margin-bottom: 1rem;
            color: #333;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state to store expenses, budgets, and financial goals
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'budget' not in st.session_state:
    st.session_state.budget = {}
if 'financial_goals' not in st.session_state:
    st.session_state.financial_goals = {}

# Function to load saved data from CSV/Excel files (persistent data)
def load_data():
    # Load expenses from CSV file
    if os.path.exists("expenses.csv"):
        try:
            df_expenses = pd.read_csv("expenses.csv")
            st.session_state.expenses = df_expenses.to_dict(orient="records") if not df_expenses.empty else []
        except Exception as e:
            st.error(f"Error loading expenses data: {e}")
            st.session_state.expenses = []  # Fallback to empty list if loading fails
    
    # Load budget from CSV file
    if os.path.exists("budget.csv"):
        try:
            df_budget = pd.read_csv("budget.csv")
            st.session_state.budget = pd.Series(df_budget['Budget'].values, index=df_budget['Category']).to_dict() if not df_budget.empty else {}
        except Exception as e:
            st.error(f"Error loading budget data: {e}")
            st.session_state.budget = {}  # Fallback to empty dict if loading fails

    # Load financial goals from JSON file
    if os.path.exists("financial_goals.json"):
        try:
            with open("financial_goals.json", "r") as file:
                st.session_state.financial_goals = json.load(file)
        except Exception as e:
            st.error(f"Error loading financial goals data: {e}")
            st.session_state.financial_goals = {}

# Function to save data to CSV files (persistent data)
def save_data():
    try:
        # Save expenses to CSV
        df_expenses = pd.DataFrame(st.session_state.expenses)
        df_expenses.to_csv("expenses.csv", index=False)
        
        # Save budget to CSV
        df_budget = pd.DataFrame(list(st.session_state.budget.items()), columns=['Category', 'Budget'])
        df_budget.to_csv("budget.csv", index=False)

        # Save financial goals to JSON
        with open("financial_goals.json", "w") as file:
            json.dump(st.session_state.financial_goals, file)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Function to display the budget form
def show_budget_form():
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader('Set Budget')
    category = st.text_input("Category", key="budget_category")
    amount = st.number_input("Amount", min_value=0, step=1, key="budget_amount")
    if st.button('Set Budget'):
        if category and amount > 0:
            st.session_state.budget[category] = amount
            save_data()
            st.success(f"Budget for {category} set to {amount}")
        else:
            st.error("Please enter a valid category and amount")
    st.markdown('</div>', unsafe_allow_html=True)

# Function to display the Add Expense form
def show_add_expense_form():
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader('Add Expense')
    category = st.text_input("Category", key="expense_category")
    amount = st.number_input("Amount", min_value=0, step=1, key="expense_amount")
    date = st.date_input("Date", key="expense_date")
    description = st.text_area("Description", key="expense_description")
    payment_method = st.text_input("Payment Method", key="payment_method")
    recurring = st.checkbox("Recurring", key="recurring")

    if st.button('Add Expense'):
        if category and amount > 0 and date:
            expense = {
                'Category': category,
                'Amount': amount,
                'Date': date,
                'Description': description,
                'Payment Method': payment_method,
                'Recurring': recurring
            }
            st.session_state.expenses.append(expense)
            save_data()
            st.success("Expense Added Successfully!")
        else:
            st.error("Please fill in all required fields.")
    st.markdown('</div>', unsafe_allow_html=True)

# Function to display the expense list
def show_expense_list():
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader('View Expenses')
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.write(df)
    else:
        st.write("No expenses added yet.")
    st.markdown('</div>', unsafe_allow_html=True)

# Function to display financial reports (with charts)
def show_reports():
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader('Financial Reports')
    
    total_expenses = sum(expense['Amount'] for expense in st.session_state.expenses)
    st.write(f"Total Expenses: ${total_expenses:.2f}")
    
    # Plot the expense by category
    expense_df = pd.DataFrame(st.session_state.expenses)
    if not expense_df.empty:
        expense_summary = expense_df.groupby('Category')['Amount'].sum().reset_index()

        # Plot using Plotly
        fig = px.bar(expense_summary, x='Category', y='Amount', title="Expenses by Category")
        st.plotly_chart(fig)

        # Budget vs Expenses Pie Chart
        budget_df = pd.DataFrame(list(st.session_state.budget.items()), columns=['Category', 'Budget'])
        budget_expenses_df = pd.merge(expense_summary, budget_df, how='left', on='Category')
        budget_expenses_df['Remaining'] = budget_expenses_df['Budget'] - budget_expenses_df['Amount']

        # Plot Budget vs Expenses
        fig2 = px.pie(budget_expenses_df, names='Category', values='Amount', title="Budget vs Expenses")
        st.plotly_chart(fig2)
    st.markdown('</div>', unsafe_allow_html=True)

# Function to display financial goals
def show_financial_goals():
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.subheader('Set Financial Goals')
    goal_name = st.text_input("Goal Name", key="goal_name")
    target_amount = st.number_input("Target Amount", min_value=0, step=1, key="target_amount")
    if st.button('Set Goal'):
        if goal_name and target_amount > 0:
            st.session_state.financial_goals[goal_name] = target_amount
            save_data()
            st.success(f"Goal '{goal_name}' set to ${target_amount}")
        else:
            st.error("Please enter a valid goal name and target amount")
    st.markdown('</div>', unsafe_allow_html=True)

# Streamlit Layout
st.title("Personal Finance Tracker")

# Load data from persistent storage
load_data()

# Layout for the main sections
tabs = st.sidebar.radio("Choose an option", ["Add Expense", "View Expenses", "Set Budget", "Financial Reports", "Financial Goals"])

# Flexbox layout for the sections
st.markdown('<div class="container">', unsafe_allow_html=True)

if tabs == "Add Expense":
    show_add_expense_form()
elif tabs == "View Expenses":
    show_expense_list()
elif tabs == "Set Budget":
    show_budget_form()
elif tabs == "Financial Reports":
    show_reports()
elif tabs == "Financial Goals":
    show_financial_goals()

st.markdown('</div>', unsafe_allow_html=True)
