import React, { useState } from "react";
import "./ProfileUpdate.css";

export default function ProfileUpdate() {
  const [profile, setProfile] = useState({
    first_name: "",
    last_name: "",
    description: "",
  });

  const [image, setImage] = useState(null);

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const changeHandler = (event) => {
    setProfile({
      ...profile,
      [event.target.name]: event.target.value,
    });
  };

  const imageHandler = (event) => {
    setImage(event.target.files[0]);
  };

  const submitHandler = async (event) => {
    event.preventDefault();

    try {
      setLoading(true);
      setMessage("");

      const formData = new FormData();

      formData.append(
        "first_name",
        profile.first_name
      );

      formData.append(
        "last_name",
        profile.last_name
      );

      formData.append(
        "description",
        profile.description
      );

      if (image) {
        formData.append("image", image);
      }

      const res = await fetch(
        "http://localhost:8000/accounts/api/v1/profile/detail/",
        {
          method: "PUT",
          credentials: "include",
          body: formData,
        }
      );

      const data = await res.json();

      if (!res.ok) {
        throw new Error(
          data.message ||
            "Failed to update profile"
        );
      }

      setMessage(
        "Profile updated successfully ✅"
      );

      console.log(data);
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="profile-edit">
      <div className="profile-edit__card">
        <div className="profile-edit__header">
          <h2>Edit Profile</h2>
          <p>
            Update your profile information
          </p>
        </div>

        <form
          onSubmit={submitHandler}
          className="profile-edit__form"
        >
          <div className="profile-edit__image-box">
            <label>
              Profile Image
            </label>

            <input
              type="file"
              accept="image/*"
              onChange={imageHandler}
            />
          </div>

          <div className="profile-edit__row">
            <div className="profile-edit__group">
              <label>
                First Name
              </label>

              <input
                type="text"
                name="first_name"
                value={
                  profile.first_name
                }
                onChange={
                  changeHandler
                }
                placeholder="Enter first name"
              />
            </div>

            <div className="profile-edit__group">
              <label>
                Last Name
              </label>

              <input
                type="text"
                name="last_name"
                value={
                  profile.last_name
                }
                onChange={
                  changeHandler
                }
                placeholder="Enter last name"
              />
            </div>
          </div>

          <div className="profile-edit__group">
            <label>
              Description
            </label>

            <textarea
              rows="6"
              name="description"
              value={
                profile.description
              }
              onChange={
                changeHandler
              }
              placeholder="Write something about yourself..."
            />
          </div>

          {message && (
            <div className="profile-edit__message">
              {message}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="profile-edit__btn"
          >
            {loading
              ? "Saving..."
              : "Save Changes"}
          </button>
        </form>
      </div>
    </div>
  );
}