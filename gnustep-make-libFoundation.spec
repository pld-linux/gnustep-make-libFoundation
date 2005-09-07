#
# Conditional build:
%bcond_without	docs	# don't build documentation (for bootstrap)
#
# TODO:
# - check spelling, typo & rel 1
# - find a nice way to include the /etc/profile.d scripts
# - think bout the %_prefix

%define		_realname	gnustep-make

Summary:	GNUstep Makefile package libFoundation version
Summary(pl):	Pakiet GNUstep Makefile wersja libFoundation
Name:		gnustep-make-libFoundation
Version:	1.11.0
Release:	0.1
License:	GPL
Vendor:		The GNUstep Project
Group:		Applications/System
Source0:	ftp://ftp.gnustep.org/pub/gnustep/core/%{_realname}-%{version}.tar.gz
# Source0-md5:	91f7e64e0531d56571ae93f6fdf14f58
URL:		http://www.gnustep.org/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_docs:BuildRequires: gnustep-make-devel}
BuildRequires:	tetex
BuildRequires:	tetex-dvips
BuildRequires:	tetex-format-latex
BuildRequires:	tetex-format-plain
BuildRequires:	texinfo-texi2dvi
Requires:	gnustep-dirs
Conflicts:	gnustep-core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/%{_lib}/GNUstep-libFoundation
%define		gsos		linux-gnu
%ifarch %{ix86}
%define		gscpu		ix86
%else
# also s/alpha.*/alpha/, but we use only "alpha" arch for now
%define		gscpu		%(echo %{_target_cpu} | sed -e 's/amd64/x86_64/;s/ppc/powerpc/')
%endif

%description
This package contains the basic tools needed to run GNUstep
applications.

This version of gnustep-make is compiled for support with libFoundation.

%description -l pl
Ten pakiet zawiera podstawowe narzêdzia potrzebne do uruchamiania
aplikacji GNUstep.

Ta wersja gnustep-make'a jest skompilowana dla wsparcia libFoundation.

%package devel
Summary:	Files needed to develop applications with gnustep-make libFoundation version
Summary(pl):	Pliki potrzebne do tworzenia aplikacji przy u¿yciu gnustep-make wersja libFoundation
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description devel
The makefile package is a simplistic, powerful and extensible way to
write makefiles for a GNUstep-based project. It allows the user to
write a GNUstep-based project without having to deal with the complex
issues associated with the configuration and installation of the core
GNUstep libraries. It also allows the user to easily create
cross-compiled binaries.

This version of gnustep-make is compiled for support with libFoundation.

%description devel -l pl
Pakiet makefile jest prost±, wydajn± i rozszerzaln± metod± pisania
makefile'i do projektów opartych o GNUstep. Pozwala u¿ytkownikowi na
tworzenie projektów z pominiêciem skomplikowanych szczegó³ów
konfiguracji i instalacji podstawowych bibliotek GNUstep. Pozwala
tak¿e ³atwo tworzyæ kompilowane skro¶nie binaria.

Ta wersja gnustep-make'a jest skompilowana dla wsparcia libFoundation.

%prep
%setup -q -n %{_realname}-%{version}

%build
cp -f /usr/share/automake/config.* .
%{__autoconf}
%configure \
	--disable-flattened \
	--with-tar=tar \
	--with-library-combo=gnu-fd-nil

%{__make}

%if %{with docs}
%{__make} -C Documentation
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	special_prefix=$RPM_BUILD_ROOT

#libFoundation + friends won't build without that
ln -s Library/Makefiles $RPM_BUILD_ROOT%{_prefix}/System/Makefiles

%if %{with docs}
%{__make} -C Documentation install \
	GNUSTEP_INSTALLATION_DIR=$RPM_BUILD_ROOT%{_prefix}/System
%endif

#install -d $RPM_BUILD_ROOT/etc/profile.d
## Create profile files
#cat > $RPM_BUILD_ROOT/etc/profile.d/GNUstep.sh << EOF
##!/bin/sh
#. %{_prefix}/System/Library/Makefiles/GNUstep.sh
#
#if [ ! -d \$GNUSTEP_USER_ROOT ]; then
#	mkdir \$GNUSTEP_USER_ROOT
#	chmod +rwx \$GNUSTEP_USER_ROOT
#	. %{_prefix}/System/Library/Makefiles/GNUstep.sh
#fi
#EOF

