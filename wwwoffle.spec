Summary:	WWW Offline Explorer - Caching Web Proxy Server (IPv6)
Summary(pl):	WWW Offline Explorer ze wsparciem dla IPv6
Name:		wwwoffle
Version:	2.5d
Release:	1
Copyright:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.demon.co.uk/pub/unix/httpd/%{name}-%{version}.tgz
Source1:	wwwoffle.init
Source2:	wwwoffle.sysconfig
Patch0:		wwwoffle-DESTDIR.patch
Patch1:		http://www.misiek.eu.org/ipv6/wwwoffle-2.5d-ipv6-01032000.patch.gz
Requires:	rc-scripts
URL:		http://www.gedanken.demon.co.uk/wwwoffle/
Buildroot:	/tmp/%{name}-%{version}-root

%define		_sysconfdir	/etc

%description
The wwwoffled program is a simple proxy server with special features
for use with dial-up internet links.  This means that it is possible to
browse web pages and read them without having to remain connected.

%description -l pl
Prosty serwer proxy przeznaczony dla komputerów ³±cz±cych siê z Internetem
przez modem. Umo¿liwia przegl±danie stron WWW w trybie offline i zaznaczanie
stron przeznaczonych do ¶ci±gniêcia po nawi±zaniu po³±czenia.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
make all \
	INSTDIR=%{_prefix} \
	SPOOLDIR=%{_var}/cache/wwwoffle \
	CONFDIR=%{_sysconfdir} \
	CFLAGS="$RPM_OPT_FLAGS" \
	LDFLAGS="-s"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

make install \
	INSTDIR=$RPM_BUILD_ROOT%{_prefix} \
	CONFDIR=$RPM_BUILD_ROOT%{_sysconfdir} \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	SBINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	SPOOLDIR=$RPM_BUILD_ROOT%{_var}/cache/wwwoffle

strip $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/*

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/wwwoffle

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	README* NEWS ChangeLog CHANGES.CONF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README*,NEWS,ChangeLog,CHANGES.CONF}.gz
%attr(600,root,root) %config %{_sysconfdir}/%{name}.conf

%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) /etc/sysconfig/wwwoffle
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man*/*
/var/cache/%{name}
