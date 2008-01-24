# Conditional build:
%bcond_without	ipv6	# without support for IPv6
#
Summary:	WWW Offline Explorer - Caching Web Proxy Server (IPv6)
Summary(pl.UTF-8):	Eksplorator Offline World Wide Web (IPv6)
Name:		wwwoffle
Version:	2.9d
Release:	1
Epoch:		0
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.gedanken.demon.co.uk/download-wwwoffle/%{name}-%{version}.tgz
# Source0-md5:	29ade3b5994169510e36024680258a1e
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-replacement.patch
Patch1:		%{name}-conf_settings.patch
Patch2:		%{name}-namazu.patch
Patch3:		%{name}-hyperestraier.patch
# http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=450852
Patch4:		%{name}-gnutls.patch
URL:		http://www.gedanken.demon.co.uk/wwwoffle/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	flex
BuildRequires:	gnutls-devel
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(postun):	sed > 4.0
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires(pre):	fileutils
Requires(pre):	sh-utils
Requires:	rc-scripts >= 0.2.0
Provides:	group(wwwoffle)
Provides:	user(wwwoffle)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags_ia32	 -fomit-frame-pointer

%description
A proxy HTTP/FTP server for computers with dial-up internet access.
- Caching of pages viewed while connected for review later.
- Browsing of cached pages while not connected, with the ability to
  follow links and mark other pages for download.
- Downloading of specified pages non-interactively.
- Monitoring of pages for regular download.
- Multiple indices of pages stored in cache for easy selection.
- Interactive or command line option to select pages for fetching
  individually or recursively.
- All options controlled using a simple configuration file with a web
  page to edit it.

%description -l de.UTF-8
Ein (HTTP/FTP) Proxy Server für Computer mit Wählverbindungen ins
Internet. Folgendes wird unterstützt:
- Seiten werden lokal gespeichert und können jederzeit erneut
  abgerufen werden, auch OHNE Verbindung ins Internet
- Seiten, die nicht lokal vorhanden sind, werden 'bestellt'.
- Seiten können abonniert, d.h. regelmäßig heruntergeladen, werden;
  dies auch rekursiv.
- Alle lokal vorhandenen Seiten sind auf verschiedene Weisen indiziert
  und durchsuchbar.
- Steuerung erfolgt per Web-Browser, Kommandozeile und einer einfachen
  Konfigurationsdatei
- Jede Meldung von WWWOFFLE kann durch eigene ersetzt werden (so wurde
  auch diese Übersetzung realisiert)
- WWWOFFLE unterstützt verschiedene Authentifikationsmethoden

%description -l es.UTF-8
Un servidor proxy HTTP/FTP para ordenadores con conexión intermitente
a internet.
- Almacenado de páginas vistas mientras se estuvo conectado para
  releerlas más tarde.
- Revisión de páginas almacenadas mientras no se está conectado, con
  la habilidad de seguir enlaces y marcar otras páginas para recogida.
- Recogida de páginas especificadas de forma no interactiva.
- Monitorizado de páginas para recogida regular.
- Múltiples índices de las páginas almacenadas para una selección
  fácil.
- Opción para seleccionar páginas de forma interactiva o en línea de
  comandos de manera individual o recursiva.
- Todas las opciones se contralan usando un simple fichero de
  configuración con una página web para editarlo.

%description -l pl.UTF-8
Serwer proxy HTTP/FTP dla komputerów z dostępem do internetu typu
dial-up.
- Buforowanie stron przeglądanych podczas połączenia.
- Przeglądanie buforowanych stron bez potrzeby połączenia, z
  możliwością podążania za łączami i oznaczania innych stron do
  pobrania.
- Pobieranie określonych stron nieinteraktywnie.
- Monitorowanie stron dla regularnego pobierania.
- Wiele indeksów przechowywanych w buforze stron dla łatwego ich
  wyboru.
- Interaktywne lub z linii komend opcje wyboru stron do pobrania
  indywidualnie lub rekursywnie.
- Wszystkie opcje są kontrolowane przy użyciu prostego pliku
  konfiguracji z możliwością edycji z poziomu strony web.

%package namazu
Summary:	Indexing and searching WWWOFFLE's cache by Namazu
Summary(pl.UTF-8):	Indeksowanie i przeszukiwanie cache'a WWWOFFLE przez Namazu
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	mknmz-wwwoffle >= 0.7.2-2
Requires:	namazu-cgi >= 2.0.12-3

%description namazu
Indexing and searching WWWOFFLE's cache by Namazu.

