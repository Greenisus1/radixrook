import subprocess,sys,tempfile,unittest
from pathlib import Path
import radixrook as r
class RadixTests(unittest.TestCase):
    def test_hex(self):self.assertEqual(r.convert('ff',16)['decimal'],'255')
    def test_negative(self):self.assertEqual(r.convert('-15',10)['hex'],'-f')
    def test_zero(self):self.assertEqual(r.encode(0,36),'0')
    def test_all_bases_roundtrip(self):
        for base in range(2,37):
            for n in (-1000,-1,0,1,12345678901234567890):self.assertEqual(r.parse(r.encode(n,base),base),n)
    def test_no_prefix(self):
        with self.assertRaises(ValueError):r.parse('0xff',16)
    def test_invalid_digits(self):
        for value in ('','-','2','1_0','1 0'):
            with self.assertRaises(ValueError):r.parse(value,2)
    def test_base_bounds(self):
        for base in (1,37,True):
            with self.assertRaises(ValueError):r.parse('1',base)
    def test_negative_twos(self):out=r.convert('-1',10,8);self.assertEqual(out['twos_complement_binary'],'11111111');self.assertEqual(out['twos_complement_hex'],'ff')
    def test_signed_limits(self):self.assertEqual(r.convert('-128',10,8)['twos_complement_hex'],'80');self.assertEqual(r.convert('127',10,8)['twos_complement_hex'],'7f')
    def test_overflow_refused(self):
        for value in ('128','-129'):
            with self.assertRaises(ValueError):r.convert(value,10,8)
    def test_width_one(self):self.assertEqual(r.convert('-1',10,1)['twos_complement_binary'],'1')
    def test_decode(self):self.assertEqual(r.decode_bits('11111111')['signed_twos_complement_decimal'],'-1');self.assertEqual(r.decode_bits('01111111')['signed_twos_complement_decimal'],'127')
    def test_leading_zero_width(self):self.assertEqual(r.decode_bits('001')['width'],3);self.assertEqual(r.decode_bits('1')['signed_twos_complement_decimal'],'-1')
    def test_decode_invalid(self):
        for bits in ('','2','0b1','1'*129):
            with self.assertRaises(ValueError):r.decode_bits(bits)
    def test_no_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'safe';p.write_text('safe')
            with self.assertRaises(FileExistsError):r.save({},p)
    def test_cli(self):out=subprocess.run([sys.executable,'radixrook.py','--value=-1','--width','8'],capture_output=True,text=True);self.assertEqual(out.returncode,0);self.assertIn('11111111',out.stdout)
    def test_conflicting_cli(self):out=subprocess.run([sys.executable,'radixrook.py','--value','1','--bits','1'],capture_output=True,text=True);self.assertEqual(out.returncode,2)
if __name__=='__main__':unittest.main()
