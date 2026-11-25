import unittest
from forecast import classify,run
class Tests(unittest.TestCase):
 def test_routes(self):
  for y,k in [([0]*10,'unknown'),([10]*10,'smooth'),([1,100]*5,'erratic'),([0,0,10]*5,'intermittent'),([0,0,1,0,0,100]*5,'lumpy')]: self.assertEqual(classify(y)[0],k)
 def test_run(self):
  r=run(); self.assertEqual(len(r['rows']),1800); self.assertTrue(all(len(x['forecast'])==14 for x in r['forecasts']))
