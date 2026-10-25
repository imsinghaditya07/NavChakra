/**
 * Serverless Route: /api/agent
 * Proxies requests to an Agent37 instance:
 * POST https://<ID>.agent37.app/v1/responses
 * Header: X-Agent37-Key (from process.env.AGENT37_KEY)
 *
 * Security:
 * - NEVER exposes AGENT37_KEY to the client
 * - Streams responses back to the caller
 */

export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).json({ error: 'Method Not Allowed. Use POST.' });
  }

  // Retrieve key and instance ID from environment (never hardcoded, never leaked)
  const apiKey = (process.env.AGENT37_KEY || process.env.AGENT37_API_KEY || '').trim();
  let instanceId = (process.env.AGENT37_INSTANCE_ID || '').trim();

  // If instanceId is not explicitly set, try extracting from AGENT37_INSTANCE_URL
  if (!instanceId && process.env.AGENT37_INSTANCE_URL) {
    try {
      const parsedUrl = new URL(process.env.AGENT37_INSTANCE_URL);
      instanceId = parsedUrl.hostname.split('.')[0];
    } catch (_) {
      // Ignore URL parse error
    }
  }

  // Check configuration
  if (!apiKey || !instanceId) {
    // If credentials are not set, stream a helpful development message rather than hard crashing
    res.setHeader('Content-Type', 'text/event-stream; charset=utf-8');
    res.setHeader('Cache-Control', 'no-cache, no-transform');
    res.setHeader('Connection', 'keep-alive');
    
    const fallbackMessage = '⚡ [Agent37 Notice]: AGENT37_KEY or AGENT37_INSTANCE_ID is not configured in environment variables. Please set AGENT37_KEY and AGENT37_INSTANCE_ID.';
    res.write(`data: ${JSON.stringify({ text: fallbackMessage, status: 'unconfigured' })}\n\n`);
    res.write('data: [DONE]\n\n');
    return res.end();
  }

  const targetUrl = `https://${instanceId}.agent37.app/v1/responses`;

  // Parse incoming payload safely
  let clientInput = '';
  let sessionId = undefined;
  let streamFlag = true;

  try {
    const body = typeof req.body === 'string' ? JSON.parse(req.body) : (req.body || {});
    clientInput = body.input || body.query || body.prompt || body.message || '';
    sessionId = body.session_id || undefined;
    if (typeof body.stream === 'boolean') {
      streamFlag = body.stream;
    }
  } catch (err) {
    return res.status(400).json({ error: 'Invalid JSON request payload' });
  }

  if (!clientInput.trim()) {
    return res.status(400).json({ error: 'Missing input/query in request body' });
  }

  // Construct upstream request payload
  const upstreamPayload = {
    input: clientInput.slice(0, 1000), // Bound max query length
    stream: streamFlag,
  };
  if (sessionId) {
    upstreamPayload.session_id = sessionId;
  }

  try {
    // Dispatch to Agent37 with private secret header
    const upstreamResponse = await fetch(targetUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream, application/json, text/plain',
        'X-Agent37-Key': apiKey // Injected privately on server, NEVER exposed to client
      },
      body: JSON.stringify(upstreamPayload)
    });

    if (!upstreamResponse.ok) {
      const errText = await upstreamResponse.text();
      return res.status(upstreamResponse.status).json({
        error: `Agent37 upstream error (${upstreamResponse.status})`,
        details: errText.slice(0, 200)
      });
    }

    // Set streaming headers
    res.setHeader('Content-Type', 'text/event-stream; charset=utf-8');
    res.setHeader('Cache-Control', 'no-cache, no-transform');
    res.setHeader('Connection', 'keep-alive');

    // Stream chunks as they arrive from Agent37
    if (upstreamResponse.body) {
      if (typeof upstreamResponse.body.getReader === 'function') {
        const reader = upstreamResponse.body.getReader();
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          res.write(value);
        }
        return res.end();
      } else if (typeof upstreamResponse.body.pipe === 'function') {
        return upstreamResponse.body.pipe(res);
      }
    }

    // Fallback if body is not a stream
    const responseText = await upstreamResponse.text();
    res.write(`data: ${JSON.stringify({ text: responseText })}\n\n`);
    res.write('data: [DONE]\n\n');
    return res.end();

  } catch (err) {
    return res.status(502).json({
      error: 'Failed to communicate with Agent37 upstream instance',
      message: err.message
    });
  }
}
