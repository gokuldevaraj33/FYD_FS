// Import required modules
const express = require('express');
const multer = require('multer');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 5000;

// Enable CORS so your frontend can talk to the backend
app.use(cors());

// Set up Multer for file uploads (files go into 'uploads' folder)
const upload = multer({ dest: 'uploads/' });

// Endpoint to handle file upload and simulate processing
app.post('/analyze', upload.single('document'), async (req, res) => {
  // Simulate processing: copy uploaded file to a new name
  const originalPath = req.file.path;
  const processedFilename = `processed_${Date.now()}.docx`;
  const processedPath = path.join(__dirname, processedFilename);

  fs.copyFileSync(originalPath, processedPath);

  // Respond with the filename for download
  res.json({ filename: processedFilename });
});

// Endpoint to serve the processed file for download
app.get('/download/:filename', (req, res) => {
  const filename = req.params.filename;
  const filePath = path.join(__dirname, filename);
  res.download(filePath);
});

// Start the server
app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});
