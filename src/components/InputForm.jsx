import React, { useState } from 'react';
import axios from 'axios';

const InputForm = () => {
  const [description, setDescription] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('/generate', {
        description,
      }, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'generated_app.zip');
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      console.error('Error generating app:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">App Generator</h1>
      <textarea
        className="w-full p-2 border rounded mb-4"
        rows="4"
        placeholder="Describe your app (e.g., A to-do list app with login)"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />
      <button
        type="submit"
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Generate App
      </button>
    </form>
  );
};

export default InputForm;