#cat > $RPM_BUILD_ROOT/etc/profile.d/GNUstep.csh << EOF
##!/bin/csh
#source %{_prefix}/System/Library/Makefiles/GNUstep.csh
#
#test -d \$GNUSTEP_USER_ROOT
#if (\$status != 0) then
#	mkdir \$GNUSTEP_USER_ROOT
#	chmod +rwx \$GNUSTEP_USER_ROOT
#	source %{_prefix}/System/Library/Makefiles/GNUstep.csh
#endif
#EOF

# not (yet?) supported by rpm-compress-doc
find $RPM_BUILD_ROOT%{_prefix}/System/Library/Documentation \
	-type f ! -name '*.html' ! -name '*.css' ! -name '*.gz' | xargs gzip -9nf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -d %{_prefix}/System/Makefiles -a ! -L %{_prefix}/System/Makefiles ]; then
	[ -d %{_prefix}/System/Library ] || install -d %{_prefix}/System/Library
	mv -f %{_prefix}/System/Makefiles %{_prefix}/System/Library
	ln -sf Library/Makefiles %{_prefix}/System/Makefiles
	echo 'Reinstall gnustep-make and gnustep-make-devel if some files are missing.' >&2
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog
#%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) /etc/profile.d/GNUstep.sh
#%attr(755,root,root) %config(noreplace) %verify(not size mtime md5) /etc/profile.d/GNUstep.csh

# GNUstep top-level
%dir %{_prefix}
%{_prefix}/Local
%dir %{_prefix}/System
%{_prefix}/System/Makefiles

# System domain
%{_prefix}/System/Applications
%dir %{_prefix}/System/Library
%{_prefix}/System/share
%attr(755,root,root) %{_prefix}/System/Tools

# System/Library folder
%{_prefix}/System/Library/ApplicationSupport
%{_prefix}/System/Library/Bundles
%{_prefix}/System/Library/ColorPickers
%{_prefix}/System/Library/Colors
%{_prefix}/System/Library/DocTemplates
%if %{with docs}
%docdir %{_prefix}/System/Library/Documentation
%dir %{_prefix}/System/Library/Documentation
%endif
%{_prefix}/System/Library/Fonts
%{_prefix}/System/Library/Frameworks
%{_prefix}/System/Library/Headers
%{_prefix}/System/Library/Images
%{_prefix}/System/Library/KeyBindings
%{_prefix}/System/Library/Libraries
%dir %{_prefix}/System/Library/Makefiles
%{_prefix}/System/Library/PostScript
%{_prefix}/System/Library/Services
%{_prefix}/System/Library/Sounds

%if %{with docs}
%dir %{_prefix}/System/Library/Documentation/Developer
%dir %{_prefix}/System/Library/Documentation/Developer/Make
%{_prefix}/System/Library/Documentation/Developer/Make/ReleaseNotes
%dir %{_prefix}/System/Library/Documentation/User
%{_prefix}/System/Library/Documentation/User/GNUstep
%dir %{_prefix}/System/Library/Documentation/info
%{_prefix}/System/Library/Documentation/info/*.info*
%dir %{_prefix}/System/Library/Documentation/man
%dir %{_prefix}/System/Library/Documentation/man/man1
%{_prefix}/System/Library/Documentation/man/man1/openapp.1*
%dir %{_prefix}/System/Library/Documentation/man/man7
%{_prefix}/System/Library/Documentation/man/man7/GNUstep.7*
%endif

%attr(755,root,root) %{_prefix}/System/Library/Makefiles/config.*
%{_prefix}/System/Library/Makefiles/tar-exclude-list
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/*.sh
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/*.csh
%dir %{_prefix}/System/Library/Makefiles/%{gscpu}
%dir %{_prefix}/System/Library/Makefiles/%{gscpu}/%{gsos}
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/%{gscpu}/%{gsos}/user_home
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/%{gscpu}/%{gsos}/which_lib

%files devel
%defattr(644,root,root,755)
%if %{with docs}
%docdir %{_prefix}/System/Library/Documentation
%{_prefix}/System/Library/Documentation/Developer/Make/Manual
%endif

%{_prefix}/System/Library/Makefiles/*.make
%{_prefix}/System/Library/Makefiles/*.template
%{_prefix}/System/Library/Makefiles/Instance
%{_prefix}/System/Library/Makefiles/Master
%{_prefix}/System/Library/Makefiles/%{gscpu}/%{gsos}/*.make
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/install-sh
%attr(755,root,root) %{_prefix}/System/Library/Makefiles/mkinstalldirs
