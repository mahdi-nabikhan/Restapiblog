# 🔐 Authentication

## Overview

This project uses **JSON Web Token (JWT)** for authentication and authorization. Instead of storing authentication tokens in the browser's Local Storage or Session Storage, JWT tokens are managed through **HTTP Cookies**, providing a more secure authentication mechanism.

The authentication system consists of two tokens:

* **Access Token**
* **Refresh Token**

The access token is used to authenticate protected API requests, while the refresh token is responsible for issuing new access tokens when the current one expires.

---

# Authentication Flow

```text
User Login
     │
     ▼
Server Generates JWT Tokens
     │
     ▼
Access Token + Refresh Token
     │
     ▼
Stored Securely in HTTP Cookies
     │
     ▼
Client Sends Cookies Automatically
     │
     ▼
Protected API Access
     │
     ▼
Access Token Expires
     │
     ▼
Refresh Token Generates New Access Token
```

---

# Why Cookies?

Instead of storing JWT tokens in Local Storage, this project stores authentication data inside **HTTP Cookies**.

Using cookies provides several advantages:

* Automatic transmission with every authenticated request.
* Better protection against JavaScript-based token theft.
* Easier session management.
* Cleaner frontend implementation.
* Improved security when configured with appropriate cookie attributes.

---

# Login Process

When the user successfully authenticates, the backend generates both an **Access Token** and a **Refresh Token**.

These tokens are stored inside HTTP cookies and are automatically included in future requests by the browser.

The frontend does not need to manually attach the JWT token to every request when cookie-based authentication is being used.

---

# Access Token

The Access Token is used to authorize requests to protected endpoints.

Characteristics:

* Short lifetime
* Used for authentication
* Sent automatically through cookies
* Can be regenerated using the Refresh Token

---

# Refresh Token

The Refresh Token has a longer lifetime than the Access Token.

Its only responsibility is generating a new Access Token after the previous one expires.

If the Refresh Token is no longer valid, the user must authenticate again.

---

# Logout

Logging out removes the authentication cookies from the client.

After logout:

* Access Token becomes unavailable.
* Refresh Token is removed.
* Protected endpoints are no longer accessible.
* The user must log in again.

---

# Protected Endpoints

Endpoints requiring authentication validate the JWT before processing the request.

If authentication fails, the server returns an appropriate HTTP error response.

Typical protected endpoints include:

* Profile
* Change Password
* Create Post
* Update Post
* Delete Post
* Upload Images
* Create Comment

---

# Token Refresh

When the Access Token expires, the client requests a new one using the Refresh Token.

If the Refresh Token is still valid, the server issues a new Access Token without requiring the user to log in again.

---

# Security Considerations

This authentication strategy is designed with security in mind.

Recommended production settings include:

* `HttpOnly` cookies
* `Secure` cookies
* `SameSite=Lax` or `SameSite=Strict`
* HTTPS in production
* Short-lived Access Tokens
* Longer-lived Refresh Tokens

---

# Authentication Lifecycle

```text
Login
   │
   ▼
Receive JWT Tokens
   │
   ▼
Store Tokens in Cookies
   │
   ▼
Access Protected APIs
   │
   ▼
Access Token Expired
   │
   ▼
Refresh Access Token
   │
   ▼
Continue Using API
   │
   ▼
Logout
   │
   ▼
Delete Authentication Cookies
```

---

# Advantages

* JWT-based authentication
* Cookie-based token storage
* Stateless authentication
* Secure session management
* Automatic authentication on requests
* Refresh token support
* Production-ready authentication workflow
