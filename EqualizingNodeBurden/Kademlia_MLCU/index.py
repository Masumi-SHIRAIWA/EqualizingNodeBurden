class index(dict): #データの保存 <Key, value>
  def __init__(self):
    pass
  
  def get_value(self, key):
    return super(index, self).__getitem__(key)
  __getitem__ = None


  def set_value(self, key, value):
    return super(index, self).__setitem__(key, value)
    # if self.cap == len(self):
    #   raise OverflowError
    # else:
    #   return super(index, self).__setitem__(key, value)
  __setitem__ = None

  def delete_value(self, key):
    return super(index, self).__delitem__(key)
  __delitem__ = None


  iteritems = None #親クラス関数の無効化
  items = None


