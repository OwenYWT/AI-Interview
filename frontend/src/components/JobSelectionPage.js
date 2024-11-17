import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Button, TextField, IconButton } from '@mui/material';
import UploadFileIcon from '@mui/icons-material/UploadFile';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { useNavigate } from 'react-router-dom';
import { getItem, setItem } from "../localStorage";
import { io } from "socket.io-client";

const socket = io("http://localhost:7230", {
    transports: ["websocket"],
    reconnectionAttempts: 5,
});

const JobSelectionPage = () => {
    const [job_description, setJobDescription] = useState('');
    const [resume_filename, setResumeFilename] = useState(null);
    const [resume_file, setResumeFile] = useState(null);
    const navigate = useNavigate();

    const roleDescriptions = {
        "Business Analyst": "Analyze business needs and develop data-driven solutions.",
        "Product Manager": "Lead product development, strategy, and lifecycle management.",
        "Software Engineer": "Develop and maintain software applications.",
        "Marketing Specialist": "Plan and execute marketing campaigns.",
        "Data Analyst": "Interpret data to drive business insights.",
        "UX/UI Designer": "Design user interfaces and optimize user experience.",
        "QA Engineer": "Test and ensure software quality and reliability.",
    };

    useEffect(() => {
        const savedDescription = getItem('job_description', '');
        const savedFileName = getItem('resume_filename', null);
        const savedFileContent = getItem('resume_file', null);

        setJobDescription(savedDescription);
        if (savedFileName) setResumeFilename(savedFileName);
        if (savedFileContent) setResumeFile(savedFileContent);

        socket.on('connect', () => {
            console.log('Connected to server');
        });

        socket.on('connect_error', (error) => {
            console.error('Connection Error:', error);
        });

        return () => {
            socket.off('connect');
            socket.off('connect_error');
        };
    }, []);

    const handleJobRoleClick = (role) => {
        const description = role === "Custom Job Description" ? "" : roleDescriptions[role];
        setJobDescription(description);
        setItem('job_description', description);
    };

    const handleGenerateQuestions = () => {
        const sessionID = Date.now();

        setItem('job_description', job_description);

        const payload = {
            session_id: sessionID,
            authorization_token: "our_auth_token",
            job_description: job_description,
            resume_filename: resume_filename,
            resume_file: resume_file,
        };
        socket.emit('init_simulation', payload);

        socket.on('upload_status', (status) => {
            if (status['success'] === true) {
                navigate('/info');
            } else {
                console.log("Backend server rejected", status);
            }
        });
    };

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        if (!file) {
            console.error('No file selected');
            return;
        }

        const maxFileSize = 3 * 1024 * 1024;
        if (file.size > maxFileSize) {
            console.error('File size exceeds the 3MB limit');
            alert('File size exceeds the 10MB limit. Please choose a smaller file.');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            const base64String = e.target.result.split(',')[1];
            setResumeFilename(file.name);
            setResumeFile(base64String);

            setItem('resume_filename', file.name);
            setItem('resume_file', base64String);
        };

        reader.onerror = (err) => {
            alert('Error reading file. Please try again.');
        };

        reader.readAsDataURL(file);
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

            <Box display="flex" flexWrap="wrap" justifyContent="center" gap={1} marginBottom={3}>
                {Object.keys(roleDescriptions).map((role) => (
                    <Button
                        key={role}
                        variant={job_description === roleDescriptions[role] ? "contained" : "outlined"}
                        color={job_description === roleDescriptions[role] ? "primary" : "default"}
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
                <Button
                    variant={job_description === '' ? "contained" : "outlined"}
                    color={job_description === '' ? "primary" : "default"}
                    onClick={() => handleJobRoleClick("Custom Job Description")}
                    style={{
                        borderRadius: '20px',
                        padding: '8px 16px',
                        textTransform: 'none',
                    }}
                >
                    Custom Job Description
                </Button>
            </Box>

            <Box style={{ maxWidth: '1500px', width: '100%', margin: '0 auto' }}>
                <TextField
                    placeholder="Select a job role above or enter a custom description"
                    multiline
                    rows={7}
                    fullWidth
                    variant="outlined"
                    value={job_description}
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
                <input
                    type="file"
                    accept=".pdf,.doc,.docx"
                    onChange={handleFileUpload}
                    style={{ display: 'none' }}
                    id="file-upload"
                />
                <label htmlFor="file-upload">
                    <IconButton component="span" style={{ marginBottom: '2px' }}>
                        <UploadFileIcon color="primary" style={{ fontSize: '2rem' }} />
                    </IconButton>
                </label>
                {resume_filename && (
                    <Typography variant="body2" align="center" style={{ fontSize: '0.875rem', marginTop: '10px' }}>
                        Uploaded file: {resume_filename}
                    </Typography>
                )}
                <Typography variant="body1" align="center" style={{ fontSize: '0.875rem' }}>
                    Optionally upload your resume and cover letter for improved, tailored questions!
                </Typography>
            </Box>

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
