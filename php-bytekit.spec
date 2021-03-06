#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname		bytekit
Summary:	An extension to represent the opcodes generated by Zend Engine
Name:		%{php_name}-%{modname}
Version:	0.1.1
Release:	4
License:	Bytekit 1.0 (based on PHP 3.0)
Group:		Development/Languages/PHP
Source0:	http://www.bytekit.org/download/%{modname}-%{version}.tgz
# Source0-md5:	83d0a325713201947aec441f30be58d8
URL:		http://www.bytekit.org/
BuildRequires:	%{php_name}-devel
BuildRequires:	rpmbuild(macros) >= 1.666
%{?requires_php_extension}
Provides:	php(bytekit) = %{version}
Obsoletes:	php-bytekit < 0.1.1-3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Bytekit is a PHP extension that provides a userspace representation of
the opcodes generated by the Zend engine compiler built into PHP.

This extension provides not only access to the raw op_array data but
also contains a Zend engine disassembler that exports control flow
information in form of code flow graphs and basic blocks. Bytekit is
meant as a tool to understand the internals of PHP better, to debug
Zend engine error cases and as base to develop all kinds of static and
dynamic code analysis tools.

%prep
%setup -q -n %{modname}-%{version}

%build
phpize
%configure
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
%{_examplesdir}/%{name}-%{version}
