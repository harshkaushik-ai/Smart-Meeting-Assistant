🎙️ Smart Meeting Assistant
A high-performance, real-time video calling application featuring an AI Meeting Assistant that transcribes, summarizes, and answers questions about your live meetings. Built with Next.js, Stream, and Gemini AI.

🚀 Overview
This project demonstrates how to build a modern "AI-in-the-loop" application. The app allows users to create video rooms where an AI bot (powered by Vision Agents) joins as a silent participant. The bot listens to the conversation and responds only when addressed, providing real-time meeting intelligence.

Key Features
Video Conferencing: Real-time video/audio calling with screen sharing and reactions.

AI Bot Participant: A Python-based agent that joins the call natively via Stream's infrastructure.

Voice Triggering: Assistant activates on the keyword phrase: "Hey assistant".

Real-time Transcriptions: Live speech-to-text panel synchronized across all participants.

Contextual Intelligence: Gemini-powered summaries based on the current meeting transcript.

🛠️ Tech Stack
Frontend
Framework: Next.js 15 (App Router)

Styling: Tailwind CSS

Video/Chat SDK: Stream Video & Audio SDK

Backend (AI Agent)
Language: Python 3.13

AI Framework: Vision Agents

LLM: Google Gemini 1.5 Flash (via Gemini Realtime API)

⚙️ Setup Instructions
1. Clone the Repository
Bash
git clone https://github.com/your-username/smart-meeting-assistant.git
cd smart-meeting-assistant
2. Environment Variables
You will need accounts at Stream and Google AI Studio.

Frontend (/.env.local):

Code snippet
NEXT_PUBLIC_STREAM_API_KEY=your_api_key
STREAM_API_SECRET=your_api_secret
NEXT_PUBLIC_CALL_ID=main-room
Backend (/backend/.env):

Code snippet
STREAM_API_KEY=your_api_key
STREAM_API_SECRET=your_api_secret
GEMINI_API_KEY=your_gemini_key
CALL_ID=main-room
3. Frontend Installation
Bash
npm install
npm run dev
4. Backend Installation (AI Agent)
It is recommended to use uv for Python package management.

Bash
cd backend
uv venv
source .venv/bin/activate  # Or .venv\Scripts\activate on Windows
uv pip install vision-agents[gemini,stream] python-dotenv
python main.py
💡 Usage
Start the Web App: Open http://localhost:3000, enter your name, and join the room.

Activate the Agent: Run the Python script. You will see the "Meeting Assistant" join the call UI.

Transcribe: Start speaking; your words will appear in the right-hand side panel.

Ask Questions: Say "Hey assistant, what have we discussed so far?" or "Hey assistant, give me a summary."

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
