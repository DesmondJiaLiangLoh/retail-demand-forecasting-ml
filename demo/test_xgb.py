import unittest, tempfile
from pathlib import Path
from xgb_forecast import run,features
from xgboost import XGBRegressor
class XGBTests(unittest.TestCase):
 def test_features(self):
  self.assertEqual(features(list(range(40)),30,0),features(list(range(30))+[999]*10,30,0))
 def test_execution(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d); r=run(p); self.assertEqual(len(r['rows']),1800); self.assertEqual(len(r['forecasts']),30); self.assertTrue(all(x['prediction']>=0 for x in r['rows'])); model=XGBRegressor(); model.load_model(p/'smooth.json')
