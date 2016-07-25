import shelve

class VolatileMap(object):
  def __init__(self, readFrom, getValue=None, volatiled=None, writeBack=False, overwrite=True):
    # properties that begin from "__" are private
    self.__overwrite = overwrite
    self.__writeBack = writeBack
    self.__map = shelve.open(readFrom, writeback=self.__writeBack)

    self.__volatility = not not volatiled
    if volatiled:
      self.__volatiled = volatiled

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

  def __exists(self, key):
    # key in map and it's not volatiled.
    return key in self.__map and \
    (not self.__volatility or not self.__volatiled(self.__map[key]))

  def __getitem__(self, key):
    if self.__exists(key):
      return self.__getValue(self.__map[key])
    else:
      return None

  def __setitem__(self, key, value):
    # if overwrite or not overwrite and not __exists(key)
    if self.__overwrite or not self.__exists(key):
      self.__map[key] = value
    return value

  def save(self):
    if self.__writeBack:
      self.__clean()
      self.__map.sync()

  def __del__(self):
    if self.__writeBack:
      self.__clean()
      self.__map.close()

  def __clean(self):
    if self.__volatility:
      for key in self.__map.keys():
        if not self.__exists(key):
          del self.__map[key]
