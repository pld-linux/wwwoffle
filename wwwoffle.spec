Summary:	WWW Offline Explorer - Caching Web Proxy Server (IPv6)
Summary(pl):	WWW Offline Explorer ze wsparciem dla IPv6
Name:		wwwoffle
Version:	2.6b
Release:	0
License:	GPL
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.demon.co.uk/pub/unix/httpd/%{name}-%{version}.tgz
Source1:	wwwoffle.init
Source2:	wwwoffle.sysconfig
URL:		http://www.gedanken.demon.co.uk/wwwoffle/
Prereq:		rc-scripts >= 0.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
%{__make} all \
	INSTDIR=%{_prefix} \
	SPOOLDIR=%{_var}/cache/wwwoffle \
	CONFDIR=%{_sysconfdir} \
	CFLAGS="$RPM_OPT_FLAGS" \
	LDFLAGS="-s"

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT%{_sysconfdir}/{rc.d/init.d,sysconfig}

%{__make} install \
	INSTDIR=$RPM_BUILD_ROOT%{_prefix} \
	CONFDIR=$RPM_BUILD_ROOT%{_sysconfdir} \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	SBINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	SPOOLDIR=$RPM_BUILD_ROOT%{_var}/cache/wwwoffle
%{__install} %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/wwwoffle

%{__gzip} -9nf ANNOUNCE CHANGES.CONF CONVERT ChangeLog* FAQ NEWS README*

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {ANNOUNCE,CHANGES.CONF,CONVERT,ChangeLog*,FAQ,NEWS,README*}.gz
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/wwwoffle
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}.conf
%{_mandir}/man[158]/*
%{_var}/cache/%{name}/[!o]*
%ghost %{_var}/cache/%{name}/outgoing
