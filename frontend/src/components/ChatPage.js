import React, { useState } from 'react';
import { Container, Box, TextField, IconButton, Typography, Button } from '@mui/material';
import MicIcon from '@mui/icons-material/Mic';
import SendIcon from '@mui/icons-material/Send';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { useNavigate } from 'react-router-dom';
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";

const ChatPage = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const navigate = useNavigate();

    const handleSendMessage = () => {
        if (input.trim()) {
            setMessages([...messages, { text: input, sender: 'user' }]);
            setInput('');
        }
    };

    const handleGetFeedback = () => {
        const evaluation = {
            overall: 'Overall, a solid performance with room for growth in specific areas.',
        };

        const overall_score = 8.5;
        const recommendation_score = 7.0;
        const structured_answers_score = 9.0;

        navigate('/feedback', {
            state: { evaluation, overall_score, recommendation_score, structured_answers_score },
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
            </Box>

            <Box display="flex" alignItems="center" style={{ borderTop: '1px solid #ccc', paddingTop: '10px' }}>
                <TextField
                    fullWidth
                    variant="outlined"
                    placeholder="Type your message..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                    style={{ marginRight: '8px' }}
                    InputProps={{ style: { fontSize: '1rem' } }}
                />

                <IconButton color="primary" onClick={() => alert('Microphone activated')}>
                    <MicIcon fontSize="large" />
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
