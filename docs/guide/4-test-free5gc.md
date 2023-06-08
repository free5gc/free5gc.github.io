# Test free5GC

Start a Wireshark capture on any core-connected interface, applying the filter `'pfcp||icmp||gtp'`.

In order to run the tests, first do this:

```bash
cd ~/free5gc
make upf
chmod +x ./test.sh
```

The tests are all run from within `~/free5gc`.

a. TestRegistration

```bash
./test.sh TestRegistration
```

b. TestGUTIRegistration

```bash
./test.sh TestGUTIRegistration
```

c. TestServiceRequest

```bash
./test.sh TestServiceRequest
```

d. TestXnHandover

```bash
./test.sh TestXnHandover
```

e. TestDeregistration

```bash
./test.sh TestDeregistration
```

f. TestPDUSessionReleaseRequest

```bash
./test.sh TestPDUSessionReleaseRequest
```

g. TestPaging

```bash
./test.sh TestPaging
```

h. TestN2Handover

```bash
./test.sh TestN2Handover
```

i. TestNon3GPP

```bash
./test.sh TestNon3GPP
```

j. TestReSynchronization

```bash
./test.sh TestReSynchronization
```

k. TestULCL

```bash
./test_ulcl.sh TestRequestTwoPDUSessions
```

