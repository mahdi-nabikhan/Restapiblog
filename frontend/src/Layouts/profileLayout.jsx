import React from 'react'
import { Outlet } from 'react-router-dom'
import TopBar from '../Components/Panel/TopBar/TopBar'
import Sidebar from '../Components/Panel/SideBar/SideBar'

export default function ProfileLayout() {
  return (
    <>
    <TopBar/>
    <Sidebar/>
    <main>
        <Outlet/>
    </main>
    
    </>
  )
}
