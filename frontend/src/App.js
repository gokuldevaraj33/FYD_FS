import React, { useState } from 'react'; // Import React and the useState hook for state management
import './App.css';
function UploadForm() {
  // Declare state variables: 'file' for the selected file, 'downloadUrl' for the download link
  const [file, setFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState('');

  // Handle file input change event
  const handleChange = (e) => setFile(e.target.files[0]); // Set 'file' to the selected file

  // Handle form submission event
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the default form submission behavior
    setDownloadUrl(''); // Clear any previous download link
    const formData = new FormData(); // Create a new FormData object for file upload
    formData.append('document', file); // Append the selected file to the FormData

    // Send the file to the backend API endpoint using fetch
    const res = await fetch('http://localhost:5000/analyze', {
      method: 'POST', // Use POST method for file upload
      body: formData, // Set the request body to the FormData containing the file
    });
    const data = await res.json(); // Parse the JSON response from the backend

    // If the backend returns a filename, set the download URL for the processed file
    if (data.filename) {
      setDownloadUrl(`http://localhost:5000/download/${data.filename}`);
    }
  };

return (
  <div className="container">
    <form className="upload-form" onSubmit={handleSubmit}>
      <input
        type="file"
        accept=".pdf,.docx,.txt"
        onChange={handleChange}
        className="file-input"
      />
      <button type="submit" className="upload-btn">
        Upload and Process
      </button>
    </form>
    {downloadUrl && (
      <a href={downloadUrl} download className="download-link">
        <button type="button" className="download-btn">
          Download Processed Document
        </button>
      </a>
    )}
  </div>
);

}

export default UploadForm; // Export the UploadForm component for use in other parts of the app



