# TODO:
# - add gui (make gui)
#
Summary:	trace-cmd - interacts with Ftrace Linux kernel internal tracer
Name:		trace-cmd
Version:	2.4
Release:	1
License:	GPLv2 and LGPLv2.1
Group:		Development/Tools
URL:		http://git.kernel.org/?p=linux/kernel/git/rostedt/trace-cmd.git;a=summary
# git clone git://git.kernel.org/pub/scm/linux/kernel/git/rostedt/trace-cmd.git
# git archive --prefix=trace-cmd-2.4/ -o trace-cmd-2.4.tar.gz trace-cmd-v2.4
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	49af232eddd763cc799c346da6902f9c
Patch0:		%{name}-build.patch
BuildRequires:	asciidoc
BuildRequires:	docbook-dtd45-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	gtk+2-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
trace-cmd is a user interface to Ftrace. Instead of needing to use the
debugfs directly, trace-cmd will handle of setting of options and
tracers and will record into a data file.

%package gui
Summary:	Graphical frontend for trace-cmd
Group:		X11/Development/Tools
Requires:	%{name} = %{version}-%{release}

%description gui
Graphical frontend for trace-cmd.

%prep
%setup -q
%patch0 -p1

sed -i -e 's#MANPAGE_DOCBOOK_XSL =.*#MANPAGE_DOCBOOK_XSL = /usr/share/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl#g' Documentation/Makefile
sed -i -e 's#$(prefix)/share/trace-cmd/#$(prefix)/%{_lib}/trace-cmd/#g' Makefile

%build
%{__make} trace_plugin_dir all gui doc \
	CC="%{__cc} %{rpmcppflags} %{rpmcflags} %{rpmldflags}" \
	V=1 \
	prefix=%{_prefix} \
	libdir=%{_lib}

%install
rm -rf $RPM_BUILD_ROOT

# prevent trace_plugin_dir from being updated
sed -i -e 's#trace-util.o: trace_plugin_dir##g' Makefile
sed -i -e 's#= trace_plugin_dir tc_version.h#= tc_version.h#g' Makefile

%{__make} install install_gui install_doc \
	V=1 \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	libdir=%{_lib}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/trace-cmd
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%attr(755,root,root) %{_libdir}/%{name}/plugins/*.so
%{_mandir}/man1/trace-cmd*.1*
%{_mandir}/man5/trace-cmd*.5*

%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kernelshark
%attr(755,root,root) %{_bindir}/trace-graph
%attr(755,root,root) %{_bindir}/trace-view
