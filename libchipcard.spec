Summary:	A library for easy access to smart cards (chipcards)
Summary(pl):	Biblioteka ³atwego dostêpu do kart procesorowych
Name:		libchipcard
Version:	0.9.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/libchipcard/%{name}-%{version}.tar.gz
# Source0-md5:	9de5833b693a5221a046d4fe7efcc4c6
Patch0:		%{name}-etc.patch
URL:		http://www.libchipcard.de/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
LibChipCard allows easy access to smart cards. It provides basic
access to memory and processor cards and has special support for
German medical cards, German "Geldkarten" and HBCI (homebanking) cards
(both type 0 and type 1). It accesses the readers via CTAPI or PC/SC
interfaces and has successfully been tested with Towitoko, Kobil and
Reiner-SCT readers.

%description -l pl
LibChipCard pozwala na ³atwy dostêp do czytników kart procesorowych.
Daje podstawowy dostêp do kart pamiêciowych i procesorowych oraz ma
specjalne wsparcie dla niemieckich kart medycznych, niemieckich
"Geldkarten" oraz kart HBCI (do homebankingu, typu 0 lub 1). Odwo³uje
siê do czytników przez interfejs CTAPI lub PC/SC. Biblioteka by³a
testowana (z sukcesem) z czytnikami Towitoko, Kobil i Reiner-SCT.

%package devel
Summary:	Header files for LibChipCard
Summary(pl):	Pliki nag³ówkowe LibChipCard
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package contains libchipcard-config and header files for writing
programs using LibChipCard.

%description devel -l pl
Ten pakiet zawiera libchipcard-config oraz pliki nag³ówkowe do
tworzenia programów u¿ywaj±cych LibChipCard.

%package static
Summary:	Static LibChipCard library
Summary(pl):	Statyczna biblioteka LibChipCard
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
Static LibChipCard library.

%description static -l pl
Statyczna biblioteka LibChipCard.

%package tools
Summary:	Terminal tools and daemons for LibChipCard
Summary(pl):	Narzêdzia terminalowe i demony dla LibChipCard
Summary(pl):	Demon ChipCard i zwi±
License:	GPL
Group:		Applications
Requires:	%{name} = %{version}

%description tools
This package contains the terminal tools and daemons for LibChipCard.
The most important daemon here is chipcardd which is needed to access
local card readers.

%description tools -l pl
Ten pakiet zawiera narzêdzia terminalowe oraz demony dla LibChipCard,
w tym najwa¿niejszego demona, chipcardd, potrzebnego do dostêpu do
lokalnych czytników kart.

%prep
%setup -q
%patch -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-pid-dir=/var/run

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_initrddir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# TODO: PLDify
install redhat/chipcardd $RPM_BUILD_ROOT%{_initrddir}
install example/chipcardc.conf $RPM_BUILD_ROOT%{_sysconfdir}
install example/chipcardd.conf $RPM_BUILD_ROOT%{_sysconfdir}

rm -f doc/html/{Makefile*,pics/Makefile*}

%find_lang %{name} --all-name

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
# COPYING contains only summary, note *GPL texts themselves
%doc AUTHORS COPYING ChangeLog FAQ README* THANKS TODO
%attr(755,root,root) %{_libdir}/libchipcard.so.*.*.*
%dir %{_datadir}/libchipcard
%dir %{_datadir}/libchipcard/commands
%{_datadir}/libchipcard/commands/ctcard.cmd
%{_datadir}/libchipcard/commands/ctgeldkarte.cmd
%{_datadir}/libchipcard/commands/ctkvkcard.cmd
%{_datadir}/libchipcard/commands/ctmemorycard.cmd
%{_datadir}/libchipcard/commands/ctprocessorcard.cmd
%{_datadir}/libchipcard/commands/hbcicard.cmd
%{_datadir}/libchipcard/commands/rsacard.cmd
%dir %{_datadir}/libchipcard/drivers
%{_datadir}/libchipcard/drivers/README
%{_datadir}/libchipcard/drivers/ctapi-fake.dsc
%{_datadir}/libchipcard/drivers/cyberjack.dsc
%{_datadir}/libchipcard/drivers/kobil.dsc
%{_datadir}/libchipcard/drivers/towitoko.dsc
%{_datadir}/libchipcard/drivers/orga.dsc
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/chipcardc.conf
%{_mandir}/man5/libchipcard.conf.5*
%{_mandir}/man5/chipcardc.conf.5*

%files devel
%defattr(644,root,root,755)
%doc doc/*.txt doc/html/*
%attr(755,root,root) %{_bindir}/libchipcard-config
%attr(755,root,root) %{_libdir}/libchipcard.so
%{_libdir}/libchipcard.la
%{_includedir}/chameleon
%{_includedir}/chipcard
%{_includedir}/chipcard.h
%{_includedir}/ctversion.h
%{_aclocaldir}/libchipcard.m4
%{_mandir}/man1/libchipcard-config.1*

%files static
%defattr(644,root,root,755)
%{_libdir}/libchipcard.a

%files tools -f %{name}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cardcommander
%attr(755,root,root) %{_bindir}/ctfstool
%attr(755,root,root) %{_bindir}/geldkarte
%attr(755,root,root) %{_bindir}/hbcicard
%attr(755,root,root) %{_bindir}/memcard
%attr(755,root,root) %{_bindir}/readertest
%attr(755,root,root) %{_sbindir}/chipcardd
%attr(755,root,root) %{_sbindir}/kvkd
%attr(754,root,root) /etc/rc.d/init.d/chipcardd
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/chipcardd.conf
%{_mandir}/man1/ctfstool.1*
%{_mandir}/man1/geldkarte.1*
%{_mandir}/man1/hbcicard.1*
%{_mandir}/man1/chipcardd.1*
%{_mandir}/man1/memcard.1*
%{_mandir}/man1/kvkd.1*
%{_mandir}/man1/readertest.1*
%{_mandir}/man5/chipcardd.conf.5*
