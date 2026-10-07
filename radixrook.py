#!/usr/bin/env python3
"""Radixrook: exact integer base conversion and fixed-width two's-complement views."""
import argparse,json,sys
from pathlib import Path
DIGITS='0123456789abcdefghijklmnopqrstuvwxyz'

def parse(value,base):
    if type(base) is not int or not 2<=base<=36:raise ValueError('Base must be 2-36.')
    if not isinstance(value,str):raise ValueError('Use text digits.')
    value=value.strip().lower()
    if not value or len(value)>256:raise ValueError('Use 1-256 characters including optional leading sign.')
    sign=-1 if value.startswith('-') else 1
    if value[0] in '+-':value=value[1:]
    if not value or any(c not in DIGITS[:base] for c in value):raise ValueError('Invalid digit for explicit base. No prefixes, spaces or underscores.')
    return sign*int(value,base)

def encode(number,base):
    if type(number) is not int or type(base) is not int or not 2<=base<=36:raise ValueError('Need an integer and base 2-36.')
    if number==0:return '0'
    sign='-' if number<0 else '';number=abs(number);out=[]
    while number:number,digit=divmod(number,base);out.append(DIGITS[digit])
    return sign+''.join(reversed(out))

def convert(value,base,width=None):
    n=parse(value,base);r={'format':'radixrook-1','source_base':base,'decimal':str(n),'binary':encode(n,2),'octal':encode(n,8),'hex':encode(n,16),'base36':encode(n,36)}
    if width is not None:
        if type(width) is not int or not 1<=width<=128:raise ValueError('Width must be 1-128 bits.')
        low=-(1<<(width-1));high=(1<<(width-1))-1
        if not low<=n<=high:raise ValueError('Number does not fit the requested signed width.')
        unsigned=n%(1<<width);r['signed_width_bits']=width;r['twos_complement_binary']=format(unsigned,f'0{width}b');r['twos_complement_unsigned_decimal']=str(unsigned);r['twos_complement_hex']=format(unsigned,f'0{(width+3)//4}x')
    return r

def decode_bits(bits):
    if not isinstance(bits,str) or not 1<=len(bits)<=128 or any(c not in '01' for c in bits):raise ValueError('Use 1-128 bits, no prefix/whitespace.')
    unsigned=int(bits,2);signed=unsigned-(1<<len(bits)) if bits[0]=='1' else unsigned
    return {'format':'radixrook-bits-1','width':len(bits),'bits':bits,'unsigned_decimal':str(unsigned),'signed_twos_complement_decimal':str(signed)}

def show(r):
    print('\nRADIXROOK | exact integer representations')
    for key,value in r.items():
        if key!='format':print(key+':',value)
    print('No unit conversions, byte order, device commands or overflow wrapping.')

def save(r,path):
    with open(Path(path).expanduser(),'x',encoding='utf-8') as f:json.dump(r,f,indent=2);f.write('\n')

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--value');p.add_argument('--base',type=int,default=10);p.add_argument('--width',type=int);p.add_argument('--bits');p.add_argument('--output');a=p.parse_args(argv)
    try:
        if a.value is not None or a.bits is not None:
            if a.value is not None and a.bits is not None:raise ValueError('Choose --value or --bits, not both.')
            r=decode_bits(a.bits) if a.bits is not None else convert(a.value,a.base,a.width);show(r)
            if a.output:save(r,a.output)
            return 0
        while True:
            print('\nRADIXROOK\n1 Integer bases  2 Decode bit string  0 Exit');c=input('> ').strip()
            if c=='0':return 0
            try:
                if c=='1':value=input('Digits (no prefixes): ');base=int(input('Source base [10]: ').strip() or '10');width=input('Optional signed width 1-128 [blank skips]: ').strip();r=convert(value,base,int(width) if width else None)
                elif c=='2':r=decode_bits(input('Exact bits, leading zeroes set width: ').strip())
                else:continue
                show(r);out=input('New JSON filename (blank skips): ').strip()
                if out:save(r,out)
            except (ValueError,OSError) as exc:print('Error:',exc)
    except (EOFError,KeyboardInterrupt):print('\nBye.')
    except (ValueError,OSError) as exc:print('Error:',exc,file=sys.stderr);return 2
    return 0
if __name__=='__main__':raise SystemExit(main())
