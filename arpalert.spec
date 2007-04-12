Summary:	A monitor ethernet networks
Name:		arpalert
Version:	2.0.5
Release:	%mkrel 1
License:	GPL
Group:		Monitoring
URL:		http://www.arpalert.org/
Source0:	http://www.arpalert.org/src/%{name}-%{version}.tar.gz
Source1:	arpalert-init
BuildRequires:	libpcap-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-buildroot

%description
This software is used for monitoring ethernet networks.
It listens on a network interface (without using 'promiscuous' mode) and
catches all conversations of MAC address to IP request.
It then compares the mac addresses it detected with a pre-configured list
of authorized MAC addresses. If the MAC is not in list, arpalert launches
a pre-defined user script with the MAC address and IP address as parameters.
This software can run in daemon mode; it's very fast (low CPU and memory
consumption).
It responds at signal SIGHUP (configuration reload) and at signals SIGTERM,
SIGINT, SIGQUIT and SIGABRT (arpalert stops itself).

%prep

%setup -q

%build
%configure --localstatedir=%_var
%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}%{_initrddir}
install -m0755 %{SOURCE1} %{buildroot}%{_initrddir}/arpalert

%clean
rm -rf %{buildroot}

%post
%_post_service %name

%preun
%_preun_service %name

%files
%defattr(-,root,root)
%doc CHANGES COPYING README
%{_initrddir}/arpalert
%dir %{_sysconfdir}/arpalert
%config(noreplace) %{_sysconfdir}/arpalert/*
%{_sbindir}/arpalert
%{_mandir}/man8/arpalert.8*



