import React from 'react'
import { Outlet } from 'react-router-dom'
import Navbar from '../Components/Main/Navbar/Navbar'
import Footer from '../Components/Main/Footer/Footer'
export default function MainLayout() {
  return (
    <>
    <Navbar/>
    <main>
        <Outlet/>
    </main>
    <Footer/>
    </>
  )
}
