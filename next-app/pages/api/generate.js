export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method not allowed' });
    return;
  }

  const { apiKey, data } = req.body || {};
  if (!apiKey || !data) {
    res.status(400).json({ error: 'Missing apiKey or data' });
    return;
  }

  try {
    const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`,
      },
      body: JSON.stringify({
        model: 'mixtral-8x7b-32768',
        messages: [
          { role: 'system', content: 'You are SubstackAssistant v1, an AI agent specialized in end-to-end Substack post creation and optimization. Follow the provided instructions and output JSON.' },
          { role: 'user', content: JSON.stringify(data) }
        ],
        temperature: 0.7
      })
    });
    const result = await response.json();
    res.status(200).json(result);
  } catch (err) {
    res.status(500).json({ error: 'Failed to contact Groq API' });
  }
}
