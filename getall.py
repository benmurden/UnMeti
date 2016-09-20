import urllib2
import json
import os
import errno

protocol = 'https'
domain = 'photo.kankouyohou.com'
prefectures_path = '/json/prefectures.json'

response = urllib2.urlopen('{prot}://{domain}{path}'.format(prot=protocol, domain=domain, path=prefectures_path))
data = json.loads(response.read())

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

for prefecture in data:
    make_sure_path_exists(prefecture['name_en'])

    for image in prefecture['images']:
        response = urllib2.urlopen('{prot}://{domain}{path}'.format(prot=protocol, domain=domain, path=image['path']))
        filename = image['path'].split('/')[-1].strip()

        with open('{dir}/{file}'.format(dir=prefecture['name_en'], file=filename), 'wb') as out:
            out.write(response.read())
            out.close()
