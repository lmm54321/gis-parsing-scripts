import re

'''Extract fields from a malformed geodb schema to create a list of C# properties'''
def get_names(fname):
    file = open(fname)
    names = []
    lines = file.readlines()

    fieldslineindex = 0
    for i in range(0, len(lines)):
      if "<Fields" in lines[i]:
        fieldslineindex = i
        break
    lines = lines[fieldslineindex:]
    
    for i in range(0,len(lines)):
      line = lines[i]
      if "<Name>" in line:
        m = re.search(r'<Name>(.*)</Name>', lines[i])
        if m:
          type = re.search(r'<Type>(.*)</Type>', lines[i+1])
          if type is not None:
			alias = re.search(r'<AliasName>(.*)</AliasName>', lines[i+6])
			if alias is not None:
			  names.append((m.group(1), type.group(1), alias.group(1)))
        else:
          print("no name found")
    file.close()
    return names

typesdict = {
  'esriFieldTypeString': 'string',
  'esriFieldTypeDouble': 'double?',
  'esriFieldTypeInteger': 'int?',
  'esriFieldTypeOID': 'int',
  'esriFieldTypeGeometry': 'Shape'
  }
    
def get_prop_array(names):
  proparray = []
  for name in names:
    currentprop = "\n/// <summary>\n/// "+name[2]+"\n/// </summary>"
    currentprop += "\npublic "+typesdict[name[1]]+" "+name[0]+" { get; set; }"
    proparray.append(currentprop)
  return proparray

def print_props(proparray):
  for prop in proparray:
    print(prop)
	
def write_out(pa, fname):
  myfile = open(fname,'w')
  for item in pa:
    myfile.write('%s\n' % item)
  myfile.close()

def do_all(fin, fout):
  tuplelist = get_names(fin)
  proparray = get_prop_array(tuplelist)
  write_out(proparray, fout)
  
def translate(names):
  fields = []
  for name in names:
    fields.append("private const string DB_FIELD_"+name[0].upper()+"       = \""+name[0].upper()+"\";")
  setters = []
  for name in names:
    setters.append("SetFieldValue(row, DB_FIELD_"+name[0].upper()+", dataObject."+name[0].capitalize()+");")
  return (fields, setters)