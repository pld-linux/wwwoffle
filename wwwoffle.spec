Summary:     WWW Offline Explorer - Caching Web Proxy Server
Summary(pl): WWW Offline Explorer
Name:        wwwoffle
Version:     2.3a
Release:     1
Copyright:   GPL
Group:       Networking/Daemons
Source:      http://www.gedanken.demon.co.uk/wwwoffle/version-%{version}/wwwoffle-%{version}.tgz
Patch:       wwwoffle-%{version}.makefile.patch
Vendor:      Andrew M. Bishop <amb@gedanken.demon.co.uk>
URL:         http://www.gedanken.demon.co.uk/wwwoffle/
Buildroot:   /tmp/%{name}-%{version}-root

%description
The wwwoffled program is a simple proxy server with special features
for use with dial-up internet links.  This means that it is possible to
browse web pages and read them without having to remain connected.

%description -l pl
Prosty serwer proxy przeznaczony dla komputerów ³±cz±cych siê z internetem
przez modem.  Umo¿liwia przegl±danie stron WWW w trybie offline i zaznaczanie
stron przeznaczonych do ¶ci±gniêcia po nawi±zaniu po³±czenia.

%prep
%setup -q
%patch -p1

%build
make 	INSTDIR=$RPM_BUILD_ROOT/usr \
	SPOOLDIR=$RPM_BUILD_ROOT/var/spool/wwwoffle \
	CONFDIR=$RPM_BUILD_ROOT/etc \
	CFLAGS="$RPM_OPT_FLAGS" \
	LDFLAGS="-s" \
	all

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

install contrib/redhat-init $RPM_BUILD_ROOT/etc/rc.d/init.d/wwwoffle.init
make 	INSTDIR=$RPM_BUILD_ROOT/usr \
	SPOOLDIR=$RPM_BUILD_ROOT/var/spool/wwwoffle \
	CONFDIR=$RPM_BUILD_ROOT/etc \
	install
strip ${RPM_BUILD_ROOT}/usr/{bin,sbin}/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644, root, root, 755)
%doc README* NEWS ChangeLog CHANGES.CONF
%attr(600, root, root) %config /etc/wwwoffle.conf
%attr(700, root, root) /etc/rc.d/init.d/wwwoffle.init
%attr(755, root, root) /usr/bin/*
%attr(755, root, root) /usr/sbin/*
%attr(644, root,  man) /usr/man/man[158]/*
/var/spool/wwwoffle

%changelog
* Tue Sep 22 1998 Piotr Dembiñski <hector@kki.net.pl>
  [2.3a-1]
- first release in rpm package.
