%define major 6
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define fver %(echo %{version} |sed s/\\\\.//g)

%define _disable_lto 1

Summary:	Public domain C++ class library of cryptographic schemes
Name:		cryptopp
Version:	5.6.5
Release:	3
License:	Public Domain
Group:		System/Libraries
Url:		http://www.cryptopp.com/
Source0:	http://www.cryptopp.com/%{name}%{fver}.zip
Source1:	cryptopp.pc
Patch0:		cryptopp-5.6.3-autotools.patch
BuildRequires:	doxygen

%description
Crypto++ Library is a public domain C++ class library of cryptographic 
schemes. Currently the library consists of the following features:

    * a class hierarchy with an API defined by abstract base classes 
    * AES(Rijndael) and AES candidates: RC6, MARS, Twofish, Serpent, 
      CAST-256
    * other symmetric block ciphers: IDEA, DES, Triple-DES (DES-EDE2 
      and DES-EDE3), DESX (DES-XEX3), RC2, RC5, Blowfish, TEA, XTEA, 
      SAFER, 3-WAY, GOST, SHARK, CAST-128, Square, Skipjack, Camellia, 
      SHACAL-2
    * generic block cipher modes: ECB, CBC, CBC ciphertext stealing 
      (CTS), CFB, OFB, counter mode (CTR)
    * stream ciphers: Salsa20, Panama, ARC4, SEAL, WAKE, WAKE-OFB, 
      BlumBlumShub
    * public-key cryptography: RSA, DSA, ElGamal, Nyberg-Rueppel (NR),
      Rabin, Rabin-Williams (RW), LUC, LUCELG, DLIES (variants of 
      DHAES), ESIGN
    * padding schemes for public-key systems: PKCS#1 v2.0, OAEP, PSS, 
      PSSR, IEEE P1363 EMSA2 and EMSA5
    * key agreement schemes: Diffie-Hellman (DH), Unified
      Diffie-Hellman (DH2), Menezes-Qu-Vanstone (MQV), LUCDIF, XTR-DH
    * elliptic curve cryptography: ECDSA, ECNR, ECIES, ECDH, ECMQV
    * one-way hash functions: SHA-1, MD2, MD4, MD5, HAVAL, RIPEMD-128, 
      RIPEMD-256, RIPEMD-160, RIPEMD-320, Tiger, SHA-2 (SHA-224, 
      SHA-256, SHA-384, and SHA-512), Panama, WHIRLPOOL
    * message authentication codes: MD5-MAC, HMAC, XOR-MAC, CBC-MAC, 
      DMAC, Two-Track-MAC
    * cipher constructions based on hash functions: Luby-Rackoff, MDC
    * pseudo random number generators (PRNG): ANSI X9.17 appendix C, 
      PGP's RandPool
    * password based key derivation functions: PBKDF1 and PBKDF2 from 
      PKCS #5
    * Shamir's secret sharing scheme and Rabin's information dispersal 
      algorithm (IDA)
    * DEFLATE (RFC 1951) compression/decompression with gzip (RFC 
      1952) and zlib (RFC 1950) format support
    * fast multi-precision integer (bignum) and polynomial operations, 
      with SSE2 optimizations for Pentium 4 processors, and support for 
      64-bit CPUs
    * finite field arithmetics, including GF(p) and GF(2^n)
    * prime number generation and verification
    * various miscellaneous modules such as base 64 coding and 32-bit 
      CRC
    * class wrappers for these operating system features (optional):
          o high resolution timers on Windows, Unix, and MacOS
          o Berkeley and Windows style sockets
          o Windows named pipes
          o /dev/random, /dev/urandom, /dev/srandom
          o Microsoft's CryptGenRandom on Windows 
    * A high level interface for most of the above, using a 
      filter/pipeline metaphor
    * benchmarks and validation testing
    * FIPS 140-2 Validated 

Because one purpose of the project is to act as a repository of public 
domain (not copyrighted) cryptographic source code, the code in 
Crypto++ was either written specifically for this project by its 
contributors and placed in the public domain, or derived from other 
sources that are public domain (again with the exception of mars.cpp).

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Base shared library part of %{name}
Group:		System/Libraries

%description -n %{libname}
Crypto++ Library is a free C++ class library of cryptographic schemes.

This package contains the library needed to run programs dynamically
linked with %{name}.

%files -n %{libname}
%{_libdir}/libcryptopp.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and development documentation for %{name}
Group:		Development/C++
Requires:	%{libname} = %{EVRD}

%description -n %{devname}
Crypto++ Library is a free C++ class library of cryptographic schemes.

This package contains the header files and development documentation
for %{name}.

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

#----------------------------------------------------------------------------

%package doc
Summary:	Documentation for %{name}
Group:		Development/C++
Obsoletes:	lib%{name}-doc < %{EVRD}

%description doc
Crypto++ Library is a free C++ class library of cryptographic schemes.

This package contains documentation for %{name}.

%files doc
%doc html-docs License.txt Readme.txt

#----------------------------------------------------------------------------

%package progs
Summary:	Programs for manipulating %{name} routines
Group:		Development/Other
Obsoletes:	lib%{name}-progs < %{EVRD}

%description progs
Crypto++ Library is a free C++ class library of cryptographic schemes.

This package contains programs for manipulating %{name} routines.

%files progs
%{_bindir}/cryptest
%{_datadir}/%{name}

#----------------------------------------------------------------------------

%prep
%setup -qc
rm -f GNUmakefile
%apply_patches
# fix file perms
chmod go+r *

%build
autoreconf -fi
%configure --disable-static

%make
doxygen

%install
%makeinstall_std

sed -i -e 's/\r$//g' License.txt Readme.txt

# Install pkg-config file
install -D -m 0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/cryptopp.pc
# Set variables
sed -i "s|@PREFIX@|%{_prefix}|g;s|@LIBDIR@|%{_libdir}|g;s|@INCLUDEDIR@|%{_includedir}|g;s|@VERSION@|%{version}|g" %{buildroot}%{_libdir}/pkgconfig/cryptopp.pc

install -d %{buildroot}%{_datadir}/%{name}/TestVectors
install -m 0644 TestVectors/* %{buildroot}%{_datadir}/%{name}/TestVectors
install -d %{buildroot}%{_datadir}/%{name}/TestData
install -m 0644 TestData/* %{buildroot}%{_datadir}/%{name}/TestData

rm -f %{buildroot}%{_bindir}/cryptestcwd

%check
./cryptestcwd v

