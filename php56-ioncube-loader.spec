# spec file for php-ioncube-loader
#
# Copyright (c) 2012-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{?scl:          %scl_package             php-ioncube-loader}
%global extname       ioncube_loader
%global debug_package %{nil}
%global with_zts      0%{?__ztsphp:1}

Name:          php56-ioncube-loader
Summary:       Loader for ionCube Encoded Files
Version:       4.7.3
Release:       1%{?dist}
License:       Distribuable
Group:         Development/Languages

URL:           http://www.ioncube.com
Source0:       http://downloads2.ioncube.com/loader_downloads/%{extname}s_lin_x86.tar.bz2
Source1:       http://downloads2.ioncube.com/loader_downloads/%{extname}s_lin_x86-64.tar.bz2

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: php56-devel

# ABI check
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}

%if 0%{?fedora} < 20 && 0%{?rhel} < 7
# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}
%endif


%description
Loader for ionCube Encoded Files.


%prep
%setup -q -T -c

%ifarch x86_64
tar xvf %{SOURCE1}
%else
tar xvf %{SOURCE0}
%endif

# Drop in the bit of configuration
cat > %{extname}.nts << 'EOF'
; Enable %{extname} extension module
zend_extension = %{php_extdir}/%{extname}.so
EOF

%if %{with_zts}
cat > %{extname}.zts << 'EOF'
; Enable %{extname} extension module
zend_extension = %{php_ztsextdir}/%{extname}.so
EOF
%endif


%build
# tarball provides binaries


%install
rm -rf %{buildroot}
ver=$(%{__php} -r 'echo PHP_MAJOR_VERSION.".".PHP_MINOR_VERSION;')

if [ ! -f ioncube/%{extname}_lin_${ver}.so ]; then
  : Module for PHP $ver not provided
  exit 1
fi

install -D -pm 755 ioncube/%{extname}_lin_${ver}.so    %{buildroot}%{php_extdir}/%{extname}.so
install -D -m 644  %{extname}.nts                      %{buildroot}%{php_inidir}/%{extname}.ini

%if %{with_zts}
install -D -pm 755 ioncube/%{extname}_lin_${ver}_ts.so %{buildroot}%{php_ztsextdir}/%{extname}.so
install -D -m 644  %{extname}.zts                      %{buildroot}%{php_ztsinidir}/%{extname}.ini
%endif


%check
# simple module load test
%{__php} --no-php-ini \
    --define zend_extension=%{buildroot}%{php_extdir}/%{extname}.so \
    --modules | grep ionCube

%if %{with_zts}
%{__ztsphp} --no-php-ini \
    --define zend_extension=%{buildroot}%{php_ztsextdir}/%{extname}.so \
    --modules | grep ionCube
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
#%doc ioncube/*txt

%config(noreplace) %{php_inidir}/%{extname}.ini
%{php_extdir}/%{extname}.so

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{extname}.ini
%{php_ztsextdir}/%{extname}.so
%endif

