import React, { useState } from 'react';
import './Budget.css';

const Budget = ({ updateBudget }) => {
  const [category, setCategory] = useState('');
  const [amount, setAmount] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (category && amount) {
      updateBudget(category, amount);
      setCategory('');
      setAmount('');
    }
  };

  return (
    <div className="budget-form">
      <h2>Set Budget</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
        <input
          type="number"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
        />
        <button type="submit">Set Budget</button>
      </form>
    </div>
  );
};

export default Budget;
