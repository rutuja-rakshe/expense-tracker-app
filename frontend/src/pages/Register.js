import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import toast from 'react-hot-toast';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: '', first_name: '', last_name: '',
    password: '', password_confirm: '', currency: 'INR'
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.password !== form.password_confirm) {
      toast.error('Passwords do not match');
      return;
    }
    setLoading(true);
    try {
      await register(form);
      toast.success('Account created!');
      navigate('/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.email?.[0] || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h1>💰 Expense Tracker</h1>
        <h2>Create Account</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <input placeholder="First Name" value={form.first_name}
              onChange={(e) => setForm({ ...form, first_name: e.target.value })} required />
            <input placeholder="Last Name" value={form.last_name}
              onChange={(e) => setForm({ ...form, last_name: e.target.value })} required />
          </div>
          <input type="email" placeholder="Email" value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          <input type="password" placeholder="Password" value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          <input type="password" placeholder="Confirm Password" value={form.password_confirm}
            onChange={(e) => setForm({ ...form, password_confirm: e.target.value })} required />
          <select value={form.currency}
            onChange={(e) => setForm({ ...form, currency: e.target.value })}>
            <option value="INR">INR - Indian Rupee</option>
            <option value="USD">USD - US Dollar</option>
            <option value="EUR">EUR - Euro</option>
          </select>
          <button type="submit" disabled={loading}>
            {loading ? 'Creating...' : 'Create Account'}
          </button>
        </form>
        <p>Already have an account? <Link to="/login">Sign In</Link></p>
      </div>
    </div>
  );
}