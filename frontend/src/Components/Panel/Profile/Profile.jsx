import React, { useEffect, useState } from "react";
import "./Profile.css";
import BACKEND_URL from "../../../Utils";
import { Link } from 'react-router-dom'
import { useMutation } from "@tanstack/react-query";
import {
  useQuery,
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);import React, { useEffect, useState } from "react";
import "./Profile.css";
import BACKEND_URL from "../../../Utils";
import { Link } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  // Modal
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Message
  const [passwordMessage, setPasswordMessage] = useState("");

  // Password Form
  const [passwordData, setPasswordData] = useState({
    old_password: "",
    new_password: "",
    new_password1: "",
  });

  // ============================
  // GET PROFILE
  // ============================

  const getProfile = async () => {
    try {
      const res = await fetch(
        `${BACKEND_URL}/accounts/api/v1/profile/detail/`,
        {
          credentials: "include",
        }
      );

      if (!res.ok) {
        throw new Error("Failed to fetch profile");
      }

      const data = await res.json();

      setProfile(data);
    } catch (err) {
      console.log(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getProfile();
  }, []);

  // ============================
  // CHANGE PASSWORD
  // ============================

  const changePasswordMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(
        `${BACKEND_URL}/accounts/api/v1/change/password`,
        {
          method: "PUT",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(passwordData),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data.password?.join(" ") ||
            data.old_password ||
            data["old password"] ||
            "Failed to change password"
        );
      }

      return data;
    },

    onSuccess: (data) => {
      setPasswordMessage(
        data.message || data.massage || "Password changed successfully."
      );

      setPasswordData({
        old_password: "",
        new_password: "",
        new_password1: "",
      });

      setTimeout(() => {
        setPasswordMessage("");
        setIsModalOpen(false);
      }, 1500);
    },

    onError: (err) => {
      setPasswordMessage(err.message);
    },
  });

  // ============================
  // HANDLERS
  // ============================

  const handlePasswordChange = (e) => {
    setPasswordData({
      ...passwordData,
      [e.target.name]: e.target.value,
    });
  };

  const closeModal = () => {
    setIsModalOpen(false);

    setPasswordData({
      old_password: "",
      new_password: "",
      new_password1: "",
    });

    setPasswordMessage("");
  };

  const submitPassword = () => {
    if (
      passwordData.new_password !==
      passwordData.new_password1
    ) {
      setPasswordMessage("Passwords do not match.");
      return;
    }

    changePasswordMutation.mutate();
  };

  // ============================
  // LOADING
  // ============================

  if (loading) {
    return <h2>Loading...</h2>;
  }

  // ============================
  // UI
  // ============================

  return (
    <div className="profile">
      <div className="profile__card">
        <div className="profile__header">
          <img
            src={
              profile.image
                ? `http://localhost:8000${profile.image}`
                : "/default-avatar.png"
            }
            alt="Profile"
            className="profile__avatar"
          />

          <div>
            <h2>
              {profile.first_name} {profile.last_name}
            </h2>

            <p>
              {profile.description ||
                "No description yet"}
            </p>
          </div>
        </div>

        <div className="profile__footer">
          <Link to="panel/profile/edit">
            Edit Your Profile
          </Link>

          <button
            className="change-password-btn"
            onClick={() => {
              setPasswordMessage("");
              setIsModalOpen(true);
            }}
          >
            Change Password
          </button>
        </div>
      </div>

      {/* ============================
            MODAL
      ============================ */}

      {isModalOpen && (
        <div
          className="modal-overlay"
          onClick={closeModal}
        >
          <div
            className="password-modal"
            onClick={(e) => e.stopPropagation()}
          >
            <h2>Change Password</h2>

            <input
              type="password"
              name="old_password"
              placeholder="Current Password"
              value={passwordData.old_password}
              onChange={handlePasswordChange}
            />

            <input
              type="password"
              name="new_password"
              placeholder="New Password"
              value={passwordData.new_password}
              onChange={handlePasswordChange}
            />

            <input
              type="password"
              name="new_password1"
              placeholder="Confirm New Password"
              value={passwordData.new_password1}
              onChange={handlePasswordChange}
            />

            {passwordMessage && (
              <p
                style={{
                  color: "crimson",
                  marginTop: "10px",
                }}
              >
                {passwordMessage}
              </p>
            )}

            <div className="modal-buttons">
              <button onClick={closeModal}>
                Cancel
              </button>

              <button
                onClick={submitPassword}
                disabled={
                  changePasswordMutation.isPending
                }
              >
                {changePasswordMutation.isPending
                  ? "Changing..."
                  : "Change Password"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
  const [passwordMessage, setPasswordMessage] = useState("");

  const changePasswordMutation = useMutation({
    mutationFn: async () => {
      const res = await fetch(
        `${BACKEND_URL}/accounts/api/v1/change/password`,
        {
          method: "PUT",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(passwordData),
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data.password ||
          data["old password"] ||
          "Failed to change password"
        );
      }

      return data;
    },

    onSuccess: (data) => {
      setPasswordMessage(data.massage);

      setPasswordData({
        old_password: "",
        new_password: "",
        new_password1: "",
      });

      setIsModalOpen(false);
    },

    onError: (err) => {
      setPasswordMessage(err.message);
    },
  });

  const [passwordData, setPasswordData] = useState({
    current_password: "",
    new_password: "",
    confirm_password: "",
  });
  const handlePasswordChange = (e) => {
    setPasswordData({
      ...passwordData,
      [e.target.name]: e.target.value,
    });
  };
  const getProfile = async () => {
    try {
      const res = await fetch(
        `${BACKEND_URL}/accounts/api/v1/profile/detail/`,
        {
          credentials: "include",
        }
      );

      if (!res.ok) {
        throw new Error("Failed to fetch profile");
      }

      const data = await res.json();

      setProfile(data);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getProfile();
  }, []);

  if (loading) {
    return <h2>Loading...</h2>;
  }

  return (
    <div className="profile">
      <div className="profile__card">
        <div className="profile__header">
          <img
            src={
              profile.image
                ? `http://localhost:8000${profile.image}`
                : "/default-avatar.png"
            }
            alt="Profile"
            className="profile__avatar"
          />

          <div>
            <h2>
              {profile.first_name} {profile.last_name}
            </h2>

            <p>
              {profile.description ||
                "No description yet"}
            </p>
          </div>
        </div>

        <div className="profile__footer">
          <Link to={`panel/profile/edit`}>Edit Your Profile</Link>
          <div className="profile__footer">
            <button
              className="change-password-btn"
              onClick={() => setIsModalOpen(true)}
            >
              Change Password
            </button>
          </div>
        </div>
      </div>
      {isModalOpen && (
        <div
          className="modal-overlay"
          onClick={() => setIsModalOpen(false)}
        >
          <div
            className="password-modal"
            onClick={(e) => e.stopPropagation()}
          >
            <h2>Change Password</h2>

            <input
              type="password"
              name="current_password"
              placeholder="Current Password"
              value={passwordData.current_password}
              onChange={handlePasswordChange}
            />

            <input
              type="password"
              name="new_password"
              placeholder="New Password"
              value={passwordData.new_password}
              onChange={handlePasswordChange}
            />

            <input
              type="password"
              name="confirm_password"
              placeholder="Confirm New Password"
              value={passwordData.confirm_password}
              onChange={handlePasswordChange}
            />

            <div className="modal-buttons">
              <button onClick={() => setIsModalOpen(false)}>
                Cancel
              </button>

              <button
                disabled={changePasswordMutation.isPending}
                onClick={() => changePasswordMutation.mutate()}
              >
                {
                  changePasswordMutation.isPending
                    ? "Changing..."
                    : "Change Password"
                }
              </button>
              {
                passwordMessage &&
                <p>{passwordMessage}</p>
              }
            </div>
          </div>
        </div>
      )}
    </div>
  );
}