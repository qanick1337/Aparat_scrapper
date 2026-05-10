import React, { useState, useEffect } from 'react';
import Api from '../Api.js';
import '../App.css'

function FilterPanel({ onFilterChange }) {
    const [filterOptions, setFilterOptions] = useState(null);
    const [filters, setFilters] = useState({
        price_min: '',
        price_max: '',
        area_min: '',
        area_max: '',
        district: '',
        metro: false,
        tram: false,
        elevator: false,
        garage: false,
        parking_lots: false,
        furnished: false,
        new_building: false,
        sort_by: '-updated_at'
    });

    useEffect(() => {
        const fetchFilterOptions = async () => {
            try {
                const response = await Api.get('filter-options/');
                setFilterOptions(response.data);
            } catch (err) {
                console.error('Error fetching filter options:', err);
            }
        };
        fetchFilterOptions();
    }, []);

    const handleRangeChange = (field, value) => {
        setFilters({
            ...filters,
            [field]: value
        });
    };

    const handleToggle = (field) => {
        setFilters({
            ...filters,
            [field]: !filters[field]
        });
    };

    const handleSortChange = (e) => {
        setFilters({
            ...filters,
            sort_by: e.target.value
        });
    };

    const applyFilters = () => {
        const params = new URLSearchParams();

        if (filters.price_min) params.append('price_min', filters.price_min);
        if (filters.price_max) params.append('price_max', filters.price_max);
        if (filters.area_min) params.append('area_min', filters.area_min);
        if (filters.area_max) params.append('area_max', filters.area_max);
        if (filters.district) params.append('district', filters.district);
        if (filters.metro) params.append('metro', 'true');
        if (filters.tram) params.append('tram', 'true');
        if (filters.elevator) params.append('elevator', 'true');
        if (filters.garage) params.append('garage', 'true');
        if (filters.parking_lots) params.append('parking_lots', 'true');
        if (filters.furnished) params.append('furnished', 'true');
        if (filters.new_building) params.append('new_building', 'true');
        if (filters.sort_by) params.append('sort_by', filters.sort_by);

        onFilterChange(`apartments/?${params.toString()}`);
    };

    const resetFilters = () => {
        setFilters({
            price_min: '',
            price_max: '',
            area_min: '',
            area_max: '',
            district: '',
            metro: false,
            tram: false,
            elevator: false,
            garage: false,
            parking_lots: false,
            furnished: false,
            new_building: false,
            sort_by: '-updated_at'
        });
        onFilterChange('apartments/');
    };

    if (!filterOptions) return <div className="filter-panel-loading">Loading filters...</div>;

    return (
        <div className="filter-panel">
            <div className="filter-header">
                <h3>Filters & Sort</h3>
                <button onClick={resetFilters} className="filter-reset-btn">Reset</button>
            </div>

            <div className="filter-section">
                <h4>Price (CZK)</h4>
                <div className="filter-range-group">
                    <input
                        type="number"
                        placeholder="Min"
                        value={filters.price_min}
                        onChange={(e) => handleRangeChange('price_min', e.target.value)}
                        className="filter-input"
                    />
                    <span>-</span>
                    <input
                        type="number"
                        placeholder="Max"
                        value={filters.price_max}
                        onChange={(e) => handleRangeChange('price_max', e.target.value)}
                        className="filter-input"
                    />
                </div>
                <div className="filter-range-hint">
                    Range: {filterOptions.price_range.min} - {filterOptions.price_range.max}
                </div>
            </div>

            <div className="filter-section">
                <h4>Area (m²)</h4>
                <div className="filter-range-group">
                    <input
                        type="number"
                        placeholder="Min"
                        value={filters.area_min}
                        onChange={(e) => handleRangeChange('area_min', e.target.value)}
                        className="filter-input"
                    />
                    <span>-</span>
                    <input
                        type="number"
                        placeholder="Max"
                        value={filters.area_max}
                        onChange={(e) => handleRangeChange('area_max', e.target.value)}
                        className="filter-input"
                    />
                </div>
                <div className="filter-range-hint">
                    Range: {filterOptions.area_range.min} - {filterOptions.area_range.max}
                </div>
            </div>

            <div className="filter-section">
                <h4>District</h4>
                <select
                    value={filters.district}
                    onChange={(e) => handleRangeChange('district', e.target.value)}
                    className="filter-select"
                >
                    <option value="">All Districts</option>
                    {filterOptions.districts.map((district) => (
                        <option key={district} value={district}>
                            Prague {district}
                        </option>
                    ))}
                </select>
            </div>

            <div className="filter-section">
                <h4>Amenities</h4>
                <div className="filter-checkboxes">
                    <label className="filter-checkbox">
                        <input
                            type="checkbox"
                            checked={filters.metro}
                            onChange={() => handleToggle('metro')}
                        />
                        <span>Metro</span>
                    </label>
                    <label className="filter-checkbox">
                        <input
                            type="checkbox"
                            checked={filters.tram}
                            onChange={() => handleToggle('tram')}
                        />
                        <span>Tram</span>
                    </label>
                    <label className="filter-checkbox">
                        <input
                            type="checkbox"
                            checked={filters.elevator}
                            onChange={() => handleToggle('elevator')}
                        />
                        <span>Elevator</span>
                    </label>
                    <label className="filter-checkbox">
                        <input
                            type="checkbox"
                            checked={filters.garage}
                            onChange={() => handleToggle('garage')}
                        />
                        <span>Garage</span>
                    </label>
                    <label className="filter-checkbox">
                        <input
                            type="checkbox"
                            checked={filters.parking_lots}
                            onChange={() => handleToggle('parking_lots')}
                        />
                        <span>Parking</span>
                    </label>
                </div>
            </div>

            <div className="filter-section">
                <h4>Furnishing</h4>
                <div className="filter-checkboxes">
                    <label className="filter-checkbox">
                        <input
                            type="checkbox"
                            checked={filters.furnished}
                            onChange={() => handleToggle('furnished')}
                        />
                        <span>Furnished</span>
                    </label>
                </div>
            </div>

            <div className="filter-section">
                <h4>Building</h4>
                <div className="filter-checkboxes">
                    <label className="filter-checkbox">
                        <input
                            type="checkbox"
                            checked={filters.new_building}
                            onChange={() => handleToggle('new_building')}
                        />
                        <span>New Building</span>
                    </label>
                </div>
            </div>

            <div className="filter-section">
                <h4>Sort By</h4>
                <select
                    value={filters.sort_by}
                    onChange={handleSortChange}
                    className="filter-select"
                >
                    <option value="-updated_at">Newest First</option>
                    <option value="price">Price: Low to High</option>
                    <option value="-price">Price: High to Low</option>
                    <option value="area_m2">Area: Small to Large</option>
                    <option value="-area_m2">Area: Large to Small</option>
                    <option value="predicted_price">Predicted Price: Low to High</option>
                    <option value="-predicted_price">Predicted Price: High to Low</option>
                    <option value="distance_to_local_hub">Distance: Close to Far</option>
                    <option value="-distance_to_local_hub">Distance: Far to Close</option>
                </select>
            </div>

            <button onClick={applyFilters} className="filter-apply-btn">
                Apply Filters
            </button>
        </div>
    );
}

export default FilterPanel;
