%define	lib_major 1
%define lib_name %mklibname xml %{lib_major}

Summary:	The libXML library
Name:		libxml
Version:	1.8.17
Release:	%mkrel 11
License:	LGPL
Group:		System/Libraries
URL:		http://www.xmlsoft.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
# (gb) 1.8.17-2mdk add missing include
Patch0:		libxml-1.8.17-includes.patch
# (fc) 1.8.17-3mdk remove -L/usr/lib from xml-config --libs
Patch1:		libxml-1.8.17-libdir.patch
BuildRequires:	zlib-devel autoconf2.5 automake1.4

%description
This library allows you to manipulate XML files.

%package -n	%{lib_name}
Summary:	%{summary}
Group:		%{group}
Obsoletes:	%{name}
Provides:	%{name} = %{version}-%{release}

%description -n	%{lib_name}
This library allows you to manipulate XML files.

%package -n	%{lib_name}-devel
Summary:	Libraries, includes and other files to develop libxml applications
Group:		Development/C
# (gb) As of 1.8.17 version, I can't see any changes that would
# require a specific dependency on release, thus permitting
# rpmlintfixes
Requires:	%{lib_name} = %{version}
Requires:	zlib-devel
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{lib_name}-devel
This packages contains the libraries, include and other files 
you can use to develop libxml applications.

%prep

%setup -q
%patch0 -p1 -b .includes
%patch1 -p1 -b .libdir

# remove conflicting ltconfig and ltmain.sh
rm -f ltmain.sh ltconfig
libtoolize --force
aclocal-1.4
automake-1.4
#also needed by patch1
FORCE_AUTOCONF_2_5=1 autoconf

%build
%configure
%make

%check
# all tests must pass
make check

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

%post -p /sbin/ldconfig -n %{lib_name}

%postun -p /sbin/ldconfig -n %{lib_name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %{lib_name}
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING COPYING.LIB TODO
%{_libdir}/lib*.so.*

%files -n %{lib_name}-devel
%defattr(-, root, root)
%{_bindir}/xml-config
%{_libdir}/lib*.so
%{_libdir}/*a
%{_libdir}/*.sh
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_datadir}/gnome-xml


