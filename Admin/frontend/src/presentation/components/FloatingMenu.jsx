import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './FloatingMenu.css'

const FloatingMenu = () => {
  const [isOpen, setIsOpen] = useState(false)
  const navigate = useNavigate()

  const toggleMenu = () => {
    setIsOpen(!isOpen)
  }

  const handleNavigation = (href) => {
    navigate(href)
    setIsOpen(false)
  }

  const menuItems = [
    { icon: '🏠', label: 'Home', href: '/' },
    { icon: '👤', label: 'Usuario', href: '/usuario'},
  ]

  return (
    <div className="floating-menu">
      {/* Botón principal del menú */}
      <button 
        className={`menu-toggle ${isOpen ? 'active' : ''}`}
        onClick={toggleMenu}
        aria-label={isOpen ? 'Cerrar menú' : 'Abrir menú'}
      >
        <span className="menu-icon">
          {isOpen ? '✕' : '☰'}
        </span>
      </button>

      {/* Menú desplegable */}
      <div className={`menu-dropdown ${isOpen ? 'open' : ''}`}>
        <div className="menu-content">
          <div className="menu-header">
            <h3 className="menu-title">Racing Calendar</h3>
          </div>
          <nav className="menu-nav">
            {menuItems.map((item, index) => (
              <button
                key={index}
                onClick={() => handleNavigation(item.href)}
                className="menu-item"
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <span className="menu-item-icon">{item.icon}</span>
                <span className="menu-item-label">{item.label}</span>
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Overlay para cerrar el menú */}
      {isOpen && (
        <div 
          className="menu-overlay"
          onClick={() => setIsOpen(false)}
        />
      )}
    </div>
  )
}

export default FloatingMenu
