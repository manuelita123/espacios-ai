with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'const MAX=800;'
new = 'const MAX=400;'
content = content.replace(old, new)

old2 = 'canvas.toDataURL(\'image/jpeg\',0.7)'
new2 = 'canvas.toDataURL(\'image/jpeg\',0.4)'
content = content.replace(old2, new2)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('OK - imagen mas pequena')
