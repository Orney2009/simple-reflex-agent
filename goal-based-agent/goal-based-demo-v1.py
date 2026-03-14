import os
import re
from typing import Any

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)

application_info = {
    "name": None,
    "email": None,
    "skills": None,
}


def extract_application_info(text: str) -> str:
    name_pattern = (
        r"(?:my name is|i am)\s+"
        r"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"
    )
    skills_pattern = r"(?:skills are|i know|i can use)\s+(.+)"

    name_match = re.search(name_pattern, text, re.IGNORECASE)
    email_match = re.search(r"\b[\w.-]+@[\w.-]+\.\w+\b", text)
    skills_match = re.search(skills_pattern, text, re.IGNORECASE)

    response = []

    if name_match and not application_info["name"]:
        application_info["name"] = name_match.group(1).title()
        response.append("✅ Name saved.")

    if email_match and not application_info["email"]:
        application_info["email"] = email_match.group(0)
        response.append("✅ Email saved.")
    if skills_match and not application_info["skills"]:
        application_info["skills"] = skills_match.group(1).strip()
        response.append("✅ Skills saved.")

    if not any([name_match, email_match, skills_match]):
        return (
            "❓ I couldn't extract any info. Could you please "
            "provide your name, email, or skills?"
        )

    return " ".join(response) + " Let me check what else I need."


@tool
def extract_application_info_tool(text: str) -> str:
    """Extract and save the user's name, email, and skills from free text."""
    return extract_application_info(text)


@tool(return_direct=True)
def check_application_goal(_: str = "") -> str:
    """Check whether all required application info is collected."""
    if all(application_info.values()):
        name = application_info["name"]
        email = application_info["email"]
        skills = application_info["skills"]
        return (
            f"✅ You're ready! Name: {name}, "
            f"Email: {email}, Skills: {skills}."
        )

    missing = [key for key, value in application_info.items() if not value]
    return (
        f"⏳ Still need: {', '.join(missing)}. "
        "Please ask the user to provide this."
    )


tools = [
    extract_application_info_tool,
    check_application_goal,
]


SYSTEM_PROMPT = """You are a helpful job application assistant.
Your goal is to collect the user's name, email, and skills.
Use the tools provided to extract this information and check whether all
required data is collected.
Once everything is collected, inform the user that the application info
is complete and stop.
"""


agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT,
    checkpointer=InMemorySaver(),
)


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        text_parts = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if text:
                    text_parts.append(str(text))
            elif isinstance(item, str):
                text_parts.append(item)
        return " ".join(text_parts).strip()
    return str(content)


def get_last_assistant_output(state: dict[str, Any]) -> str:
    messages = state.get("messages", [])
    for message in reversed(messages):
        if isinstance(message, dict):
            role = message.get("role") or message.get("type")
            if role in {"assistant", "ai", "tool"}:
                return _content_to_text(message.get("content", "")).strip()
        if getattr(message, "type", "") in {"ai", "tool"}:
            return _content_to_text(getattr(message, "content", "")).strip()
    return ""


print(
    "📝 Hi! I'm your job application assistant. "
    "Please tell me your name, email, and skills."
)

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("👋 Bye! Good luck.")
        break

    try:
        response = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]},
            config={"configurable": {"thread_id": "job-app-session"}},
        )
    except Exception as error:
        print("Bot: ⚠️ Model request failed.", str(error))
        print("Try again in a moment, or type 'quit' to exit.")
        continue

    assistant_output = get_last_assistant_output(response)
    print("Bot:", assistant_output)

    # If goal achieved, stop
    if "you're ready" in assistant_output.lower():
        print("🎉 Application info complete!")
        break
