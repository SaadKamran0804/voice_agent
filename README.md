You can copy and paste the markdown below directly into your repository:


# Project Setup Guide

Welcome to the project! This guide will walk you through setting up both the backend and frontend environments. Follow the steps below to get everything running smoothly on your local machine.

## Prerequisites

Before starting the backend setup, you need to install `uv`, which is an extremely fast Python package installer and resolver. 

Open your terminal and run the following command to install it:

```bash
pip install uv
```

---

## Setup Backend

The backend is powered by Python. We use `uv` to manage our dependencies and run our agent scripts efficiently.

**1. Navigate to the backend folder** First, move into the backend directory of the project:

```bash
cd ./backend

```

**2. Sync dependencies** Install and synchronize all the required Python packages for the backend:

```bash
uv sync

```

**3. Download necessary files** Before running the agent, you need to download the required initial files or models:

```bash
uv src/agent.py download-files

```

**4. Run the agent in Console Mode** If you want to interact with or test the agent directly in your terminal, run:

```bash
uv src/agent.py console

```

**5. Run the Dev Server** To start the backend development server (usually needed so the frontend can communicate with it), run:

```bash
uv src/agent.py dev

```

---

## Setup Frontend

The frontend is the user interface of the application. You will need Node.js installed on your computer to run these commands.

**1. Navigate to the frontend folder** Open a *new* terminal window (so your backend keeps running) and move into the frontend directory:

```bash
cd ./frontend

```

**2. Install dependencies** Install all the required packages for the frontend to work. You can use either `npm` or `pnpm` depending on your preference:

```bash
npm install
# OR
pnpm install

```

**3. Start the frontend development server** Once the installation is complete, start up the frontend server:

```bash
npm run dev
# OR
pnpm run dev

```
