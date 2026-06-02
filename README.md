# 🚀 NEXAURA

<div align="center">

### 🤖 AI-Powered Virtual Assistant Built with Python

Voice Commands • Automation • AI Responses • Productivity

</div>

---

## 📖 About Nexaura

**Nexaura** is an AI-powered virtual assistant developed in Python that combines voice recognition, automation, and conversational AI into a single system.

It listens to voice commands, understands user requests, performs tasks such as opening websites and applications, and generates intelligent responses using AI.

The project is designed to help users interact with their computers naturally through voice commands while also serving as a learning project for AI, automation, and Python development.

---

## ✨ Features

* 🎙️ Voice recognition and speech processing
* 🧠 AI-powered intelligent conversations
* 🌐 Open websites using voice commands
* 💻 Launch desktop applications
* 🔎 Perform internet searches
* 📅 Time and date utilities
* ⚡ Fast and lightweight architecture
* 🛠️ Modular and expandable design
* 📂 Beginner-friendly project structure

---

## 🎥 How It Works

```text
User Speaks
      │
      ▼
Speech Recognition
      │
      ▼
Command Processing
      │
      ▼
Task Execution / AI Response
      │
      ▼
Output to User
```

---

## 🧰 Technologies Used

### Programming Language

* Python

### Libraries

| Library             | Purpose                   |
| ------------------- | ------------------------- |
| speech_recognition  | Converts speech into text |
| google.generativeai | AI-generated responses    |
| webbrowser          | Opens websites            |
| datetime            | Date and time handling    |
| os                  | System operations         |
| re                  | Command processing        |

---

## 📁 Project Structure

```bash
NEXAURA/
│
├── main.py               # Main assistant program
├── requirements.txt      # Project dependencies
├── README.md             # Documentation
├── assets/               # Images, icons, resources
├── modules/              # Assistant modules
└── .gitignore
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Sam-Dev-161127/Nexaura.git
```

### 2️⃣ Navigate to the Project Folder

```bash
cd Nexaura
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 AI API Configuration

Nexaura supports multiple AI providers. Choose **any one** (or combine them) based on your preference.

---

### 🟦 Option 1 — Google Gemini API

Install the library:

```bash
pip install google-generativeai
```

Configure and use:

```python
import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-pro")

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# Example usage
reply = ask_gemini("What is artificial intelligence?")
print(reply)
```

> 🔗 Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

---

### 🟩 Option 2 — OpenAI API (ChatGPT)

Install the library:

```bash
pip install openai
```

Configure and use:

```python
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def ask_openai(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",  # or "gpt-3.5-turbo" for a faster, cheaper option
        messages=[
            {"role": "system", "content": "You are a helpful assistant named Nexaura."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Example usage
reply = ask_openai("What is artificial intelligence?")
print(reply)
```

> 🔗 Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

**Available Models:**

| Model         | Description                        |
| ------------- | ---------------------------------- |
| gpt-4o        | Most capable, multimodal           |
| gpt-4-turbo   | Fast and powerful                  |
| gpt-3.5-turbo | Lightweight and cost-effective     |

---

### 🟪 Option 3 — Anthropic Claude API

Install the library:

```bash
pip install anthropic
```

Configure and use:

```python
import anthropic

client = anthropic.Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")

def ask_claude(prompt):
    message = client.messages.create(
        model="claude-sonnet-4-5",  # or "claude-haiku-4-5" for faster responses
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

# Example usage
reply = ask_claude("What is artificial intelligence?")
print(reply)
```

> 🔗 Get your API key from [Anthropic Console](https://console.anthropic.com/)

**Available Models:**

| Model                | Description                        |
| -------------------- | ---------------------------------- |
| claude-opus-4-5      | Most powerful, best reasoning      |
| claude-sonnet-4-5    | Balanced speed and intelligence    |
| claude-haiku-4-5     | Fastest and most lightweight       |

---

### 🟥 Option 4 — DeepSeek API

Install the library:

```bash
pip install openai  # DeepSeek uses the OpenAI-compatible SDK
```

Configure and use:

```python
from openai import OpenAI

client = OpenAI(
    api_key="YOUR_DEEPSEEK_API_KEY",
    base_url="https://api.deepseek.com"
)

def ask_deepseek(prompt):
    response = client.chat.completions.create(
        model="deepseek-chat",  # or "deepseek-reasoner" for step-by-step reasoning
        messages=[
            {"role": "system", "content": "You are a helpful assistant named Nexaura."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Example usage
reply = ask_deepseek("What is artificial intelligence?")
print(reply)
```

> 🔗 Get your API key from [DeepSeek Platform](https://platform.deepseek.com/)

**Available Models:**

| Model               | Description                              |
| ------------------- | ---------------------------------------- |
| deepseek-chat       | General purpose, fast responses          |
| deepseek-reasoner   | Advanced step-by-step reasoning (R1)     |

---

### 🔀 Switching Between APIs in main.py

You can easily switch between providers with a simple config variable:

```python
# Set your preferred AI provider: "gemini", "openai", "claude", "deepseek"
AI_PROVIDER = "gemini"

def get_ai_response(prompt):
    if AI_PROVIDER == "gemini":
        return ask_gemini(prompt)
    elif AI_PROVIDER == "openai":
        return ask_openai(prompt)
    elif AI_PROVIDER == "claude":
        return ask_claude(prompt)
    elif AI_PROVIDER == "deepseek":
        return ask_deepseek(prompt)
    else:
        return "No AI provider configured."
```

This way, you only need to change one line to switch providers.

---

## ▶️ Running Nexaura

Start the assistant using:

```bash
python main.py
```

After launching, Nexaura will begin listening for voice commands.

---

## 🎤 Example Commands

| Command                 | Action                   |
| ----------------------- | ------------------------ |
| Open YouTube            | Opens YouTube            |
| Open Google             | Opens Google             |
| Open GitHub             | Opens GitHub             |
| Search Python tutorials | Performs a web search    |
| What is AI?             | Generates an AI response |
| Tell me the time        | Shows current time       |
| Tell me today's date    | Shows current date       |

---

## 🧠 How Nexaura Works

1. Nexaura listens for voice input.
2. Speech Recognition converts audio into text.
3. The command is cleaned and analyzed.
4. Appropriate actions are executed.
5. AI generates responses when needed.
6. Results are returned to the user.

---

## 🎯 Learning Objectives

This project demonstrates:

* 🤖 Artificial Intelligence Integration
* 🎙️ Speech Recognition
* ⚡ Automation Systems
* 💻 Human-Computer Interaction
* 🐍 Python Development
* 🔌 API Integration

---

## 🔮 Future Roadmap

Planned improvements include:

* 🎯 Higher voice recognition accuracy
* 🧠 Better conversational memory
* 🌤️ Weather information support
* 📧 Email automation
* 📁 File management commands
* 🖥️ Modern graphical user interface
* 🔊 Text-to-Speech responses
* 🤖 Custom AI agent capabilities

---

## 🤝 Contributing

Contributions, ideas, and suggestions are welcome.

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit your changes

```bash
git commit -m "Added new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Create a Pull Request

---

## 👨‍💻 Author

### Sameer Patra

🎓 Student
🐍 Python Developer
🤖 AI Enthusiast
🔧 Robotics Learner

---

## ⭐ Support

If you like this project, consider giving it a **Star ⭐** on GitHub.

It motivates further development and helps others discover the project.

---

## 📜 License

This project is licensed under the MIT License.