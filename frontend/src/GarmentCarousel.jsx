import { useEffect, useState } from "react";
import "./App.css";

// Clueless-inspired two-row carousel: tops (top row) and bottoms (bottom row)
export default function GarmentCarousel() {
  const [tops, setTops] = useState([]);
  const [bottoms, setBottoms] = useState([]);
  const [topIndex, setTopIndex] = useState(0);
  const [bottomIndex, setBottomIndex] = useState(0);
  const [showTryOn, setShowTryOn] = useState(false);

  useEffect(() => {
    const fetchGarments = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/garments");
        const data = await res.json();

        // map a few tolerant type names to tops/bottoms
        const topsData = data.filter(item => ["top", "shirt", "jacket", "coat"].includes((item.garment_type || "").toLowerCase()));
        const bottomsData = data.filter(item => ["bottom", "skirt", "pants", "jeans", "trousers"].includes((item.garment_type || "").toLowerCase()));

        setTops(topsData);
        setBottoms(bottomsData);
        setTopIndex(0);
        setBottomIndex(0);
      } catch (error) {
        console.error("Failed to fetch garments:", error);
      }
    };

    fetchGarments();
  }, []);

  // safe wrap helpers
  const next = (arr, idxSetter, idx) => {
    if (!arr.length) return;
    idxSetter((idx + 1) % arr.length);
  };
  const prev = (arr, idxSetter, idx) => {
    if (!arr.length) return;
    idxSetter((idx - 1 + arr.length) % arr.length);
  };

  const selectedTop = tops[topIndex];
  const selectedBottom = bottoms[bottomIndex];

  return (
    <div className="closet-container">
      <header className="closet-header">
        <h1 className="closet-title">Digital Closet</h1>
        <p className="closet-sub">pick a top and a bottom</p>
      </header>

      {/* TOP CAROUSEL */}
      <section className="carousel-row top-row">
        <h2 className="row-title">Tops</h2>
        <div className="carousel">
          <button className="arrow-btn left" onClick={() => prev(tops, setTopIndex, topIndex)} aria-label="Previous top">◀</button>

          <div className="slot">
            {tops.length > 0 ? (
              <div className="garment-card glossy" key={selectedTop.filename || topIndex}>
                <img src={selectedTop.image_url} alt={selectedTop.filename || 'Top'} className="garment-img" />
                <div className="garment-meta">
                  <span className="meta-type">{selectedTop.garment_type}</span>
                </div>
              </div>
            ) : (
              <div className="empty-card">No tops available</div>
            )}
          </div>

          <button className="arrow-btn right" onClick={() => next(tops, setTopIndex, topIndex)} aria-label="Next top">▶</button>
        </div>
      </section>

      {/* BOTTOM CAROUSEL */}
      <section className="carousel-row bottom-row">
        <h2 className="row-title">Bottoms</h2>
        <div className="carousel">
          <button className="arrow-btn left" onClick={() => prev(bottoms, setBottomIndex, bottomIndex)} aria-label="Previous bottom">◀</button>

          <div className="slot">
            {bottoms.length > 0 ? (
              <div className="garment-card glossy" key={selectedBottom.filename || bottomIndex}>
                <img src={selectedBottom.image_url} alt={selectedBottom.filename || 'Bottom'} className="garment-img" />
                <div className="garment-meta">
                  <span className="meta-type">{selectedBottom.garment_type}</span>
                </div>
              </div>
            ) : (
              <div className="empty-card">No bottoms available</div>
            )}
          </div>

          <button className="arrow-btn right" onClick={() => next(bottoms, setBottomIndex, bottomIndex)} aria-label="Next bottom">▶</button>
        </div>
      </section>

      <div className="match-area">
        <button className="match-btn" onClick={() => setShowTryOn(true)} disabled={!(selectedTop && selectedBottom)}>
          Try On ✨
        </button>
      </div>

      {/* Try-on modal / preview */}
      {showTryOn && (
        <div className="match-modal" onClick={() => setShowTryOn(false)}>
          <div className="match-card" onClick={(e) => e.stopPropagation()}>
            <h3 className="match-title">Try On</h3>
            <div className="match-preview">
              <div className="preview-column">
                {selectedTop ? <img src={selectedTop.image_url} alt="Selected top" /> : <div className="preview-empty">No top</div>}
                <div className="preview-label">Top</div>
              </div>

              <div className="preview-column">
                {selectedBottom ? <img src={selectedBottom.image_url} alt="Selected bottom" /> : <div className="preview-empty">No bottom</div>}
                <div className="preview-label">Bottom</div>
              </div>
            </div>

            <div className="match-actions">
              <button className="btn-secondary" onClick={() => setShowTryOn(false)}>Close</button>
              <button className="btn-primary" onClick={() => { /* placeholder for integration with AI try-on */ alert('Generating outfit preview...'); }}>Generate Preview</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}