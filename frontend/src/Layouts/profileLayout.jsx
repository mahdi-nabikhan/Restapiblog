import React from 'react'
import { Outlet } from 'react-router-dom'
import TopBar from '../Components/Panel/TopBar/TopBar'
import Sidebar from '../Components/Panel/SideBar/SideBar'
import './ProfileLayout.css'
export default function ProfileLayout() {
  return (
    <>
     <div className="panel-layout">
      <Sidebar />

      <div className="panel-main">
        <TopBar />
        <main className="panel-content">
          <Outlet />
        </main>
      </div>
    </div>
    </>
  )
}
