Summary:	WWW Offline Explorer - Caching Web Proxy Server (IPv6)
Summary(pl):	Eksplorator Offline World Wide Web ze wsparciem dla IPv6
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
BuildRequires:	flex
Prereq:		rc-scripts >= 0.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The wwwoffled program is a simple proxy server with special features
for use with dial-up internet links.  This means that it is possible to
browse web pages and read them without having to remain connected.

%description -l de
Ein (HTTP/FTP) Proxy Server für Computer mit Wählverbindungen ins Internet.
Folgendes wird unterstützt:
- Seiten werden lokal gespeichert und können jederzeit erneut abgerufen
  werden, auch OHNE Verbindung ins Internet
- Seiten, die nicht lokal vorhanden sind, werden 'bestellt'.
- Seiten können abonniert, d.h. regelmäßig heruntergeladen, werden; dies
  auch rekursiv.
- Alle lokal vorhandenen Seiten sind auf verschiedene Weisen indiziert und
  durchsuchbar.
- Steuerung erfolgt per Web-Browser, Kommandozeile und einer einfachen
  Konfigurationsdatei
- Jede Meldung von WWWOFFLE kann durch eigene ersetzt werden (so wurde auch
  diese Übersetzung realisiert)
- WWWOFFLE unterstützt verschiedene Authentifikationsmethoden

%description -l es
Un servidor proxy HTTP/FTP para ordenadores con conexión intermitente a
internet.
- Almacenado de páginas vistas mientras se estuvo conectado para releerlas
  más tarde.
- Revisión de páginas almacenadas mientras no se está conectado, con la
  habilidad de seguir enlaces y marcar otras páginas para recogida.
- Recogida de páginas especificadas de forma no interactiva.
- Monitorizado de páginas para recogida regular.
- Múltiples índices de las páginas almacenadas para una selección fácil.
- Opción para seleccionar páginas de forma interactiva o en línea de
  comandos de manera individual o recursiva.
- Todas las opciones se contralan usando un simple fichero de configuración
  con una página web para editarlo.

%description -l pl
Serwer proxy HTTP/FTP dla komputerów z dostêpem do internetu typu dial-up.
- Buforowanie stron przegl±danych podczas po³±czenia.
- Przegl±danie buforowanych stron bez potrzeby po³±czenia, z mo¿liwo¶cia
  pod±¿ania za ³±czami i oznaczania innych stron do pobrania.
- Pobieranie okre¶lonych stron nieinteraktywnie.
- Monitorowanie stron dla regularnego pobierania.
- Wiele indeksów przechowywanych w buforze stron dla ³atwego ich wyboru.
- Interaktywne lub z linii komend opcje wyboru stron do pobrania
  indywidualnie lub rekursywnie.
- Wszystkie opcje s± kontrolowane przy u¿yciu prostego pliku konfiguracji
  z mo¿liwo¶ci± edycji z poziomu strony web.

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
%dir %{_var}/cache/%{name}/outgoing
%config(missingok) %{_var}/cache/%{name}/outgoing/*
