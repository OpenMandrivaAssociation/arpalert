Summary:	A monitor ethernet networks
Name:		arpalert
Version:	2.0.12
Release:	2
License:	GPLv2
Group:		Monitoring
URL:		https://www.arpalert.org/
Source0:	http://www.arpalert.org/src/%{name}-%{version}.tar.gz
Source1:	arpalert.init
Patch0:		arpalert-2.0.9-fix-str-fmt.diff
BuildRequires:	libpcap-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre):	rpm-helper
Requires(postun): rpm-helper

%description
This software is used for monitoring ethernet networks. It listens on a network
interface (without using 'promiscuous' mode) and catches all conversations of
MAC address to IP request. It then compares the mac addresses it detected with
a pre-configured list of authorized MAC addresses. If the MAC is not in list,
arpalert launches a pre-defined user script with the MAC address and IP address
as parameters. This software can run in daemon mode; it's very fast (low CPU
and memory consumption). It responds at signal SIGHUP (configuration reload)
and at signals SIGTERM, SIGINT, SIGQUIT and SIGABRT (arpalert stops itself).

%prep

%setup -q
%patch0 -p0

%build
%serverbuild
%configure2_5x \
    --localstatedir=/var

perl -pi -e "s|^lock_dir.*|lock_dir=/var/run/%{name}|g" Makefile
perl -pi -e "s|^log_dir.*|log_dir=/var/log/%{name}|g" Makefile
%make

%install
%makeinstall_std

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}/var/log/%{name}
install -d %{buildroot}/var/run/%{name}
install -d %{buildroot}%{_localstatedir}/lib/%{name}

install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

# cleanup
rm -f %{buildroot}%{_includedir}/arpalert.h

%pre
%_pre_useradd %{name} %{_localstatedir}/lib/%{name} /bin/sh

%post
%_post_service %name

%preun
%_preun_service %name

%postun
%_postun_userdel %{name}

%files
%doc CHANGES COPYING README
%{_initrddir}/arpalert
%dir %{_sysconfdir}/arpalert
%config(noreplace) %{_sysconfdir}/arpalert/*
%{_sbindir}/arpalert
%{_mandir}/man8/arpalert.8*
%dir %attr(0755,%{name},%{name}) /var/log/%{name}
%dir %attr(0755,%{name},%{name}) /var/run/%{name}
%dir %attr(0755,%{name},%{name}) %{_localstatedir}/lib/%{name}


%changelog
* Sun Feb 14 2010 Sandro Cazzaniga <kharec@mandriva.org> 2.0.11-1mdv2010.1
+ Revision: 505945
- del patch, rename
- update to 2.0.11

* Sun Oct 04 2009 Oden Eriksson <oeriksson@mandriva.com> 2.0.9-5mdv2010.0
+ Revision: 453535
- fix build
- rebuild

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 2.0.9-3mdv2009.1
+ Revision: 298231
- rebuilt against libpcap-1.0.0

* Thu Jun 19 2008 Thierry Vignaud <tvignaud@mandriva.com> 2.0.9-2mdv2009.0
+ Revision: 226170
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Nov 19 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0.9-1mdv2008.1
+ Revision: 110278
- 2.0.9
- make it use %%serverbuild optflags

* Tue Aug 28 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0.8-1mdv2008.0
+ Revision: 72767
- 2.0.8
- conform to the 2008 specs (don't start it per default)

* Mon Aug 06 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0.7-1mdv2008.0
+ Revision: 59288
- 2.0.7

* Thu Jun 07 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0.6-1mdv2008.0
+ Revision: 36559
- 2.0.6
- reworked the initscript
- run it under the arpalert uid/gid
- added some directories


* Tue Mar 13 2007 Oden Eriksson <oeriksson@mandriva.com> 2.0.5-1mdv2007.1
+ Revision: 142177
- 2.0.5

  + Olivier Thauvin <nanardon@mandriva.org>
    - initial rpm

