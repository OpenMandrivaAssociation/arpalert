Summary:	A monitor ethernet networks
Name:		arpalert
Version:	2.0.9
Release:	%mkrel 2
License:	GPL
Group:		Monitoring
URL:		http://www.arpalert.org/
Source0:	http://www.arpalert.org/src/%{name}-%{version}.tar.gz
Source1:	arpalert.init
Patch0:		arpalert-optflags.diff
BuildRequires:	libpcap-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-buildroot

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
rm -rf %{buildroot}

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGES COPYING README
%{_initrddir}/arpalert
%dir %{_sysconfdir}/arpalert
%config(noreplace) %{_sysconfdir}/arpalert/*
%{_sbindir}/arpalert
%{_mandir}/man8/arpalert.8*
%dir %attr(0755,%{name},%{name}) /var/log/%{name}
%dir %attr(0755,%{name},%{name}) /var/run/%{name}
%dir %attr(0755,%{name},%{name}) %{_localstatedir}/lib/%{name}
