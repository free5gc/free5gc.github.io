# TLS Certificates and Keys

!!! danger "Do not use the bundled keys outside a lab"
    The private keys under `cert/` are public. With the default `oauth: true`, anyone can sign OAuth2 access tokens that NFs accept with the bundled `nrf.key`, even over `http`. Generate your own keys before any non-lab use.

## Which files are used for what

| File | Used by | Purpose |
| --- | --- | --- |
| `root.key`, `root.pem` | NRF | Root CA; with OAuth2, NRF signs `nrf.pem` and NF certificates with it |
| `nrf.key` | NRF | Signs OAuth2 access tokens |
| `nrf.pem` | NFs | Verifies access tokens; with OAuth2, NRF rewrites it on each start |
| `<nf>.key`, `<nf>.pem` | each NF | HTTPS server certificate (`scheme: https`) |
| `chf.key`, `chf.pem` | CHF | Also Diameter TLS (ABMF / Rf) |
| `n3iwf.*`, `tngf.*` | N3IWF, TNGF | N3IWF: IKEv2 towards the UE; the bundled n3iwf and tngf files are the same key |
| `af.pem` | NRF | Webconsole public key; NRF creates it, no need to generate |

## 1. Generate a new PKI

Use RSA keys without a passphrase; free5GC cannot load other key types or encrypted keys. Do not let NRF regenerate a missing `root.pem`: it creates a non-CA certificate that cannot sign NF certificates.

You need `bash`, GNU `date` and OpenSSL 1.1.1 or later. Move the bundled files out of `cert/`, then run the blocks below in order inside the empty `cert/`, in the same terminal.

**Settings.** Use your own country and home network domain (`5gc.mnc<MNC>.mcc<MCC>.3gppnetwork.org`, three-digit MNC). For free5gc-compose, set `EXTRA_DOMAIN=free5gc.org`.

```bash
COUNTRY=TW
DOMAIN=5gc.mnc093.mcc208.3gppnetwork.org
EXTRA_DOMAIN=""
DAYS_LEFT=$(( ( $(date -u -d 2030-12-31T23:59:59Z +%s) - $(date -u +%s) ) / 86400 ))
DAYS=$(( DAYS_LEFT < 365 ? DAYS_LEFT : 365 ))
```

**Root CA.** Creates `root.key` and a self-signed `root.pem` valid until the end of 2030.

```bash
cat > root.cnf <<EOF
[req]
distinguished_name = dn
x509_extensions = root_ca
[dn]
[root_ca]
basicConstraints = critical,CA:TRUE,pathlen:0
keyUsage = critical,keyCertSign,cRLSign
subjectKeyIdentifier = hash
EOF
(umask 077 && openssl genrsa -out root.key 3072)
openssl req -x509 -new -config root.cnf -key root.key -sha256 -days $DAYS_LEFT \
  -subj "/C=$COUNTRY/O=$DOMAIN/CN=free5GC Root CA" -out root.pem
```

**NF certificate function.** `nf_cert <name> <FQDN> [<NF type>]` creates `<name>.key` and a root-signed `<name>.pem`.

```bash
nf_cert() (
  set -eu
  umask 077
  nf=$1 fqdn=$2 type=${3:-}
  san="DNS:$fqdn"
  if [ -n "$EXTRA_DOMAIN" ] && [ "$nf.$EXTRA_DOMAIN" != "$fqdn" ]; then
    san="$san,DNS:$nf.$EXTRA_DOMAIN"
  fi
  openssl genrsa -out $nf.key 2048
  openssl req -new -config root.cnf -key $nf.key \
    -subj "/C=$COUNTRY/O=$DOMAIN/CN=$fqdn" -out $nf.csr
  {
    echo "keyUsage = critical,digitalSignature"
    echo "extendedKeyUsage = serverAuth,clientAuth"
    echo "subjectAltName = critical,$san"
    echo "subjectKeyIdentifier = hash"
    echo "authorityKeyIdentifier = keyid:always"
    if [ -n "$type" ]; then
      echo "1.3.6.1.5.5.7.1.34 = ASN1:SEQUENCE:nftypes"
      echo "[nftypes]"
      echo "t1 = IA5STRING:$type"
    fi
  } > $nf.ext
  openssl x509 -req -in $nf.csr -CA root.pem -CAkey root.key -CAcreateserial \
    -sha256 -days $DAYS -extfile $nf.ext -out $nf.pem
  rm $nf.csr $nf.ext
)
```

**One certificate per NF.** Adjust the FQDNs. AMF uses `<AMF-id>.amf.<DOMAIN>`; N3IWF and TNGF must match `fqdn` / `FQDN` in their configs.

```bash
nf_cert amf   amf1.amf.$DOMAIN   AMF
nf_cert ausf  ausf.$DOMAIN       AUSF
nf_cert bsf   bsf.$DOMAIN        BSF
nf_cert chf   chf.$DOMAIN        CHF
nf_cert nef   nef.$DOMAIN        NEF
nf_cert nrf   nrf.$DOMAIN        NRF
nf_cert nssf  nssf.$DOMAIN       NSSF
nf_cert pcf   pcf.$DOMAIN        PCF
nf_cert scp   scp.$DOMAIN        SCP
nf_cert smf   smf.$DOMAIN        SMF
nf_cert udm   udm.$DOMAIN        UDM
nf_cert udr   udr.$DOMAIN        UDR
nf_cert n3iwf n3iwf.free5gc.org  N3IWF
nf_cert tngf  tngf.free5gc.org
```

**Clean up.**

```bash
rm -f root.cnf root.srl
```

??? note "3GPP TS 33.310 (Rel-17) references"
    | Setting | Reference |
    | --- | --- |
    | SHA-256; RSA 3072 root expiring before 2031 | §6.1.1 |
    | Root `CA:TRUE, pathlen:0`, `keyCertSign, cRLSign` | §6.1.4a |
    | NF: signed by the root, ≤ 1 year, `C=` / `O=<home domain>`, `keyUsage`, `extendedKeyUsage`, critical `subjectAltName` with the FQDN, `nfTypes` (RFC 9310) | §6.1.3c.3 |
    | FQDN formats (`nrf.<DOMAIN>`, AMF Name) | TS 23.003 §28.3.2 |
    | N3IWF certificate must match the selected N3IWF | TS 33.501 §7.2.1 |

## 2. Use the new files

- The default paths already match. If NFs run on other hosts, copy `nrf.pem` and their own `<nf>.key` / `<nf>.pem` there.
- Set `certificateAuthority` (`n3iwfcfg.yaml`) and `CertificateAuthority` (`tngfcfg.yaml`) to `cert/root.pem`.
- free5gc-compose: add `./cert:/free5gc/cert` to the `n3iwf` volumes; its image contains the bundled key.
- Restart free5GC.
- `cert/` is tracked by git: `git checkout .`, `git stash` or `git reset --hard` restore the bundled keys.

## 3. Verify

Run inside `cert/`. Bundled certificates are self-signed, so they fail here.

```bash
for f in root amf ausf bsf chf n3iwf nef nrf nssf pcf scp smf tngf udm udr; do
  openssl verify -CAfile root.pem $f.pem
done | grep -v ': OK$'                       # expect no output
openssl x509 -in amf.pem -noout -enddate -ext keyUsage,extendedKeyUsage,subjectAltName
```

## Known limitations

- `scheme: https` with `oauth: true` does not work: NFs send no client certificate, so none can register.
- NF HTTPS clients do not verify server certificates, so your own PKI does not stop a man-in-the-middle on SBI. Protect the SBI network.
