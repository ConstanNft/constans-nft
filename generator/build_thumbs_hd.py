"""Single-tier HD: 720px q85 — sharp for modal, manageable size."""
from PIL import Image
import io, base64, json, os, time

src_dir = '/home/ubuntu/formula-nft/output_v2'
out_path = '/home/ubuntu/formula-nft-web/items_hd.json'

with open(f'{src_dir}/collection.json') as f:
    coll = json.load(f)

t0 = time.time()
items = []
for item in coll['items']:
    tid = item['token_id']
    fname = item['image']
    im = Image.open(f'{src_dir}/{fname}').convert('RGB')
    im.thumbnail((720, 990), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=85, optimize=True, progressive=True)
    img_b64 = base64.b64encode(buf.getvalue()).decode('ascii')

    attrs = {a['trait_type']: a['value'] for a in item['attributes']}
    items.append({
        'id': tid,
        'name': item['name'],
        'desc': item['description'],
        'formula': attrs.get('Formula'),
        'code': attrs.get('Code'),
        'palette': attrs.get('Palette'),
        'year': attrs.get('Year'),
        'discoverer': attrs.get('Discoverer'),
        'sig': item.get('signature'),
        'img': img_b64,
    })
    if tid % 50 == 0:
        print(f'  {tid}/333 ({time.time()-t0:.1f}s)', flush=True)

with open(out_path, 'w') as f:
    json.dump({'items': items}, f, separators=(',', ':'))

sz = os.path.getsize(out_path)
print(f'Done in {time.time()-t0:.1f}s')
print(f'items_hd.json: {sz/1048576:.2f} MB')
