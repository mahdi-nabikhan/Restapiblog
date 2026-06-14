import React, { createContext, useEffect, useState } from "react";

export const AuthContext = createContext();

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const getMe = async () => {
    try {
      const res = await fetch(
        "http://localhost:8000/accounts/api/v1/me/",
        {
          credentials: "include",
        }
      );

      if (!res.ok) {
        setUser(null);
        return;
      }

      const data = await res.json();
      setUser(data);
    } catch (err) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let ignore = false;

    const run = async () => {
      try {
        const res = await fetch(
          "http://localhost:8000/accounts/api/v1/me/",
          {
            credentials: "include",
          }
        );

        if (!res.ok) {
          if (!ignore) {
            setUser(null);
            setLoading(false);
          }
          return;
        }

        const data = await res.json();

        if (!ignore) {
          setUser(data);
          setLoading(false);
        }
      } catch (err) {
        if (!ignore) {
          setUser(null);
          setLoading(false);
        }
      }
    };

    run();

    return () => {
      ignore = true;
    };
  }, []);

  const logout = async () => {
    try {
      await fetch(
        "http://localhost:8000/accounts/api/v1/logout/",
        {
          method: "POST",
          credentials: "include",
        }
      );
    } catch (e) {}

    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isLoggedIn: !!user,
        logout,
        refreshAuth: getMe,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}