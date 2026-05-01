import React from 'react';
import { Link } from 'react-router-dom';
import { MapPin, Maximize, TrendingDown, TrendingUp } from 'lucide-react';

const ApartmentCard = ({ apartment }) => {
  const isGoodDeal = apartment.price_diff > 0;
  const priceDiff = Math.abs(apartment.price_diff);
  const priceDiffPercent = ((priceDiff / apartment.price) * 100).toFixed(1);

  return (
    <Link to={`/apartment/${apartment.sreality_id}`} className="apartment-card">
      <div className="apartment-card-header">
        <h3>Prague {apartment.district}</h3>
        {apartment.price_diff && (
          <span className={`apartment-card-badge ${isGoodDeal ? 'apartment-card-badge-good' : 'apartment-card-badge-bad'}`}>
            {isGoodDeal ? <TrendingDown size={14} /> : <TrendingUp size={14} />}
            <span>{isGoodDeal ? 'Good Deal' : 'Overpriced'}</span>
            <span>{isGoodDeal ? '-' : '+'}{priceDiffPercent}%</span>
          </span>
        )}
      </div>

      <div className="apartment-card-details">
        <p><MapPin size={14} /> {apartment.distance_to_local_hub.toFixed(1)} km to center</p>
        <p><Maximize size={14} /> {apartment.area_m2} m²</p>
      </div>

      <div className="apartment-card-price-container">
        <p className="apartment-card-price">{apartment.price.toLocaleString('cs-CZ')} CZK</p>
        {apartment.predicted_price && (
          <p className="apartment-card-predicted-price">
            ML Estimate: {apartment.predicted_price.toLocaleString('cs-CZ')} CZK
          </p>
        )}
      </div>
    </Link>
  );
};

export default ApartmentCard;
