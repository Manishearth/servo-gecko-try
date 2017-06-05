# Servo-Gecko-Try

Service for forwarding Servo pull requests to Gecko's Try build
infrastructure.

This is a small flask app which:

* Maintains clones of the Servo and Mozilla-Central repositories
* Listens for GitHub's pull request webhooks on the port specified in the
  config file
* Turns each PR into a Mercurial (HG) patch using `run.sh`
* Submits that patch to Gecko's infrastructure using `mach try` and the
  hg credentials configured for the user that's running the app.

## Setup:


* Create a user to run the app as.
* Clone Servo from https://github.com/servo/servo/, probably into that user's
  homedir. Make sure the path to the clone in this app's `config.json` is
  correct.
* Clone https://hg.mozilla.org/mozilla-central/ and
  https://hg.mozilla.org/integration/autoland/, and set their paths in
  `config.json`
* Clone http://hg.mozilla.org/hgcustom/version-control-tools/ into the user's
  `~/.mozbuild/version-control-tools`
* Give the user a keypair that lets it push to try. We got ours at
  https://bugzilla.mozilla.org/show_bug.cgi?id=1347259
* Put the following in the user's `~/.hgrc`:

```
[extensions]
mq =
push-to-try = ~/.mozbuild/version-control-tools/hgext/push-to-try

[ui]
username = Bors <whatever@whatever.com>
ssh = ssh -l 'borsusername@bors.com' -i '/path/to/key.pub'

```

* Point a webhook from `servo/servo` to notify the app of incoming PRs
* Run the app.
