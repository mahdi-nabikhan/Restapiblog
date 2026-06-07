import React from 'react'
import './Navbar.css'

export default function Navbar() {
    return (
        <div>

            <nav className="navbar">
                <div className="navbar__logo">
                    <h2>MyBlog</h2>
                </div>

                <ul className="navbar__links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/posts">Posts</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                </ul>

                <div className="navbar__auth">
                    <button className="btn btn-login">Login</button>
                    <button className="btn btn-register">Register</button>
                </div>
            </nav>
        </div>
    )
}
