# LangChain Multi-Tool Calling

A simple LangChain project demonstrating how an LLM can decide which tool to call based on the user's request, execute the selected tool, and generate a final response.

## 🚀 Features

* LangChain tool calling
* Multiple tools
* Weather information using OpenWeather API
* Random inspirational quotes
* Automatic tool selection by the LLM
* Tool execution using `invoke()`
* Returning tool results using `ToolMessage`
* Final response generation using the LLM
* Groq LLM integration

## 🛠️ Technologies

* Python
* LangChain
* Groq
* OpenWeather API
* DummyJSON Quotes API
* python-dotenv

## 📂 Project Structure

```text
langchain-multi-tool-calling/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
└── .env
```

> `.env` is used only locally and should never be pushed to GitHub.

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/Shiva2355/Langchain-multi-tool-calling.git
```

Go into the project directory:

```bash
cd Langchain-multi-tool-calling
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
api_key=your_openweather_api_key
```

Do not commit `.env` to GitHub.

Add this to `.gitignore`:

```gitignore
.env
__pycache__/
*.pyc
```

## 🔧 Available Tools

### 1. Get Weather

The `get_weather` tool gets current weather information for a given location.

It returns:

* Location
* Temperature
* Feels-like temperature
* Weather condition
* Humidity
* Wind speed

Example user request:

```text
What is the weather in Kakinada?
```

The LLM can decide to call:

```text
get_weather
```

### 2. Get Quote

The `get_quote` tool retrieves a random inspirational quote.

Example user request:

```text
Give me an inspirational quote.
```

The LLM can decide to call:

```text
get_quote
```

## 🔄 How Tool Calling Works

The application follows this flow:

```text
User Request
     ↓
LLM
     ↓
Tool Selection
     ↓
Tool Call
     ↓
Python Function Execution
     ↓
ToolMessage
     ↓
LLM
     ↓
Final Response
```

For example:

```text
User:
What is the weather in Kakinada?

        ↓

LLM:
Call get_weather

        ↓

get_weather("Kakinada")

        ↓

ToolMessage:
Temperature: ...
Humidity: ...
Condition: ...

        ↓

LLM:

The current weather in Kakinada is ...
```

## 🧠 Core Code

Tools are registered with the model:

```python
model_bind = model.bind_tools([
    get_quote,
    get_weather
])
```

The LLM response is checked for tool calls:

```python
for tool_call in response.tool_calls:

    select_tool = tools[tool_call["name"]]

    result = select_tool.invoke(
        tool_call["args"]
    )
```

The tool result is converted into a `ToolMessage`:

```python
ToolMessage(
    content=str(result),
    tool_call_id=tool_call["id"]
)
```

Finally, the tool result is passed back to the LLM to generate the final response.

## ▶️ Run the Project

```bash
python app.py
```

## 🔒 Security

Never commit API keys or other secrets to GitHub.

Keep credentials inside `.env` and add `.env` to `.gitignore`.

## 📚 Learning Goals

This project is built to understand:

* LLM tool calling
* `bind_tools()`
* `tool_calls`
* Tool selection
* Tool execution
* `ToolMessage`
* Multi-tool workflow
