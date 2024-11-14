import React, { useEffect, useState } from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import { getItem } from '../localStorage';
import { useNavigate } from 'react-router-dom';

const DisplayUploadedFilePage = () => {
    const [uploadedFile, setUploadedFile] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const savedFile = getItem('uploadedFile', null);
        if (savedFile) {
            setUploadedFile(savedFile);
        }
    }, []);

    const handleBack = () => {
        navigate('/');
    };

    return (
        <Container maxWidth="md" style={{ textAlign: 'center', padding: '20px' }}>
            <Typography variant="h4" gutterBottom style={{ fontWeight: 'bold', marginBottom: '30px' }}>
                Uploaded File
            </Typography>

            {uploadedFile ? (
                <Box
                    display="flex"
                    flexDirection="column"
                    alignItems="center"
                    justifyContent="center"
                    p={2}
                    border="1px solid #ccc"
                    borderRadius="8px"
                    style={{ backgroundColor: '#f9f9f9', marginBottom: '30px' }}
                >
                    <Typography variant="h6" gutterBottom>
                        File Name: {uploadedFile.name}
                    </Typography>
                    <Typography variant="body1" gutterBottom>
                        File Type: {uploadedFile.type}
                    </Typography>

                    {uploadedFile.type.startsWith('image/') ? (
                        <img
                            src={`data:${uploadedFile.type};base64,${uploadedFile.base64}`}
                            alt={uploadedFile.name}
                            style={{ maxWidth: '100%', height: 'auto', marginTop: '20px' }}
                        />
                    ) : uploadedFile.type === 'application/pdf' ? (
                        <embed
                            src={`data:application/pdf;base64,${uploadedFile.base64}`}
                            type="application/pdf"
                            width="100%"
                            height="500px"
                            style={{ marginTop: '20px' }}
                        />
                    ) : (
                        <Typography variant="body2" style={{ marginTop: '20px', color: '#666' }}>
                            File preview not available for this file type.
                        </Typography>
                    )}
                </Box>
            ) : (
                <Typography variant="body1" color="textSecondary">
                    No file uploaded.
                </Typography>
            )}

            <Button
                variant="contained"
                color="primary"
                onClick={handleBack}
                style={{ marginTop: '20px', borderRadius: '20px', padding: '10px 20px' }}
            >
                Back to Job Selection
            </Button>
        </Container>
    );
};

export default DisplayUploadedFilePage;
