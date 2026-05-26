analyze_code = """export const config = { api: { bodyParser: { sizeLimit: '50mb' } } };
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  if (req.method !== 'POST') return res.status(405).json({ error: 'not allowed' });
  try {
    const { imageBase64, country } = req.body;
    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-api-key': process.env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
      body: JSON.stringify({ model: 'claude-sonnet-4-20250514', max_tokens: 500, messages: [{ role: 'user', content: [{ type: 'image', source: { type: 'base64', media_type: 'image/jpeg', data: imageBase64 } }, { type: 'text', text: 'Describe este espacio en JSON: {diagnostico,potencial,propuesta,colores:[{hex,nombre,uso}],productos:[{tienda,producto,descripcion,precio,ikea,ikea_search}],consejos:[]}' }] }] })
    });
    const d = await r.json();
    if (!d.content) return res.status(500).json({ error: 'API error', detail: JSON.stringify(d) });
    const txt = d.content[0].text;
    const m = txt.match(/\{[\s\S]*\}/);
    if (!m) return res.status(500).json({ error: 'no json', raw: txt });
    const result = JSON.parse(m[0]);
    result.ikeaBase = 'https://www.ikea.com/co/es';
    return res.status(200).json(result);
  } catch(e) { return res.status(500).json({ error: e.message }); }
}"""

with open('api/analyze.js', 'w', encoding='utf-8') as f:
    f.write(analyze_code)
print('OK')
