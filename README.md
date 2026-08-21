# AI English E-Learning Assistant

An intelligent multi-agent e-learning assistant designed to support students, instructors, and administrators within an e-learning platform. Built with **LangGraph**, **LangChain**, **Google Gemini**, and **ChromaDB**, the assistant combines tool calling, **Retrieval-Augmented Generation (RAG)**, short-term and long-term memory, and role-based permissions to provide personalized learning support, progress tracking, course assistance, and educational management capabilities.

---

## Features

- 🤖 Multi-agent architecture
- 📚 Retrieval-Augmented Generation (RAG)
- 🧠 Short-term conversation memory
- 💾 Long-term semantic memory
- 🔍 Intelligent tool routing
- 👨‍🎓 Student management
- 👩‍🏫 Instructor information
- 📖 Learning resources
- 🔐 Role-based access control
- 🔎 Fuzzy name matching

---

# Architecture

```
                    User
                      │
                      ▼
              History Agent
         (Long-Term Memory)
                      │
          ┌───────────┴───────────┐
          │                       │
  Retrieve Relevant History   Chat Summary
          │                       │
          └───────────┬───────────┘
                      ▼
             Conversation Context
                      │
                      ▼
                                          ┌─────────────────┐
                         │   Main Agent    │
                         └────────┬────────┘
                                  │
        ┌───────────────┬─────────┼──────────┬───────────────┐
        │               │         │          │               │
        ▼               ▼         ▼          ▼               │
 ┌────────────┐ ┌────────────┐ ┌──────────┐ ┌────────────┐  │
 │  Student   │ │  Learning  │ │Instructor│ │    RAG     │  │
 │   Tools    │ │   Tools    │ │   Tool   │ │            │  │
 └─────┬──────┘ └─────┬──────┘ └────┬─────┘ └─────┬──────┘  │
       │              │             │             │         │
       └──────────────┴─────────────┴─────────────┘         │
                              │                              │
                              ▼                              │
                    ┌─────────────────┐                      │
                    │ Response        │◄─────────────────────┘
                    │ Synthesis       │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Final Response  │
                    └─────────────────┘
                      │
                      ▼
      Save useful conversations to Memory
```

---

# Main Components

## 1. Main Agent

The Main Agent is responsible for answering user questions.

It can:

- Decide which tools to use.
- Combine multiple tool outputs.
- Use retrieved conversation history.
- Answer using RAG.
- Perform reasoning with the LLM.
- Enforce authorization rules.

---

## 2. History Agent

The History Agent provides context for the Main Agent.

It never answers the user's question directly.

Instead, it:

1. Searches semantic conversation history.
2. If nothing relevant is found, retrieves the chat summary.
3. Produces a concise context for the Main Agent.

This greatly reduces prompt size while preserving long-term memory.

---

# Memory

## Short-Term Memory

Implemented using **LangGraph InMemorySaver**.

Stores the current conversation thread.

Example:

```
User:
What is her email?

↓

Assistant knows "her" refers to Sarah Johnson.
```

---

## Long-Term Memory

Implemented using **ChromaDB**.

Each useful interaction is stored as:

```
User:
How is Barbara Smith doing?

Assistant:
Barbara Smith is currently in the A1 level...
```

When a similar question appears later, semantic search retrieves the relevant conversations.

Only useful conversations are stored.

Permission denials and failed requests are ignored.

---

# Retrieval-Augmented Generation (RAG)

The assistant uses RAG for educational content.

Pipeline:

```
Question
      │
      ▼
Vector Search
      │
Retrieve Top-k Documents
      │
      ▼
Gemini
      │
Human-like Answer
```

The retrieved documents are summarized before generating the final response.

---

# Available Tools

## Student Tools

- Search student
- Student profile
- Student progress
- Student summary
- Recommend next skill

---

## Learning Tools

- Number of enrolled students
- Course statistics
- Exam links

---

## Instructor Tool

Provides information about:

- Biography
- Contact information
- Teaching experience
- Social media

---

## RAG Tool

Retrieves relevant educational documents and summarizes them before returning the result.

---

# Tool Routing

The Main Agent automatically selects the appropriate tools.

Examples:

### Student Question

```
Show Barbara Smith's profile.
```

↓

Uses:

```
get_student_profile
```

---

### Learning Question

```
How many students are enrolled in B1?
```

↓

Uses:

```
num_of_enrolled_students
```

---

### Mixed Question

```
Compare Barbara's progress with the A1 curriculum.
```

↓

Uses:

```
get_student_course_progress
get_courses_stats_by_level
```

Then combines both outputs into a natural answer.

---

# Permissions

Two roles are supported.

## Student

Can only access their own profile.

Example:

```
Show Meriem's progress.
```

↓

Access denied.

---

```
What is my progress?
```

↓

Returns the authenticated student's information.

---

## Admin

Can access every student's information.

---

# Name Resolution

RapidFuzz is used for fuzzy matching.

Examples:

```
Barbra Smith
```

↓

Barbara Smith

---

```
Srah Johnson
```

↓

Sarah Johnson

This improves the user experience by handling spelling mistakes automatically.

---

# Conversation History

The assistant remembers previous conversations.

Example:

```
User:
Show Barbara Smith's profile.
```

Later:

```
User:
How is she doing?
```

The History Agent resolves that **"she"** refers to Barbara Smith.

---

# Technologies

- Python
- LangGraph
- LangChain
- Google Gemini
- ChromaDB
- RapidFuzz

---

# Project Highlights

- Multi-agent architecture
- Semantic long-term memory
- Retrieval-Augmented Generation
- Dynamic tool routing
- Permission-aware responses
- Context-aware conversations
- Fuzzy entity matching
- Modular and extensible design

---

# Future Improvements

- Persistent SQL conversation history
- Hybrid retrieval (BM25 + embeddings)
- User preference memory
- Multi-user authentication
- Streaming responses
- Web dashboard
- Conversation analytics
- Automatic memory summarization

---

# Example Workflow

```
User
 │
 ▼
"What should she focus on?"
 │
 ▼
History Agent
 │
 ▼
Retrieve Barbara Smith
 │
 ▼
Main Agent
 │
 ├── get_student_progress()
 ├── recommend_next_skill()
 │
 ▼
LLM combines both outputs
 │
 ▼
Final Answer
 │
 ▼
Save conversation if useful
```
# Run the project
### 1. Download the repo
```bash
git clone https://github.com/Akchiche-Mohamed-Aymen/e-learning-chat-agent.git
```
### 2. Go to the folder
```bash 
cd e-learning-chat-agent 
```
### 3. Install libraries
```bash 
pip install -r requirements.txt
```
### 4. Create the vector database 
```python
py embed_knowledge.py
```
### 5. Start the agent
```python
py main.py
```

## 📬 Contact Me

If you have any questions, suggestions, or would like to discuss this project, feel free to contact me.

* **LinkedIn:** [akchiche_mohamed_aymen](https://www.linkedin.com/in/mohamed-aymen-akchiche-b9b0b7303/)
* **Email:** [akchiche.mohamedaymen@gmail.com](mailto:akchiche.mohamedaymen@gmail.com)



