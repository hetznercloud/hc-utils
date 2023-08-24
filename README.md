# Hetzner Cloud Utils
hc-utils contains utilities to provide an easier and automatic use of features of the Hetzner Cloud platform
(e.g. private networks, block storage)

# How to build

* Debian/Ubuntu
`dpkg-buildpackage`

* Fedora 29/30
```
$ sudo dnf install rpkg
$ rpkg local
```

* CentOS 7
copy sources to `~rpmbuild/SOURCES/` and run `rpmbuild -bb` in hc-utils dir
