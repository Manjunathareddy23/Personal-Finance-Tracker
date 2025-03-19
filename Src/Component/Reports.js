import React from 'react';
import './Reports.css';

const Reports = ({ expenses }) => {
  const totalExpenses = expenses.reduce((acc, expense) => acc + parseFloat(expense.amount), 0);

  return (
    <div className="reports">
      <h2>Financial Reports</h2>
      <p>Total Expenses: ${totalExpenses}</p>
      {/* Implement more detailed reports like pie charts or bar graphs later */}
    </div>
  );
};

export default Reports;
