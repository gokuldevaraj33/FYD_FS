import React, { useState, useEffect } from 'react';
import './App.css';

function UploadForm() {
  const [file, setFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [isDragActive, setIsDragActive] = useState(false);
  const allowedTypes = [
  'application/pdf',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'text/plain'
];

  // Prevent browser from opening files when dropped outside the drop area
  useEffect(() => {
    const preventDefault = (e) => e.preventDefault();
    window.addEventListener('dragover', preventDefault);
    window.addEventListener('drop', preventDefault);
    return () => {
      window.removeEventListener('dragover', preventDefault);
      window.removeEventListener('drop', preventDefault);
    };
  }, []);

  // Handle file input change
  const handleChange = (e) => {
  const selected = e.target.files[0];
  if (selected && !allowedTypes.includes(selected.type)) {
    setError('Unsupported file type. Please upload a PDF, DOCX, or TXT file.');
    setFile(null);
    return;
  }
  setError('');
  setFile(selected);
};


  // Handle file drop
  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
  const dropped = e.dataTransfer.files[0];
  if (!allowedTypes.includes(dropped.type)) {
    setError('Unsupported file type. Please upload a PDF, DOCX, or TXT file.');
    setFile(null);
    return;
  }
  setError('');
  setFile(dropped);
}

  };

  // Highlight drop area on drag over
  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragActive(true);
  };

  // Remove highlight when drag leaves
  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragActive(false);
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setDownloadUrl('');
    setError('');
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('document', file);

      const res = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        body: formData,
      });
      if (!res.ok) throw new Error('Upload failed');
      const data = await res.json();

      if (data.filename) {
        setDownloadUrl(`http://localhost:5000/download/${data.filename}`);
      } else {
        setError('Processing failed. Please try again.');
      }
    } catch (err) {
      setError('An error occurred. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div className="bg-container">
      <div className="center-box">
        {/* Loading Spinner Overlay */}
        {loading && (
          <div className="loading-overlay">
            <div className="spinner"></div>
            <p>Processing your document...</p>
          </div>
        )}
        {/* Error Message */}
        {error && <div className="error-message">{error}</div>}

        <h1 className="headline">Upload Your Document</h1>
        <p className="subtext">Supported formats: PDF, DOCX, TXT</p>

        <form className="upload-form" onSubmit={handleSubmit}>
          {/* Drop area wraps only the file input and file name */}
          <div
            className={`drop-area${isDragActive ? ' drag-active' : ''}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
          >
            <label htmlFor="upload" className="upload-btn">
              Choose File
              <input
                id="upload"
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleChange}
                className="file-input"
                style={{ display: 'none' }}
                aria-label="Upload document file"
              />
            </label>
            {/* Consistent space for filename */}
            <div className="filename-container">
              {file ? (
                <p className="filename">Selected: {file.name}</p>
              ) : (
                <div className="filename-placeholder"></div>
              )}
            </div>
            {isDragActive && (
              <div className="drop-message">Drop your file here!</div>
            )}
          </div>
          {/* Submit button is outside drop area for spacing */}
          <button type="submit" className="process-btn" disabled={!file}>
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
    </div>
  );
}

export default UploadForm;
