import os

analyze = """export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });
  res.setHeader('Access-Control-Allow-Origin', '*');
  const { imageBase64, country, styles, budget } = req.body;
  const ikeaUrls = { 'Colombia':'https://www.ikea.com/co/es','Mexico':'https://www.ikea.com/mx/es','Chile':'https://www.ikea.com/cl/es','Peru':'https://www.ikea.com/pe/es' };
  const storeMap = { 'Colombia':'IKEA Colombia, Homecenter, Falabella','Mexico':'IKEA Mexico, Liverpool','Chile':'IKEA Chile, Falabella, Sodimac','Peru':'IKEA Peru, Falabella, Sodimac' };
  const budgetText = { economico:'hasta 500 USD',medio:'500-2000 USD',alto:'2000-10000 USD',premium:'sin limite' }[budget] || 'moderado';
  const stores = storeMap[country] || 'IKEA y tiendas locales';
  const prompt = 'Eres disenador de interiores experto en ' + country + '. Analiza la imagen y responde UNICAMENTE con JSON valido sin markdown, sin explicaciones, sin texto adicional. El JSON debe tener exactamente esta estructura: {"diagnostico":"texto","potencial":"texto","propuesta":"texto","colores":[{"hex":"#C9A84C","nombre":"Dorado","uso":"paredes"}],"productos":[{"tienda":"IKEA ' + country + '","producto":"KALLAX","descripcion":"Estanteria modular","precio":".000 COP","ikea":true,"ikea_search":"KALLAX estanteria"},{"tienda":"IKEA ' + country + '","producto":"MALM","descripcion":"Cama doble","precio":".000 COP","ikea":true,"ikea_search":"MALM cama"},{"tienda":"IKEA ' + country + '","producto":"BILLY","descripcion":"Librero","precio":".000 COP","ikea":true,"ikea_search":"BILLY librero"},{"tienda":"Homecenter","producto":"Sofa esquinero","descripcion":"Sofa gris","precio":".200.000 COP","ikea":false,"ikea_search":""},{"tienda":"Falabella","producto":"Mesa centro","descripcion":"Mesa madera","precio":".000 COP","ikea":false,"ikea_search":""},{"tienda":"Homecenter","producto":"Lampara piso","descripcion":"Lampara moderna","precio":".000 COP","ikea":false,"ikea_search":""}],"consejos":["Consejo 1","Consejo 2","Consejo 3"]}. Adapta los valores al espacio de la foto. Pais: ' + country + '. Estilo: ' + (styles||'contemporaneo') + '. Presupuesto: ' + budgetText;
  try {
    const r = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: { 'Content-Type':'application/json','x-api-key':process.env.ANTHROPIC_API_KEY,'anthropic-version':'2023-06-01' },
      body: JSON.stringify({ model:'claude-sonnet-4-20250514', max_tokens:2000, messages:[{role:'user',content:[{type:'image',source:{type:'base64',media_type:'image/jpeg',data:imageBase64}},{type:'text',text:prompt}]}]})
    });
    const d = await r.json();
    if (!d.content) return res.status(500).json({ error: 'API error', detail: JSON.stringify(d) });
    const txt = d.content.map(b=>b.text||'').join('').trim();
    const jsonMatch = txt.match(/\{[\s\S]*\}/);
    if (!jsonMatch) return res.status(500).json({ error: 'No JSON found', raw: txt });
    const result = JSON.parse(jsonMatch[0]);
    if (!result.productos) result.productos = [];
    if (!result.colores) result.colores = [];
    if (!result.consejos) result.consejos = [];
    result.ikeaBase = ikeaUrls[country] || 'https://www.ikea.com';
    return res.status(200).json(result);
  } catch(e) { return res.status(500).json({ error: e.message }); }
}"""

with open('api/analyze.js', 'w', encoding='utf-8') as f:
    f.write(analyze)
print('analyze.js actualizado OK')
