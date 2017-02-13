import xlrd
import codecs

'''Extract entries from an Excel entity catalog to create a list of C# properties'''
typesdict = {
  'StructuredText': 'string',
  'String': 'string',
  'Real': 'double?',
  'Integer': 'int?',
  'integer': 'int?',
  'Enumeration': 'enum_here',
  'CONSTRAINED_STRING': 'string',
  'CodeList': 'codelist',
  'CODELIST_ZI020_GE4':'codelist'
  }

def do_all (fname):
  UTF8Writer = codecs.getwriter('utf8')
  
  book = xlrd.open_workbook(fname)
  firstsheet = book.sheet_by_index(0)
  names = get_names(firstsheet)
  alias = get_alias(firstsheet)
  types = get_type(firstsheet)
  charlimit = get_char_limit(firstsheet)
  measure = get_measure(firstsheet)
  comments = get_comments(firstsheet)
  fulllist = zip(names, alias, types, charlimit, measure, comments)
  printablelist = []
  for item in fulllist:
    printablelist.append(printable_item(item))
  return printablelist
  
def get_names(sheet):
  names = sheet.col_slice(start_rowx=0, end_rowx=1024, colx=0)
  return [item.value.encode('ascii','ignore') for item in names]
  
def get_alias(sheet):
  alias = sheet.col_slice(start_rowx=0, end_rowx=1024, colx=1)
  return [item.value.encode('ascii','ignore') for item in alias]
  
def get_type(sheet):
  array = sheet.col_slice(start_rowx=0, end_rowx=1024, colx=2)
  return [item.value.encode('ascii','ignore') for item in array]

def get_char_limit(sheet):
  array = sheet.col_slice(start_rowx=0, end_rowx=1024, colx=3)
  return [item.value.encode('ascii','ignore') for item in array]
  
def get_measure(sheet):
  array = sheet.col_slice(start_rowx=0, end_rowx=1024, colx=4)
  return [item.value.encode('ascii','ignore') for item in array]

def get_comments(sheet):
  array = sheet.col_slice(start_rowx=0, end_rowx=1024, colx=5)
  return [item.value.encode('ascii','ignore') for item in array]

def printable_item(item):
  retval = ''
  retval += '\n/// <summary>'
  retval += '\n/// '+item[1]
  retval += '\n///'
  retval += '\n/// '+'\n/// ['.join(item[5].split('['))
  retval += '\n/// [Measure] '+item[4]
  retval += '\n/// </summary>'
  if (item[3] is not '') and ('unlimited' not in item[3]):
    retval += '\n[StringLength(%s)]' % item[3]
  retval += '\npublic '+typesdict[item[2]]+' '+item[0]+' { get; set; }\n'
  retval = retval.encode('ascii','ignore')
  return retval  
