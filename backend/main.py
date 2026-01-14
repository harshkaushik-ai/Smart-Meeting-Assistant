
# import asyncio
# import os
# from flask import Flask
# from threading import Thread
# import logging
# from uuid import uuid4
# from dotenv import load_dotenv
# from flask_cors import CORS # You may need to pip install flask-cors

# # Vision Agents imports
# from vision_agents.core import agents
# from vision_agents.plugins import getstream, gemini
# from vision_agents.core.edge.types import User

# # Core events
# from vision_agents.core.events import (
#     CallSessionParticipantJoinedEvent,
#     CallSessionParticipantLeftEvent,
#     CallSessionStartedEvent,
#     CallSessionEndedEvent,
#     PluginErrorEvent
# )

# # LLM events
# from vision_agents.core.llm.events import (
#     RealtimeUserSpeechTranscriptionEvent, 
#     LLMResponseChunkEvent
# )


# app = Flask(__name__)
# CORS(app)

# @app.route('/')
# def home():
#     return """
#     <html>
#         <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
#             <h1>🎙️ Meeting Assistant is Live</h1>
#             <p>Status: <b>Active</b></p>
#             <p>Monitoring Call ID: <code>demo-meeting-room</code></p>
#             <hr>
#             <p><small>Check the Render logs for the live transcript.</small></p>
#         </body>
#     </html>
#     """, 200

# @app.route('/health')
# def health():
#     return "OK", 200

# def run_health_server():
#     port = int(os.environ.get("PORT", 8080))
#     app.run(host='0.0.0.0', port=port)

# def keep_alive():
#     """Starts the Flask server in a background thread."""
#     t = Thread(target=run_health_server, daemon=True)
#     t.start()    



# # Setup logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Load environment variables
# load_dotenv()

# # Meeting data storage
# meeting_data = {
#     "transcript": [],
#     "is_active": False
# }

# async def start_agent(call_id: str):
#     logger.info("🤖 Starting Meeting Assistant...")
#     logger.info(f"📞 Call ID: {call_id}")
    
#     # Create agent with Gemini Realtime
#     agent = agents.Agent(
#         edge=getstream.Edge(),
#         agent_user=User(
#             id="meeting-assistant-bot",
#             name="Meeting Assistant"
#         ),
#         instructions="""
#         You are a meeting transcription bot.
        
#         CRITICAL RULES - FOLLOW EXACTLY:
#         1. YOU MUST NEVER SPEAK unless someone says "Hey Assistant"
#         2. DO NOT respond to conversations between users
#         3. DO NOT acknowledge anything users say to each other
#         4. DO NOT explain that you're staying silent
#         5. DO NOT say "I should remain silent" or any variation
#         6. ONLY RESPOND when you explicitly hear "Hey Assistant" followed by a question
#         7. If unsure whether to speak: DON'T SPEAK
        
#         Your ONLY job:
#         - Listen silently
#         - Transcribe everything
#         - Wait for "Hey Assistant"
        
#         When you DO hear "Hey Assistant":
#         - Answer the question using meeting transcript and notes
#         - Keep answer short and factual
#         - Use only information from this meeting
        
#         Example:
#         ❌ User: "Let's discuss the budget" → You: STAY COMPLETELY SILENT
#         ❌ User: "What do you think?" → You: STAY COMPLETELY SILENT
        
#         ✅ User: "Hey Assistant, what are the action items?" → You: Answer with action items
#         ✅ User: "Hey Assistant, summarize the meeting" → You: Provide summary
#         """,
#         llm=gemini.Realtime(fps=0),
#     )
    
#     meeting_data["agent"] = agent
#     meeting_data["call_id"] = call_id
    
#     @agent.events.subscribe
#     async def handle_session_started(event: CallSessionStartedEvent):
#         meeting_data["is_active"] = True
#         logger.info("🎙️ Meeting started")
        
