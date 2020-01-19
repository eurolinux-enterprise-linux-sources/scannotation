%global namedreltag .Final
%global namedversion %{version}%{?namedreltag}
%global alphatag r12

Name: scannotation
Version: 1.0.3
Release:  0.7.%{alphatag}%{?dist}
Summary: A Java annotation scanner
Group: Development/Libraries
License: ASL 2.0
URL: http://scannotation.sourceforge.net

# How we created tarball:
# svn export -r 12  https://scannotation.svn.sourceforge.net/svnroot/scannotation scannotation-1.0.3.Final
# tar -caJf scannotation-1.0.3.Final.tar.xz scannotation-1.0.3.Final
Source0: %{name}-%{namedversion}.tar.xz
#Adding License file
Source1: License.txt

Patch0: %{name}-%{namedversion}-remove-dependencies.patch

BuildArch: noarch

BuildRequires: junit4
BuildRequires: javassist

BuildRequires: jpackage-utils
BuildRequires: java-devel
BuildRequires: maven-local
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-provider-junit4

Requires: jpackage-utils
Requires: java
Requires: javassist

%description
Scannotation is a Java library that creates an annotation database 
from a set of .class files.This database is really just a set of maps that index
what annotations are used and what classes are using them. Why do you need this? 
What if you are an annotation framework like an EJB 3.0 container and you want 
to automatically scan your classpath for EJB annotations so that you know what 
to deploy? Scannotation gives you apis that allow you to find archives in your 
classpath or WAR (web application) that you want to scan, then automatically 
scans them without loading each and every class within those archives

%package javadoc
Summary: Javadocs for %{name}
Group: Documentation
Requires: jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{name}-%{namedversion}
%patch0 -p1 -b .p0
cp -p %SOURCE1 .

%build
# building jar files using mvn
mvn-rpmbuild install javadoc:aggregate

%install
# JAR
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 %{name}/target/%{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar

# POM
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}-all.pom
install -pm 644 %{name}/pom.xml $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{name}.pom

# DEPMAP - this is still ok, but we use different pom
%add_maven_depmap JPP-%{name}.pom %{name}.jar

# all is the proper name in this case, this just to be there - not usable at all :)
%add_maven_depmap JPP-%{name}-all.pom

# APIDOCS
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -rp target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%files
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/*
%doc License.txt

%files javadoc
%{_javadocdir}/%{name}

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.3-0.7.r12
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.6.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.0.3-0.5.r12
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.4.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-0.3.r12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 14 2011 Kashyap Chamarthy <kashyapc@fedoraproject.org> 1.0.3-0.2.r12
- Preserve time stamps of files(License.txt in this case) being installed

* Thu Dec 1 2011 Kashyap Chamarthy <kashyapc@fedoraproject.org> 1.0.3-0.1.r12
- Initial packaging. With help from Ade Lee <vakwetu@fedoraproject.org>

