Summary:	WWW Offline Explorer - Caching Web Proxy Server (IPv6)
Summary(pl):	Eksplorator Offline World Wide Web (IPv6)
Name:		wwwoffle
Version:	2.7g
Release:	2
License:	GPL
Group:		Networking/Daemons
#Source0:	ftp://ftp.demon.co.uk/pub/unix/httpd/%{name}-%{version}.tgz
Source0:	ftp://ftp.ibiblio.org/pub/Linux/apps/www/servers/%{name}-%{version}.tgz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-replacement.patch
URL:		http://www.gedanken.demon.co.uk/wwwoffle/
BuildRequires:	flex
BuildRequires:	zlib-devel
PreReq:		rc-scripts >= 0.2.0
Requires(pre):	fileutils
Requires(pre):	sh-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%description -l de
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

%description -l es
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

%description -l pl
Serwer proxy HTTP/FTP dla komputerów z dostêpem do internetu typu
dial-up.
- Buforowanie stron przegl±danych podczas po³±czenia.
- Przegl±danie buforowanych stron bez potrzeby po³±czenia, z
  mo¿liwo¶cia pod±¿ania za ³±czami i oznaczania innych stron do
  pobrania.
- Pobieranie okre¶lonych stron nieinteraktywnie.
- Monitorowanie stron dla regularnego pobierania.
- Wiele indeksów przechowywanych w buforze stron dla ³atwego ich
  wyboru.
- Interaktywne lub z linii komend opcje wyboru stron do pobrania
  indywidualnie lub rekursywnie.
- Wszystkie opcje s± kontrolowane przy u¿yciu prostego pliku
  konfiguracji z mo¿liwo¶ci± edycji z poziomu strony web.

%prep
%setup -q
%patch0 -p1

%build
%configure2_13 \
	--with-zlib \
	--with-ipv6 \
	--with-spooldir=%{_var}/cache/%{name}
%{__make} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig} \
	$RPM_BUILD_ROOT%{_var}/cache/%{name}/{ftp,prev{out,time}{1,2,3,4,5,6,7},temp}

%{__make} install DESTDIR=$RPM_BUILD_ROOT
mv -f $RPM_BUILD_ROOT%{_var}/cache/%{name}/html $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s %{_datadir}/%{name} $RPM_BUILD_ROOT%{_var}/cache/%{name}/html

install src/uncompress-cache $RPM_BUILD_ROOT%{_bindir}
install -s src/convert-cache conf

install -d $RPM_BUILD_ROOT%{_mandir}/fr/man5
install doc/fr/wwwoffle.conf.man $RPM_BUILD_ROOT%{_mandir}/fr/man5/wwwoffle.conf.5
rm -f doc/fr/wwwoffle.conf.man*

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

mv doc/es/contrib/README doc/es/README-contrib
mv doc/es/testprogs/README doc/es/README-testprogs
rm -rf doc/es/{contrib,testprogs}

%triggerpostun -- wwwoffle < 2.7

echo Note!  Your existing cache and config file look earlier than
echo 2.7 version. There have been several major changes in config
echo file and some minor changes in cache handling. Read the file
echo NEWS and following at a pinch for details. All the necessary
echo files are available from within your documentation directory.

%clean
rm -rf $RPM_BUILD_ROOT

%pre
test -h %{_var}/cache/%{name}/html || rm -rf %{_var}/cache/%{name}/html

%files
%defattr(644,root,root,755)
%lang(de) %doc doc/de
%lang(es) %doc doc/es
%lang(fr) %doc doc/fr
%lang(pl) %doc doc/pl
%doc doc/{ANNOUNCE,CHANGES.CONF,CONVERT,FAQ,NEWS,README*}
%doc ChangeLog* conf/{convert-cache,upgrade-config*}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/%{name}
%attr(660,http,http) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}.conf
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
%defattr(664,http,http,775)
%dir %{_var}/cache/%{name}
#%{_var}/cache/%{name}/[!o]*
%dir %{_var}/cache/%{name}/ftp
%{_var}/cache/%{name}/html
%dir %{_var}/cache/%{name}/http
%dir %{_var}/cache/%{name}/lastout
%dir %{_var}/cache/%{name}/lasttime
%dir %{_var}/cache/%{name}/local
%dir %{_var}/cache/%{name}/monitor
%dir %{_var}/cache/%{name}/prevout1
%dir %{_var}/cache/%{name}/prevout2
%dir %{_var}/cache/%{name}/prevout3
%dir %{_var}/cache/%{name}/prevout4
%dir %{_var}/cache/%{name}/prevout5
%dir %{_var}/cache/%{name}/prevout6
%dir %{_var}/cache/%{name}/prevout7
%dir %{_var}/cache/%{name}/prevtime1
%dir %{_var}/cache/%{name}/prevtime2
%dir %{_var}/cache/%{name}/prevtime3
%dir %{_var}/cache/%{name}/prevtime4
%dir %{_var}/cache/%{name}/prevtime5
%dir %{_var}/cache/%{name}/prevtime6
%dir %{_var}/cache/%{name}/prevtime7
%dir %{_var}/cache/%{name}/temp
%dir %{_var}/cache/%{name}/outgoing
%config(missingok) %{_var}/cache/%{name}/outgoing/*
%dir %{_var}/cache/%{name}/search
%dir %{_var}/cache/%{name}/search/htdig
%dir %{_var}/cache/%{name}/search/htdig/db
%dir %{_var}/cache/%{name}/search/htdig/db-lasttime
%dir %{_var}/cache/%{name}/search/htdig/tmp
%dir %{_var}/cache/%{name}/search/htdig/conf
%attr(644,http,http) %config(noreplace) %verify(not md5 size mtime) %{_var}/cache/%{name}/search/htdig/conf/*
%dir %{_var}/cache/%{name}/search/htdig/scripts
%attr(655,http,http) %config(noreplace) %verify(not md5 size mtime) %{_var}/cache/%{name}/search/htdig/scripts/*

%dir %{_var}/cache/%{name}/search/mnogosearch
%dir %{_var}/cache/%{name}/search/mnogosearch/db
%dir %{_var}/cache/%{name}/search/mnogosearch/conf
%attr(644,http,http) %config(noreplace) %verify(not md5 size mtime) %{_var}/cache/%{name}/search/mnogosearch/conf/*
%dir %{_var}/cache/%{name}/search/mnogosearch/scripts
%attr(655,http,http) %config(noreplace) %verify(not md5 size mtime) %{_var}/cache/%{name}/search/mnogosearch/scripts/*

%dir %{_var}/cache/%{name}/search/namazu
%dir %{_var}/cache/%{name}/search/namazu/db
%dir %{_var}/cache/%{name}/search/namazu/conf
%attr(644,http,http) %config(noreplace) %verify(not md5 size mtime) %{_var}/cache/%{name}/search/namazu/conf/*
%dir %{_var}/cache/%{name}/search/namazu/scripts
%attr(655,http,http) %config(noreplace) %verify(not md5 size mtime) %{_var}/cache/%{name}/search/namazu/scripts/*
