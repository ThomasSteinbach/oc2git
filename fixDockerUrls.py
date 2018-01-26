#
# This python script would recreate the original image source of image streams
# in oc exports (issue https://github.com/openshift/origin/issues/16531).
# It also removes the 'kubectl.kubernetes.io/last-applied-configuration' information
# to create leaner exports.

import sys
import yaml
import re

if len(sys.argv) < 2:
    print("Please provide export file path and project name as arguments")
    sys.exit(1)

filename = sys.argv[1]
projectname = sys.argv[2]

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

        is_meta_annot=i['metadata']['annotations']
        if 'openshift.io/image.dockerRepositoryCheck' in is_meta_annot:
          del is_meta_annot['openshift.io/image.dockerRepositoryCheck']

        spec_tags = i['spec']['tags'][0]
        if spec_tags['annotations'] is not None:
            spec_tags['from']['name'] = spec_tags['annotations']['openshift.io/imported-from']
    if(i['kind'] == 'PersistentVolumeClaim'):
      pvc_meta_annot = i['metadata']['annotations']
      if 'control-plane.alpha.kubernetes.io/leader' in pvc_meta_annot:
        del pvc_meta_annot['control-plane.alpha.kubernetes.io/leader']
      if 'pv.kubernetes.io/bind-completed' in pvc_meta_annot:
        del pvc_meta_annot['pv.kubernetes.io/bind-completed']
      if 'pv.kubernetes.io/bound-by-controller' in pvc_meta_annot:
        del pvc_meta_annot['pv.kubernetes.io/bound-by-controller']
      if 'volumeName' in i['spec']:
        del i['spec']['volumeName']

stream = yaml.dump(fExport, default_flow_style=False)

# fix date formats
stream = re.sub('(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})',r'\1T\2Z',stream)
stream = stream.replace(projectname, 'OC_PROJECT_NAME')
stream = stream.replace('\n\n        \'', '\'')

with open(sys.argv[1], "w") as f:
    f.write(stream)
