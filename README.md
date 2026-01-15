🎙️ Smart Meeting Assistant (AI-Powered Video Conferencing)
A cutting-edge, full-stack video calling application featuring a Real-time AI Meeting Assistant. The assistant joins calls, transcribes conversations in real-time, and provides intelligent summaries or Q&A support using Google Gemini AI and Vision Agents.

🚀 Features
📺 Real-time Video Calls – High-quality video conferencing powered by Stream SDK.

🤖 AI Meeting Assistant – A native AI bot that joins the call to listen, learn, and assist.

🗣️ Voice Activation – Trigger the AI simply by saying "Hey assistant" followed by a command.

📝 Live Transcriptions – Side-panel displaying real-time speech-to-text for all participants.

🧠 Intelligent Q&A – Ask the assistant about past points, action items, or summaries of the current session.

🛠️ Call Controls – Screen sharing, recording, reactions, and device management (mic/camera).

🔐 Secure Access – JWT-based authentication and unique meeting tokens.

🛠 Tech Stack
Frontend
Next.js 15 (App Router)

Tailwind CSS (Styling)

Stream Video & Chat SDK (Real-time Infrastructure)

Backend (AI Agent)
Python 3.13

Vision Agents Framework (Open-source Video AI)

Google Gemini 1.5 Flash (LLM & Real-time API)

Server (API)
Node.js / Next.js Server Actions

Stream Node SDK (Token Generation)

📂 Project Structure
Plaintext
├── client/                 # Next.js Frontend
│   ├── components/         # UI: MeetingRoom, TranscriptionPanel, etc.
│   ├── hooks/              # useStreamClients, useMeetingLogic
│   └── app/                # App Router: Home & Meeting Pages
├── backend/                # Python AI Assistant
│   ├── main.py             # Agent logic & event handlers
│   └── .env                # Agent specific credentials
└── api/                    # Server-side token management
⚙️ Environment Variables
Create a .env.local in the root and a .env in the backend/ directory.

Frontend (.env.local)

Code snippet
NEXT_PUBLIC_STREAM_API_KEY=your_stream_api_key
STREAM_API_SECRET=your_stream_api_secret
NEXT_PUBLIC_CALL_ID=demo_room_123
Backend (backend/.env)

Code snippet
STREAM_API_KEY=your_stream_api_key
STREAM_API_SECRET=your_stream_api_secret
GEMINI_API_KEY=your_google_gemini_key
CALL_ID=demo_room_123
▶️ Getting Started
1. Clone the Repository
Bash
git clone https://github.com/your-username/smart-meeting-assistant.git
2. Install & Run Frontend
Bash
cd client
npm install
npm run dev
3. Install & Run AI Assistant
Bash
cd backend
# Recommendation: Use 'uv' or 'venv'
uv venv
source .venv/bin/activate
uv pip install vision-agents[gemini,stream] python-dotenv
python main.py
🧠 AI Agent Workflow
Join: The Python agent connects to the Stream Call using a dedicated Bot ID.

Listen: It receives real-time audio segments and transcribes them locally.

Trigger: It ignores all chatter until the "Hey assistant" keyword is detected.

Process: The relevant question + meeting history is sent to Gemini AI.

Respond: The agent speaks the answer directly into the call and posts text to the chat.

📌 Future Enhancements
Multi-language Support – Real-time translation of meeting transcripts.

Action Item Extraction – Automatically email meeting notes to participants after the call.

Visual Recognition – Ability for the agent to "see" shared screens or participants.

CRM Integration – Save meeting summaries directly to Notion or Salesforce.

📄 License
This project is for educational and portfolio purposes.

🙌 Author
Harsh Kaushik | Full Stack Developer | AI Enthusiast .

⭐ If you find this project helpful, give it a star on GitHub!
