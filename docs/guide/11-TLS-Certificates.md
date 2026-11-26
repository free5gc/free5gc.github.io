# TLS Certificates and Keys

!!! danger "Do not use the bundled keys outside a lab"
    The private keys under `cert/` are public. With the default `oauth: true`, anyone can sign OAuth2 access tokens that NFs accept with the bundled `nrf.key`, even over `http`. Generate your own keys before any non-lab use.

## Which files are used for what

| File | Used by | Purpose |
| --- | --- | --- |
| `root.key`, `root.pem` | NRF | Root CA; with OAuth2, NRF signs `nrf.pem` and NF certificates with it |
| `nrf.key` | NRF | Signs OAuth2 access tokens |
| `nrf.pem` | NFs | Verifies access tokens; with OAuth2, NRF replaces it if it has no `urn:uuid:` URI SAN |
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

**NF certificate function.** `nf_cert <name> <FQDN> [<NF type>] [<IP>]` creates `<name>.key` and a root-signed `<name>.pem`. The IP is only needed for [certificate verification](#4-enable-certificate-verification).

```bash
nf_cert() (
  set -eu
  umask 077
  nf=$1 fqdn=$2 type=${3:-} ip=${4:-}
  san="DNS:$fqdn"
  if [ -n "$EXTRA_DOMAIN" ] && [ "$nf.$EXTRA_DOMAIN" != "$fqdn" ]; then
    san="$san,DNS:$nf.$EXTRA_DOMAIN"
  fi
  if [ -n "$ip" ]; then
    san="$san,IP:$ip"
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

**One certificate per NF.** Adjust the FQDNs and IPs. AMF uses `<AMF-id>.amf.<DOMAIN>`; the IP is the NF's `registerIPv4` (the defaults in `config/` are shown); N3IWF and TNGF must match `fqdn` / `FQDN` in their configs.

```bash
nf_cert amf   amf1.amf.$DOMAIN   AMF   127.0.0.18
nf_cert ausf  ausf.$DOMAIN       AUSF  127.0.0.9
nf_cert bsf   bsf.$DOMAIN        BSF   127.0.0.15
nf_cert chf   chf.$DOMAIN        CHF   127.0.0.113
nf_cert nef   nef.$DOMAIN        NEF   127.0.0.5
nf_cert nrf   nrf.$DOMAIN        NRF   127.0.0.10
nf_cert nssf  nssf.$DOMAIN       NSSF  127.0.0.31
nf_cert pcf   pcf.$DOMAIN        PCF   127.0.0.7
nf_cert scp   scp.$DOMAIN        SCP   127.0.0.6
nf_cert smf   smf.$DOMAIN        SMF   127.0.0.2
nf_cert udm   udm.$DOMAIN        UDM   127.0.0.3
nf_cert udr   udr.$DOMAIN        UDR   127.0.0.4
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

## 4. Enable certificate verification

Needs free5GC built from `main` after v4.3.0. By default NFs accept any server certificate. With `verify: true`, an NF checks the certificate chain and host name of every NF it calls over HTTPS, and drops the connection if the check fails.

1. In every NF config, set `scheme: https` and `verify: true`, and use `https://` in `nrfUri`. NRF reads `verify` under `sbi.cert`, the other NFs under `sbi.tls`:

    ```yaml
    sbi:
      scheme: https
      tls:            # nrfcfg.yaml: cert
        verify: true
        pem: cert/amf.pem
        key: cert/amf.key
    ```

2. Each certificate must contain the host that other NFs connect to: the NF's `registerIPv4`, and for NRF the host in `nrfUri`. The IPs in the `nf_cert` lines cover the defaults in `config/`; with free5gc-compose, `EXTRA_DOMAIN` adds the host names.
3. Add `root.pem` to the system trust store on every NF host, then restart free5GC. NFs trust the system CA list; there is no setting for a CA file. On Ubuntu:

    ```bash
    sudo cp cert/root.pem /usr/local/share/ca-certificates/free5gc-root.crt
    sudo update-ca-certificates
    ```

    free5gc-compose: mount `./cert/root.pem` at `/etc/ssl/certs/free5gc-root.pem` in each NF service.

Keep `oauth: false` with `https` (see below). NEF also applies `verify` to its PFD change notifications and AF callbacks.

## Known limitations

- `scheme: https` with `oauth: true` does not work: NFs send no client certificate, so none can register.
- `verify` is off by default, so your own PKI alone does not stop a man-in-the-middle on SBI. [Enable it](#4-enable-certificate-verification) or protect the SBI network.
- With `verify: true`, NFs trust every CA in the system list, not only `root.pem`, and check only the host name, not the NF instance ID or NF type in the certificate.
