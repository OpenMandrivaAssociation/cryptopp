#!/bin/sh
curl -L https://cryptopp.com/ 2>/dev/null |grep -E 'Version [0-9.]* released' |head -n1 |sed -e 's,.*Version ,,;s, released.*,,'
