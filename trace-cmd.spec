# TODO:
# - add gui (make gui)
#
Summary:	trace-cmd - interacts with Ftrace Linux kernel internal tracer
Name:		trace-cmd
Version:	1.0.0
Release:	1
License:	GPLv2 and LGPLv2.1
Group:		Development/Tools
URL:		http://ftp.kernel.org/pub/linux/kernel/people/jkacur/trace-cmd/
Source0:	http://ftp.kernel.org/pub/linux/kernel/people/jkacur/trace-cmd/%{name}-%{version}.tar.bz2
# Source0-md5:	a15a33f5835955ad0704f2f29d6c5c24

BuildRequires:	asciidoc
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
trace-cmd is a user interface to Ftrace. Instead of needing to use the
debugfs directly, trace-cmd will handle of setting of options and
tracers and will record into a data file.

%prep
%setup -q

sed -i -e 's#$(prefix)/share/trace-cmd/#$(DESTDIR)%{_libdir}/trace-cmd/#g' Makefile

%build
%{__make} all doc \
	CC="%{__cc} %{rpmcppflags} %{rpmcflags} %{rpmldflags}" \
	V=1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install install_doc \
	DESTDIR=$RPM_BUILD_ROOT \
	prefix=$RPM_BUILD_ROOT%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/trace-cmd
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
