import React, { useState } from 'react';
import axios from 'axios';
import BlogCards from './BlogCards';

export default function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setResponse('');
    try {
      const res = await axios.post('/api/query', { query });
      setResponse(res.data.response || 'No response received.');
    } catch (err) {
      setError('Error fetching response.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <React.Fragment>
      {/* Decorative marketing emoji icons */}
      <div className="side-icon left" style={{position: 'fixed', top: '20%', left: '60px', width: '80px', height: '80px', fontSize: '64px', opacity: 0.18, zIndex: 0, pointerEvents: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <span role="img" aria-label="idea">💡</span>
      </div>
      <div className="side-icon right" style={{position: 'fixed', top: '20%', right: '60px', width: '80px', height: '80px', fontSize: '64px', opacity: 0.18, zIndex: 0, pointerEvents: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <span role="img" aria-label="growth">📈</span>
      </div>

      <div className="container">
        <h1>Marketing Blogs Agent</h1>
        <form onSubmit={handleSubmit} className="form">
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="Ask about marketing blogs..."
            className="input"
            required
          />
          <button type="submit" className="button" disabled={loading}>
            {loading ? 'Loading...' : 'Submit'}
          </button>
        </form>
        {error && <div className="error">{error}</div>}
        {response && (
          <div className="response">
            <h2>Response</h2>
            <p>{response}</p>
          </div>
        )}
        <BlogCards />
      </div>
    </React.Fragment>
  );
}