#         try:
#             channel = agent.edge.client.channel("messaging", call_id)
#             await channel.watch()
#             meeting_data["channel"] = channel
#             logger.info("✅ Chat channel initialized")
#         except Exception as e:
#             logger.error(f"❌ Chat channel error: {e}")
    
#     @agent.events.subscribe
#     async def handle_participant_joined(event: CallSessionParticipantJoinedEvent):
#         if event.participant.user.id == "meeting-assistant-bot":
#             return
#         participant_name = event.participant.user.name
#         logger.info(f"👤 Participant joined: {participant_name}")
    
#     @agent.events.subscribe
#     async def handle_participant_left(event: CallSessionParticipantLeftEvent):
#         if event.participant.user.id == "meeting-assistant-bot":
#             return
#         participant_name = event.participant.user.name
#         logger.info(f"👋 Participant left: {participant_name}")
    
#     @agent.events.subscribe
#     async def handle_transcript(event: RealtimeUserSpeechTranscriptionEvent):
#         """Handle transcripts"""
#         if not event.text or len(event.text.strip()) == 0:
#             return
        
#         speaker = getattr(event, 'participant_id', 'Unknown')
#         transcript_text = event.text
        
#         # Store transcript
#         meeting_data["transcript"].append({
#             "speaker": speaker,
#             "text": transcript_text,
#             "timestamp": getattr(event, 'timestamp', None)
#         })
        
#         logger.info(f"📝 [{speaker}]: {transcript_text}")
        
#         # Q&A handling
#         if transcript_text.lower().startswith("hey assistant"):
#             question = transcript_text[13:].strip()
            
#             if question:
#                 logger.info(f"❓ Q&A triggered: {question}")
                
#                 # Build context from transcript
#                 context = "MEETING TRANSCRIPT:\n\n"
#                 for entry in meeting_data["transcript"]:
#                     context += f"[{entry['speaker']}]: {entry['text']}\n"
                
#                 prompt = f"""
#                 {context}
                
#                 USER QUESTION: {question}
                
#                 Answer based ONLY on the meeting transcript above.
#                 Be concise and helpful.
#                 """
                
#                 try:
#                     await agent.simple_response(prompt)
#                     logger.info(f"🤖 Responding to question")
#                 except Exception as e:
#                     logger.error(f"❌ Q&A error: {e}")
    
#     @agent.events.subscribe
#     async def handle_llm_response(event: LLMResponseChunkEvent):
#         """Log agent responses"""
#         if hasattr(event, 'delta') and event.delta:
#             logger.info(f"🤖 Agent: {event.delta}")
    
#     @agent.events.subscribe
#     async def handle_session_ended(event: CallSessionEndedEvent):
#         meeting_data["is_active"] = False
#         logger.info("🛑 Meeting ended")
#         logger.info(f"📊 Final Stats:")
#         logger.info(f"   - Transcript entries: {len(meeting_data['transcript'])}")
    
#     @agent.events.subscribe
#     async def handle_errors(event: PluginErrorEvent):
#         logger.error(f"❌ Plugin error: {event.error_message}")
#         if event.is_fatal:
#             logger.error("🚨 Fatal error")
    
#     # Initialize agent
#     await agent.create_user()
#     call = agent.edge.client.video.call("default", call_id)

    
#     logger.info(f"🔄 Starting monitoring loop for: {call_id}")
    
#     while True:
#         try:
#             logger.info("✅ Attempting to join call...")
#             async with agent.join(call):
#                 logger.info("\n" + "="*60)
#                 logger.info("🎙️  MEETING ASSISTANT ACTIVE!")
#                 logger.info("="*60)
#                 logger.info(f"\n🔗 Meeting ID: {call_id}\n")
                
#                 # CRITICAL: This line stops the code here and keeps the bot 
#                 # in the room until the connection breaks.
#                 await agent.wait_until_done() 
        