%description namazu -l pl.UTF-8
Indeksowanie i przeszukiwanie cache'a WWWOFFLE przez Namazu.

%package hyperestraier
Summary:	Indexing and searching WWWOFFLE's cache by Hyperestraier
Summary(pl.UTF-8):	Indeksowanie i przeszukiwanie cache'a WWWOFFLE przez Hyperestraier
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	hyperestraier

%description hyperestraier
Indexing and searching WWWOFFLE's cache by Hyperestraier.

%description hyperestraier -l pl.UTF-8
Indeksowanie i przeszukiwanie cache'a WWWOFFLE przez Hyperestraier.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
cp /usr/share/automake/config.sub .
%{__aclocal}
%{__autoconf}
%configure2_13 \
	--with-gnutls \
	--with-zlib \
	%{?with_ipv6:--with-ipv6} \
	--with-spooldir=%{_var}/cache/wwwoffle
%{__make} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig,%{name}/{hyperestraier,namazu}} \
	$RPM_BUILD_ROOT%{_var}/cache/wwwoffle/{ftp,prev{out,time}{1,2,3,4,5,6,7},temp}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv -f $RPM_BUILD_ROOT%{_var}/cache/wwwoffle/html $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s %{_datadir}/%{name} $RPM_BUILD_ROOT%{_var}/cache/wwwoffle/html

