Summary:	WWW Offline Explorer - Caching Web Proxy Server
Summary(pl):	WWW Offline Explorer
Name:		wwwoffle
Version:	2.5
Release:	1
Copyright:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	http://www.gedanken.demon.co.uk/download-wwwoffle/%{name}-%{version}.tgz
Source1:	wwwoffle.init
Patch:		wwwoffle-DESTDIR.patch
Requires:	rc-scripts
URL:		http://www.gedanken.demon.co.uk/wwwoffle/
Buildroot:	/tmp/%{name}-%{version}-root

%define		_sysconfdir	/etc

%description
The wwwoffled program is a simple proxy server with special features
for use with dial-up internet links.  This means that it is possible to
browse web pages and read them without having to remain connected.

%description -l pl
Prosty serwer proxy przeznaczony dla komputerów łączących się z Internetem
przez modem. Umożliwia przeglądanie stron WWW w trybie offline i zaznaczanie
stron przeznaczonych do ściągnięcia po nawiązaniu połączenia.

%prep
%setup -q
%patch -p0

%build
make all \
	INSTDIR=%{_prefix} \
	SPOOLDIR=/var/spool/wwwoffle \
	CONFDIR=%{_sysconfdir} \
	CFLAGS="$RPM_OPT_FLAGS" \
	LDFLAGS="-s"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

make install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTDIR=%{_prefix} \
	CONFDIR=%{_sysconfdir} \
	BINDIR=%{_bindir} \
	SBINDIR=%{_sbindir} \
	MANDIR=%{_mandir} \
	SPOOLDIR=/var/spool/wwwoffle

strip $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/*

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	README* NEWS ChangeLog CHANGES.CONF INSTALL

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README*,NEWS,ChangeLog,CHANGES.CONF,INSTALL}.gz
%attr(600,root,root) %config %{_sysconfdir}/%{name}.conf

%attr(751,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*

%{_mandir}/man*/*

/var/spool/%{name}
