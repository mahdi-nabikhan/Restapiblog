# 📡 API Documentation

Base URL

```text
http://localhost:8000/api/v1/
```

Authentication

Endpoints that require authentication must include:

```http
Authorization: Bearer <access_token>
```

---

# 🔐 Authentication APIs

---

## Register

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/register/` |
| Authentication | ❌ |
| Content-Type | application/json |

### Request

```json
{
    "email": "user@test.com",
    "password": "12345678",
    "password2": "12345678"
}
```

### Success Response

```json
{
    "message": "Activation email sent."
}
```

---

## Send Registration Token

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/token/register/` |
| Authentication | ❌ |

---

## Login (Token Authentication)

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/token/login/` |
| Authentication | ❌ |

### Response

```json
{
    "token": "xxxxxxxxxxxxxxxxxxxx"
}
```

---

## Custom Token Login

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/custom/token/login` |
| Authentication | ❌ |

---

## Logout (Token)

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/discard/token/` |
| Authentication | ✅ |

---

## JWT Login

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/jwt/create/` |
| Authentication | ❌ |

### Request

```json
{
    "email": "user@test.com",
    "password": "12345678"
}
```

### Response

```json
{
    "refresh": "...",
    "access": "..."
}
```

---

## Refresh JWT

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/jwt/refresh/` |
| Authentication | ❌ |

---

## Verify JWT

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/jwt/verify/` |
| Authentication | ❌ |

---

## Custom JWT Login

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/jwt/custom/` |
| Authentication | ❌ |

---

## Logout JWT

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/jwt/custom/delete` |
| Authentication | ✅ |

---

## Change Password

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/change/password` |
| Authentication | ✅ |

---

## Send Email

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/send/email/` |
| Authentication | ✅ |

---

## Send Template Email

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/send-template-email/` |
| Authentication | ✅ |

---

## Confirm Account Activation

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/accounts/activation/confirm/<token>/` |
| Authentication | ❌ |

---

## Resend Activation Email

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/accounts/activation/resend/` |
| Authentication | ❌ |

---

## Current User

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/accounts/me/` |
| Authentication | ✅ |

---

## User Profile

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/accounts/profile/` |
| Authentication | ✅ |

---

## Profile Detail

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/accounts/profile/detail/` |
| Authentication | ✅ |

---

# 📝 Post APIs

---

## List Posts

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/posts/post/` |
| Authentication | ❌ |

---

## Create Post

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/posts/post/` |
| Authentication | ✅ |

---

## Retrieve Post

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/posts/post/{id}/` |
| Authentication | ❌ |

---

## Update Post

| Property | Value |
|----------|-------|
| Method | PUT |
| Endpoint | `/posts/post/{id}/` |
| Authentication | ✅ |

---

## Partial Update Post

| Property | Value |
|----------|-------|
| Method | PATCH |
| Endpoint | `/posts/post/{id}/` |
| Authentication | ✅ |

---

## Delete Post

| Property | Value |
|----------|-------|
| Method | DELETE |
| Endpoint | `/posts/post/{id}/` |
| Authentication | ✅ |

---

# ViewSet Endpoints

---

## List Posts

| Method | GET |
|---------|-----|
| Endpoint | `/posts/posts/` |

---

## Create Post

| Method | POST |
|---------|------|
| Endpoint | `/posts/posts/` |

---

## Retrieve Post

| Method | GET |
|---------|-----|
| Endpoint | `/posts/posts/{id}/` |

---

## Update Post

| Method | PUT |
|---------|-----|
| Endpoint | `/posts/posts/{id}/` |

---

## Partial Update

| Method | PATCH |
|---------|-------|
| Endpoint | `/posts/posts/{id}/` |

---

## Delete Post

| Method | DELETE |
|---------|--------|
| Endpoint | `/posts/posts/{id}/` |

---

## User Posts

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/posts/user/post/` |
| Authentication | ✅ |

---

## Cached Posts

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/posts/post/list/cache/` |
| Authentication | ❌ |

---

# 💬 Comment APIs

---

## List Comments

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/posts/comments/{post_id}/` |
| Authentication | ❌ |

---

## Create Comment

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/posts/comments/{post_id}/` |
| Authentication | ✅ |

---

## Retrieve Comment

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/posts/comment/detail/{id}/` |
| Authentication | ❌ |

---

## Update Comment

| Property | Value |
|----------|-------|
| Method | PUT |
| Endpoint | `/posts/comment/detail/{id}/` |
| Authentication | ✅ |

---

## Delete Comment

| Property | Value |
|----------|-------|
| Method | DELETE |
| Endpoint | `/posts/comment/detail/{id}/` |
| Authentication | ✅ |

---

# 🖼 Image APIs

---

## Upload Post Image

| Property | Value |
|----------|-------|
| Method | POST |
| Endpoint | `/posts/img/post/{post_id}/` |
| Authentication | ✅ |
| Content-Type | multipart/form-data |

### Body

| Field | Type |
|-------|------|
| image | File |

---

## List Post Images

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/posts/img/post/{post_id}/` |
| Authentication | ❌ |

---

# 🔍 Search API

---

## Search Posts

| Property | Value |
|----------|-------|
| Method | GET |
| Endpoint | `/posts/search/?q=<keyword>` |
| Authentication | ❌ |

### Example

```http
GET /api/v1/posts/search/?q=django
```

### Response

```json
[
    {
        "id": 1,
        "title": "Learning Django"
    }
]
```

Powered by **Elasticsearch Full-Text Search** with fuzzy matching.

---

# 📑 HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Internal Server Error |

---

# 🔒 Authentication Summary

| Endpoint Type | Authentication |
|---------------|----------------|
| Register | ❌ |
| Login | ❌ |
| Refresh Token | ❌ |
| Verify Token | ❌ |
| Activation | ❌ |
| Posts (Create/Update/Delete) | ✅ |
| Comments (Create/Delete) | ✅ |
| Profile | ✅ |
| Upload Images | ✅ |
| Search | ❌ |

---

# 📌 Notes

- All request and response bodies use **JSON**, except file upload endpoints which require **multipart/form-data**.
- JWT authentication is the recommended authentication mechanism.
- Search functionality is powered by **Elasticsearch**.
- Pagination is available on list endpoints where configured.
- Protected endpoints require a valid `Authorization: Bearer <access_token>` header.