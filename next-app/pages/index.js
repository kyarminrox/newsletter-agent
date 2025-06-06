import { useState } from 'react';

const sampleInput = `{
  "previous_posts": [],
  "objective": "increase subscriber replies"
}`;

export default function Home() {
  const [apiKey, setApiKey] = useState('');
  const [input, setInput] = useState(sampleInput);
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setOutput('');

    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ apiKey, data: JSON.parse(input) }),
      });
      const json = await res.json();
      setOutput(JSON.stringify(json, null, 2));
    } catch (err) {
      setOutput('Error generating output');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: '0 auto', padding: 20 }}>
      <h1>SubstackAssistant v1</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="apiKey">Groq API Key:</label>
          <input
            id="apiKey"
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            style={{ width: '100%' }}
          />
        </div>
        <div style={{ marginTop: 10 }}>
          <label htmlFor="input">Input JSON:</label>
          <textarea
            id="input"
            rows={10}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            style={{ width: '100%' }}
          />
        </div>
        <button type="submit" disabled={loading} style={{ marginTop: 10 }}>
          {loading ? 'Generating...' : 'Generate'}
        </button>
      </form>
      <pre style={{ marginTop: 20, whiteSpace: 'pre-wrap' }}>{output}</pre>
    </div>
  );
}
