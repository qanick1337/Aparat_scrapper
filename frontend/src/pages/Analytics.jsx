import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Link } from 'react-router-dom';
import { ArrowLeft, Check, X, MapPin, Maximize, Coins, BrainCircuit, ExternalLink } from 'lucide-react';
import api from '../api';

const Analytics = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    api.get('analytics/')
      .then(response => {
        const formattedData = response.data.map(item => ({
          name: `Prague ${item.district}`,
          "AVG price (CZK)": Math.round(item.avg_price),
          "Total apartments": item.total_apartments,
          "Min price apartment": item.min_price,
          "Max price apartment": item.max_price,
          "AVG price per m2": item.avg_price_per_m2,
          "Median price": item.median_price
        }));
        setData(formattedData);
      })
      .catch(err => console.error("Помилка завантаження аналітики", err));
  }, []);

  return (
    <div>
    <Link to="/">
        <button className="apartment-back-btn">
            <ArrowLeft size={18} /> Back to the list
        </button>
    </Link>
      <h1>Apartments data analytics</h1>
      <p>Average rent for a 1+kk flat by district in Prague</p>

      <div style={{ width: '100%', height: 400, marginTop: '40px', backgroundColor: '#fcfcfc', padding: '20px', borderRadius: '12px' }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis yAxisId="left" orientation="left" stroke="#8884d8" />
            <YAxis yAxisId="right" orientation="right" stroke="#82ca9d" />
            <Tooltip formatter={(value) => value.toLocaleString('cs-CZ')} />
            <Legend />
            <Bar yAxisId="left" dataKey="AVG price (CZK)" fill="#8884d8" name="AVG price" />
            <Bar yAxisId="right" dataKey="Total apartments" fill="#82ca9d" name="Total apartments" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <p>Minimum rent price for a 1+kk flat by district in Prague</p>
      <div style={{ width: '100%', height: 400, marginTop: '40px', backgroundColor: '#fcfcfc', padding: '20px', borderRadius: '12px' }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis yAxisId="left" orientation="left" stroke="#84bdd8" />
            <Tooltip formatter={(value) => value.toLocaleString('cs-CZ')} />
            <Legend />
            <Bar yAxisId="left" dataKey="Min price apartment" fill="#84bdd8" name="Min price apartment" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <p>Maximum rent price for a 1+kk flat by district in Prague</p>
      <div style={{ width: '100%', height: 400, marginTop: '40px', backgroundColor: '#fcfcfc', padding: '20px', borderRadius: '12px' }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis yAxisId="left" orientation="left" stroke="#caa182" />
            <Tooltip formatter={(value) => value.toLocaleString('cs-CZ')} />
            <Legend />
            <Bar yAxisId="left" dataKey="Max price apartment" fill="#caa182" name="Max price apartment" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <p>Average price per m² and median price for a 1+kk flat by district in Prague</p>
      <div style={{ width: '100%', height: 400, marginTop: '40px', backgroundColor: '#fcfcfc', padding: '20px', borderRadius: '12px' }}>
        <ResponsiveContainer>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis yAxisId="left" orientation="left" stroke="#456ef3" />
            <YAxis yAxisId="right" orientation="right" stroke="#e2df97" />
            <Tooltip formatter={(value) => value.toLocaleString('cs-CZ')} />
            <Legend />
            <Bar yAxisId="left" dataKey="AVG price per m2" fill="#456ef3" name="AVG price per m²" />
            <Bar yAxisId="right" dataKey="Median price" fill="#e2df97" name="Median price" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      
    </div>
    
  );
};

export default Analytics;