import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./RegisterForm.css";
import BACKEND_URL from "../../../Utils";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";


const registerUser = async (data) => {
  const res = await fetch(
    `${BACKEND_URL}/accounts/api/v1/register/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    credentials: 'include',
    body: JSON.stringify({
      email: data.email,
      passwod: data.password,
      password2: data.confirmPassword

    })
  }

  )
  if (!res.ok) {
    throw new Error('register failed')
  }
  return res.json()





}


export default function RegisterForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate();

  const submitHandler = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    // validation
    if (!email || !password || !confirmPassword) {
      setError("All fields are required.");
      return;
    }

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      setLoading(true);

      const res = await fetch(
        `${BACKEND_URL}/accounts/api/v1/register/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email,
            password,
            password2: confirmPassword,
          }),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data?.detail || "Registration failed");
      }

      setSuccess("Account created successfully 🎉");
      setTimeout(() => {
        navigate("/");
      }, 5000);


      setEmail("");
      setPassword("");
      setConfirmPassword("");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-container">
      <form className="register-card" onSubmit={submitHandler}>
        <h2>Create Account</h2>

        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}

        <label>Email</label>
        <input
          type="email"
          value={email}
          placeholder="Enter email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <label>Password</label>
        <input
          type="password"
          value={password}
          placeholder="Enter password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <label>Confirm Password</label>
        <input
          type="password"
          value={confirmPassword}
          placeholder="Confirm password"
          onChange={(e) => setConfirmPassword(e.target.value)}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Creating..." : "Register"}
        </button>
      </form>
    </div>
  );
}