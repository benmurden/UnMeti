from __future__ import unicode_literals
import urllib2
import json
import os
import errno

protocol = 'https'
domain = 'photo.kankouyohou.com'
prefectures_path = '/json/prefectures.json'

response = urllib2.urlopen('{prot}://{domain}{path}'.format(prot=protocol, domain=domain, path=prefectures_path))
content = response.read()

data = json.loads(content)
credits_content = '# Photo Credits\n'

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

for prefecture in data:
    make_sure_path_exists(prefecture['name_en'])
    credits_content += '## {name_en} ({name_jp})\n'.format(name_en=prefecture['name_en'], name_jp=prefecture['name'])

    images = []
    for image in prefecture['images']:
        image_url = '{prot}://{domain}{path}'.format(prot=protocol, domain=domain, path=image['path'])
        response = urllib2.urlopen(image_url)
        filename = image['path'].split('/')[-1].strip()
        credits_content += '### [{name_en} ({name_jp})]({link})\n'.format(name_en=image['name_en'], name_jp=image['name'], link=image_url)
        credits_content += 'Photo credit: {} ({})\n'.format(image['photographer_name_en'], image['photographer_name'])

        image_path = '{dir}/{file}'.format(dir=prefecture['name_en'], file=filename)

        with open(image_path, 'wb') as out:
            out.write(response.read())
            out.close()

        # Replace old image path with new one (as used in this repo)
        image['path'] = image_path

        # Don't need the download path - why a .zip of a .jpeg???
        image.pop('dl_path', None)

        # Image size given in kb is highly unhelpful when showing a download bar
        image['size'] = os.stat(image_path).st_size

        images.append(image)

    prefecture['images'] = images


with open('prefectures.json', 'w') as out:
    out.write(json.dumps(data, indent=2))
    out.close()

with open('CREDITS.md', 'w') as out:
    out.write(credits_content.encode('utf8'))
    out.close()
