%{?scl:%scl_package perl-Sub-Exporter}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}perl-Sub-Exporter
Version:	0.987
Release:	3%{?dist}
Summary:	Sophisticated exporter for custom-built routines
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		https://metacpan.org/release/Sub-Exporter
Source0:	http://cpan.metacpan.org/authors/id/R/RJ/RJBS/Sub-Exporter-%{version}.tar.gz
Patch0:		Sub-Exporter-0.987-tm094.patch
Patch1:		Sub-Exporter-0.987-tm088.patch
BuildRoot:	%{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	%{?scl_prefix}perl(Carp)
BuildRequires:	%{?scl_prefix}perl(Data::OptList) >= 0.1
BuildRequires:	%{?scl_prefix}perl(Package::Generator)
BuildRequires:	%{?scl_prefix}perl(Params::Util) >= 0.14
BuildRequires:	%{?scl_prefix}perl(Sub::Install) >= 0.92
# Test suite
BuildRequires:	%{?scl_prefix}perl(base)
BuildRequires:	%{?scl_prefix}perl(Exporter)
BuildRequires:	%{?scl_prefix}perl(File::Spec)
BuildRequires:	%{?scl_prefix}perl(IO::Handle)
BuildRequires:	%{?scl_prefix}perl(IPC::Open3)
BuildRequires:	%{?scl_prefix}perl(lib)
BuildRequires:	%{?scl_prefix}perl(subs)
BuildRequires:	%{?scl_prefix}perl(Test::More)
# Extra tests
BuildRequires:	%{?scl_prefix}perl(Test::Pod)
# Runtime
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})
Requires:	%{?scl_prefix}perl(Package::Generator)

# We need to patch the test suite if we have an old version of Test::More
%{?scl:%global quite_old_test_more %(scl enable %{scl} "perl -MTest::More -e 'print ((\\$Test::More::VERSION < 0.94) ? 1 : 0)'" 2>/dev/null || echo 0)}
%{!?scl:%global quite_old_test_more %(perl -MTest::More -e 'print ($Test::More::VERSION < 0.94 ? 1 : 0);' 2>/dev/null || echo 0)}
%{?scl:%global old_test_more %(scl enable %{scl} "perl -MTest::More -e 'print ((\\$Test::More::VERSION < 0.88) ? 1 : 0)'" 2>/dev/null || echo 0)}
%{!?scl:%global old_test_more %(perl -MTest::More -e 'print ($Test::More::VERSION < 0.88 ? 1 : 0);' 2>/dev/null || echo 0)}

# Don't want doc-file provides or dependencies
%global our_docdir %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{?scl:%{name}}%{!?scl:%{pkg_name}}-%{version}}
%global __provides_exclude_from %{our_docdir}/
%global __requires_exclude_from %{our_docdir}/

%if ( 0%{?rhel} && 0%{?rhel} < 7 )
%filter_provides_in %{our_docdir}
%filter_requires_in %{our_docdir}
%filter_setup
%endif

%description
Sub::Exporter provides a sophisticated alternative to Exporter.pm. It allows
for renaming, currying/sub-generation, and other cool stuff.

ACHTUNG! If you're not familiar with Exporter or exporting, read
Sub::Exporter::Tutorial first!

%prep
%setup -q -n Sub-Exporter-%{version}

echo %{our_docdir} %{name} %{pkg_name}
# We need to patch the test suite if we have an old version of Test::More
%if 00%{quite_old_test_more}
%patch0
%endif
%if 00%{old_test_more}
%patch1
%endif

# Fix shellbangs
find t/ -type f -exec sed -i -e 's|^#!perl|#!/usr/bin/perl|' {} \;

# Filter bogus provides/requires if we don't have rpm ≥ 4.9
%global provfilt /bin/sh -c "%{__perl_provides} | grep -Ev '^perl[(]Test::SubExporter.*[)]'"
%define __perl_provides %{provfilt}
%global reqfilt /bin/sh -c "%{__perl_requires} | grep -Ev '^perl[(](base|Test::SubExporter.*)[)]'"
%define __perl_requires %{reqfilt}

