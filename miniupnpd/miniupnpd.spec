Summary: UPnP IGD
Name: miniupnpd
Version: __VERSION__
Release: 1%{?dist}
License: MINIUPNP
Group: Applications/Network

Source0: %{name}-%{version}.tar.gz
Source1: miniupnpd
Source2: miniupnpd.service

URL: http://miniupnp.free.fr/
Packager: AdamRushad
BuildRequires: iptables-devel openssl-devel which iproute util-linux
Requires: iptables openssl-libs util-linux systemd

%description
Implements the Universal Plug and Play Internet
Gateway Device and NAT-PMP interfaces. Allows
users to forward ports on the firewall to themselves
without network administrator intervention. Admin
can set ACL to restrict who can map which ports.

%prep
%setup

%build
CONFIG_OPTIONS="--ipv6 --strict --vendorcfg --pcp-peer --portinuse" make -f Makefile.linux
make -f Makefile.linux check

%install
PREFIX="%{buildroot}" make -f Makefile.linux install
rm -f %{buildroot}%{_sysconfdir}/init.d/miniupnpd
install -D -m0755 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/miniupnpd
install -D -m0644 %{SOURCE2} %{buildroot}%{_unitdir}/miniupnpd.service
install miniupnpdctl %{buildroot}%{_sbindir}/miniupnpdctl

%post
%systemd_post miniupnpd.service

%preun
%systemd_preun miniupnpd.service

%postun
%systemd_postun_with_restart miniupnpd.service

%files
%license LICENSE
%doc README
%doc INSTALL
%{_sbindir}/miniupnpd
%{_sbindir}/miniupnpdctl
%config(noreplace) %{_sysconfdir}/miniupnpd/miniupnpd.conf
%{_sysconfdir}/miniupnpd/iptables_init.sh
%{_sysconfdir}/miniupnpd/iptables_removeall.sh
%{_sysconfdir}/miniupnpd/ip6tables_init.sh
%{_sysconfdir}/miniupnpd/ip6tables_removeall.sh
%{_sysconfdir}/miniupnpd/miniupnpd_functions.sh
%{_mandir}/man8/miniupnpd.8.gz
