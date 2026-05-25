import os
os.makedirs('api', exist_ok=True)

analyze = """export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  res.setHeader('Access-Control-Allow-Origin', '*');
  const { imageBase64, country, styles, budget } = req.body;
  const ikeaUrls = { 'Colombia':'https://www.ikea.com/co/es','Mexico':'https://www.ikea.com/mx/es','Chile':'https://www.ikea.com/cl/es','Peru':'https://www.ikea.com/pe/es' };
  const storeMap = { 'Colombia':'IKEA Colombia, Homecenter, Falabella','Mexico':'IKEA Mexico, Liverpool','Chile':'IKEA Chile, Falabella, Sodimac','Peru':'IKEA Peru, Falabella, Sodimac' };
  const budgetText = { economico:'hasta 500 USD',medio:'500-2000 USD',alto:'2000-10000 USD',premium:'sin limite' }[budget] || 'moderado';
  const stores = storeMap[country] || 'IKEA y tiendas locales';
  const prompt = 'Eres disenador de interiores experto. Analiza la foto y responde SOLO JSON sin markdown: ' + JSON.stringify({diagnostico:'...',potencial:'...',propuesta:'...',colores:[{hex:'#hex',nombre:'nombre',uso:'uso'}],productos:[{tienda:'tienda',producto:'producto',descripcion:'desc',precio:'precio',ikea:true,ikea_search:'termino'}],consejos:['consejo1']}) + ' Incluye 3 productos IKEA reales y 3 locales de ' + country + '. Estilo: ' + styles + '. Presupuesto: ' + budgetText;
  try {
    const r = await fetch('https://api.anthropic.com/v1/messages', { method:'POST', headers:{'Content-Type':'application/json','x-api-key':process.env.ANTHROPIC_API_KEY,'anthropic-version':'2023-06-01'}, body:JSON.stringify({ model:'claude-sonnet-4-20250514', max_tokens:1500, messages:[{role:'user',content:[{type:'image',source:{type:'base64',media_type:'image/jpeg',data:imageBase64}},{type:'text',text:prompt}]}]})});
    const d = await r.json();
    const result = JSON.parse(d.content.map(b=>b.text||'').join('').replace(/`json|`/g,'').trim());
    result.ikeaBase = ikeaUrls[country] || 'https://www.ikea.com';
    return res.status(200).json(result);
  } catch(e) { return res.status(500).json({ error: e.message }); }
}"""

with open('api/analyze.js', 'w', encoding='utf-8') as f:
    f.write(analyze)

print('analyze.js OK')
