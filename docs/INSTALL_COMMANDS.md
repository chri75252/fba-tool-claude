# Dependency Installation Cheat Sheet

This document lists typical commands for installing packages from the host domains referenced in the allowed list.

## Operating System Packages

### Ubuntu/Debian (`debian.org`, `ubuntu.com`, `launchpad.net`, `packages.microsoft.com`, `ppa.launchpad.net`, `apt.llvm.org`)
```bash
sudo apt update
sudo apt install <package-name>
```

### Fedora/CentOS (`fedoraproject.org`, `centos.org`)
```bash
sudo dnf install <package-name>
```

### Alpine Linux (`alpinelinux.org`)
```bash
sudo apk add <package-name>
```

### Arch Linux (`archlinux.org`)
```bash
sudo pacman -S <package-name>
```

## Python Packages (`pypi.org`, `pypa.io`, `pythonhosted.org`)
```bash
pip install <package-name>
```

## Node.js Packages (`nodejs.org`, `npmjs.com`, `npmjs.org`, `yarnpkg.com`)
```bash
npm install <package-name>
# or
yarn add <package-name>
```

## Ruby Gems (`ruby-lang.org`, `rubygems.org`, `rubyonrails.org`, `rubyforge.org`)
```bash
gem install <package-name>
```

## Rust Crates (`rustup.rs`, `crates.io`)
```bash
cargo install <crate-name>
```

## Go Modules (`golang.org`, `pkg.go.dev`, `goproxy.io`)
```bash
go install <module>@latest
```

## Docker Images (`docker.com`, `docker.io`, `gcr.io`, `ghcr.io`, `quay.io`, `mcr.microsoft.com`)
```bash
docker pull <image>
```

## .NET Packages (`dotnet.microsoft.com`, `nuget.org`, `microsoft.com`)
```bash
dotnet add package <package-name>
```

## Java Dependencies (`maven.org`, `gradle.org`, `jcenter.bintray.com`, `apache.org`)
Use Maven:
```bash
mvn install:install-file -DgroupId=<group> -DartifactId=<artifact> -Dversion=<version> -Dpackaging=jar -Dfile=<path>
```
Use Gradle:
```bash
gradle build
```

## PHP Packages (`packagist.org`)
```bash
composer require <package-name>
```

## iOS/Swift Dependencies (`cocoapods.org`, `swift.org`)
```bash
pod install           # CocoaPods
swift package update  # Swift Package Manager
```

## Haskell Packages (`haskell.org`)
```bash
cabal install <package-name>
```

## Other Sources (`eclipse.org`, `sourceforge.net`, `oracle.com`, etc.)
Refer to each project's documentation for manual download and installation steps.

This cheat sheet maps allowed domains to common commands for installing software from those ecosystems.
