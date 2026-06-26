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
      password: data.password,
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
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const { register, handleSubmit, formState: { errors }, } = useForm();
  const mutaions = useMutation({
    mutationFn: registerUser,
    onSuccess: () => {

      setSuccess("Register successful 🎉 Welcome");

      setTimeout(() => {
        navigate("/");
      }, 3000);
    },
    onError: (error) => {
      setError(error.message)

    }
  })




  const submitHandler = (data) => {

    setError("");
    setSuccess("");
    if (!data.email || !data.password || !data.confirmPassword) {
      setError("All fields are required.");
      return;
    }

    if (data.password !== data.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }


    mutaions.mutate(data)


  };

  return (
    <div className="register-container">
      <form className="register-card" onSubmit={handleSubmit(submitHandler)}>
        <h2>Create Account</h2>

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
          placeholder="Enter your Password"
          {...register("password", {
            required: "Password is required",
          })}
        />
        {errors.password && (
          <p className="error">
            {errors.password.message}
          </p>
        )}
        <label>Confirm Password</label>
        <input
          type="password"
          placeholder="Confirm your Password"
          {...register("confirmPassword", {
            required: "Confirm Password is required",
          })}
        />
        {errors.confirmPassword && (
          <p className="errors">{errors.confirmPassword.message}</p>
        )}
        <button type="submit" disabled={mutaions.isPending}>
          {mutaions.isPending ? "Creating..." : "Register"}
        </button>
      </form>
    </div>
  );
}