%build
%{?scl:scl enable %{scl} "}
perl Makefile.PL INSTALLDIRS=vendor
%{?scl:"}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} "}
make pure_install DESTDIR=%{buildroot}
%{?scl:"}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}
%{?scl:scl enable %{scl} - << \EOF}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%{?scl:EOF}

%clean
rm -rf %{buildroot}

%files
%doc Changes README t/
%dir %{perl_vendorlib}/Sub/
%dir %{perl_vendorlib}/Sub/Exporter/
%{perl_vendorlib}/Sub/Exporter.pm
%{perl_vendorlib}/Sub/Exporter/Util.pm
%doc %{perl_vendorlib}/Sub/Exporter/Cookbook.pod
%doc %{perl_vendorlib}/Sub/Exporter/Tutorial.pod
%{_mandir}/man3/Sub::Exporter.3pm*
%{_mandir}/man3/Sub::Exporter::Cookbook.3pm*
%{_mandir}/man3/Sub::Exporter::Tutorial.3pm*
%{_mandir}/man3/Sub::Exporter::Util.3pm*

%changelog
* Tue Feb 11 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.987-3
- Fixed getting of %%old_test_more
- Resolves: rhbz#1063206

* Thu Nov 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.987-2
- Rebuild for SCL

* Sat Oct 19 2013 Paul Howarth <paul@city-fan.org> - 0.987-1
- Update to 0.987 (update bugtracker metadata)
- Update patches as needed

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.986-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 31 2013 Paul Howarth <paul@city-fan.org> - 0.986-3
- Handle filtering of provides/requires from unversioned doc-dirs from F-20

* Sun Jul 21 2013 Petr Pisar <ppisar@redhat.com> - 0.986-2
- Perl 5.18 rebuild

* Sat Jun 15 2013 Paul Howarth <paul@city-fan.org> - 0.986-1
- Update to 0.986 (typo fixes in docs)
- Use metacpan URLs

* Thu Feb 21 2013 Paul Howarth <paul@city-fan.org> - 0.985-1
- Update to 0.985 (documentation fixes)
- Add patch to support building with Test::More < 0.88
- Run the extra tests too
- BR: perl(File::Find) and perl(File::Temp) for test suite
- BR: perl(Test::Pod) for the extra tests

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.984-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Petr Pisar <ppisar@redhat.com> - 0.984-4
- Specify all dependencies

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.984-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 0.984-2
- Perl 5.16 rebuild

* Tue Jun  5 2012 Paul Howarth <paul@city-fan.org> - 0.984-1
- Update to 0.984 (documentation fixes)
- Add filters for provides/requires from the test suite
- BR: perl(base) and perl(Exporter) for the test suite

* Sun Mar 18 2012 Paul Howarth <paul@city-fan.org> - 0.982-11
- Drop %%defattr, redundant since rpm 4.4

* Sat Mar  3 2012 Paul Howarth <paul@city-fan.org> - 0.982-10
- Explicitly require perl(Package::Generator)
- Make %%files list more explicit
- Mark POD files as %%doc
- Use DESTDIR rather than PERL_INSTALL_ROOT
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Use tabs

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.982-8
- Perl mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.982-6
- Rebuild to fix problems with vendorarch/lib (#661697)

* Thu May 06 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.982-5
- Mass rebuild with perl-5.12.0

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> - 0.982-4
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.982-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.982-1
- Update to 0.982

* Sun Oct 26 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.981-1
- Update to 0.981

* Thu Oct 23 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.980-1
- Update to 0.980

* Mon Jun 30 2008 Chris Weyl <cweyl@alumni.drew.edu> - 0.979-1
- Update to 0.979
- Drop BR's on: perl(Test::Pod::Coverage), perl(Test::Pod)

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.978-2
- Rebuild for perl 5.10 (again)

* Thu Jan 24 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.978-1
- Update to 0.978
- Fix license tag
- Rebuild for new perl

* Thu Aug 09 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.975-1
- Update to 0.975

* Fri Jun 01 2007 Chris Weyl <cweyl@alumni.drew.edu> - 0.974-1
- Update to 0.974

* Sat Dec 09 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.972-1
- Update to 0.972

* Thu Sep 07 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.970-2
- Bump

* Sat Sep 02 2006 Chris Weyl <cweyl@alumni.drew.edu> - 0.970-1
- Specfile autogenerated by cpanspec 1.69.1
