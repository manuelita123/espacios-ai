import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = 'function processFile(file){const reader=new FileReader();reader.onload=e=>{uploadedImageBase64=e.target.result.split(\',\')[1];document.getElementById(\'preview-img\').src=e.target.result;document.getElementById(\'preview-container\').style.display=\'block\';zone.style.display=\'none\';checkReady()};reader.readAsDataURL(file)}'

new = '''function processFile(file){
  const canvas=document.createElement('canvas');
  const img=new Image();
  const reader=new FileReader();
  reader.onload=e=>{
    img.onload=()=>{
      const MAX=800;
      let w=img.width,h=img.height;
      if(w>h){if(w>MAX){h=h*(MAX/w);w=MAX;}}else{if(h>MAX){w=w*(MAX/h);h=MAX;}}
      canvas.width=w;canvas.height=h;
      canvas.getContext('2d').drawImage(img,0,0,w,h);
      const compressed=canvas.toDataURL('image/jpeg',0.7);
      uploadedImageBase64=compressed.split(',')[1];
      document.getElementById('preview-img').src=compressed;
      document.getElementById('preview-container').style.display='block';
      zone.style.display='none';
      checkReady();
    };
    img.src=e.target.result;
  };
  reader.readAsDataURL(file);
}'''

content = content.replace(old, new)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('index.html actualizado OK')
