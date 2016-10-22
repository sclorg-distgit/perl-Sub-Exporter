%{?scl:%scl_package perl-Sub-Exporter}

# We need to patch the test suite if we have an old version of Test::More
%global quite_old_test_more %(%{?scl:scl enable %{scl} '}perl -MTest::More -e %{?scl:'"}'%{?scl:"'}print (($Test::More::VERSION < 0.94) ? 1 : 0);%{?scl:'"}'%{?scl:"'} 2>/dev/null || echo 0%{?scl:'})
%global old_test_more %(%{?scl:scl enable %{scl} '}perl -MTest::More -e %{?scl:'"}'%{?scl:"'}print (($Test::More::VERSION < 0.88) ? 1 : 0);%{?scl:'"}'%{?scl:"'} 2>/dev/null || echo 0%{?scl:'})

Name:		%{?scl_prefix}perl-Sub-Exporter
Version:	0.987
Release:	10%{?dist}
Summary:	Sophisticated exporter for custom-built routines
License:	GPL+ or Artistic
Group:		Development/Libraries
URL:		https://metacpan.org/release/Sub-Exporter
Source0:	http://cpan.metacpan.org/authors/id/R/RJ/RJBS/Sub-Exporter-%{version}.tar.gz
Patch0:		Sub-Exporter-0.987-tm094.patch
Patch1:		Sub-Exporter-0.987-tm088.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	%{?scl_prefix}perl
BuildRequires:	%{?scl_prefix}perl-generators
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.30
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
%if !%{defined perl_small}
BuildRequires:	%{?scl_prefix}perl(Test::Pod)
%endif
# Runtime
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:	%{?scl_prefix}perl(Package::Generator)

# Don't want doc-file provides or dependencies
%global our_docdir %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}

%if 0%{?rhel} < 7
# RPM 4.8 style
%{?filter_setup:
%filter_provides_in ^%{our_docdir}/
%filter_requires_in ^%{our_docdir}/
%filter_from_requires /^%{?scl_prefix}perl(Data::OptList)$/d
%filter_from_requires /^%{?scl_prefix}perl(Params::Util)$/d
%?perl_default_filter
}
%else
# RPM 4.9 style
%global __provides_exclude_from ^%{our_docdir}/
%global __requires_exclude_from ^%{our_docdir}/
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^%{?scl_prefix}perl\\((Data::OptList|Params::Util)\\)$
%endif

%description
Sub::Exporter provides a sophisticated alternative to Exporter.pm. It allows
for renaming, currying/sub-generation, and other cool stuff.

ACHTUNG! If you're not familiar with Exporter or exporting, read
Sub::Exporter::Tutorial first!

%prep
%setup -q -n Sub-Exporter-%{version}

# We need to patch the test suite if we have an old version of Test::More
%if %{quite_old_test_more}
%patch0
%endif
%if %{old_test_more}
%patch1
%endif

# Fix shellbangs
find t/ -type f -exec \
    %{?scl:scl enable %{scl} '}perl -MExtUtils::MakeMaker -e %{?scl:'"}'%{?scl:"'}ExtUtils::MM_Unix->fixin(qw{{}})%{?scl:'"}'%{?scl:"'}%{?scl:'} \;


%if 0%{?rhel} < 7
# Filter bogus provides/requires if we don't have rpm ≥ 4.9
%global provfilt /bin/sh -c "%{__perl_provides} | grep -Ev '^perl[(]Test::SubExporter.*[)]'"
%global __perl_provides %{provfilt}
%global reqfilt /bin/sh -c "%{__perl_requires} | grep -Ev '^perl[(](base|Test::SubExporter.*)[)]'"
%global __perl_requires %{reqfilt}
%endif

%build
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name .packlist -exec rm -f {} \;
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}
%{?scl:scl enable %{scl} '}make test TEST_FILES="$(echo $(find xt/ -name %{?scl:'"}'%{?scl:"'}*.t%{?scl:'"}'%{?scl:"'}))"%{?scl:'}

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
%{_mandir}/man3/Sub::Exporter.3*
%{_mandir}/man3/Sub::Exporter::Cookbook.3*
%{_mandir}/man3/Sub::Exporter::Tutorial.3*
%{_mandir}/man3/Sub::Exporter::Util.3*

%changelog
* Tue Jul 19 2016 Petr Pisar <ppisar@redhat.com> - 0.987-10
- SCL

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.987-9
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.987-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan  7 2016 Paul Howarth <paul@city-fan.org> - 0.987-7
- Don't use %%define

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.987-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.987-5
- Perl 5.22 rebuild

* Fri Jan 16 2015 Petr Pisar <ppisar@redhat.com> - 0.987-4
- Do not hard-code interpreter name

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.987-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.987-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

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
