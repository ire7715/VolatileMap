from VolatileMap import VolatileMap
import time
import unittest

class TestRegularVolatileMap(unittest.TestCase):
  def setUp(self):
    self.regular = VolatileMap("test.shelve", \
    getValue=lambda data: data[1], \
    volatiled=lambda tup: time.time() - float(tup[0]) > 2)
    # default writeBack=False, overwrite=True

  @unittest.expectedFailure
  def testSetOverwrite(self):
    self.regular.overwrite = False

  def testValues(self):
    key = "k"
    values = [(time.time(), "v"), (time.time(), "w")]
    self.assertEqual(self.regular[key], None, \
      "Initial self.regular[%s] should be None" % key)

    self.regular[key] = values[0]
    self.assertEqual(self.regular[key], values[0][1], \
      "After assignment self.regular[%s] should be %s" % (key, values[0][1]))

    self.regular[key] = values[1]
    self.assertEqual(self.regular[key], values[1][1], \
      "After overwrite self.regular[%s] should be %s" % (key, values[1][1]))

    time.sleep(3)

    self.assertEqual(self.regular[key], None, \
      "After sleep self.regular[%s] should be None" % key)

    del self.regular

if __name__ == "__main__":
  unittest.main()
