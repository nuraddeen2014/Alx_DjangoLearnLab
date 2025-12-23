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


## Follows & Feeds 🔁

The app exposes simple follow/unfollow endpoints (in `accounts.urls`) and a feed endpoint (in `posts.urls`). All endpoints are included under the project prefix `/api/` (see [social_media_api/urls.py](social_media_api/urls.py)).

- **Follow / Unfollow (actual routes)**
  - `POST /api/follow/<pk>/` — follow the user whose id is `<pk>`.
  - `DELETE /api/unfollow/<pk>/` — unfollow the user whose id is `<pk>`.

  - These routes are defined in [accounts/urls.py](accounts/urls.py#L1-L40) and implemented as function-based views in [accounts/views.py](accounts/views.py#L1-L200): `follow(request, pk)` and `unfollow(request, pk)`.

  - Authentication: both endpoints require authentication. Add header `Authorization: Token <your_token>`.

  - Example cURL — follow a user:

```bash
curl -X POST http://localhost:8000/api/follow/3/ \
  -H "Authorization: Token <your_token>"
```

  - Example cURL — unfollow a user:

```bash
curl -X DELETE http://localhost:8000/api/unfollow/3/ \
  -H "Authorization: Token <your_token>"
```

- **Feed endpoint (actual route)**
  - `GET /api/feeds/` — returns recent posts authored by users the authenticated user follows.
  - This route is defined in [posts/urls.py](posts/urls.py#L1-L50) and implemented by `FeedViewSet` in [posts/views.py](posts/views.py#L1-L200) which uses the authenticated user to filter posts.

  - Example cURL — get your feed:

```bash
curl -X GET http://localhost:8000/api/feeds/ \
  -H "Authorization: Token <your_token>"
```

- **Notes about the current implementation (important)**
  - `FeedViewSet.get_queryset()` filters posts using `user.following.all()` (i.e. authors the current user is following).
  - However, the `follow` and `unfollow` views in `accounts/views.py` currently call `request.user.followers.add(target_user)` and `request.user.followers.remove(target_user)`. That operation adds/removes the *target user* to the *authenticated user’s followers* set — which actually makes the target user follow the requester, not the other way around.

  - Recommended fix: change `follow`/`unfollow` to modify the `following` relationship of the requester, for example:

```python
# in accounts/views.py
request.user.following.add(target_user)    # follow
request.user.following.remove(target_user) # unfollow
```

  - Alternatively, perform the inverse operation on the target user to be explicit:

```python
# make the target user record that they have a new follower
target_user.followers.add(request.user)
# remove follower
target_user.followers.remove(request.user)
```

  - Without the fix, the feed may appear empty because `FeedViewSet` looks at `user.following`, which is not updated by the current `follow` implementation.

  - See the implementations here: [accounts/views.py#L1-L200](accounts/views.py#L1-L200) and [posts/views.py#L1-L200](posts/views.py#L1-L200).

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