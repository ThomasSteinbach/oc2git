#
# This python script would recreate the original image source of image streams
# in oc exports (issue https://github.com/openshift/origin/issues/16531).
# It also removes the 'kubectl.kubernetes.io/last-applied-configuration' information
# to create leaner exports.

import sys
import yaml
import re
from subprocess import check_output

if len(sys.argv) < 2:
    print("Please provide export file path and project name as arguments")
    sys.exit(1)

filename = sys.argv[1]
projectname = sys.argv[2]

# load yaml to fExport variable
with open(sys.argv[1]) as f:
    fExport = yaml.load(f)

imagestreams = yaml.load(check_output(["oc","get","is","-o","yaml"]))

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

        for tag in i['spec']['tags']:
          for imgstr in imagestreams['items']:
            if i['metadata']['name'] == imgstr['metadata']['name']:
              if 'tags' in imgstr['spec']:
                for istag in imgstr['spec']['tags']:
                  if tag['name'] == istag['name']:
                    tag['from']['name'] = istag['from']['name']

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
stream = re.sub('(image:\s+[\w\d.:_-]+\/)' + projectname + '(\/.*)',r'\1OC_PROJECT_NAME\2',stream)
stream = re.sub('(name:\s+[\w\d.:_-]+\/)' + projectname + '(\/.*)',r'\1OC_PROJECT_NAME\2',stream)
stream = re.sub('(host: .*)' + projectname + '(.*)', r'\1OC_PROJECT_NAME\2', stream)
stream = stream.replace('namespace: ' + projectname, 'namespace: OC_PROJECT_NAME')
stream = stream.replace('.' + projectname + '.svc', '.OC_PROJECT_NAME.svc')
stream = stream.replace('\n\n        \'', '\'')

with open(sys.argv[1], "w") as f:
    f.write(stream)
