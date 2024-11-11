import React, { useState } from 'react';
import { Container, Typography, Box, Button, TextField, IconButton } from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { useNavigate } from 'react-router-dom';

const JobSelectionPage = () => {
    const [jobDescription, setJobDescription] = useState('');
    const navigate = useNavigate();

    const roles = [
        "Custom Job Description", "Business Analyst", "Product Manager", "Software Engineer",
        "Marketing Specialist", "Data Analyst", "UX/UI Designer", "QA Engineer"
    ];

    const handleJobRoleClick = (role) => {
        setJobDescription(role === "Custom Job Description" ? "" : role);
    };

    const handleGenerateQuestions = () => {
        if (jobDescription) {
            navigate('/chat');
        } else {
            alert("Please select or enter a job description.");
        }
    };

    return (
        <Container maxWidth="md" style={{ textAlign: 'center', padding: '20px' }}>
            <Typography
                variant="h4"
                gutterBottom
                style={{ fontWeight: 'bold', marginBottom: '30px' }}
            >
                Select a job description
            </Typography>

            {/* Job Role Buttons */}
            <Box display="flex" flexWrap="wrap" justifyContent="center" gap={1} marginBottom={3}>
                {roles.map((role) => (
                    <Button
                        key={role}
                        variant={role === jobDescription ? "contained" : "outlined"}
                        color={role === jobDescription ? "primary" : "default"}
                        onClick={() => handleJobRoleClick(role)}
                        style={{
                            borderRadius: '20px',
                            padding: '8px 16px',
                            textTransform: 'none',
                        }}
                    >
                        {role}
                    </Button>
                ))}
            </Box>

            {/* Text Area */}
            <Box style={{ maxWidth: '1500px', width: '100%', margin: '0 auto' }}>
                <TextField
                    placeholder="Select a job role above or paste your own description here"
                    multiline
                    rows={7}
                    fullWidth
                    variant="outlined"
                    value={jobDescription}
                    onChange={(e) => setJobDescription(e.target.value)}
                    required
                    style={{
                        marginBottom: '20px',
                        fontSize: '1.2rem',
                        padding: '10px',
                        width: '100%',
                    }}
                    inputProps={{
                        maxLength: 5000,
                        style: { fontSize: '1rem', padding: '4px' },
                    }}
                />
            </Box>

            {/* Resume Upload */}
            <Box
                display="flex"
                flexDirection="column"
                alignItems="center"
                justifyContent="center"
                p={1}
                mb={5}
                border="1px dashed #ccc"
                borderRadius="8px"
                style={{
                    backgroundColor: '#f9f9f9',
                    maxWidth: '500px',
                    maxHeight: '150px',
                    margin: 'auto',
                    marginBottom: '30px',
                }}
            >
                <Box display="flex" flexDirection="column" alignItems="center">
                    <IconButton style={{ marginBottom: '2px' }}>
                        <UploadFileIcon color="primary" style={{ fontSize: '2rem' }} />
                    </IconButton>
                    <Typography variant="body1" align="center" style={{ fontSize: '0.875rem' }}>
                        Upload your resume and cover letter for improved, tailored questions!
                    </Typography>
                </Box>
            </Box>

            {/* Generate Questions Button */}
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
                onClick={handleGenerateQuestions}
            >
                Generate Questions
            </Button>
        </Container>
    );
};

export default JobSelectionPage;
