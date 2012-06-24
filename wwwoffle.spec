Summary:	WWW Offline Explorer - Caching Web Proxy Server
Summary(pl):	Eksplorator Offline World Wide Web
Name:		wwwoffle
Version:	2.6c
Release:	2
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.demon.co.uk/pub/unix/httpd/%{name}-%{version}.tgz
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-replacement.patch
Patch1:		%{name}-install_dirs.patch
URL:		http://www.gedanken.demon.co.uk/wwwoffle/
BuildRequires:	flex
Prereq:		rc-scripts >= 0.2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The wwwoffled program is a simple proxy server with special features
for use with dial-up internet links. This means that it is possible to
browse web pages and read them without having to remain connected.

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
%patch1 -p1

%build
%{__make} all \
	INSTDIR=%{_prefix} \
	SPOOLDIR=%{_var}/cache/%{name} \
	CONFDIR=%{_sysconfdir} \
	CFLAGS="%{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	INSTDIR=$RPM_BUILD_ROOT%{_prefix} \
	SPOOLDIR=%{_var}/cache/%{name} \
	SPOOLDIR_BUILD=$RPM_BUILD_ROOT%{_var}/cache/%{name} \
	CONFDIR=%{_sysconfdir} \
	CONFDIR_BUILD=$RPM_BUILD_ROOT%{_sysconfdir} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	SBINDIR=$RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

gzip -9nf ANNOUNCE CHANGES.CONF CONVERT ChangeLog* FAQ NEWS \
	README README.* convert-cache upgrade-config*

%triggerpostun -- wwwoffle < 2.6

echo Your existing cache and config file are looking earlier than
echo 2.6 version. There have been several major changes in config
echo file and some minor changes in cache handling. Read the file
echo NEWS and following at a pinch for details. All the necessary
echo files are available from within your documentation directory.

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/sysconfig/%{name}
%attr(600,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/%{name}.conf
%{_mandir}/man[158]/*
%dir %{_var}/cache/%{name}
%{_var}/cache/%{name}/[!o]*
%dir %{_var}/cache/%{name}/outgoing
%config(missingok) %{_var}/cache/%{name}/outgoing/*
