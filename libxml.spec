%define	lib_major 1
%define lib_name %mklibname xml %{lib_major}

Summary:	The libXML library
Name:		libxml
Version:	1.8.17
Release:	%mkrel 20
License:	LGPL
Group:		System/Libraries
URL:		http://www.xmlsoft.org/
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources/%{name}/%{name}-%{version}.tar.bz2
# (gb) 1.8.17-2mdk add missing include
Patch0:		libxml-1.8.17-includes.patch
# (fc) 1.8.17-3mdk remove -L/usr/lib from xml-config --libs
Patch1:		libxml-1.8.17-libdir.patch
Patch2:		libxml-1.8.17-open.patch
Patch3:		libxml-1.8.17-fix-str-fmt.patch
Patch4:		libxml-1.8.17-CVE-2009-2414,2416.diff
Patch5:		libxml-1.8.17-CVE-2011-1944.diff
BuildRequires:	zlib-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch2 -p1
%patch3 -p0 -b .str
%patch4 -p0 -b .CVE-2009-2414,2416
%patch5 -p0 -b .CVE-2011-1944

%build
autoreconf -fi
%configure2_5x
%make

%check
# all tests must pass
make check

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std

%if %mdkversion < 200900
%post -p /sbin/ldconfig -n %{lib_name}
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig -n %{lib_name}
%endif

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


%changelog
* Sun Oct 09 2011 Oden Eriksson <oeriksson@mandriva.com> 1.8.17-18.1
- P5: security fix for CVE-2011-1944 (redhat)

* Fri Apr 29 2011 Oden Eriksson <oeriksson@mandriva.com> 1.8.17-18mdv2011.0
+ Revision: 660302
- mass rebuild

* Thu Nov 25 2010 Oden Eriksson <oeriksson@mandriva.com> 1.8.17-17mdv2011.0
+ Revision: 601063
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.8.17-16mdv2010.1
+ Revision: 520967
- rebuilt for 2010.1

* Wed Aug 12 2009 Oden Eriksson <oeriksson@mandriva.com> 1.8.17-15mdv2010.0
+ Revision: 415501
- P4: security fix for CVE-2009-2414 and CVE-2009-2416

* Thu Apr 09 2009 Funda Wang <fwang@mandriva.org> 1.8.17-14mdv2009.1
+ Revision: 365427
- fix str fmt

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.8.17-14mdv2009.0
+ Revision: 265003
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu May 29 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.8.17-13mdv2009.0
+ Revision: 213115
- Specify mode when calling open(2) with O_CREAT flag. Instead of using
  default umask, follow pattern already existing in file.

* Sun Jan 13 2008 Thierry Vignaud <tv@mandriva.org> 1.8.17-12mdv2008.1
+ Revision: 150863
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.8.17-11mdv2008.0
+ Revision: 89852
- rebuild


* Tue Oct 31 2006 Oden Eriksson <oeriksson@mandriva.com> 1.8.17-10mdv2007.0
+ Revision: 74789
- bunzip patches
- misc spec file fixes
- Import libxml

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 1.8.17-9mdk
- Rebuild

* Mon Feb 28 2005 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.8.17-8mdk
- rpmlint fixes
- cleanups for libdir patch and multiarch support

* Wed Jun 09 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.8.17-7mdk
- force use of automake1.4 and autoconf2.5
- fix %%{lib_major} macro
- cosmetics

* Mon Dec 22 2003 Stefan van der Eijk <stefan@eijk.nu> - 1.8.17-6mdk
- rebuild for new pkgconfig Requires

