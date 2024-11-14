from flask import Flask, jsonify
from flask_socketio import SocketIO, emit
import base64
import os
import datetime

RESUME_FOLDER = 'resumes'
os.makedirs(RESUME_FOLDER, exist_ok=True)

app = Flask(__name__)
socketio = SocketIO(app, async_mode='eventlet', cors_allowed_origins="*")  # Ensures compatibility with Flask

chat_histories = {}

class ChatHistory:
    def __init__(self, system_prompt, candidate_name="") -> None:
        self.messages = []
        self.add_message("system", system_prompt)
        self.candidate_name = candidate_name

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_message(self):
        return self.messages

def system_prompt_helper(interviewer_name=None, candidate_name=None, company=None, position_name=None, qualifications=None, behavioral_count=0, technical_count=0):
    company = "" if not company else f" at {company}"
    interviewer_name_p = f"Your name is {interviewer_name}." if interviewer_name else ""
    candidate_name_p = f"The candidate you are interviewing today is {candidate_name}." if candidate_name else ""
    position_name_p = f"The position the candidate applied for is {position_name}." if position_name else ""
    qualifications_p = f"The qualifications required include {qualifications}." if qualifications else ""
    question_count_p = f"This interview consists of {behavioral_count} behavioral questions and {technical_count} technical questions."
    prompt = f"""You are the interviewer{company}. {interviewer_name_p} {candidate_name_p} {position_name_p} {qualifications_p} {question_count_p}
Date and time now: {datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")}.
Do not disclose answers directly. Remain casual and conversational throughout the interview."""
    return prompt

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    socketio.emit('connection_response', {'status': 'connected'})

@socketio.on('init_simulation')
def handle_connect(data):

    session_id = data['session_id']
    authorization_token = data['authorization_token']
    resume_filename = data['resume_filename']
    resume_file = data['resume_file']

    file_data = resume_file.split(",")[1]
    file_binary_data = base64.b64decode(file_data)
    resume_file_path = os.path.join(RESUME_FOLDER, f"{session_id}_{resume_filename}")
    with open(resume_file_path, 'wb') as f:
        f.write(file_binary_data)
    print(f"Client connected with session id {session_id} and resume saved as {resume_file_path}")

    emit('upload_status', {'status': 'success', 'message': f"File '{resume_filename}' uploaded successfully."})

@socketio.on('addition_information')
def handle_additional_information(data):
    session_id = data['session_id']
    behavioral_question_count = data.get('behavioral_question_count', 0)
    technical_question_count = data.get('technical_question_count', 0)

    print(f"Session {session_id} - Behavioral: {behavioral_question_count}, Technical: {technical_question_count}")
    emit('info_received', {'status': 'success', 'session_id': session_id})

@socketio.on('llm_completion')
def handle_llm_completion(data):
    emit('completion_status', {'status': 'error', 'message': 'Not implemented'}, 400)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=7230)
