%define ruby_dist ruby-enterprise
%define ruby_dist_dash %{ruby_dist}-
%define _prefix /opt/ruby-enterprise
%define _gem %{_prefix}/bin/gem
%define _ruby %{_prefix}/bin/ruby

# Generated from chef-server-webui-0.10.0.rc.1.gem by gem2rpm -*- rpm-spec -*-
%define ruby_sitelib %(%{_ruby} -rrbconfig -e "puts Config::CONFIG['sitelibdir']")
%define gemdir %(%{_ruby} -rubygems -e 'puts Gem::dir' 2>/dev/null)
%define gemname chef-server-webui
%define geminstdir %{gemdir}/gems/%{gemname}-%{version}

Summary: A systems integration framework, built to bring the benefits of configuration management to your entire infrastructure
Name: %{?ruby_dist_dash}rubygem-%{gemname}
Version: 0.10.4
Release: 1%{?buildstamp}%{?dist}
Group: Development/Languages
License: GPLv2+ or Ruby
URL: http://wiki.opscode.com/display/chef
Source0: http://rubygems.org/downloads/%{gemname}-%{version}.gem
Source1: chef-server-webui.init
Source2: chef-server-webui.sysconfig
Source3: chef-server-webui.logrotate
Source4: config.rb

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: %{?ruby_dist_dash}rubygems
Requires: %{?ruby_dist_dash}rubygem(merb-core) = 1.1.3
Requires: %{?ruby_dist_dash}rubygem(merb-assets) = 1.1.3
Requires: %{?ruby_dist_dash}rubygem(merb-helpers) = 1.1.3
Requires: %{?ruby_dist_dash}rubygem(merb-haml) = 1.1.3
Requires: %{?ruby_dist_dash}rubygem(merb-param-protection) = 1.1.3
Requires: %{?ruby_dist_dash}rubygem(json) <= 1.4.6
Requires: %{?ruby_dist_dash}rubygem(json) >= 1.4.4
Requires: %{?ruby_dist_dash}rubygem(thin) >= 0
Requires: %{?ruby_dist_dash}rubygem(haml) >= 0
Requires: %{?ruby_dist_dash}rubygem(ruby-openid) >= 0
Requires: %{?ruby_dist_dash}rubygem(coderay) >= 0
BuildRequires: %{?ruby_dist_dash}rubygems
BuildArch: noarch
Provides: %{?ruby_dist_dash}rubygem(%{gemname}) = %{version}

Requires(post): chkconfig
Requires(preun): chkconfig
# This is for /sbin/service
Requires(preun): initscripts
Requires(postun): initscripts

%description
A systems integration framework, built to bring the benefits of configuration
management to your entire infrastructure.


%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{gemdir}
mkdir -p %{buildroot}/etc/rc.d/init.d
mkdir -p %{buildroot}/var/log/chef
mkdir -p %{buildroot}%{_sysconfdir}/chef
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig/
mkdir -p %{buildroot}/var/run/chef
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d

%{_gem} install --local --install-dir %{buildroot}%{gemdir} \
                --force --rdoc %{SOURCE0}
mkdir -p %{buildroot}/%{_bindir}
mv %{buildroot}%{gemdir}/bin/* %{buildroot}/%{_bindir}
rmdir %{buildroot}%{gemdir}/bin
find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

cp %{SOURCE1} %{buildroot}/etc/rc.d/init.d/chef-server-webui
chmod +x %{buildroot}/etc/rc.d/init.d/chef-server-webui
cp %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/chef-server-webui
cp %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/chef-server-webui
cp %{SOURCE4} %{buildroot}%{_sysconfdir}/chef/webui.rb

%clean
rm -rf %{buildroot}

%post
# This adds the proper /etc/rc*.d links for the script
/sbin/chkconfig --add chef-server-webui

if [ -z "`/usr/bin/id chef 2> /dev/null`" ]; then
	%{_sbindir}/adduser chef >/dev/null 2>&1 
	chown -R chef %{_sysconfdir}/chef
fi

%preun
if [ $1 -eq 0 ] ; then
    /sbin/service chef-server-webui stop >/dev/null 2>&1
    /sbin/chkconfig --del chef-server-webui
fi

%postun
if [ "$1" -ge "1" ] ; then
    /sbin/service chef-server-webui restart >/dev/null 2>&1 || :
fi

%files
%defattr(-, root, root, -)
%{_bindir}/chef-server-webui
%{gemdir}/gems/%{gemname}-%{version}/
%doc %{gemdir}/doc/%{gemname}-%{version}
%doc %{geminstdir}/README.rdoc
%doc %{geminstdir}/LICENSE
%doc %{geminstdir}/config.ru
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec
%config(noreplace) %{_sysconfdir}/sysconfig/chef-server-webui
%config(noreplace) %{_sysconfdir}/logrotate.d/chef-server-webui
%config(noreplace) %{_sysconfdir}/chef/webui.rb
%{_sysconfdir}/rc.d/init.d/chef-server-webui
%{_sysconfdir}/chef

%changelog
* Mon Oct  3 2011 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0.10.4-1.hhg
- Rebuild for Ruby Enterprise Edition

* Wed Jul 27 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.4-1
- preparing for 0.10.4

* Mon Jul 25 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-3
- updated release version format

* Mon Jul 25 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-2
- rubygem-chef-server.spec

* Mon Jul 04 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.2-1
- upstream update

* Fri May 06 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-2
- changes in default config

* Tue May 03 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0-1
- upstream update

* Mon May 02 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.2-1
- upstream update

* Fri Apr 29 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.1-2
- add init script
- create default dirs
- add logrotate and server.rb configs
- create chef user

* Thu Apr 28 2011 Sergio Rubio <rubiojr@frameos.org> - 0.10.0.rc.1-1
- Initial package
