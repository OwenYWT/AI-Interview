import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Button, IconButton } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { getItem, setItem } from "../localStorage";

const FeedbackPage = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const [feedback, setFeedback] = useState({
        evaluation: { overall: "Overall evaluation is not available." },
        overall_score: "Overall score is not available.",
        recommendation_score: "Recommendation score is not available.",
        structured_answers_score: "Structured answers score is not available.",
    });

    useEffect(() => {
        if (location.state) {
            setFeedback(location.state);
            setItem('feedback', location.state);
        } else {
            const savedFeedback = getItem('feedback', feedback);
            setFeedback(savedFeedback);
        }
    }, [location.state]);

    return (
        <Container maxWidth="md" style={{ padding: '20px', textAlign: 'center' }}>
            <Box display="flex" alignItems="center" justifyContent="center" style={{ marginBottom: '20px', position: 'relative' }}>
                <IconButton onClick={() => navigate(-1)} style={{ position: 'absolute', left: 0 }}>
                    <ArrowBackIcon fontSize="large" />
                </IconButton>

                <Typography variant="h4" align="center" style={{ fontWeight: 'bold' }}>
                    Your Mock Interview Feedback
                </Typography>
            </Box>

            <Box mt={4} textAlign="left">
                {/* Evaluation Sections */}
                <Typography variant="h6" gutterBottom>
                    Overall Evaluation:
                </Typography>
                <Typography variant="body1" style={{ marginBottom: '20px' }}>
                    {feedback.evaluation?.overall}
                </Typography>

                {/* Score Sections */}
                <Typography variant="h6" gutterBottom>
                    Overall Score:
                </Typography>
                <Typography variant="body1" style={{ marginBottom: '20px' }}>
                    {feedback.overall_score}
                </Typography>

                <Typography variant="h6" gutterBottom>
                    Recommendation Score:
                </Typography>
                <Typography variant="body1" style={{ marginBottom: '20px' }}>
                    {feedback.recommendation_score}
                </Typography>

                <Typography variant="h6" gutterBottom>
                    Structured Answers Score:
                </Typography>
                <Typography variant="body1" style={{ marginBottom: '20px' }}>
                    {feedback.structured_answers_score}
                </Typography>
            </Box>

            <Box display="flex" justifyContent="center" style={{ marginTop: '15px' }}>
                <Button
                    variant="contained"
                    color="primary"
                    onClick={() => navigate('/job-selection')}
                    style={{
                        borderRadius: '20px',
                        padding: '10px 20px',
                        maxWidth: '300px',
                        fontSize: '16px',
                        textTransform: 'none',
                    }}
                >
                    Back to Job Selection
                </Button>
            </Box>
        </Container>
    );
};

export default FeedbackPage;
