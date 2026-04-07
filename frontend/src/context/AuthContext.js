import { createContext, useContext, useState, useEffect } from 'react';
import API from '../api/axios';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) fetchProfile();
    else setLoading(false);
  }, []);

  const fetchProfile = async () => {
    try {
      const res = await API.get('/api/v1/auth/profile/');
      setUser(res.data);
    } catch {
      localStorage.clear();
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, password) => {
    const res = await API.post('/api/v1/auth/login/', { email, password });
    localStorage.setItem('access_token', res.data.access);
    localStorage.setItem('refresh_token', res.data.refresh);
    await fetchProfile();
  };

  const register = async (data) => {
    const res = await API.post('/api/v1/auth/register/', data);
    localStorage.setItem('access_token', res.data.tokens.access);
    localStorage.setItem('refresh_token', res.data.tokens.refresh);
    setUser(res.data.user);
  };

  const logout = async () => {
    try {
      await API.post('/api/v1/auth/logout/', {
        refresh: localStorage.getItem('refresh_token'),
      });
    } finally {
      localStorage.clear();
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);