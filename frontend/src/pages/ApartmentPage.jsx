import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../Api';
import { ArrowLeft, Check, X, MapPin, Maximize, Coins, BrainCircuit, ExternalLink } from 'lucide-react';

const ApartmentDetail = () => {
  const { id } = useParams(); // Отримуємо ID з URL
  const navigate = useNavigate();
  const [apartment, setApartment] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`apartments/${id}/`)
      .then(res => {
        setApartment(res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setLoading(false);
      });
  }, [id]);

  if (loading) return <p>Loading object data...</p>;
  if (!apartment) return <p>Item not found</p>;

  const diff = apartment.predicted_price - apartment.price;
  const isGoodDeal = diff > 0;
  const srealityLink = `http://127.0.0.1:8000/api/apartments/${apartment.sreality_id}/redirect`;

  return (
    <div className="apartment-page-container">
      <button onClick={() => navigate(-1)} className="apartment-back-btn">
        <ArrowLeft size={18} /> Back to the list
      </button>

      <div className="apartment-main-info">
        <h1>1+kk, {apartment.area_m2} m², Prague {apartment.district}</h1>
        <p className="apartment-id">ID Sreality: {apartment.sreality_id}</p>

        <div className="apartment-grid">
          <div className="apartment-stat"><Coins /> <strong>{apartment.price.toLocaleString()} CZK</strong></div>
          <div className="apartment-stat"><Maximize /> <strong>{apartment.area_m2} m²</strong></div>
          <div className="apartment-stat"><MapPin /> <strong>{apartment.distance_to_local_hub.toFixed(2)} km to the local center</strong></div>
        </div>
      </div>


      <div>
        <div style={{ marginTop: '20px' }}>
            <a 
              href={srealityLink} 
              target="_blank"
            >
              Переглянути на Sreality <ExternalLink size={14} />
            </a>
          </div>
      </div>

      <div className="apartment-analysis" style={{borderColor: isGoodDeal ? '#48bb78' : '#f56565', borderLeftColor: isGoodDeal ? '#48bb78' : '#f56565'}}>
        <div className="apartment-analysis-header">
          <BrainCircuit color={isGoodDeal ? '#48bb78' : '#f56565'} size={24} />
          <h2>Market Value Analysis</h2>
        </div>
        <p>Model rating: <strong style={{color: isGoodDeal ? '#48bb78' : '#f56565'}}>{apartment.predicted_price?.toLocaleString()} CZK</strong></p>
        <p style={{color: isGoodDeal ? '#38a169' : '#e53e3e', fontWeight: 'bold', fontSize: '16px'}}>
          {isGoodDeal ? `✓ Great value for ${diff.toLocaleString()} CZK` : `✕ Overpayment of ${Math.abs(diff).toLocaleString()} CZK`}
        </p>
      </div>

      <div className="apartment-specs">
        <h3>Technical specifications</h3>
        <div className="apartment-specs-grid">
          <SpecItem label="Furnished" value={apartment.furnished} />
          <SpecItem label="Elevator" value={apartment.elevator} />
          <SpecItem label="Nearby metro" value={apartment.metro} />
          <SpecItem label="New building" value={apartment.new_building} />
          <SpecItem label="Brick" value={apartment.brick} />
          <SpecItem label="Parking" value={apartment.parking_lots} />
        </div>
      </div>
    </div>
  );
};

const SpecItem = ({ label, value }) => (
  <div className="apartment-spec-item">
    {value ? <Check size={16} color="green" /> : <X size={16} color="red" />}
    <span>{label}</span>
  </div>
);

export default ApartmentDetail;