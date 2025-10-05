import { useState } from 'react';
import './App.css';
import GarmentCarousel from "./GarmentCarousel";
   // make sure this file exists in src/

function App() {
  // state hooks 
  const [preview, setPreview] = useState(null);
  const [garmentType, setGarmentType] = useState("");

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setPreview(URL.createObjectURL(file));

    const formData = new FormData();
    formData.append("file", file);
    formData.append("garment_type", garmentType);

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    console.log("Uploaded:", data);
  };

  return (
    <div className="App">
      <h1>Upload a Garment</h1>

      {/* File input */}
      <input type="file" onChange={handleUpload} />

      {/* Garment type selection */}
      <select value={garmentType} onChange={(e) => setGarmentType(e.target.value)}>
        <option value="">Select Type</option>
        <option value="skirt">Skirt</option>
        <option value="jacket">Jacket</option>
        <option value="top">Top</option>
        <option value="dress">Dress</option>
      </select>

      {/* Preview image */}
      {preview && <img src={preview} alt="Garment Preview" style={{ width: '200px' }} />}

      {/* Carousel below upload */}
      <GarmentCarousel />
    </div>
  );
}

export default App;