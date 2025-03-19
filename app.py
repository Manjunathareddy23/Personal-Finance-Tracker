import streamlit as st
import pandas as pd

# Initialize session state to store expenses and budgets
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'budget' not in st.session_state:
    st.session_state.budget = {}

# Function to display the budget form
def show_budget_form():
    st.subheader('Set Budget')
    category = st.text_input("Category", key="budget_category")
    amount = st.number_input("Amount", min_value=0, step=1, key="budget_amount")
    if st.button('Set Budget'):
        if category and amount > 0:
            st.session_state.budget[category] = amount
            st.success(f"Budget for {category} set to {amount}")
        else:
            st.error("Please enter a valid category and amount")

# Function to display the Add Expense form
def show_add_expense_form():
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
            st.success("Expense Added Successfully!")
        else:
            st.error("Please fill in all required fields.")

# Function to display the expense list
def show_expense_list():
    st.subheader('View Expenses')
    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        st.write(df)
    else:
        st.write("No expenses added yet.")

# Function to display financial reports
def show_reports():
    st.subheader('Financial Reports')
    total_expenses = sum(expense['Amount'] for expense in st.session_state.expenses)
    st.write(f"Total Expenses: ${total_expenses:.2f}")

    # Display Budget vs Expenses
    budget_df = pd.DataFrame(st.session_state.budget.items(), columns=['Category', 'Budget'])
    expense_df = pd.DataFrame(st.session_state.expenses)
    if not expense_df.empty:
        expense_summary = expense_df.groupby('Category')['Amount'].sum().reset_index()
        expense_summary = pd.merge(expense_summary, budget_df, how='left', on='Category')
        expense_summary['Remaining'] = expense_summary['Budget'] - expense_summary['Amount']
        st.write(expense_summary)

# Streamlit Layout
st.title("Personal Finance Tracker")

# Layout for the main sections
tabs = st.sidebar.radio("Choose an option", ["Add Expense", "View Expenses", "Set Budget", "Financial Reports"])

if tabs == "Add Expense":
    show_add_expense_form()
elif tabs == "View Expenses":
    show_expense_list()
elif tabs == "Set Budget":
    show_budget_form()
elif tabs == "Financial Reports":
    show_reports()
