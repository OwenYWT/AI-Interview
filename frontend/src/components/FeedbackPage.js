import React from 'react';
import { Container, Typography, Box, Button, IconButton } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';

const FeedbackPage = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const { evaluation, overall_score, recommendation_score, structured_answers_score } = location.state || {};

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
                    {evaluation?.overall || "Overall evaluation is not available."}
                </Typography>

                {/* Score Sections */}
                <Typography variant="h6" gutterBottom>
                    Overall Score:
                </Typography>
                <Typography variant="body1" style={{ marginBottom: '20px' }}>
                    {overall_score !== undefined ? overall_score : "Overall score is not available."}
                </Typography>

                <Typography variant="h6" gutterBottom>
                    Recommendation Score:
                </Typography>
                <Typography variant="body1" style={{ marginBottom: '20px' }}>
                    {recommendation_score !== undefined ? recommendation_score : "Recommendation score is not available."}
                </Typography>

                <Typography variant="h6" gutterBottom>
                    Structured Answers Score:
                </Typography>
                <Typography variant="body1" style={{ marginBottom: '20px' }}>
                    {structured_answers_score !== undefined ? structured_answers_score : "Structured answers score is not available."}
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
