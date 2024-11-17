import React, { useState } from 'react';
import { Container, Typography, Box, TextField, Button, IconButton, MenuItem } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { useNavigate } from 'react-router-dom';
import { getItem, setItem } from "../localStorage";
import { io } from "socket.io-client";

const socket = io("http://localhost:7230", {
    transports: ["websocket"],
    reconnectionAttempts: 5,
});

const InfoPage = () => {
    const [problemCountBehavior, setProblemCountBehavior] = useState('');
    const [problemCountTechnical, setProblemCountTechnical] = useState('');
    const [expectedDuration, setExpectedDuration] = useState('');
    const [preferName, setPreferName] = useState('');
    const [companyName, setCompanyName] = useState('');
    const [positionTitle, setPositionTitle] = useState('');
    const [technicalDifficulty, setTechnicalDifficulty] = useState('medium'); // Default value
    const navigate = useNavigate();

    const handleSubmit = () => {
        const sessionID = getItem('session_id');
        if (!sessionID) {
            alert('Session ID not found! Please go back and start again.');
            return;
        }

        const payload = {
            session_id: sessionID,
            behavioral_question_count: parseInt(problemCountBehavior, 10) || 1,
            technical_question_count: parseInt(problemCountTechnical, 10) || 1,
            expected_duration: parseInt(expectedDuration, 10) || 10,
            preferred_name: preferName,
            company_name: companyName,
            position_title: positionTitle,
            technical_question_difficulty: technicalDifficulty,
        };

        socket.emit('addition_information', payload, (response) => {
            if (response.success) {
                console.log('Information submitted successfully:', response);
                navigate('/chat');
            } else {
                console.error('Failed to submit information:', response);
                alert(`Error: ${response.message}`);
            }
        });
    };

    return (
        <Container maxWidth="md" style={{ textAlign: 'center', padding: '20px' }}>
            {/* Back Button */}
            <Box display="flex" alignItems="center" justifyContent="space-between" style={{ marginBottom: '20px' }}>
                <IconButton onClick={() => navigate(-1)}>
                    <ArrowBackIcon fontSize="large" />
                </IconButton>

                <Typography variant="h4" style={{ fontWeight: 'bold', flexGrow: 1 }}>
                    Fill Your Information
                </Typography>
            </Box>

            {/* Form Fields */}
            <Box display="flex" flexDirection="column" alignItems="center" gap={2} style={{ marginBottom: '30px' }}>
                <TextField
                    label="Problem Count - Behavior"
                    variant="outlined"
                    fullWidth
                    type="number"
                    value={problemCountBehavior}
                    onChange={(e) => {
                        const value = e.target.value;
                        if (/^\d*$/.test(value)) {
                            setProblemCountBehavior(value);
                        }
                    }}
                />

                <TextField
                    label="Problem Count - Technical"
                    variant="outlined"
                    fullWidth
                    type="number"
                    value={problemCountTechnical}
                    onChange={(e) => {
                        const value = e.target.value;
                        if (/^\d*$/.test(value)) {
                            setProblemCountTechnical(value);
                        }
                    }}
                />

                <TextField
                    label="Expected Duration (Minutes)"
                    variant="outlined"
                    fullWidth
                    type="number"
                    value={expectedDuration}
                    onChange={(e) => {
                        const value = e.target.value;
                        if (/^\d*$/.test(value)) {
                            setExpectedDuration(value);
                        }
                    }}
                />
                <TextField
                    label="Preferred Name"
                    variant="outlined"
                    fullWidth
                    value={preferName}
                    onChange={(e) => setPreferName(e.target.value)}
                />
                <TextField
                    label="Company Name (Optional)"
                    variant="outlined"
                    fullWidth
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                />
                <TextField
                    label="Position Title (Optional)"
                    variant="outlined"
                    fullWidth
                    value={positionTitle}
                    onChange={(e) => setPositionTitle(e.target.value)}
                />
                <TextField
                    select
                    label="Technical Question Difficulty"
                    variant="outlined"
                    fullWidth
                    value={technicalDifficulty}
                    sx={{ width: '200px' }}
                    onChange={(e) => setTechnicalDifficulty(e.target.value)}
                >
                    <MenuItem value="easy" sx={{ textAlign: 'left' }}>Easy</MenuItem>
                    <MenuItem value="medium" sx={{ textAlign: 'left' }}>Medium</MenuItem>
                    <MenuItem value="hard" sx={{ textAlign: 'left' }}>Hard</MenuItem>
                </TextField>
            </Box>

            {/* Submit Button */}
            <Button
                variant="contained"
                color="primary"
                endIcon={<ArrowForwardIosIcon />}
                fullWidth
                style={{
                    borderRadius: '20px',
                    padding: '10px',
                    fontSize: '16px',
                    textTransform: 'none',
                    maxWidth: '300px',
                }}
                onClick={handleSubmit}
            >
                Proceed to Chat
            </Button>
        </Container>
    );
};

export default InfoPage;
