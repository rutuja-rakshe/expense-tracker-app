import { useState, useEffect } from 'react';
import API from '../api/axios';
import { useAuth } from '../context/AuthContext';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import toast from 'react-hot-toast';

const COLORS = ['#6366f1', '#f59e0b', '#10b981', '#ef4444', '#8b5cf6', '#ec4899'];
const CATEGORIES = ['food','transport','housing','utilities','healthcare','entertainment','shopping','education','travel','salary','freelance','investment','other'];

export default function Dashboard() {
  const { user, logout } = useAuth();
  const [dashboard, setDashboard] = useState(null);
  const [expenses, setExpenses] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const today = new Date();
  const [year, setYear] = useState(today.getFullYear());
  const [month, setMonth] = useState(today.getMonth() + 1);

  const [form, setForm] = useState({
    title: '', amount: '', category: 'food',
    type: 'expense', date: today.toISOString().split('T')[0], notes: ''
  });

  useEffect(() => {
    fetchData();
  }, [year, month]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [dashRes, expRes] = await Promise.all([
        API.get(`/api/v1/dashboard/?year=${year}&month=${month}`),
        API.get(`/api/v1/expenses/?year=${year}&month=${month}`)
      ]);
      setDashboard(dashRes.data);
      setExpenses(expRes.data.results);
    } catch {
      toast.error('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleAddExpense = async (e) => {
    e.preventDefault();
    try {
      await API.post('/api/v1/expenses/', form);
      toast.success('Expense added!');
      setShowForm(false);
      setForm({ title: '', amount: '', category: 'food', type: 'expense', date: today.toISOString().split('T')[0], notes: '' });
      fetchData();
    } catch {
      toast.error('Failed to add expense');
    }
  };

  const handleDelete = async (id) => {
    try {
      await API.delete(`/api/v1/expenses/${id}/`);
      toast.success('Deleted');
      fetchData();
    } catch {
      toast.error('Failed to delete');
    }
  };

  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

  return (
    <div className="dashboard">
      <header className="navbar">
        <h1>💰 Expense Tracker</h1>
        <div className="nav-right">
          <span>Hi, {user?.first_name}!</span>
          <button onClick={logout} className="btn-outline">Logout</button>
        </div>
      </header>

      <div className="container">
        {/* Month Selector */}
        <div className="month-selector">
          <select value={month} onChange={(e) => setMonth(Number(e.target.value))}>
            {months.map((m, i) => <option key={i} value={i + 1}>{m}</option>)}
          </select>
          <select value={year} onChange={(e) => setYear(Number(e.target.value))}>
            {[2024, 2025, 2026].map(y => <option key={y} value={y}>{y}</option>)}
          </select>
          <button onClick={() => setShowForm(true)} className="btn-primary">+ Add Expense</button>
        </div>

        {/* Summary Cards */}
        {dashboard && (
          <div className="cards-grid">
            <div className="card green">
              <p>Total Income</p>
              <h2>₹{Number(dashboard.total_income).toLocaleString()}</h2>
            </div>
            <div className="card red">
              <p>Total Expenses</p>
              <h2>₹{Number(dashboard.total_expenses).toLocaleString()}</h2>
            </div>
            <div className={`card ${Number(dashboard.net_balance) >= 0 ? 'blue' : 'orange'}`}>
              <p>Net Balance</p>
              <h2>₹{Number(dashboard.net_balance).toLocaleString()}</h2>
            </div>
            <div className="card purple">
              <p>Transactions</p>
              <h2>{dashboard.transaction_count}</h2>
            </div>
          </div>
        )}

        <div className="charts-grid">
          {/* Bar Chart */}
          {dashboard && (
            <div className="chart-card">
              <h3>Daily Spending</h3>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={dashboard.daily_totals.filter(d => d.expense > 0 || d.income > 0)}>
                  <XAxis dataKey="date" tickFormatter={d => d.split('-')[2]} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="expense" fill="#ef4444" name="Expense" />
                  <Bar dataKey="income" fill="#10b981" name="Income" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Pie Chart */}
          {dashboard?.expense_by_category?.length > 0 && (
            <div className="chart-card">
              <h3>By Category</h3>
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie data={dashboard.expense_by_category} dataKey="total" nameKey="category_display" cx="50%" cy="50%" outerRadius={80}>
                    {dashboard.expense_by_category.map((_, i) => (
                      <Cell key={i} fill={COLORS[i % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(v) => `₹${Number(v).toLocaleString()}`} />
                </PieChart>
              </ResponsiveContainer>
              <div className="legend">
                {dashboard.expense_by_category.map((c, i) => (
                  <span key={i} className="legend-item">
                    <span style={{ background: COLORS[i % COLORS.length] }} className="legend-dot"></span>
                    {c.category_display} ({c.percentage}%)
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Expense List */}
        <div className="expense-list">
          <h3>Transactions ({expenses.length})</h3>
          {loading ? <p>Loading...</p> : expenses.length === 0 ? (
            <p className="empty">No transactions this month. Add one!</p>
          ) : (
            <table>
              <thead>
                <tr><th>Date</th><th>Title</th><th>Category</th><th>Type</th><th>Amount</th><th></th></tr>
              </thead>
              <tbody>
                {expenses.map(e => (
                  <tr key={e.id}>
                    <td>{e.date}</td>
                    <td>{e.title}</td>
                    <td><span className="badge">{e.category_display}</span></td>
                    <td><span className={`badge ${e.type}`}>{e.type}</span></td>
                    <td className={e.type === 'income' ? 'green' : 'red'}>
                      {e.type === 'income' ? '+' : '-'}₹{Number(e.amount).toLocaleString()}
                    </td>
                    <td><button onClick={() => handleDelete(e.id)} className="btn-delete">✕</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      {/* Add Expense Modal */}
      {showForm && (
        <div className="modal-overlay" onClick={() => setShowForm(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Add Transaction</h3>
            <form onSubmit={handleAddExpense}>
              <input placeholder="Title" value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })} required />
              <input type="number" placeholder="Amount" value={form.amount}
                onChange={(e) => setForm({ ...form, amount: e.target.value })} required />
              <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
                {CATEGORIES.map(c => <option key={c} value={c}>{c.charAt(0).toUpperCase() + c.slice(1)}</option>)}
              </select>
              <select value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })}>
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
              <input type="date" value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })} required />
              <textarea placeholder="Notes (optional)" value={form.notes}
                onChange={(e) => setForm({ ...form, notes: e.target.value })} />
              <div className="modal-actions">
                <button type="button" onClick={() => setShowForm(false)} className="btn-outline">Cancel</button>
                <button type="submit" className="btn-primary">Add</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}