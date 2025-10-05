import { useState } from "react";
import "./App.css";

function App() {
  const [city, setCity] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);

  // ---- Upload handler ----
  const handleUpload = async (e) => {
    const file = e.target.files[0];
    setUploadedFile(file);
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://127.0.0.1:8000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    console.log(data);
    alert(`Uploaded: ${data.filename}`);
  };

  // ---- Weather handler ----
  const getWeather = async () => {
    if (!city) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(`http://127.0.0.1:8000/weather?city=${city}`);
      const data = await response.json();

      if (data.error) {
        setError(data.error);
      } else {
        // Enrich clothing recommendation with weather condition
        let recommendation = data.recommendation;
        if (data.weather) {
          const desc = data.weather.toLowerCase();
          if (desc.includes("rain")) {
            recommendation += " 🌧️ Bring an umbrella!";
          }
          if (desc.includes("snow")) {
            recommendation += " ❄️ Wear boots and gloves.";
          }
          if (desc.includes("wind")) {
            recommendation += " 💨 A windbreaker will help.";
          }
        }
        setResult({ ...data, recommendation });
      }
    } catch (err) {
      setError("Failed to fetch weather.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h1>FitForecast 👕🧥</h1>

      {/* Upload Section */}
      <section style={{ marginBottom: "30px" }}>
        <h2>Upload a Garment</h2>
        <input type="file" onChange={handleUpload} />
        {uploadedFile && <p>Last uploaded: {uploadedFile.name}</p>}
      </section>

      {/* Weather Section */}
      <section>
        <h2>Weather Clothing Recommendation</h2>
        <input
          type="text"
          placeholder="Enter a city"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          style={{ padding: "8px", marginRight: "8px" }}
        />
        <button onClick={getWeather} style={{ padding: "8px 12px" }}>
          Get Recommendation
        </button>

        {loading && <p>Loading...</p>}
        {error && <p style={{ color: "red" }}>{error}</p>}

        {result && (
          <div
            style={{
              marginTop: "20px",
              padding: "15px",
              border: "1px solid #ddd",
              borderRadius: "8px",
            }}
          >
            <h3>{result.city}</h3>
            <p>
              <b>Temperature:</b> {result.temperature}°C
            </p>
            {result.weather && (
              <p>
                <b>Condition:</b> {result.weather}
              </p>
            )}
            <p style={{ fontSize: "1.1em" }}>{result.recommendation}</p>
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
