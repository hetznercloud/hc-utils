# SPEC file overview:
# https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/#con_rpm-spec-file-overview
# Fedora packaging guidelines:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8
%global predict 1
%else
%global predict 0
%endif

Name:		hc-utils
Version:	0.0.1
Release:	0%{?dist}
Summary:	A set of utilities for Hetzner Cloud
Group:		System Tools

License:	MIT
URL:		https://github.com/hetznercloud/hc-utils
Source0:	81-hc-network-interfaces.rules
Source1:	99-hc-volume-automount.rules
Source2:	hc-ifscan
Source3:	hc-net-ifup@.service
Source4:	hc-net-scan.service
Source5:	90-hc-utils.preset
Source6:	81-hc-network-interfaces.rules.legacy
Source7:	hc-ifscan.legacy

BuildArch:	noarch
BuildRequires:	systemd-units
Requires:	curl
Requires:	dhclient
Requires:	iproute
Requires:	systemd-units

%description
hc-utils contains utilities to automatically configure
Hetzner Cloud private network interfaces and block storage volumes

%prep

%build

%install
install -d -m755 $RPM_BUILD_ROOT%{_udevrulesdir}
install -pm644 %{SOURCE1} $RPM_BUILD_ROOT%{_udevrulesdir}

install -d -m755 $RPM_BUILD_ROOT%{_unitdir}
install -pm644 %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/hc-net-scan.service
install -pm644 %{SOURCE3} $RPM_BUILD_ROOT%{_unitdir}/hc-net-ifup@.service

install -m644 -D %{SOURCE5} $RPM_BUILD_ROOT%{_prefix}/lib/systemd/system-preset/90-hc-utils.preset

install -d -m755 $RPM_BUILD_ROOT%{_sbindir}
%if %{predict}
install -m644 %{SOURCE0} $RPM_BUILD_ROOT%{_udevrulesdir}/81-hc-network-interfaces.rules
install -m755 %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}/hc-ifscan
%else
install -m644 %{SOURCE6} $RPM_BUILD_ROOT%{_udevrulesdir}/81-hc-network-interfaces.rules
install -m755 %{SOURCE7} $RPM_BUILD_ROOT%{_sbindir}/hc-ifscan
%endif # predict

%post
%systemd_post hc-net-scan.service
%systemd_post hc-net-ifup@.service

%preun
%systemd_preun hc-net-scan.service
%systemd_preun hc-net-ifup@.service

%files
%{_udevrulesdir}/81-hc-network-interfaces.rules
%{_udevrulesdir}/99-hc-volume-automount.rules
%{_sbindir}/hc-ifscan
%attr(0644,root,root) %{_unitdir}/hc-net-scan.service
%attr(0644,root,root) %{_unitdir}/hc-net-ifup@.service
%{_prefix}/lib/systemd/system-preset/90-hc-utils.preset

%doc

%license

%changelog
* Wed Jul 03 2019 Markus Schade <markus.schade@hetzner.com>
- initial packaging as rpm
