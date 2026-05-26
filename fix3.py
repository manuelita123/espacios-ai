with open('api/analyze.js', 'r', encoding='utf-8') as f:
    content = f.read()

old = "  const { imageBase64, country, styles, budget } = req.body;"
new = """  const { imageBase64, country, styles, budget } = req.body;
  if (!imageBase64) return res.status(400).json({ error: 'No image provided' });
  if (imageBase64.length > 500000) return res.status(413).json({ error: 'Image too large. Please use a smaller photo.' });"""

content = content.replace(old, new)
with open('api/analyze.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK')
