import React from 'react';
import './ExpenseList.css';

const ExpenseList = ({ expenses }) => {
  return (
    <div className="expense-list">
      <h2>View Expenses</h2>
      <table>
        <thead>
          <tr>
            <th>Category</th>
            <th>Amount</th>
            <th>Date</th>
            <th>Description</th>
            <th>Payment Method</th>
            <th>Recurring</th>
          </tr>
        </thead>
        <tbody>
          {expenses.map((expense, index) => (
            <tr key={index}>
              <td>{expense.category}</td>
              <td>{expense.amount}</td>
              <td>{expense.date}</td>
              <td>{expense.description}</td>
              <td>{expense.payment_method}</td>
              <td>{expense.recurring ? 'Yes' : 'No'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ExpenseList;
