import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';
import { FiLogOut, FiHome, FiClock } from 'react-icons/fi';
import './Navbar.css';

function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <h2>Chemical Equipment Analyzer</h2>
      </div>
      <div className="navbar-links">
        <Link to="/dashboard" className="nav-link">
          <FiHome /> Dashboard
        </Link>
        <Link to="/history" className="nav-link">
          <FiClock /> History
        </Link>
      </div>
      <div className="navbar-user">
        <span>Welcome, {user?.username}</span>
        <button onClick={logout} className="logout-btn">
          <FiLogOut /> Logout
        </button>
      </div>
    </nav>
  );
}

export default Navbar;