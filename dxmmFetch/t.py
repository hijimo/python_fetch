global wxindex
wxindex = 0


def a():
  global wxindex
  wxindex +=1

  print(wxindex)


a()