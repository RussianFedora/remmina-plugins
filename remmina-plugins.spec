%global minorversion 0.9

Name:           remmina-plugins
Version:        0.9.2
Release:        6%{?dist}
Summary:        Plugins for Remmina Remote Desktop Client

Group:          Applications/Internet
License:        GPLv2+
URL:            http://remmina.sourceforge.net/
Source0:        http://downloads.sourceforge.net/remmina/%{name}-%{version}.tar.gz
# from https://bugzilla.redhat.com/show_bug.cgi?id=656120
Patch0:         remmina-plugins-0.9.2-32bpp.patch
# taken from http://remmina.git.sourceforge.net/git/gitweb.cgi?p=remmina/remmina;a=commit;h=3a512f55
# fixes https://bugzilla.redhat.com/show_bug.cgi?id=753792
Patch1:         remmina-plugins-0.9.2-fix-libssh-0.5-compatibility.patch
# Taken from http://remmina.git.sourceforge.net/git/gitweb.cgi?p=remmina/remmina;a=commit;h=3f6c309f
# fixes https://bugzilla.redhat.com/show_bug.cgi?id=753792
Patch2:         remmina-plugins-0.9.2-add-another-ssh_seet_fd_towrite.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  intltool, 
BuildRequires:  gtk2-devel
BuildRequires:  remmina-devel >= %{minorversion}
BuildRequires:  libssh-devel
BuildRequires:  libxkbfile-devel


%description
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

Remmina supports multiple network protocols in an integrated and consistent
user interface. Currently NX, RDP, Telepathy, VNC, XDMCP and SSH are supported.

This package contains the plugins for Remmina.


%package        common
Summary:        Common files for Remmina Remote Desktop Client plugins
Group:          Applications/System
Requires:       remmina >= 0.9

%description    common
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains files shared among all plugins for the Remmina remote 
desktop client.


%package        nx
Summary:        NX plugin for Remmina Remote Desktop Client
Group:          Applications/System
Requires:       %{name}-common = %{version}-%{release}
Requires:       nx

%description    nx
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains the NX plugin for the Remmina remote desktop client.


%package        rdp
Summary:        RDP plugin for Remmina Remote Desktop Client
Group:          Applications/System
BuildRequires:  freerdp-devel
Requires:       %{name}-common = %{version}-%{release}
Requires:       freerdp

%description    rdp
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains the Remote Desktop Protocol (RDP) plugin for the Remmina
remote desktop client.


%package        telepathy
Summary:        Telepathy plugin for Remmina Remote Desktop Client
Group:          Applications/System
BuildRequires:  telepathy-glib-devel
Requires:       %{name}-common = %{version}-%{release}

%description    telepathy
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains the Telepathy plugin for the Remmina remote desktop 
client.


%package        vnc
Summary:        VNC plugin for Remmina Remote Desktop Client
Group:          Applications/System
BuildRequires:  gnutls-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libvncserver-devel
Requires:       %{name}-common = %{version}-%{release}

%description    vnc
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains the VNC plugin for the Remmina remote desktop 
client.


%package        xdmcp
Summary:        XDMCP plugin for Remmina Remote Desktop Client
Group:          Applications/System
Requires:       %{name}-common = %{version}-%{release}
Requires:       xorg-x11-server-Xephyr

%description    xdmcp
Remmina is a remote desktop client written in GTK+, aiming to be useful for 
system administrators and travelers, who need to work with lots of remote 
computers in front of either large monitors or tiny netbooks.

This package contains the XDMCP plugin for the Remmina remote desktop 
client.


%prep
%setup -q
%patch0 -p1 -b .32bpp

%if 0%{?fedora} >= 16
%patch1 -p2 -b .fix-libssh-0.5-compatibility
%patch2 -p2 -b .add-another-ssh_seet_fd_towrite
%endif


%build
%configure --disable-static --enable-vnc=dl
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
%find_lang %{name}


%clean
rm -rf $RPM_BUILD_ROOT


%files common -f %{name}.lang
%defattr(-,root,root,-)
# FIXME: Add ChangeLog, NEWS and README if not empty
%doc AUTHORS COPYING
%dir %{_libdir}/remmina/
%dir %{_libdir}/remmina/plugins/

%files nx
%defattr(-,root,root,-)
%{_libdir}/remmina/plugins/remmina-plugin-nx.so
%{_datadir}/remmina/icons/hicolor/*/emblems/remmina-nx.png

%files rdp
%defattr(-,root,root,-)
%{_libdir}/remmina/plugins/remmina-plugin-rdp.so
%{_datadir}/remmina/icons/hicolor/*/emblems/remmina-rdp-ssh.png
%{_datadir}/remmina/icons/hicolor/*/emblems/remmina-rdp.png

%files telepathy
%defattr(-,root,root,-)
%{_libdir}/remmina/plugins/remmina-plugin-telepathy.so
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Remmina.service
%{_datadir}/telepathy/clients/Remmina.client

%files vnc
%defattr(-,root,root,-)
%{_libdir}/remmina/plugins/remmina-plugin-vnc.so
%{_datadir}/remmina/icons/hicolor/*/emblems/remmina-vnc-ssh.png
%{_datadir}/remmina/icons/hicolor/*/emblems/remmina-vnc.png

%files xdmcp
%defattr(-,root,root,-)
%{_libdir}/remmina/plugins/remmina-plugin-xdmcp.so
%{_datadir}/remmina/icons/hicolor/*/emblems/remmina-xdmcp-ssh.png
%{_datadir}/remmina/icons/hicolor/*/emblems/remmina-xdmcp.png


%changelog
* Tue Mar 27 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 0.9.2-6
- rebuilt for new freerdp

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 31 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.2-4
- Fix nx plugin (#753792)
- Rebuild against libvncserver 0.9.8.2

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.9.2-3
- Rebuild for new libpng

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Christoph Wickert <cwickert@fedoraproject.org> - 0.9.2-1
- Update to 0.9.2
- Enable 32-bit color depth (#656120)

* Tue Nov 30 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.4-2
- Fix dependencies for remmina-plugins-common package
- Rename plugins packages to remmina-plugins-* for consistency.

* Sun Nov 21 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.4-1
- Update to 0.8.4

* Mon Jul 12 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.8.1-1
- Update to 0.8.1

* Fri Jun 25 2010 Christoph Wickert <cwickert@fedoraproject.org> - 0.7.99-1
- Initial package

