# TODO:
# - PLDify init script
# - revise split (e.g. which data should go to -tools)
#
# Conditional build:
%bcond_without	sysfs	# don't use sysfs to scan for ttyUSB
#
Summary:	A library for easy access to smart cards (chipcards)
Summary(pl.UTF-8):	Biblioteka łatwego dostępu do kart procesorowych
Name:		libchipcard
Version:	4.1.0
Release:	0.1
License:	LGPL v2.1 with OpenSSL linking exception
Group:		Libraries
Source0:	http://www.aquamaniac.de/sites/download/download.php?package=02&release=02&file=01&dummy=%{name}-%{version}.tar.gz
# Source0-md5:	cd6226f232b362cae3b38627f2e24e82
Patch0:		%{name}-visibility.patch
URL:		http://www.libchipcard.de/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	gwenhywfar-devel >= 3.0.0
BuildRequires:	libtool
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
%{?with_sysfs:BuildRequires:	sysfsutils-devel >= 1.3.0-3}
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
%{?with_sysfs:Requires:	sysfsutils-devel >= 1.3.0-3}

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

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_sysfs:ac_cv_header_sysfs_libsysfs_h=no}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	initscriptdir=/etc/rc.d/init.d

rm -f $RPM_BUILD_ROOT%{_libdir}/gwenhywfar/plugins/*/ct/*.la
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard/client/chipcardc.conf{.default,}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard/client/chipcardc.conf.example
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard/server/chipcardd.conf{.default,}
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/chipcard/server/chipcardd.conf.example

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post tools
/sbin/chkconfig --add chipcardd

%preun tools
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del chipcardd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO doc/{CERTIFICATES,CONFIG,IPCCOMMANDS} etc/*.conf.*
%attr(755,root,root) %{_libdir}/libchipcardc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libchipcardc.so.2
%attr(755,root,root) %{_libdir}/libchipcardd.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libchipcardd.so.0
%attr(755,root,root) %{_libdir}/libchipcard_ctapi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libchipcard_ctapi.so.0
%dir %{_libdir}/chipcard
%dir %{_libdir}/chipcard/server
%dir %{_libdir}/chipcard/server/drivers
%{_libdir}/chipcard/server/drivers/*.xml
%attr(755,root,root) %{_libdir}/chipcard/server/drivers/SKEL1
%attr(755,root,root) %{_libdir}/chipcard/server/drivers/ctapi
%attr(755,root,root) %{_libdir}/chipcard/server/drivers/ifd
%dir %{_libdir}/chipcard/server/lowlevel
%dir %{_libdir}/chipcard/server/services
%{_libdir}/chipcard/server/services/*.xml
%attr(755,root,root) %{_libdir}/chipcard/server/services/kvks
%attr(755,root,root) %{_libdir}/gwenhywfar/plugins/*/ct/*.so*
%{_libdir}/gwenhywfar/plugins/*/ct/*.xml
%dir %{_datadir}/chipcard
%dir %{_datadir}/chipcard/client
%{_datadir}/chipcard/client/apps
%{_datadir}/chipcard/client/cards
%dir %{_datadir}/chipcard/server
%{_datadir}/chipcard/server/drivers
%dir %{_sysconfdir}/chipcard
%dir %{_sysconfdir}/chipcard/client
%dir %{_sysconfdir}/chipcard/client/certs
# used by libchipcardc
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chipcard/client/chipcardc.conf

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/chipcard-config
%attr(755,root,root) %{_libdir}/libchipcardc.so
%attr(755,root,root) %{_libdir}/libchipcardd.so
%attr(755,root,root) %{_libdir}/libchipcard_ctapi.so
%{_libdir}/libchipcardc.la
%{_libdir}/libchipcardd.la
%{_libdir}/libchipcard_ctapi.la
%{_includedir}/chipcard
%{_aclocaldir}/chipcard.m4

%files tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cardcommander
%attr(755,root,root) %{_bindir}/chipcard-tool
%attr(755,root,root) %{_bindir}/geldkarte
%attr(755,root,root) %{_bindir}/kvkcard
%attr(755,root,root) %{_bindir}/memcard
%attr(755,root,root) %{_sbindir}/chipcardd4
%attr(754,root,root) /etc/rc.d/init.d/chipcardd
%dir %{_sysconfdir}/chipcard/server
%dir %{_sysconfdir}/chipcard/server/certs
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/chipcard/server/chipcardd.conf
