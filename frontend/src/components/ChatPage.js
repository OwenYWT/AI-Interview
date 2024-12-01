import React, { useState, useRef, useEffect } from 'react';
import { Container, Box, TextField, IconButton, Typography, Button } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import SendIcon from '@mui/icons-material/Send';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import DeleteIcon from '@mui/icons-material/Delete';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { useNavigate } from 'react-router-dom';
import { io } from "socket.io-client";
import { getItem, removeItem } from "../localStorage";

const utterance = new SpeechSynthesisUtterance("");
utterance.voice =  window.speechSynthesis.getVoices()[191];
// var currHist = "";
const socket = io("http://localhost:7230", {
    transports: ["websocket"],
    reconnectionAttempts: 5,
});
const ChatPage = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isRecording, setIsRecording] = useState(false);
    const navigate = useNavigate();
    const recognitionRef = useRef(null);
    const sessionID = getItem('session_id');
    const silenceTimeoutRef = useRef(null);
    const messagesEndRef = useRef(null);

    useEffect(() => {
        // Automatically scroll to the bottom when new messages are added
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    useEffect(() => {
        if ('webkitSpeechRecognition' in window && !recognitionRef.current) {
            recognitionRef.current = new window.webkitSpeechRecognition();
            recognitionRef.current.continuous = false;
            recognitionRef.current.interimResults = true;

            let finalTranscript = '';

            recognitionRef.current.onresult = (event) => {
                let transcript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    transcript += event.results[i][0].transcript;
                }
                finalTranscript = transcript.trim();
                setInput(finalTranscript);
            };

            recognitionRef.current.onend = () => {
                setIsRecording(false);
                if (finalTranscript.trim()) {
                    handleSendMessage(finalTranscript.trim());
                    finalTranscript = '';
                }
            };

            recognitionRef.current.onerror = (event) => {
                console.error("Speech recognition error", event.error);
                setIsRecording(false);
            };
        } else if (!('webkitSpeechRecognition' in window)) {
            alert("Your browser does not support speech recognition.");
        }
    }, []);

    useEffect(() => {
        socket.on('completion_status', (status) => {
            if (status.status === 'success' && status.response) {
                const assistantMessage = { text: status.response, sender: 'assistant' };
                setMessages((prevMessages) => [...prevMessages, assistantMessage]);
                playTTS(status.response);
            } else {
                console.log("Backend server rejected", status);
            }
        });

        return () => {
            socket.off('completion_status');
        };
    }, []);
    

    const playTTS = (text) => {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.voice = window.speechSynthesis.getVoices()[191];
        // utterance.lang = 'en-US';
        utterance.rate = 1.2;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        

        window.speechSynthesis.speak(utterance);

        utterance.onend = () => {
            console.log("Speech synthesis completed.");
            if (!isRecording) {
                toggleRecognition();
            }
        };

        utterance.onerror = (e) => {
            console.error("Speech synthesis error:", e);
        };
    };

    const handleSendMessage = (messageText = input) => {
        if (messageText.trim() && sessionID) {
            const userMessage = { text: messageText, sender: 'user' };
            setMessages((prevMessages) => [...prevMessages, userMessage]);

            const payload = {
                session_id: sessionID,
                input_content: messageText,
            };

            socket.emit('llm_completion', payload);

            socket.on('completion_status', (status) => {
                if (status.success) {
                    const interviewerResponse = { sender: 'interviewer', text: status.response };
                    setMessages((prevMessages) => [...prevMessages, interviewerResponse]);
                } else {
                    console.log("Backend server received message", status);
                }
            });
            socket.on('llm_ended_interview', (status) => {
                console.log("Backend server ended interview", status);
                // currHist = status['messageString'];
                // currHist = "some message"
                localStorage.setItem("currHist", status['messageString']);
                navigate('/feedback');
            });

            setInput('');
        } else {
            alert('Message cannot be empty or session ID is missing.');
        }
    };


    const toggleRecognition = () => {
        if (isRecording) {
            recognitionRef.current.stop();
            setIsRecording(false);
            clearTimeout(silenceTimeoutRef.current);
        } else {
            recognitionRef.current.start();
            setIsRecording(true);
            startSilenceDetection();
        }
    };

    const startSilenceDetection = () => {
        clearTimeout(silenceTimeoutRef.current);
        silenceTimeoutRef.current = setTimeout(() => {
            if (isRecording) {
                recognitionRef.current.stop();
            }
        }, 3000);
    };

    const handleClearMessages = () => {
        setMessages([]);
        removeItem('messages');
    };

    const handleGetFeedback = () => {
        socket.emit("end_of_interview", {"session_id": sessionID})
        setIsRecording(false);
        console.log("something");
        console.log(localStorage);
        const data = { "text": "Interviewer: Can you tell me about yourself?\n" +
                "Interviewee: Uh... yeah, so, um, I'm, uh, John Doe. I, uh, studied... computer science. Yeah, and, um, I've done some, uh, coding... here and there.\n" +
                "\n" +
                "Interviewer: Can you elaborate on any specific projects or roles you've worked on?\n" +
                "Interviewee: Uh... let me think. Um... yeah, so there was this one project where, uh, I tried to, um, make a website. But, uh, I didn’t really finish it because I, uh, got busy.\n" +
                "\n" +
                "Interviewer: Can you tell me about a time when you worked on a team?\n" +
                "Interviewee: Uh... yeah, so, um, one time we were, uh, doing group work for, um, a class project. And, uh, we had to make, um, a presentation, I think. I didn’t, uh, talk much because, um, the others kind of took over.\n" +
                "\n" +
                "Interviewer: How do you handle tight deadlines?\n" +
                "Interviewee: Um, yeah, deadlines are, like, hard for me. Sometimes I, uh, miss them, but, uh, I try to do better.\n" +
                "\n" +
                "Interviewer: What are your strengths?\n" +
                "Interviewee: Uh... I'm not sure, but, um, I think I’m good at, um, learning stuff.\n" +
                "\n" +
                "Interviewer: What are your weaknesses?\n" +
                "Interviewee: Uh, there are, like, a lot. I, um, forget things sometimes and, uh, I get distracted easily.\n" +
                "\n" +
                "Interviewer: Why do you want this position?\n" +
                "Interviewee: Um, I think it’s, uh, a good opportunity to, um, get experience.\n" +
                "\n" +
                "Interviewer: Is there anything you’d like to ask us?\n" +
                "Interviewee: Uh... not really, no." };

        fetch('http://143.215.106.81:8888/process_text3', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            // body: JSON.stringify(data),
            body: JSON.stringify({"text": localStorage.getItem("currHist")}),
        })
            .then((response) => response.json())
            .then((responseData) => {
                console.log('Response:', responseData);

                const evaluation = responseData.evaluation || 'No evaluation provided.';
                const overall_score = responseData.overall_score || 0;
                const recommendation_score = responseData.recommendation_score || 0;
                const structured_answers_score = responseData.structured_answers_score || 0;

                navigate('/feedback', {
                    state: { evaluation, overall_score, recommendation_score, structured_answers_score },
                });
            })
            .catch((error) => {
                console.error('Error:', error);
                alert('Failed to process the request. Please try again.');
            });
    };

    return (
        <Container maxWidth="md" style={{ height: '90vh', display: 'flex', flexDirection: 'column', padding: '20px' }}>
            <Box display="flex" alignItems="center" justifyContent="space-between" style={{ marginBottom: '20px' }}>
                <IconButton onClick={() => navigate(-1)}>
                    <ArrowBackIcon fontSize="large" />
                </IconButton>

                <Typography variant="h4" align="center" style={{ fontWeight: 'bold', flexGrow: 1 }}>
                    Chat with HireSmart
                </Typography>

                <IconButton onClick={handleClearMessages} color="primary" title="Clear Chat">
                    <DeleteIcon fontSize="large" />
                </IconButton>
            </Box>

            <Box
                sx={{
                    flexGrow: 1,
                    overflowY: 'auto',
                    border: '1px solid #ccc',
                    borderRadius: '8px',
                    padding: '10px',
                    marginBottom: '20px',
                    backgroundColor: '#f9f9f9',
                }}
            >
                {messages.map((message, index) => (
                    <Box
                        key={index}
                        sx={{
                            display: 'flex',
                            justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start',
                            marginBottom: '10px',
                        }}
                    >
                        <Box
                            sx={{
                                maxWidth: '70%',
                                padding: '10px',
                                borderRadius: '10px',
                                backgroundColor: message.sender === 'user' ? '#1976d2' : '#e0e0e0',
                                color: message.sender === 'user' ? 'white' : 'black',
                            }}
                        >
                            <Typography variant="body1">{message.text}</Typography>
                        </Box>
                    </Box>
                ))}
                <div ref={messagesEndRef} /> {/* This div will be used to scroll */}
            </Box>

            <Box display="flex" alignItems="center" style={{ borderTop: '1px solid #ccc', paddingTop: '10px' }}>
                <TextField
                    fullWidth
                    variant="outlined"
                    placeholder="Type your message..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            handleSendMessage();
                        }
                    }}
                    style={{ marginRight: '8px' }}
                    InputProps={{ style: { fontSize: '1rem' } }}
                />

                <IconButton color="primary" onClick={toggleRecognition}>
                    <MicIcon fontSize="large" style={{ color: isRecording ? 'red' : 'inherit' }} />
                </IconButton>

                <IconButton color="primary" onClick={handleSendMessage}>
                    <SendIcon fontSize="large" />
                </IconButton>
            </Box>

            <Box display="flex" justifyContent="center" style={{ marginTop: '15px' }}>
                <Button
                    variant="contained"
                    color="primary"
                    endIcon={<ArrowForwardIosIcon />}
                    onClick={handleGetFeedback}
                    style={{
                        borderRadius: '20px',
                        padding: '10px 20px',
                        maxWidth: '300px',
                        fontSize: '16px',
                        textTransform: 'none',
                    }}
                >
                    Get Feedback
                </Button>
            </Box>
        </Container>
    );
};

export default ChatPage;
