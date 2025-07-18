import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import HomePage from './presentation/pages/HomePage'
import EditApi from './presentation/pages/EditApi'
import FloatingMenu from './presentation/components/FloatingMenu'
import './shared/styles/App.css'

function App() {
  return (
    <Router>
      <div className="App">
        <FloatingMenu />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/edit-api" element={<EditApi />} />
          <Route path="/usuario" element={<div>Página de Usuario (en desarrollo)</div>} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
