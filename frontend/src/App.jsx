import React, { useState } from 'react';
import axios from 'axios';
import toast, { Toaster } from 'react-hot-toast';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [processedImage, setProcessedImage] = useState(null);

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      // Check file type
      const fileType = file.type.split('/')[1];
      if (!['png', 'jpg', 'jpeg'].includes(fileType)) {
        toast.error('Please select a PNG, JPG, or JPEG image');
        return;
      }

      setSelectedFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      toast.error('Please select an image first');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('https://parking-production-3f64.up.railway.app/identify-parking', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Accept': 'image/jpeg',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST',
          'Access-Control-Allow-Headers': 'Content-Type'
        },
        responseType: 'arraybuffer',
        withCredentials: false
      });

      // Convert the binary data to base64
      const base64Image = btoa(
        new Uint8Array(response.data)
          .reduce((data, byte) => data + String.fromCharCode(byte), '')
      );
      const imageUrl = `data:image/jpeg;base64,${base64Image}`;
      setProcessedImage(imageUrl);
      toast.success('Image processed successfully!');
    } catch (error) {
      const errorMessage = error.response?.data?.message || error.message || 'Error processing image';
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl mx-auto space-y-8">
        {/* Main Card */}
        <div className="bg-white shadow-lg rounded-lg p-6">
          <h1 className="text-2xl font-bold text-center mb-8">Parking Space Detection</h1>
          
          <div className="space-y-6">
            {/* File Upload Area */}
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <input
                type="file"
                accept=".png,.jpg,.jpeg"
                onChange={handleFileSelect}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="cursor-pointer inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
              >
                Select Image
              </label>
              <p className="mt-2 text-sm text-gray-600">
                Supported formats: PNG, JPG, JPEG
              </p>
            </div>

            {/* Preview Area */}
            {preview && (
              <div className="mt-4">
                <p className="text-sm font-medium text-gray-700 mb-2">Preview:</p>
                <img
                  src={preview}
                  alt="Preview"
                  className="max-h-64 mx-auto rounded-lg"
                />
              </div>
            )}

            {/* Upload Button */}
            <button
              onClick={handleUpload}
              disabled={!selectedFile || loading}
              className={`w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white 
                ${!selectedFile || loading
                  ? 'bg-gray-400 cursor-not-allowed'
                  : 'bg-green-600 hover:bg-green-700'
                }`}
            >
              {loading ? 'Processing...' : 'Process Image'}
            </button>
          </div>
        </div>

        {/* Processed Image Card */}
        {processedImage && (
          <div className="bg-white shadow-lg rounded-lg p-6">
            <h2 className="text-xl font-bold mb-4">Processed Result</h2>
            <img
              src={processedImage}
              alt="Processed Result"
              className="w-full rounded-lg"
            />
          </div>
        )}
      </div>
      <Toaster position="top-right" />
    </div>
  );
}

export default App;