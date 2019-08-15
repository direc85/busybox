Summary: Single binary providing simplified versions of system commands
Name: busybox
Version: 1.31.0
Release: 1
License: GPLv2
Group: System/Shells
Source0: http://www.busybox.net/downloads/%{name}-%{version}.tar.bz2
Source1: rpm/udhcpd.service
Source2: busybox-static.config
Source3: busybox-sailfish.config
Patch0:  0001-Copy-extended-attributes-if-p-flag-is-provided-to-cp.patch
URL: https://git.sailfishos.org/mer-core/busybox

Obsoletes: time <= 1.7
Provides: time > 1.7

# Providing only part of iputils, but should be enough for us. 
Obsoletes: iputils <= 20101006
Provides: iputils > 20101006

BuildRequires: glibc-static

%define debug_package %{nil}

%description
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
Obsoletes: %{name}-docs

%description doc
Busybox user guide.

%package static
Group: System Environment/Shells
Summary: Statically linked version of busybox

%description static
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This package provides
a statically linked version of Busybox.

%package symlinks-dosfstools
Requires: %{name} = %{version}-%{release}
Group: System/Shells
Summary: Busybox replacements for dosfstools

%description symlinks-dosfstools
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This
is the symlinks implementing part of dosfstools.

%package symlinks-gzip
Requires: %{name} = %{version}-%{release}
Group: System/Shells
Summary: Busybox replacements for gzip
Provides: gzip = %{version}
Obsoletes: gzip <= 1.5

%description symlinks-gzip
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This
is the symlinks implementing gzip replacements.

%package symlinks-dhcp
Requires: %{name} = %{version}-%{release}
Group: System/Shells
Summary: Busybox dhcp utilities

%description symlinks-dhcp
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This contains
the symlinks implementing the dhcp utilities (udhcpc/udhcpcd).

%package symlinks-diffutils
Requires: %{name} = %{version}-%{release}
Group: System/Shells
Summary: Busybox replacements for diffutils
Provides: diffutils = %{version}
Conflicts: gnu-diffutils

%description symlinks-diffutils
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This
is the symlinks implementing part of diffutils replacements.

%package symlinks-findutils
Requires: %{name} = %{version}-%{release}
Group: System/Shells
Summary: Busybox replacements for findutils
Provides: findutils = %{version}
Conflicts: gnu-findutils

%description symlinks-findutils
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This
is the symlinks implementing findutils replacements.

%package symlinks-grep
Requires: %{name} = %{version}-%{release}
Group: System/Shells
Summary: Busybox replacements for grep
Provides: grep = %{version}
Provides: /bin/grep
Conflicts: gnu-grep

%description symlinks-grep
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This
is the symlinks implementing grep, egrep and fgrep replacements.

%package symlinks-cpio
Requires: %{name} = %{version}-%{release}
Group: System/Shells
Summary: Busybox replacements for cpio
Provides: cpio
Conflicts: gnu-cpio

%description symlinks-cpio
Busybox is a single binary which includes versions of a large number
of system commands, including a shell. This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This contains
the symlinks implementing cpio replacements.

%package symlinks-tar
Requires: %{name} = %{version}-%{release}
Group: System/Shells
Summary: Busybox replacements for tar
Provides: tar = %{version}
Conflicts: gnu-tar

%description symlinks-tar
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This
is the symlink implementing tar replacement.

%package symlinks-which
Requires: %{name} = %{version}-%{release}
Group: System/Shells
Summary: Busybox replacements for which
Provides: which = %{version}
Conflicts: util-linux <= 2.33+git1

%description symlinks-which
Busybox is a single binary which includes versions of a large number
of system commands, including a shell.  This package can be very
useful for recovering from certain types of system failures,
particularly those involving broken shared libraries. This
is the symlink implementing which replacement.

%prep
%setup -q -n %{name}-%{version}/upstream
%patch0 -p1

%build
# TODO: This config should be synced with the dynamic config at some point
# currently the features differ quite a bit
cp %{SOURCE2} .config
yes "" | make oldconfig
make %{?_smp_mflags}
cp busybox busybox-static

# clean any leftovers from static build
make clean
make distclean

# Build dynamic version
cp %{SOURCE3} .config

yes "" | make oldconfig
make %{_smp_mflags}
make busybox.links
cat >> busybox.links << EOF
%{_bindir}/gzip
%{_bindir}/gunzip
/usr/sbin/udhcpc
/bin/find
%{_bindir}/cpio
%{_bindir}/tar
EOF

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/bin
install -m 755 busybox %{buildroot}/bin/busybox
install -m 644 -D %{SOURCE1} %{buildroot}/lib/systemd/system/udhcpd.service
applets/install.sh %{buildroot} --symlinks
rm -f %{buildroot}/sbin/udhcpc

install -m 755 busybox-static %{buildroot}/bin/busybox-static
mkdir -p %{buildroot}/%{_docdir}/%{name}-%{version}
install -m 644 -t %{buildroot}/%{_docdir}/%{name}-%{version} \
	docs/BusyBox.html docs/BusyBox.txt

%files
%defattr(-,root,root,-)
%license LICENSE
/bin/busybox
/bin/ping
/bin/ping6
%{_bindir}/time
%{_bindir}/traceroute
%{_bindir}/traceroute6
/usr/sbin/arping

%files static
%defattr(-,root,root,-)
/bin/busybox-static

%files doc
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}

%files symlinks-dosfstools
%defattr(-,root,root,-)
/sbin/mkdosfs
/sbin/mkfs.vfat

%files symlinks-gzip
%defattr(-,root,root,-)
/bin/gunzip
%{_bindir}/gunzip
/bin/gzip
%{_bindir}/gzip
/bin/zcat

%files symlinks-dhcp
%defattr(-,root,root,-)
/usr/sbin/udhcpc
/usr/sbin/udhcpd
/lib/systemd/system/udhcpd.service

%files symlinks-diffutils
%defattr(-,root,root,-)
%{_bindir}/diff
%{_bindir}/cmp

%files symlinks-findutils
%defattr(-,root,root,-)
/bin/find
%{_bindir}/find
%{_bindir}/xargs

%files symlinks-grep
%defattr(-,root,root,-)
/bin/grep
/bin/egrep
/bin/fgrep

%files symlinks-cpio
%defattr(-,root,root,-)
%{_bindir}/cpio
/bin/cpio

%files symlinks-tar
%defattr(-,root,root,-)
%{_bindir}/tar
/bin/tar

%files symlinks-which
%defattr(-,root,root,-)
%{_bindir}/which
