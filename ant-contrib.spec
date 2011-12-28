#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		subver	b2
%define		rel		1
Summary:	Collection of tasks for Ant
Name:		ant-contrib
Version:	1.0
Release:	0.%{subver}.%{rel}
License:	ASL 2.0
Group:		Development/Libraries
URL:		http://ant-contrib.sourceforge.net/
Source0:	http://downloads.sourceforge.net/ant-contrib/%{name}-%{version}%{subver}-src.tar.gz
# Source0-md5:	66511dddcef3dc9798db33dbaca0d3de
Patch0:		build_xml.patch
Patch1:		antservertest.patch
BuildRequires:	ant >= 1.6
BuildRequires:	ant-junit >= 1.6.2
BuildRequires:	java-bcel >= 5.0
BuildRequires:	java-junit >= 3.8.0
BuildRequires:	java-xerces
BuildRequires:	jdk >= 1.4.2
BuildRequires:	jpackage-utils >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	ant >= 1.6.2
Requires:	java(jaxp_parser_impl)
Requires:	java-junit >= 3.8.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Ant-Contrib project is a collection of tasks (and at one point
maybe types and other tools) for Apache Ant.

%package javadoc
Summary:	Javadoc for Ant contrib tasks
Group:		Documentation

%description javadoc
API documentation for Ant contrib tasks.

%prep
%setup -q -n %{name}
%patch0
%patch1
%undos manual/tasks/foreach.html manual/tasks/for.html

%{__rm} -r test/src/net/sf/antcontrib/antclipse

install -d test/lib

%build
junit_jar=$(find-jar junit)
xerces_jar=$(find-jar xercesImpl)
ln -sf $junit_jar test/lib
ln -sf $xerces_jar lib

export OPT_JAR_LIST="ant/ant-junit junit"
CLASSPATH=build/lib/ant-contrib-%{version}.jar:$CLASSPATH
%ant jar %{?with_javadoc:docs} \
	-Djavac.target=1.4 \
	-Djavac.source=1.4 \
	-Dversion=%{version} \
	-Dbcel.jar=file://%{_javadir}/bcel.jar

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}/ant
cp -p build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/ant/%{name}.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf build/docs/api

install -d $RPM_BUILD_ROOT%{_sysconfdir}/ant.d
echo "ant/ant-contrib" > $RPM_BUILD_ROOT%{_sysconfdir}/ant.d/ant-contrib

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc build/docs/LICENSE.txt
%doc build/docs/tasks/*
%{_sysconfdir}/ant.d/ant-contrib
%{_javadir}/ant/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
%endif
