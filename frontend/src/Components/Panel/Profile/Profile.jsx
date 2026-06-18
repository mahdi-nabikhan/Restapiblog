import React, { useEffect, useState } from "react";
import "./Profile.css";
import BACKEND_URL from "../../../Utils";

export default function Profile() {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

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
          <button className="profile__btn">
            Edit Profile
          </button>
        </div>
      </div>
    </div>
  );
}