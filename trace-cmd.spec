Summary:	trace-cmd - interact with Ftrace Linux kernel internal tracer
Summary(pl.UTF-8):	trace-cmd - interakcja z Ftrace - wewnętrznym systemem śledzenia jądra Linuksa
Name:		trace-cmd
Version:	3.2
Release:	1
License:	GPL v2
Group:		Development/Tools
Source0:	https://git.kernel.org/pub/scm/utils/trace-cmd/trace-cmd.git/snapshot/%{name}-v%{version}.tar.gz
# Source0-md5:	aebecc253f0991368fe8d88c20b9713c
Patch0:		%{name}-link.patch
URL:		https://www.trace-cmd.org/
BuildRequires:	asciidoc
BuildRequires:	audit-libs-devel
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	libtraceevent-devel >= 1.5
BuildRequires:	libtracefs-devel >= 1.6
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	swig-python >= 2
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel >= 1.4.0
Requires:	libtraceevent >= 1.5
Requires:	libtracefs >= 1.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
trace-cmd is a user interface to Ftrace. Instead of needing to use the
debugfs directly, trace-cmd will handle of setting of options and
tracers and will record into a data file.

%description -l pl.UTF-8
trace-cmd to interfejs użytkownika do Ftrace. Zamiast konieczności
bezpośrednich odwołań do debugfs, trace-cmd obsługuje ustawianie opcji
i śledzenia oraz zapisuje wyniki do plików danych.

%package python
Summary:	Python plugin support for trace-cmd
Summary(pl.UTF-8):	Obsługa wtyczek trace-cmd napisanych w Pythonie
Group:		Development/Tools
Requires:	%{name} = %{version}-%{release}

%description python
Python (3.x) plugin support for trace-cmd.

%description python -l pl.UTF-8
Obsługa wtyczek trace-cmd napisanych w Pythonie (3.x).

%prep
%setup -q -n %{name}-v%{version}
%patch -P0 -p1

%{__sed} -i -e '1s,/usr/bin/env python2,%{__python},' python/event-viewer.py

%build
CFLAGS="%{rpmcflags}" \
CPPFLAGS="%{rpmcppflags}" \
LDFLAGS="%{rpmldflags}" \
%{__make} all doc \
	CC="%{__cc}" \
	PYTHON_VERS=python3 \
	V=1 \
	prefix=%{_prefix} \
	libdir_relative=%{_lib}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins

%{__make} install install_doc \
	DESTDIR=$RPM_BUILD_ROOT \
	BASH_COMPLETE_DIR=%{bash_compdir} \
	PYTHON_VERS=python3 \
	V=1 \
	prefix=%{_prefix} \
	libdir_relative=%{_lib}

chmod 755 $RPM_BUILD_ROOT%{_libdir}/%{name}/python/ctracecmd.so

# remove libtracecmd docs
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man3
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libtracecmd-doc
# just HTML'd manuals
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/trace-cmd

# python2/pygtk script
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/python/event-viewer.py

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/trace-cmd
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{bash_compdir}/trace-cmd.bash
%{_mandir}/man1/trace-cmd*.1*
%{_mandir}/man5/trace-cmd.dat.v*.5*

%files python
%defattr(644,root,root,755)
%dir %{_libdir}/%{name}/python
%attr(755,root,root) %{_libdir}/%{name}/python/ctracecmd.so
%{_libdir}/%{name}/python/tracecmd.py
