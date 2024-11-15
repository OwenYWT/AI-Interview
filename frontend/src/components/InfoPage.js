import React, { useState } from 'react';
import { Container, Typography, Box, TextField, Button, IconButton } from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { useNavigate } from 'react-router-dom';

const InfoPage = () => {
    const [problemCountBehavior, setProblemCountBehavior] = useState('');
    const [problemCountTechnical, setProblemCountTechnical] = useState('');
    const [expectedDuration, setExpectedDuration] = useState('');
    const [preferName, setPreferName] = useState('');
    const [companyName, setCompanyName] = useState('');
    const [positionTitle, setPositionTitle] = useState('');
    const navigate = useNavigate();

    const handleSubmit = () => {
        navigate('/chat');
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
                    value={problemCountBehavior}
                    onChange={(e) => setProblemCountBehavior(e.target.value)}
                />
                <TextField
                    label="Problem Count - Technical"
                    variant="outlined"
                    fullWidth
                    value={problemCountTechnical}
                    onChange={(e) => setProblemCountTechnical(e.target.value)}
                />
                <TextField
                    label="Expected Duration"
                    variant="outlined"
                    fullWidth
                    value={expectedDuration}
                    onChange={(e) => setExpectedDuration(e.target.value)}
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
