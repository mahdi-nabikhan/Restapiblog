import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "./LoginForm.css";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import BACKEND_URL from '../../../Utils'
const loginUser = async (data) => {
  const res = await fetch(
    `${BACKEND_URL}/accounts/api/v1/jwt/custom/`,
    {
      method: 'POST',
      credentials: 'include',
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: data.email,
        password: data.password
      }

      )
    }
  )
  if (!res.ok) {
    throw new Error('login failed')
  }
  return await res.json()




};


export default function LoginForm() {

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();


  const mutation = useMutation({
    mutationFn: loginUser,

    onSuccess: () => {
      setSuccess("Login successful 🎉 Welcome back!");

      setTimeout(() => {
        navigate("/");
      }, 3000);
    },

    onError: (error) => {
      setError(error.message);
    },
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const navigate = useNavigate();

  const submitHandler = (data) => {
    setError('')
    setSuccess('')
    mutation.mutate(data)

  };

  return (
    <div className="login-container">
      <form className="login-card" onSubmit={handleSubmit(submitHandler)}>
        <h2 className="title">Welcome Back</h2>

        {error && <div className="error">{error}</div>}

        {success && <div className="success">{success}</div>}

        <label>Email</label>
        <input
          type="email"
          placeholder="Enter your email"
          {...register("email", {
            required: "Email is required",
          })}
        />
        {errors.email && (
          <p className="error">
            {errors.email.message}
          </p>
        )}

        <label>Password</label>
        <input
          type="password"
          placeholder="Enter your password"
          {...register("password", {
            required: "password is required",
          })}
        />
        {errors.password && (
          <p className="error">
            {errors.password.message}
          </p>
        )}

        <button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
}