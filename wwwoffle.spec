Summary:	WWW Offline Explorer - Caching Web Proxy Server (IPv6)
Summary(pl):	Eksplorator Offline World Wide Web (IPv6)
Name:		wwwoffle
Version:	2.7e
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	ftp://ftp.demon.co.uk/pub/unix/httpd/%{name}-%{version}.tgz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-replacement.patch
URL:		http://www.gedanken.demon.co.uk/wwwoffle/
BuildRequires:	flex
BuildRequires:	zlib-devel
PreReq:		rc-scripts >= 0.2.0
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
Ein (HTTP/FTP) Proxy Server f�r Computer mit W�hlverbindungen ins
Internet. Folgendes wird unterst�tzt:
- Seiten werden lokal gespeichert und k�nnen jederzeit erneut
  abgerufen werden, auch OHNE Verbindung ins Internet
- Seiten, die nicht lokal vorhanden sind, werden 'bestellt'.
- Seiten k�nnen abonniert, d.h. regelm��ig heruntergeladen, werden;
  dies auch rekursiv.
- Alle lokal vorhandenen Seiten sind auf verschiedene Weisen indiziert
  und durchsuchbar.
- Steuerung erfolgt per Web-Browser, Kommandozeile und einer einfachen
  Konfigurationsdatei
- Jede Meldung von WWWOFFLE kann durch eigene ersetzt werden (so wurde
  auch diese �bersetzung realisiert)
- WWWOFFLE unterst�tzt verschiedene Authentifikationsmethoden

%description -l es
Un servidor proxy HTTP/FTP para ordenadores con conexi�n intermitente
a internet.
- Almacenado de p�ginas vistas mientras se estuvo conectado para
  releerlas m�s tarde.
- Revisi�n de p�ginas almacenadas mientras no se est� conectado, con
  la habilidad de seguir enlaces y marcar otras p�ginas para recogida.
- Recogida de p�ginas especificadas de forma no interactiva.
- Monitorizado de p�ginas para recogida regular.
- M�ltiples �ndices de las p�ginas almacenadas para una selecci�n
  f�cil.
- Opci�n para seleccionar p�ginas de forma interactiva o en l�nea de
  comandos de manera individual o recursiva.
- Todas las opciones se contralan usando un simple fichero de
  configuraci�n con una p�gina web para editarlo.

%description -l pl
Serwer proxy HTTP/FTP dla komputer�w z dost�pem do internetu typu
dial-up.
- Buforowanie stron przegl�danych podczas po��czenia.
- Przegl�danie buforowanych stron bez potrzeby po��czenia, z
  mo�liwo�cia pod��ania za ��czami i oznaczania innych stron do
  pobrania.
- Pobieranie okre�lonych stron nieinteraktywnie.
- Monitorowanie stron dla regularnego pobierania.
- Wiele indeks�w przechowywanych w buforze stron dla �atwego ich
  wyboru.
- Interaktywne lub z linii komend opcje wyboru stron do pobrania
  indywidualnie lub rekursywnie.
- Wszystkie opcje s� kontrolowane przy u�yciu prostego pliku
  konfiguracji z mo�liwo�ci� edycji z poziomu strony web.

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
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

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
%defattr(664,http,http,775)
%dir %{_var}/cache/%{name}
%{_var}/cache/%{name}/[!ho]*
%dir %{_var}/cache/%{name}/html
%{_var}/cache/%{name}/html/default
%{_var}/cache/%{name}/html/en
%lang(de) %{_var}/cache/%{name}/html/de
%lang(es) %{_var}/cache/%{name}/html/es
%lang(fr) %{_var}/cache/%{name}/html/fr
%lang(it) %{_var}/cache/%{name}/html/it
%lang(nl) %{_var}/cache/%{name}/html/nl
%lang(pl) %{_var}/cache/%{name}/html/pl
%lang(ru) %{_var}/cache/%{name}/html/ru
%{_var}/cache/%{name}/http
%dir %{_var}/cache/%{name}/outgoing
%config(missingok) %{_var}/cache/%{name}/outgoing/*
