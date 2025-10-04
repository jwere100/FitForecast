import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  handleUpload = async (e) => {
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    console.log(data); // should log { filename: "yourfile.jpg" }
  };

  return (
    <div>
      <h1>Upload a Garment</h1>
      <input type="file" onChange={handleUpload} />
    </div>
  );
}

export default App;

