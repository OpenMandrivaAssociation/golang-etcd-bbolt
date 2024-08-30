%global debug_package %{nil}

# Run tests in check section
# error: out of memory
%bcond_with check

# https://github.com/etcd-io/bbolt
%global goipath		go.etcd.io/bbolt
%global forgeurl	https://github.com/etcd-io/bbolt
Version:		1.3.11

%gometa

Summary:	An embedded key/value database for Go
Name:		golang-etcd-bbolt

Release:	1
Source0:	https://github.com/etcd-io/bbolt/archive/v%{version}/bbolt-%{version}.tar.gz
URL:		https://github.com/etcd-io/bbolt
License:	MIT
Group:		Development/Other
BuildRequires:	compiler(go-compiler)
BuildRequires:	golang(github.com/stretchr/testify/require)
BuildRequires:	golang(golang.org/x/sys/unix)
%if %{with check}
BuildRequires:	golang(github.com/stretchr/testify/assert)
%endif

%description
bbolt is a fork of Ben Johnson's Bolt key/value store.
The purpose of this fork is to provide the Go community
with an active maintenance and development target for Bolt;
the goal is improved reliability and stability.  bbolt
includes bug fixes, performance enhancements, and features
not found in Bolt while preserving backwards compatibility
with the Bolt API.

Bolt is a pure Go key/value store inspired by Howard Chu's
LMDB project. The goal of the project is to provide a simple,
fast, and reliable database for projects that don't require a
full database server such as Postgres or MySQL.

Since Bolt is meant to be used as such a low-level piece of
functionality, simplicity is key.  The API will be small and
only focus on getting values and setting values.

%files
%license LICENSE
%doc README.md
%{_bindir}/bbolt

#-----------------------------------------------------------------------

%package devel
Summary:	%{summary}
Group:		Development/Other
BuildArch:	noarch

%description devel
%{description}

This package contains library source intended for
building other packages which use import path with
%{goipath} prefix.

%files devel -f devel.file-list
%license LICENSE
%doc README.md

#-----------------------------------------------------------------------

%prep
%autosetup -p1 -n bbolt-%{version}

%build
%gobuildroot
for cmd in $(ls -1 cmd) ; do
	%gobuild -o _bin/$cmd %{goipath}/cmd/$cmd
done

%install
%goinstall
for cmd in $(ls -1 _bin) ; do
	install -Dpm 0755 _bin/$cmd %{buildroot}%{_bindir}/$cmd
done

%check
%if %{with check}
%gochecks
%endif

