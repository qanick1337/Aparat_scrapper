import React, {useState, useEffect} from 'react';
import Api from "../Api.js";
import ApartmentCard from "../components/ApartmentCard.jsx";

function ApartmentList() {
    const [apartments, setApartments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const [nextUrl, setNextUrl] = useState(null);
    const [prevUrl, setPrevUrl] = useState(null);
    const [totalCount, setTotalCount] = useState(0);
    const [currentPage, setCurrentPage] = useState(1);
    const [pageSize, setPageSize] = useState(20);

    const getPageNumberFromUrl = (url) => {
        if (!url) return 1;
        const pageMatch = url.match(/[?&]page=(\d+)/);
        return pageMatch ? parseInt(pageMatch[1]) : 1;
    };

    const getTotalPages = () => {
        return Math.ceil(totalCount / pageSize);
    };

    const total = getTotalPages();

    const getPageNumbers = () => {    
        const current = currentPage;
        const range = 1;
        const pages = [];

        for (let i = Math.max(1, current - range); i <= Math.min(total, current + range); i++) {
            pages.push(i);
        }

        return pages;
    };

    const fetchApartments = async (url = 'apartments/') => {
        setLoading(true);
        try {
            const isFullUrl = url.startsWith('http');
            const response = await (isFullUrl ? Api.get(url, {baseURL: ''}) : Api.get(url));

            setApartments(response.data.results);
            setNextUrl(response.data.next);
            setPrevUrl(response.data.previous);
            setTotalCount(response.data.count);
            setCurrentPage(getPageNumberFromUrl(url ||response.data.next || response.data.previous ));

            setLoading(false);
            window.scrollTo(0, 0);
        } catch (err) {
            console.error("Error while downloading:", err);
            setError("Unable to load the data.");
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchApartments();
    }, []);

    if (error) {
        return <div className="apartment-list-error">{error}</div>;
    }

    return (
        <div className="apartment-list-container">
            <h1>Real Estate Analytics (Prague)</h1>
            <p>Total found: {totalCount} offers</p>

            {loading ? (
                <div className="apartment-list-loading">Loading...</div>
            ) : (
                <>
                    <div className="apartment-list-cards">
                        {apartments.map((apt) => (
                            <ApartmentCard key={apt.id} apartment={apt}/>
                        ))}
                    </div>

                    <div className="apartment-list-pagination">
                        <button
                            onClick={() => fetchApartments(`apartments/?page=1`)}
                            disabled={currentPage == 1}
                            className="pagination-btn"
                        >
                            ← On the start
                        </button>

                        <div className="pagination-numbers">
                            {getPageNumbers().map((page) => (
                                <button
                                    key={page}
                                    onClick={() => fetchApartments(`apartments/?page=${page}`)}
                                    className={`pagination-number ${page === currentPage ? 'active' : ''}`}
                                >
                                    {page}
                                </button>
                            ))}
                        </div>

                        <button
                            onClick={() => fetchApartments(`apartments/?page=${total}`)}
                            disabled={currentPage == total}
                            className="pagination-btn"
                        >
                            On the last page →
                        </button>
                    </div>
                </>
            )}
        </div>
    );
}

export default ApartmentList;