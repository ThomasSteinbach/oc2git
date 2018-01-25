#
# This python script would recreate the original image source of image streams
# in oc exports (issue https://github.com/openshift/origin/issues/16531).
# It also removes the 'kubectl.kubernetes.io/last-applied-configuration' information
# to create leaner exports.

import sys
import yaml
import re

# load yaml to fExport variable
with open(sys.argv[1]) as f:
    fExport = yaml.load(f)

for i in fExport['items']:
    if 'status' in i:
      del i['status']
    if ('annotations' in i['metadata'] and
       'kubectl.kubernetes.io/last-applied-configuration' in i['metadata']['annotations']):
          del i['metadata']['annotations']['kubectl.kubernetes.io/last-applied-configuration']
    if(i['kind'] == 'ImageStream'):
        del i['metadata']['annotations']['openshift.io/image.dockerRepositoryCheck']
        tags = i['spec']['tags'][0]
        if tags['annotations'] is not None:
            tags['from']['name'] = tags['annotations']['openshift.io/imported-from']

stream = yaml.dump(fExport, default_flow_style=False)

# fix date formats
stream = re.sub('(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})',r'\1T\2Z',stream)

with open(sys.argv[1], "w") as f:
    f.write(stream.replace('\n\n        \'', '\''))
