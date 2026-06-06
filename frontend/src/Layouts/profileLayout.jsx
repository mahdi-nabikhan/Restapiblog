import React from 'react'
import { Outlet } from 'react-router-dom'

export default function profileLayout() {
  return (
    <>
    <main>
        <Outlet/>
    </main>
    
    </>
  )
}
