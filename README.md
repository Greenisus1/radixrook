# Radixrook

Exact integer base conversion for bases 2-36, plus optional fixed-width two's-complement views and signed bit-string decoding. Arithmetic only: no device commands, unit conversions, byte-order assumptions or overflow wrapping.

Python 3.9+, standard library only. No network or packages.

## Run locally

Published in a private GitHub repository. Download its ZIP while signed into the owner account, extract it and open a terminal inside the source folder. Not verified as store-installed.

```text
python3 radixrook.py
python3 radixrook.py --value ff --base 16
python3 radixrook.py --value=-1 --width 8
python3 radixrook.py --bits 11111111
python3 radixrook.py --value 255 --output number.json
python3 -m unittest -v
bash app-store.sh install
bash app-store.sh run
```

Source base is explicit, default decimal. Digits 0-9/a-z, case-insensitive. Optional leading plus/minus; no automatic 0x/0b prefixes, underscores, fractions or internal spaces. Input cap 256 characters. Ordinary binary/octal/hex/base36 displays use a minus sign for negatives, not two's complement.

Optional width is **signed** 1-128 bits. Values outside the signed range are rejected, not truncated. A negative value is encoded modulo 2^width after the range check. Fixed-width binary includes leading zeroes. Hex uses enough digits to cover the width; for widths not divisible by four the top hex nibble includes padding zero bits, not extra signed-width bits. Example: -1 in 5 bits is binary 11111, hex 1f, not ff.

Bit-string decoding uses exact length as width, so `1` means signed -1 in one bit while `01` means signed +1 in two bits. It also reports the unsigned interpretation. No byte ordering, byte arrays, instruction decoding, checksums or hardware interpretation. A representation is not a command or safe range for a device.

CLI accepts either --value or --bits, never both. --width is used only for --value; --base is used only for --value. JSON uses decimal strings for exact large values, not lossy floating numbers. Reports refuse overwrite. No persistent history. CLI errors exit 2, successful calculations exit 0.

Root marker/version files are prepared locally only; no publication/store discovery asserted.

17 tests cover roundtrips in all 35 bases, sign/zero, invalid prefixes/digits, two's-complement limits/overflow, one-bit cases, bit width preservation, export refusal and CLI. Linux tested, physical Pi/non-Linux platforms untested.
