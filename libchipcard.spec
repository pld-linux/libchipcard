# TODO:
# - revise split (e.g. which data should go to -tools)
#
Summary:	A library for easy access to smart cards (chipcards)
Summary(pl.UTF-8):	Biblioteka łatwego dostępu do kart procesorowych
Name:		libchipcard
Version:	5.0.0
Release:	5
License:	LGPL v2.1 with OpenSSL linking exception
Group:		Libraries
# http://www2.aquamaniac.de/sites/download/packages.php
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	9e1ae41016c894be30021a7e9b820680
Patch0:		%{name}-visibility.patch
Patch1:		%{name}-pcsc.patch
URL:		http://www.libchipcard.de/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	gwenhywfar-devel >= 3.5.0
BuildRequires:	libtool
BuildRequires:	pcsc-lite-devel >= 1.6.2
BuildRequires:	pkgconfig
BuildRequires:	which
Obsoletes:	libchipcard-static
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
Requires:	gwenhywfar-devel >= 3.0.0

%description devel
This package contains libchipcard-config and header files for writing
programs using LibChipCard.

%description devel -l pl.UTF-8
Ten pakiet zawiera libchipcard-config oraz pliki nagłówkowe do
tworzenia programów używających LibChipCard.

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
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	--with-pcsc-libs=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initscriptdir=/etc/rc.d/init.d

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard/chipcardc.conf{.default,}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/gwenhywfar/plugins/*/ct/*.la \
	$RPM_BUILD_ROOT%{_sysconfdir}/chipcard/chipcardc.conf.example \
	$RPM_BUILD_ROOT%{_libdir}/*.la

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
%attr(755,root,root) %{_libdir}/gwenhywfar/plugins/*/ct/*.so*
%{_libdir}/gwenhywfar/plugins/*/ct/*.xml
# used by libchipcardc
%dir %{_sysconfdir}/chipcard
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chipcard/chipcardc.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chipcard-config
%attr(755,root,root) %{_libdir}/libchipcard.so
%{_includedir}/libchipcard5
%{_aclocaldir}/chipcard.m4

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cardcommander
%attr(755,root,root) %{_bindir}/chipcard-tool
%attr(755,root,root) %{_bindir}/geldkarte
%attr(755,root,root) %{_bindir}/kvkcard
%attr(755,root,root) %{_bindir}/memcard
