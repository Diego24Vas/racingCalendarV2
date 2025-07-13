import React from 'react'
import WelcomeCard from '../components/WelcomeCard'
import MapHome from '../components/MapHome'
import './HomePage.css'
import EstadoApi from "../components/EstadoApi";

const HomePage = () => {
  return (
    <div className="home-page">
      <MapHome />
      <EstadoApi />
    </div>
  )
}

export default HomePage
