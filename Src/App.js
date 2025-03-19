import React, { useState } from 'react';
import './styles/App.css';
import AddExpense from './components/AddExpense';
import ExpenseList from './components/ExpenseList';
import Budget from './components/Budget';
import Reports from './components/Reports';

const App = () => {
  const [expenses, setExpenses] = useState([]);
  const [budget, setBudget] = useState({});

  const addExpense = (expense) => {
    setExpenses([...expenses, expense]);
  };

  const updateBudget = (category, amount) => {
    setBudget({ ...budget, [category]: amount });
  };

  return (
    <div className="App">
      <h1>Personal Finance Tracker</h1>
      <div className="main-container">
        <AddExpense addExpense={addExpense} />
        <Budget updateBudget={updateBudget} />
      </div>
      <ExpenseList expenses={expenses} />
      <Reports expenses={expenses} />
    </div>
  );
};

export default App;
