import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import './App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Gestão de Ativos TI</h1>
          <p>Sistema de gerenciamento de ativos de TI</p>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

function Dashboard() {
  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      <p>Bem-vindo ao sistema de gestão de ativos TI</p>
      <div className="dashboard-cards">
        <div className="card">
          <h3>Total de Ativos</h3>
          <p>Carregando...</p>
        </div>
        <div className="card">
          <h3>Ativos Disponíveis</h3>
          <p>Carregando...</p>
        </div>
        <div className="card">
          <h3>Ativos Alocados</h3>
          <p>Carregando...</p>
        </div>
      </div>
    </div>
  )
}

export default App