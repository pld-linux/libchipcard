# TODO:
# - revise split (e.g. which data should go to -tools)
#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	A library for easy access to smart cards (chipcards)
Summary(pl.UTF-8):	Biblioteka łatwego dostępu do kart procesorowych
Name:		libchipcard
Version:	5.0.4
Release:	2
License:	LGPL v2.1 with OpenSSL linking exception
Group:		Libraries
#Source0Download: https://www.aquamaniac.de/sites/download/packages.php
Source0:	https://www.aquamaniac.de/sites/download/download.php?package=02&release=200&file=01&dummy=/%{name}-%{version}.tar.gz
# Source0-md5:	f26766f5e699899ed8b2b6e6b188de73
URL:		https://www.aquamaniac.de/sites/libchipcard/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake
BuildRequires:	gwenhywfar-devel >= 4.0.0
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pcsc-lite-devel >= 1.6.2
BuildRequires:	pkgconfig
BuildRequires:	which
BuildRequires:	zlib-devel
Requires:	gwenhywfar >= 4.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libchipcard allows easy access to smart cards. It provides basic
access to memory and processor cards and has special support for
German medical cards, German "GeldKarte" and HBCI (homebanking) cards
(both type 0 and type 1). It accesses the readers via CTAPI or IFD
interfaces and has successfully been tested with Towitoko, Kobil, SCM,
Orga, Omnikey and Reiner-SCT readers.

%description -l pl.UTF-8
libchipcard pozwala na łatwy dostęp do kart procesorowych. Daje
podstawowy dostęp do kart pamięciowych i procesorowych, ma także
specjalną obsługę niemieckich kart medycznych, niemieckich kart
"GeldKarte" oraz kart HBCI (do homebankingu, zarówno typu 0 jak i 1).
Z czytnikami komunikuje się poprzez interfejs CTAPI lub IFD, była
testowana z czytnikami Towitoko, Kobil, SCM, Orga, Omnikey i
Reiner-SCT.

%package devel
Summary:	Header files for libchipcard
Summary(pl.UTF-8):	Pliki nagłówkowe libchipcard
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gwenhywfar-devel >= 4.0.0
Requires:	pcsc-lite-devel >= 1.6.2
Requires:	zlib-devel

%description devel
This package contains libchipcard-config and header files for writing
programs using LibChipCard.

%description devel -l pl.UTF-8
Ten pakiet zawiera libchipcard-config oraz pliki nagłówkowe do
tworzenia programów używających LibChipCard.

%package static
Summary:	Static libchipcard library
Summary(pl.UTF-8):	Statyczna biblioteka libchipcard
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libchipcard library.

%description static -l pl.UTF-8
Statyczna biblioteka libchipcard.

%package tools
Summary:	Terminal tools and daemons for libchipcard
Summary(pl.UTF-8):	Narzędzia terminalowe i demony dla libchipcard
Group:		Applications
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name} = %{version}-%{release}
Requires:	rc-scripts

%description tools
This package contains the terminal tools and daemons for libchipcard.
The most important daemon here is chipcardd which is needed to access
local card readers.

%description tools -l pl.UTF-8
Ten pakiet zawiera narzędzia terminalowe oraz demony dla libchipcard,
w tym najważniejszego demona, chipcardd, potrzebnego do dostępu do
lokalnych czytników kart.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static} \
	--with-init-script-dir=/etc/rc.d/init.d \
	--with-pcsc-libs=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/chipcard/chipcardc.conf{.default,}
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/chipcard/chipcardc.conf.example \
	$RPM_BUILD_ROOT%{_libdir}/*.la \
	$RPM_BUILD_ROOT%{_libdir}/gwenhywfar/plugins/*/ct/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gwenhywfar/plugins/*/ct/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/{CERTIFICATES,CONFIG,IPCCOMMANDS} etc/*.conf.*
%attr(755,root,root) %{_libdir}/libchipcard.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libchipcard.so.6
%dir %{_datadir}/chipcard
%dir %{_datadir}/chipcard/drivers
%{_datadir}/chipcard/drivers/*.xml
%dir %{_datadir}/chipcard/apps
%dir %{_datadir}/chipcard/cards
%{_datadir}/chipcard/apps/*.xml
%{_datadir}/chipcard/cards/*.xml
%dir %{_datadir}/chipcard/cards/cyberjack_pcsc
%{_datadir}/chipcard/cards/cyberjack_pcsc/*.xml
%dir %{_datadir}/chipcard/cards/generic_pcsc
%{_datadir}/chipcard/cards/generic_pcsc/*.xml
%attr(755,root,root) %{_libdir}/gwenhywfar/plugins/*/ct/ddvcard.so
%{_libdir}/gwenhywfar/plugins/*/ct/ddvcard.xml
%attr(755,root,root) %{_libdir}/gwenhywfar/plugins/*/ct/starcoscard.so
%{_libdir}/gwenhywfar/plugins/*/ct/starcoscard.xml
%attr(755,root,root) %{_libdir}/gwenhywfar/plugins/*/ct/zkacard.so
%{_libdir}/gwenhywfar/plugins/*/ct/zkacard.xml
# used by libchipcardc
%dir %{_sysconfdir}/chipcard
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chipcard/chipcardc.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chipcard-config
%attr(755,root,root) %{_libdir}/libchipcard.so
%{_includedir}/libchipcard5
%{_aclocaldir}/chipcard.m4

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libchipcard.a
%endif

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cardcommander
%attr(755,root,root) %{_bindir}/chipcard-tool
%attr(755,root,root) %{_bindir}/geldkarte
%attr(755,root,root) %{_bindir}/kvkcard
%attr(755,root,root) %{_bindir}/memcard
