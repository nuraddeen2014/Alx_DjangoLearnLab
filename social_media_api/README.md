# Social Media API — Usage Guide 📘

This document explains how to authenticate and interact with the Posts and Comments endpoints in this project.

---

## 🔐 Authentication

- **Register**
  - Endpoint: `POST /api/register/`
  - Body (JSON):

```json
{
  "username": "your_username",
  "password": "your_password",
  "email": "you@example.com"
}
```

- **Login**
  - Endpoint: `POST /api/login/`
  - Body (JSON):

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

- On success you will receive an authentication **token** (check response body or headers depending on your auth implementation).

**Use the token in requests:**

- Add the header `Authorization: Token <your_token>` to authenticated requests.

> ⚠️ Always prefix the token with the word `Token` and a space (example: `Authorization: Token abc123...`).

---

## Posts ✍️

Base endpoint: `/api/posts/`

- **List posts**
  - `GET /api/posts/` — returns all posts.

- **Retrieve single post**
  - `GET /api/posts/{id}/` — returns a single post. Responses include **post fields** (id, author, title, content, created/updated timestamps) and may include nested comments if configured.

- **Create post** (authenticated)
  - `POST /api/posts/`
  - Body (JSON):

```json
{
  "title": "My first post",
  "content": "Hello world"
}
```
- `author` is set automatically from the authenticated user (do not send it in the request).

- **Update / Partial update** (author-only)
  - `PUT /api/posts/{id}/` or `PATCH /api/posts/{id}/` — only the post author can update the post (you will get `403 Forbidden` otherwise).

- **Delete** (author-only)
  - `DELETE /api/posts/{id}/` — only the post author can delete it.

Example cURL to create a post:

```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello","content":"My post content"}'
```

---

## Comments 💬

Base endpoint: `/api/comments/`

- **List comments**
  - `GET /api/comments/` — returns all comments.
  - You can request only comments for a specific post by filtering client-side on the `post` field, or implement server-side filters (e.g. `?post=<post_id>`) if added.

- **Create comment** (authenticated)
  - `POST /api/comments/`
  - Body (JSON):

```json
{
  "post": 1,
  "content": "Nice post!"
}
```

- `author` is set automatically from the authenticated user (do not send it in the request).

- **Update / Delete** (author-only)
  - `PUT/PATCH /api/comments/{id}/` and `DELETE /api/comments/{id}/` — only the comment author may update or delete their comment.

Example cURL to create a comment:

```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Token <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"post": 1, "content": "Great post!"}'
```

---

## Permissions & behavior 🔒

- Views use token/session authentication; add `Authorization: Token <token>` for authenticated requests.
- The project includes an object-level permission that **allows only the author** of a post/comment to update or delete it. Unauthenticated users can only access read endpoints (depending on global settings).

> Tip: if posts aren't showing nested comments, you can either:
> - Call the comments endpoint and filter by `post` id client-side, or
> - Add a `related_name` to the `Comment.post` FK and expose a nested field in `PostSerializer`.

---

## Quick testing checklist ✅

- Register a user and obtain a token.
- Create a post using that token.
- Create a comment on that post using the same token.
- Attempt to update/delete the post/comment as a different user (should return `403`).
- Verify that requests without authentication are limited to read-only (unless global settings differ).

---

If you'd like, I can add a short section with example responses or add server-side filtering for comments by post (e.g., `?post=<id>`).