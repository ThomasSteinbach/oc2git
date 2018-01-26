Track OpenShift API Objects in Git
==================================

This repository delivers two shell scripts to you, that allow you to easily maintain
your OpenShift API object in Git.

Installation
------------

On most Linux systems, where _/usr/local/bin_ is in your $PATH, just run

```
./install.sh
```

Otherwise you have to manually add symlinks of following files to your $PATH:

* oc-sync-git -> oc-sync-git.sh
* oc-edit     -> oc-edit.sh

Usage
-----

When using the default install script, the three commands `oc-sync-git`, `oc-edit` and `oc-apply`
should be available to you system wide.

  * `oc-sync-git` will export all OpenShift API objects but secrets of your current active
     project to the _api-objects.yaml_ file and create a git commit if changes occur
  * `oc-edit` will
    * first call `oc-sync-git` to gather all externally made changes
    * second open an editor for changing all your OpenShift API objects but secrets
    * finally call `oc-sync-git` again to commit your changes to Git
  * `oc-apply` will import the previously exported API objects to the current logged in
    OpenShift project again

To setup a new project you need to fullfill following prerequisites:

* Having an OpenShift project meaningfully containing some API objects
* Having the `oc` binary installed and beeing logged into the cluster and project
* Beeing inside the (empty) git repository clone you want the API objects being committet to

Then you can call

* `oc-edit` whenenver you want to edit the API objects and commit them to git
* `oc-sync-git` whenever you have intentionally made changes to your OpenShift project
  'from outside' and want to commit them to git

None of the scripts will do a `git push`. This you have to do explicitly!

The scripts will replace every occurence of the project name in the exported _api-objects.yaml_
with the placeholder `OC_PROJECT_NAME`. You should use the `oc-apply` to import the objects
conveniently to the current OpenShift project.
