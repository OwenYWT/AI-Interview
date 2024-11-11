import React from 'react';
import { Container, Typography, Button, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const WelcomePage = () => {
    const navigate = useNavigate();

    const handleStart = () => {
        navigate('/job-selection');
    };

    return (
        <Container
            maxWidth="sm"
            style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'center',
                height: '100vh',
                textAlign: 'center',
            }}
        >
            <Typography variant="h3" gutterBottom style={{ fontWeight: 'bold', marginBottom: '20px' }}>
                Welcome to HireSmart!
            </Typography>
            <Typography variant="body1" style={{ marginBottom: '40px' }}>
                Your AI-powered mock interview assistant.
            </Typography>
            <Button
                variant="contained"
                color="primary"
                size="large"
                onClick={handleStart}
                style={{ borderRadius: '20px', padding: '10px 30px', fontSize: '16px' }}
            >
                Start
            </Button>
        </Container>
    );
};

export default WelcomePage;
