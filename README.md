# Workspaces API 🗂️

A small, friendly **Flask REST API** for managing users — the kind of clean little
CRUD backend you actually enjoy reading. It ships with an in-memory store, real
input validation, consistent JSON errors, and a tidy test suite. No frameworks
piled on top of frameworks. Just Flask, doing an honest day's work.

> Think of it as a starter kit with its life together: small enough to grok in one
> sitting, solid enough to build on.

---

## ✨ What's inside

- **Full CRUD** for users — create, read, update, delete.
- **Real validation** — email sanity checks, empty-name guards, and duplicate-email
  protection (no two Alices sharing an inbox).
- **Consistent JSON errors** — every failure comes back as `{"error": "..."}` with a
  sensible HTTP status (`400`, `404`, `405`, `409`).
- **Zero-config startup** — runs on port `5000` out of the box, or read `HOST` /
  `PORT` / `FLASK_DEBUG` from the environment.
- **A proper test suite** — 18 pytest cases covering the happy paths *and* the sad ones.
- **Docker-ready** — a slim `Dockerfile` for when you want to ship it.

---

## 🧑‍🍳 The endpoints

| Method   | Path              | What it does                        |
| -------- | ----------------- | ----------------------------------- |
| `GET`    | `/`               | Friendly index listing every route  |
| `GET`    | `/health`         | Health check + current user count   |
| `GET`    | `/users`          | List all users                      |
| `GET`    | `/users/<id>`     | Fetch one user                      |
| `POST`   | `/users`          | Create a user                       |
| `PUT`    | `/users/<id>`     | Update a user (full or partial)     |
| `DELETE` | `/users/<id>`     | Delete a user                       |

---

## 🚀 Getting started (from absolute zero)

You'll need **Python 3.10+**. That's it. Let's roll.

### 1. Grab the code

```bash
git clone https://github.com/waleedsworld/workspaces.git
cd workspaces
```

### 2. Make a cozy virtual environment

A virtual environment keeps this project's packages from crashing the party in your
other projects. Highly recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
```

### 3. Install the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run it!

```bash
python app.py
```

You should see Flask boot up on **http://localhost:5000**. Open it in your browser —
the index page will greet you and list every endpoint. 🎉

Prefer a different port? No problem:

```bash
PORT=8080 python app.py
```

(See [`.env.example`](.env.example) for all the knobs you can turn.)

---

## 🕹️ Taking it for a spin

Once it's running, poke at it with `curl`:

```bash
# Say hello
curl http://localhost:5000/health
# → {"status": "healthy", "user_count": 2}

# List everyone
curl http://localhost:5000/users

# Add someone new
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie", "email": "charlie@example.com"}'
# → {"id": 3, "name": "Charlie", "email": "charlie@example.com"}

# Update them
curl -X PUT http://localhost:5000/users/3 \
  -H "Content-Type: application/json" \
  -d '{"name": "Charlie B."}'

# And... goodbye
curl -X DELETE http://localhost:5000/users/3
# → {"message": "User deleted successfully"}
```

The API pushes back when you feed it nonsense, exactly as it should:

```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Oops", "email": "not-an-email"}'
# → 400 {"error": "A valid email is required"}

curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Copycat", "email": "alice@example.com"}'
# → 409 {"error": "Email is already in use"}
```

---

## 🧪 Running the tests

The test suite is the project's safety net — run it any time you change something.

```bash
pip install -r requirements.txt   # pytest is already in there
pytest -q
```

You should see a satisfying row of green dots and `18 passed`. If a dot turns into an
`F`, pytest will tell you exactly which case complained and why.

---

## 🐳 Running with Docker

Don't want to touch your local Python at all? Ship it in a container:

```bash
docker build -t workspaces-api .
docker run -p 5000:5000 workspaces-api
```

Then hit `http://localhost:5000` just like before.

---

## 🧭 Project layout

```
workspaces/
├── app.py               # The whole API — routes, validation, error handlers
├── test_app.py          # 18 pytest cases
├── requirements.txt     # Flask + pytest
├── Dockerfile           # Slim container image
├── .env.example         # Optional HOST / PORT / FLASK_DEBUG config
└── .devcontainer/       # VS Code dev container setup
```

---

## 🛠️ Where to take it next

This is a launchpad, not a landing pad. A few natural next steps:

- Swap the in-memory list for a real database (SQLite or Postgres + SQLAlchemy).
- Add pagination and filtering to `GET /users`.
- Bolt on authentication (API keys or JWTs).
- Wire up CI so the tests run on every push.

---

## 🌐 Live demo

Deploying soon — check back for a hosted link.

---

## 📄 License

Free to use, learn from, and build on. Go make something. 🚀