# changes for wwwoffle-namazu
mv -f $RPM_BUILD_ROOT%{_var}/cache/wwwoffle/search/namazu/conf/*rc \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/namazu
mv -f $RPM_BUILD_ROOT%{_var}/cache/wwwoffle/search/namazu/scripts/wwwoffle-mknmz-* \
	$RPM_BUILD_ROOT%{_bindir}

# changes for wwwoffle-hyperestraier
mv -f $RPM_BUILD_ROOT%{_var}/cache/wwwoffle/search/hyperestraier/conf/estseek.{conf,tmpl,top} \
	$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/hyperestraier
ln -sf %{_sysconfdir}/%{name}/hyperestraier/estseek.conf \
	$RPM_BUILD_ROOT%{_var}/cache/wwwoffle/search/hyperestraier/conf/estseek.conf
ln -sf %{_sysconfdir}/%{name}/hyperestraier/estseek.tmpl \
	$RPM_BUILD_ROOT%{_var}/cache/wwwoffle/search/hyperestraier/conf/estseek.tmpl
ln -sf %{_sysconfdir}/%{name}/hyperestraier/estseek.top \
	$RPM_BUILD_ROOT%{_var}/cache/wwwoffle/search/hyperestraier/conf/estseek.top
mv -f $RPM_BUILD_ROOT%{_var}/cache/wwwoffle/search/hyperestraier/scripts/wwwoffle-estcmd-full \
	$RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT%{_mandir}/fr/man5
install doc/fr/wwwoffle.conf.man $RPM_BUILD_ROOT%{_mandir}/fr/man5/wwwoffle.conf.5
rm -f doc/fr/wwwoffle.conf.man*

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

mv doc/es/contrib/README doc/es/README-contrib
mv doc/es/testprogs/README doc/es/README-testprogs
rm -rf doc/es/{contrib,testprogs}
rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

%triggerpostun -- %{name} < 2.7

echo Note!  Your existing cache and config file look earlier than
echo 2.7 version. There have been several major changes in config
echo file and some minor changes in cache handling. Read the file
echo NEWS and following at a pinch for details. All the necessary
echo files are available from within your documentation directory.

%triggerpostun -- %{name} < 2.8

chown wwwoffle:wwwoffle -R \
	%{_var}/cache/wwwoffle/{ftp,http,lastout,lasttime,local,monitor,outgoing,temp,prevout[1-7],prevtime[1-7]}

%clean
rm -rf $RPM_BUILD_ROOT

%pretrans
test -h %{_var}/cache/wwwoffle/html || rm -rf %{_var}/cache/wwwoffle/html

%pre
%groupadd -g 119 -r -f wwwoffle
%useradd -o -r -u 119 -s /bin/false -g wwwoffle -c "%{name} daemon" -d /var/cache/wwwoffle wwwoffle

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "%{name} daemon"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove wwwoffle
	%groupremove wwwoffle
fi

%files
%defattr(644,root,root,755)
%lang(de) %doc doc/de
%lang(es) %doc doc/es
%lang(fr) %doc doc/fr
%lang(pl) %doc doc/pl
%doc doc/{ANNOUNCE,CHANGES.CONF,FAQ,NEWS,README*}
%doc ChangeLog* conf/upgrade-config*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%dir %{_sysconfdir}/%{name}
%attr(660,root,wwwoffle) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/%{name}.conf
%{_mandir}/man[158]/*
%lang(fr) %{_mandir}/fr/man5/*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/default
%{_datadir}/%{name}/en
%lang(de) %{_datadir}/%{name}/de
%lang(es) %{_datadir}/%{name}/es
%lang(fr) %{_datadir}/%{name}/fr
%lang(it) %{_datadir}/%{name}/it
%lang(nl) %{_datadir}/%{name}/nl
%lang(pl) %{_datadir}/%{name}/pl
%lang(ru) %{_datadir}/%{name}/ru
%defattr(664,wwwoffle,wwwoffle,775)
%dir %{_var}/cache/wwwoffle
#%%{_var}/cache/wwwoffle/[!o]*
%{_var}/cache/wwwoffle/html
%dir %{_var}/cache/wwwoffle/ftp
%dir %{_var}/cache/wwwoffle/http
%dir %{_var}/cache/wwwoffle/lastout
%dir %{_var}/cache/wwwoffle/lasttime
%dir %{_var}/cache/wwwoffle/local
%dir %{_var}/cache/wwwoffle/monitor
%dir %{_var}/cache/wwwoffle/outgoing
%config(missingok) %{_var}/cache/wwwoffle/outgoing/*
%dir %{_var}/cache/wwwoffle/prevout[1-7]
%dir %{_var}/cache/wwwoffle/prevtime[1-7]
%dir %{_var}/cache/wwwoffle/temp
%dir %{_var}/cache/wwwoffle/search
%dir %{_var}/cache/wwwoffle/search/htdig
%dir %{_var}/cache/wwwoffle/search/htdig/db
%dir %{_var}/cache/wwwoffle/search/htdig/db-lasttime
%dir %{_var}/cache/wwwoffle/search/htdig/tmp
%dir %{_var}/cache/wwwoffle/search/htdig/conf
%config(noreplace) %verify(not md5 mtime size) %{_var}/cache/wwwoffle/search/htdig/conf/*
%dir %{_var}/cache/wwwoffle/search/htdig/scripts
%attr(754,root,root) %{_var}/cache/wwwoffle/search/htdig/scripts/*

%dir %{_var}/cache/wwwoffle/search/mnogosearch
%dir %{_var}/cache/wwwoffle/search/mnogosearch/db
%dir %{_var}/cache/wwwoffle/search/mnogosearch/conf
%config(noreplace) %verify(not md5 mtime size) %{_var}/cache/wwwoffle/search/mnogosearch/conf/*
%dir %{_var}/cache/wwwoffle/search/mnogosearch/scripts
%attr(754,root,root) %{_var}/cache/wwwoffle/search/mnogosearch/scripts/*

%files hyperestraier
%defattr(644,root,root,755)
%dir %{_var}/cache/wwwoffle/search/hyperestraier
%dir %{_var}/cache/wwwoffle/search/hyperestraier/conf
%dir %{_var}/cache/wwwoffle/search/hyperestraier/db
%dir %{_var}/cache/wwwoffle/search/hyperestraier/scripts
%attr(644,root,wwwoffle) %{_var}/cache/wwwoffle/search/hyperestraier/conf/estseek.conf
%attr(644,root,wwwoffle) %{_var}/cache/wwwoffle/search/hyperestraier/conf/estseek.tmpl
%attr(644,root,wwwoffle) %{_var}/cache/wwwoffle/search/hyperestraier/conf/estseek.top
%{_var}/cache/wwwoffle/search/hyperestraier/conf/estseek.help
%dir %{_sysconfdir}/%{name}/hyperestraier
%attr(640,root,wwwoffle) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/hyperestraier/estseek.conf
%attr(640,root,wwwoffle) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/hyperestraier/estseek.tmpl
%attr(640,root,wwwoffle) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/hyperestraier/estseek.top
%attr(750,root,root) %{_bindir}/wwwoffle-estcmd-full
%attr(750,root,wwwoffle) %{_var}/cache/wwwoffle/search/hyperestraier/scripts/wwwoffle-estseek

%files namazu
%defattr(644,root,root,755)
%dir %{_sysconfdir}/%{name}/namazu
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/namazu/*
%attr(755,root,root) %{_bindir}/wwwoffle-mknmz-*
%dir %{_var}/cache/wwwoffle/search/namazu/scripts
%attr(755,root,root) %{_var}/cache/wwwoffle/search/namazu/scripts/wwwoffle-namazu
%dir %{_var}/cache/wwwoffle/search/namazu
%dir %{_var}/cache/wwwoffle/search/namazu/db
