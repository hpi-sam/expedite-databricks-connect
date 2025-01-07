import React, { useState } from 'react';
import InputCodeEditor from '../components/InputCodeEditor';
import OutputCodeEditor from '../components/OutputCodeEditor';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import CircularProgress from '@mui/material/CircularProgress'; // For loading indicator
import Snackbar from '@mui/material/Snackbar'; // For notifications
import Alert from '@mui/material/Alert';

import './Pages.css';

const StartPage = () => {
  const [inputCode, setInputCode] = useState(`# Copy and paste your legacy code in this editor
"""
Example Code:
"""
class PythonLinter:
    def __init__(self):
        self.matchers: List[Matcher] = []

    def add_matcher(self, matcher: Matcher):
        """Add a matcher to the linter."""
        self.matchers.append(matcher)

    def lint(self, code: str) -> List[Dict]:
        """Parse code and run all matchers on the AST."""
        tree = ast.parse(code)
        diagnostics = []

        for node in ast.walk(tree):
            for matcher in self.matchers:
                diagnostics.extend(matcher.lint(node))
`);

  const [outputCode, setOutputCode] = useState('');
  const [loading, setLoading] = useState(false);
  const [snackbarOpen, setSnackbarOpen] = useState(false);
  const [snackbarMessage, setSnackbarMessage] = useState('');
  const [snackbarSeverity, setSnackbarSeverity] = useState('success');

  const handleButtonClick = async (event) => {
    event.preventDefault(); // Prevent default behavior if inside a form

    if (inputCode.trim() === '') {
      setOutputCode('Please enter code to migrate.');
      setSnackbarMessage('Please enter code to migrate.');
      setSnackbarSeverity('warning');
      setSnackbarOpen(true);
      return;
    }

    setLoading(true); // Start loading
    setOutputCode(''); // Optional: Clear previous output

    try {
      const response = await fetch('/api/migrate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: inputCode })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.error || 'Unknown error'}`);
      }

      const data = await response.json();
      setOutputCode(data.result);
      setSnackbarMessage('Migration successful!');
      setSnackbarSeverity('success');
      setSnackbarOpen(true);
    } catch (error) {
      console.error('Error:', error);
      setOutputCode('An error occurred while migrating the code.');
      setSnackbarMessage('Migration failed.');
      setSnackbarSeverity('error');
      setSnackbarOpen(true);
    } finally {
      setLoading(false); // End loading
    }
  };

  return (
    <>
      <div className="page-container">
        <div className="editors-container">
          <div className="left-box">
            <InputCodeEditor code={inputCode} setCode={setInputCode} />
          </div>
          <div className="right-box">
            <OutputCodeEditor code={outputCode} />
          </div>
        </div>
        <div className="center-button">
          <Stack spacing={2} direction="row">
            <Button 
              type="button" 
              variant="contained" 
              onClick={handleButtonClick}
              disabled={loading}
              style={{ backgroundColor: '#b20036'}}
              startIcon={loading && <CircularProgress size={20} />}
            >
              {loading ? 'Migrating...' : 'Migrate'}
            </Button>
          </Stack>
        </div>
      </div>
      <Snackbar 
        open={snackbarOpen} 
        autoHideDuration={3000} 
        onClose={() => setSnackbarOpen(false)}
      >
        <Alert onClose={() => setSnackbarOpen(false)} severity={snackbarSeverity} sx={{ width: '100%' }}>
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </>
  );
};

export default StartPage;
