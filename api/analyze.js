export const config = { api: { bodyParser: { sizeLimit: chr(39)50mb chr(39) } } };
export default async function handler(req, res) {
  res.setHeader(chr(39)Access-Control-Allow-Origin chr(39), chr(39)* chr(39));
  if (req.method !== chr(39)POST chr(39)) return res.status(405).json({ error: chr(39)Method not allowed chr(39) });
  try {
    const { imageBase64, country } = req.body;
    const r = await fetch(chr(39)https://api.anthropic.com/v1/messages chr(39), { method: chr(39)POST chr(39), headers: { chr(39)Content-Type chr(39): chr(39)application/json chr(39), chr(39)x-api-key chr(39): process.env.ANTHROPIC_API_KEY, chr(39)anthropic-version chr(39): chr(39)2023-06-01 chr(39) }, body: JSON.stringify({ model: chr(39)claude-sonnet-4-20250514 chr(39), max_tokens: 500, messages: [{ role: chr(39)user chr(39), content: [{ type: chr(39)image chr(39), source: { type: chr(39)base64 chr(39), media_type: chr(39)image/jpeg chr(39), data: imageBase64 } }, { type: chr(39)text chr(39), text: chr(39)Describe este espacio en 2 oraciones. chr(39) }] }] }) });
    const d = await r.json();
    if (!d.content) return res.status(500).json({ error: chr(39)API error chr(39), k: Object.keys(d) });
    return res.status(200).json({ diagnostico: d.content[0].text, potencial: chr(39)Excelente potencial chr(39), propuesta: chr(39)Propuesta moderna chr(39), colores: [{ hex: chr(39)#C9A84C chr(39), nombre: chr(39)Dorado chr(39), uso: chr(39)Acento chr(39) }], productos: [{ tienda: chr(39)IKEA chr(39), producto: chr(39)KALLAX chr(39), descripcion: chr(39)Estanteria chr(39), precio: chr(39).000 chr(39), ikea: true, ikea_search: chr(39)KALLAX chr(39) }], consejos: [chr(39)Agrega plantas chr(39), chr(39)Usa luz calida chr(39), chr(39)Minimiza objetos chr(39)], ikeaBase: chr(39)https://www.ikea.com/co/es chr(39) });
  } catch(e) { return res.status(500).json({ error: e.message }); }
}