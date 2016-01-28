from VolatileMap.VolatileMap import VolatileMap
import time

def main():
  regularMap = VolatileMap("test.shelve", \
    getValue=lambda data: data[1], \
    volatiled=lambda tup: time.time() - float(tup[0]) > 2)
  print("rM.overwrite: " + str(regularMap.overwrite))
  try:
    regularMap.overwrite = True
    print("rM.overwrite after set: " + str(regularMap.overwrite))
  except AttributeError:
    print("rM.overwrite can't be set")

  print("rM[\"k\"] before assignment: " + str(regularMap["k"]))
  regularMap["k"] = (time.time(), "v")
  print("rM[\"k\"]: " + str(regularMap["k"]))
  regularMap["k"] = (time.time(), "w")
  print("rM[\"k\"] true assignment: " + str(regularMap["k"]))
  print("wait few seconds...")
  time.sleep(3)
  print("rM[\"k\"] after sleep: " + str(regularMap["k"]))

  regularMap = None

  return

if __name__ == "__main__":
  main()
