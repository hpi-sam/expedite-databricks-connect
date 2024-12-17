import React from 'react';
import { saveAs } from 'file-saver';
import '../styles/ButtonStyles.css';

function ProcessButton({ label }) {
    async function handleDownload() {
        try {
            // Fetch the ZIP file from the Flask backend
            const response = await fetch('/api/download-results', {
                method: 'GET',
            });

            if (!response.ok) {
                throw new Error('Failed to download the file');
            }

            // Get the file blob
            const blob = await response.blob();

            // Trigger file download
            saveAs(blob, 'results.zip');
        } catch (error) {
            console.error('Error while downloading the file:', error);
            alert('Error downloading the filtered Excel file: ' + error.message);
        }
    }

    return (
        <div>
            <button className="button-style" onClick={handleDownload}>{label}</button>
        </div>
    );
}

export default ProcessButton;
