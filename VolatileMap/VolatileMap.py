import shelve

class VolatileMap(object):
  def __init__(self, readFrom, getValue=None, volatiled=None, writeBack=False, overwrite=True):
    # properties that begin from "__" are private
    self.__overwrite = overwrite
    self.__writeBack = writeBack
    self.__map = shelve.open(readFrom, writeback=self.__writeBack)
    if volatiled:
      self.__volatiled = volatiled
    else:
      # No volatiled function means data never volatile
      self.__volatiled = lambda testee: False

    if getValue:
      self.__getValue = getValue
    else:
      self.__getValue = lambda data: data

    if not writeBack:
      self.__map = dict(self.__map)

  # by @property and the class inherits object, "overwrite" is immutable
  @property
  def overwrite(self):
      return self.__overwrite

  @property
  def writeBack(self):
      return self.__writeBack

  def __getitem__(self, key):
    if key not in self.__map or self.__volatiled(self.__map[key]):
      return None
    else:
      return self.__getValue(self.__map[key])

  def __setitem__(self, key, value):
    if self.__overwrite or key not in self.__map or self.__volatiled(self.__map[key]):
      self.__map[key] = value
    return value

  def save(self):
    if self.__writeBack:
      self.__map.sync(self.__map)

  def __del__(self):
    if self.__writeBack:
      self.__map.close()
