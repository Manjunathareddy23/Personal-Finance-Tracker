import React, { useState } from 'react';
import './AddExpense.css';

const AddExpense = ({ addExpense }) => {
  const [expense, setExpense] = useState({
    category: '',
    amount: '',
    date: '',
    description: '',
    payment_method: '',
    recurring: false,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setExpense({ ...expense, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (expense.category && expense.amount && expense.date) {
      addExpense(expense);
      setExpense({
        category: '',
        amount: '',
        date: '',
        description: '',
        payment_method: '',
        recurring: false,
      });
    }
  };

  return (
    <div className="add-expense-form">
      <h2>Add Expense</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="category"
          placeholder="Category"
          value={expense.category}
          onChange={handleChange}
        />
        <input
          type="number"
          name="amount"
          placeholder="Amount"
          value={expense.amount}
          onChange={handleChange}
        />
        <input
          type="date"
          name="date"
          value={expense.date}
          onChange={handleChange}
        />
        <textarea
          name="description"
          placeholder="Description"
          value={expense.description}
          onChange={handleChange}
        />
        <input
          type="text"
          name="payment_method"
          placeholder="Payment Method"
          value={expense.payment_method}
          onChange={handleChange}
        />
        <label>
          Recurring
          <input
            type="checkbox"
            name="recurring"
            checked={expense.recurring}
            onChange={(e) => setExpense({ ...expense, recurring: e.target.checked })}
          />
        </label>
        <button type="submit">Add Expense</button>
      </form>
    </div>
  );
};

export default AddExpense;