#         except Exception as e:
#             # If Render's CPU spikes and kills the connection, we catch it here
#             logger.error(f"⚠️ Connection dropped: {e}")
#             logger.info("🔄 Waiting 10 seconds before rejoining...")
#             await asyncio.sleep(5)  

# def print_meeting_summary():
#     """Print meeting summary"""
#     print("\n" + "="*70)
#     print("📋 MEETING SUMMARY")
#     print("="*70)
    
#     print(f"\n📝 Transcript ({len(meeting_data['transcript'])} entries):")
#     print("-"*70)
#     for entry in meeting_data['transcript']:
#         print(f"[{entry['speaker']}]: {entry['text']}")
    
#     print("\n" + "="*70)
#     print("✅ Summary Complete")
#     print("="*70 + "\n")

# if __name__ == "__main__":
#     call_id = os.getenv("CALL_ID", f"meeting-{uuid4().hex[:8]}")    
    
#     print("\n" + "="*70)
#     print("🎯 SMART MEETING ASSISTANT")
#     print("="*70)
#     print("\n✨ Features:")
#     print("   1. Auto-transcription")
#     print("   2. Q&A with 'Hey Assistant'")
#     print("="*70 + "\n")

#     keep_alive()
    
#     try:
#         asyncio.run(start_agent(call_id))
#     except KeyboardInterrupt:
#         print("\n\n🛑 Stopped by user")
#     finally:
#         if meeting_data["transcript"]:
#             print_meeting_summary()


import asyncio
import os
import logging
import sys
from flask import Flask
from threading import Thread
from uuid import uuid4
from dotenv import load_dotenv
from flask_cors import CORS

from vision_agents.core import agents
from vision_agents.plugins import getstream, gemini
from vision_agents.core.edge.types import User
from vision_agents.core.events import CallSessionStartedEvent
from vision_agents.core.llm.events import RealtimeUserSpeechTranscriptionEvent

# 1. FLASK SETUP
app = Flask(__name__)
CORS(app)

meeting_data = {"is_active": False, "call_id": None}

@app.route('/health')
def health(): return "OK", 200

@app.route('/')
def home(): return f"Status: {meeting_data['is_active']}", 200

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

# 2. BOT LOGIC
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
load_dotenv()

async def start_agent():
    call_id = os.getenv("CALL_ID", "demo-meeting-room")
    meeting_data["call_id"] = call_id
    
    while True:
        try:
            # Re-initialize Edge inside the loop for fresh credentials
            edge = getstream.Edge()
            unique_sid = f"assistant-{uuid4().hex[:4]}"
            
            agent = agents.Agent(
                edge=edge,
                agent_user=User(id=unique_sid, name="Meeting Assistant"),
                instructions="Listen and transcribe. Only speak if you hear 'Hey Assistant'.",
                llm=gemini.Realtime(fps=0),
            )

            @agent.events.subscribe
            async def on_start(event: CallSessionStartedEvent):
                meeting_data["is_active"] = True
                logger.info("🎙️ Connected to Stream!")

            @agent.events.subscribe
            async def on_transcript(event: RealtimeUserSpeechTranscriptionEvent):
                if event.text:
                    logger.info(f"📝 {unique_sid} heard: {event.text}")

            await agent.create_user()
            call = edge.client.video.call("default", call_id)

            logger.info(f"🚀 Joining room: {call_id} as {unique_sid}")
            
            # Using 10 minute timeout to be safe
            async with agent.join(call, participant_wait_timeout=600.0):
                await agent.finish()
        
        except Exception as e:
            meeting_data["is_active"] = False
            logger.error(f"❌ Critical Error: {e}")
            await asyncio.sleep(10) # Cooldown before restart

if __name__ == "__main__":
    # Start Flask in background thread
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Start the async bot loop
    try:
        asyncio.run(start_agent())
    except KeyboardInterrupt:
        logger.info("Clean shutdown")