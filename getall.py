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
with open('prefectures.json', 'w') as out:
    out.write(content)
    out.close()

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

    for image in prefecture['images']:
        image_url = '{prot}://{domain}{path}'.format(prot=protocol, domain=domain, path=image['path'])
        response = urllib2.urlopen(image_url)
        filename = image['path'].split('/')[-1].strip()
        credits_content += '### [{name_en} ({name_jp})]({link})\n'.format(name_en=image['name_en'], name_jp=image['name'], link=image_url)
        credits_content += 'Photo credit: {} ({})\n'.format(image['photographer_name_en'], image['photographer_name'])

        with open('{dir}/{file}'.format(dir=prefecture['name_en'], file=filename), 'wb') as out:
            out.write(response.read())
            out.close()

with open('CREDITS.md', 'w') as out:
    out.write(credits_content.encode('utf8'))
    out.close()
