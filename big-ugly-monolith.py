#!/usr/bin/python
# -*- coding: UTF-8 -*-

###############################
# version: 1.14               #
# author: Heyder Pestana Dias #
# create: 12/11/2015 02:30    #
# update: 27/11/2015 16:31    #
###############################

########
# IMPORT
#!/usr/bin/python
import os, sys, hashlib, pickle, re, itertools, webbrowser, copy, codecs
from cgi import escape
from colorama import init, Back, Fore
init()
from msvcrt import getch
from datetime import datetime
# IMPORT
########

#########
# globals

### global var
hourglass_pass = {'limit':0, 'status':0, 'point':0}
path_version = ''
path = './'
path_log = path+path_version
path_file = path+'antes/'
path_file_change = path+'depois/'
do_all_process_alone = False
mark_all_files_to_execute = False
mark_for_this_files = False
select_mode = ''
# link to referenc: https://msdn.microsoft.com/en-us/library/3ca8tfek(v=vs.84).aspx
rsets_names_DEF = {'accepted': [], 'unaccepted': ['Abs','Array','Asc','Atn','CBool','CByte','CCur','CDate','CDbl','Chr','CInt','CLng','Conversions','Cos','CreateObject','CSng','CStr','Date','DateAdd','DateDiff','DatePart','DateSerial','DateValue','Day','Escape','Eval','Exp','Filter','FormatCurrency','FormatDateTime','FormatNumber','FormatPercent','GetLocale','GetObject','GetRef','Hex','Hour','InputBox','InStr','InStrRev','Int','Fix','IsArray','IsDate','IsEmpty','IsNull','IsNumeric','IsObject','Join','LBound','LCase','Left','Len','LoadPicture','Log','LTrim','RTrim','Trim','Maths','Mid','Minute','Month','MonthName','MsgBox','Now','Oct','Replace','RGB','Right','Rnd','Round','ScriptEngine','ScriptEngineBuildVersion','ScriptEngineMajorVersion','ScriptEngineMinorVersion','Second','SetLocale','Sgn','Sin','Space','Split','Sqr','StrComp','String','StrReverse','Tan','Time','Timer','TimeSerial','TimeValue','TypeName','UBound','UCase','Unescape','VarType','Weekday','WeekdayName','Year']}
rsets_names = copy.copy(rsets_names_DEF)
result_list = {}
process_directory = {}
erro_list = {}
### global var

### match paterns
# patern_data_files_div TOTAL 19
patern_have_JSCript = '(<%[ \t]*@[ \t]*Language[ \t]*=[ \t]*JSCript[ \t]*%>)'
patern_find_all_functions = '^[ \t]*(?:sub|Function)[ \t]+([\w]+)[ \t\(\n]'
patern_find_all_includes = '<!--[ \t\n]*\'?[ \t]*#[ \t]*include[ \t]*(virtual|file)[ \t]*=[ \t]*"([\w\/]*?\/)?([\w\.]+)"[ \t\n]*-->'
patern_have_layout_link_ARR =   ['(set[ \t]+','.seguranca[ \t]*=[ \t]*oseg)']
patern_findtoMAKE_layout_link = '(?:Dim[ \t]+[\w]+[ \t]*:)?[ \t]*Set[ \t]+([\w]+)[ \t]*=[ \t]*New[ \t]+Layout\n'
patern_have_obj_include =     '(dim[ \t]+oseg[ \t]*\:[ \t]*set[ \t]+oseg[ \t]*\=[ \t]*new[ \t]+seguranca)'
patern_findtoMAKE_obj_include = '(?:<!--[ \t]*\'?[ \t]*#INCLUDE[ \t]+VIRTUAL[ \t]*=[ \t]*\"[ /"\w\.]+\"[ \t]*-->\n)+(\n)'
patern_findtoMAKE_obj_include_unique = '<%[ \t\n]*?@[ \t]*?Language[ \t]*?=[ \t]*?VBScript[ \t\n]*?%>[ \t]*(?:\n?[ \t\n]*<%[ \t\n]*?Option[ \t]*?Explicit[ \t\n]*?%>[ \t\n]*)?(\n)'
patern_findtoMAKE_obj_include_force = '[ \t\n]*<%[ \t\n]*?Option[ \t]*?Explicit[ \t\n]*?%>[ \t\n]*(\n)'
patern_line_break = '^([^\n]*\n?)'
patern_asp_tag = '<%([\w\W]+?)%>'
patern_if_then_condition = '[ \t]+If([\w\W\n]+?)then([\w\W\n]+?)End[ \t]+If'
patern_data_files_div_especific = '(?:<%s>\n)([<>\/ :\w\n]*)(?:\n<\/%s>)'
patern_data_files_div = "^(?:<<([\w_]+)>>)\n?([\w\W]*?)\n<\/\1\/>"
patern_other_objects = '(?!Set[ |\t]+)(\w+?)(?:[ |\t]*=[ |\t]*\w+\.(?!CreateObject[ |\t]*\(\"ADODB\.Recordset"\)))'
patern_is_in_seguranca = 'oSeg\.(?:RemoveHtml|HTMLEncode|URLEncode|StripNodes|RequestEnc|RequestForm|RequestQueryString)[ \t]*\([ \t]*([\w]+?\(\"[\w]+?\"\)(?:\.value)?|"[ \t\w]*"|)[ \t]*\)' # grupo 1 é o recordset ou conteudo da entrada da funcao
patern_for_each = '(For[ \t]+Each[ \t]+[\w\W]+?[ \t]+in[ \t]+[\w\W]+?\n)'
MODE = {'find_recordset': {}, 'modify_recordset': {}, 'modify_request': {}}
# patern_find_dim_recordset
MODE['find_recordset']['dim'] = '(?!Set[ |\t]+)(\w+?)([ |\t]*=[ |\t]*\w+\.CreateObject[ |\t]*\(\"ADODB\.Recordset"\))'
MODE['find_recordset']['call'] = '(?=(?<=[,+*/%&=( \-\t\n])|(?<=^))(\w+)([ \t]*\(\"\w+\"\)(\.\w+)?)(?=(?=[,+*/%&) \-\t\n])|(?=$))'
# patern_find_call_recordset
patern_find_call_recordset = ['(?=(?<=[,+*/%&=( \-\t\n])|(?<=^))(',')([ \t]*\(\"\w+\"\)(\.\w+)?)(?=(?=[,+*/%&) \-\t\n])|(?=$))']
MODE['modify_recordset']['call'] = None
# patern_recordset_name_extrator
# patern_find_call_request
MODE['modify_request']['enc'] = '(?=(?<=[,+*/%&=( \-\t\n])|(?<=^))(request[ \t]*)(\(\"?\w+\"?\)(\.\w+)?)(?=(?=[,+*/%&) \-\t\n])|(?=$))'
# patern_find_call_request_query
MODE['modify_request']['query'] = '(?=(?<=[,+*/%&=( \-\t\n])|(?<=^))(request\.QueryString[ \t]*)(\((\"?\w+\"?)?\)(\.\w+)?)?(?=(?=[,+*/%&) \-\t\n])|(?=$))'
# patern_find_call_request_form
MODE['modify_request']['form'] = '(?=(?<=[,+*/%&=( \-\t\n])|(?<=^))(request\.Form[ \t]*)(\(\"?\w+\"?\)(\.\w+)?)(?=(?=[,+*/%&) \-\t\n])|(?=$))'
### match paterns

### colorama colors vars
_N = Back.BLACK  + Fore.WHITE
_W = Back.WHITE  + Fore.BLACK
_R = Back.RED    + Fore.WHITE
_G = Back.GREEN  + Fore.WHITE
_B = Back.BLUE   + Fore.WHITE
_T = Back.WHITE  + Fore.RED
_A = _R #Back.RED  + Fore.BLACK
### colorama colors vars

# globals
#########

#####
#MAIN
def MAIN ():
  opt_load_data()
  while True:
    opt_menu_main()
  sys.exit(0)
#MAIN
#####

#########
#FUNCTION
def opt_menu_main ():
  global rsets_names, result_list, erro_list
  opt_info = '''
  Versao 1.14

    [RecordSet]
            Nomes: *
        Recusados: *

    [Arquivos]
            Total: %s
      Processados: %s
        Incluidos: %s

    [Info]
       Alteracoes: %s
              Erro: %s
  ''' % (count_files_total(), count_files_process(), count_files_include(), count_result(), count_erro())
  #''' % (count_rsets_names(), count_rsets_names_unaccepted(), count_files_total(), count_files_process(), count_files_include(), count_result(), count_erro())

  opt_main = opt_info+'''
  [0]=Resetar
  [1]=Carregar
  [2]=Salvar
  [3]=Escolher diretorios
  [4]=Executar correcoes
  [5]=Criar log de alteracoes
  [6]=Sair
  '''

  execute = consoleShow( opt_main, 'Generic')
  if   execute == 0:
    opt_reset_program()
  elif execute == 1:
    opt_load_data()
  elif execute == 2:
    opt_save_data()
  elif execute == 3:
    opt_chose_directories()
  elif execute == 4:
    if process_directory == {}:
      print 'Escolha os diretorios para o processo'
      raw_input('\nContinue...')
      opt_chose_directories()
    else:
      execute = consoleShow(_A+'Executar processo completo?'+_N, 'YesOrNo')
      if execute:
        opt_do_all_process()
  elif execute == 5:
    writeLogFile()
  elif execute == 6:
    sys.exit(0)
  elif execute == 7:
    installObjInFiles()
  elif execute == 8:
    make_full_correction()
  elif execute == 9:
    drop_all_corrections()
    process_patern_list('modify_request')
  elif execute == 10:
    drop_all_corrections()
  elif execute == 11:
    correction_multiple_include()
  elif execute == 12:
    printErroList()
  elif execute == 13:
    print_rsets_names()

def count_rsets_names ():
  global rsets_names
  count = 0
  for k, Names in rsets_names.iteritems():
    for RS in Names:
      count += 1
  return count

def count_rsets_names_accepted ():
  global rsets_names
  count = 0
  for RS in rsets_names['accepted']:
    count += 1
  return count

def count_rsets_names_unaccepted ():
  global rsets_names
  count = 0
  for RS in rsets_names['unaccepted']:
    count += 1
  return count

def count_files_total ():
  global result_list
  count = 0
  for id, File in result_list.iteritems():
    count += 1
  return count

def count_files_process ():
  global result_list
  count = 0
  for id, File in result_list.iteritems():
    if File['process']:
      count += 1
  return count

def count_files_include ():
  global result_list
  count = 0
  for id, File in result_list.iteritems():
    if not File['process']:
      count += 1
  return count

def count_result ():
  global result_list
  count = 0
  for Id, File in result_list.iteritems():
    if File['maths']['include']:
      count += 1
    '''if 'maths' in File.keys() and 'data' in File['maths'].keys():
      for k, math in File['maths']['data'].iteritems():
        if math['work_type'] not in ['find_recordset_dim', 'find_recordset_call']:
          count += 1'''
  return count

def count_erro ():
  global erro_list
  count = 0
  for id, file in erro_list.iteritems():
    count += 1
  return count

def create_recordset_patern ():
  global rsets_names
  MODE['modify_recordset']['call'] = ''
  if rsets_names['accepted'] != {}:
    Names = '|'.join(rsets_names['accepted'])
    if len(Names) > 0:
      MODE['modify_recordset']['call'] = patern_find_call_recordset[0] +Names+ patern_find_call_recordset[1]
  return MODE['modify_recordset']['call']

def process_patern_list (select_mode):
  global MODE
  list_patern = MODE[select_mode]
  for mode, patern in list_patern.iteritems():
    find_maths_in_file_list(patern, select_mode, mode)

def opt_chose_directories ():
  global process_directory, path_file
  text = '''
  Escolha os dirtorios que serão tratados:

%s

  Comandos: Esc ^ v Enter'''
  if process_directory == {}:
    process_directory = {'accepted': [], 'unaccepted': []}
    temP_file_list = os.listdir( path_file+'/web' )
    for file in temP_file_list:
      if len(file.split('.')) == 1:
        process_directory['unaccepted'] += ['web/'+file]
  # convert TO nav
  tmp_process_directory = []
  for path in process_directory['accepted']:
    tmp_process_directory += [{'path': path+'/', 'sel': True}]
  for path in process_directory['unaccepted']:
    tmp_process_directory += [{'path': path+'/', 'sel': False}]
  # convert TO nav
  tmp_process_directory = consoleNav(tmp_process_directory, text)
  # convert FROM nav
  process_directory = {'accepted': [], 'unaccepted': []}
  for Item in tmp_process_directory:
    if Item['sel']:
      process_directory['accepted'] += [ Item['path'].lower() ]
    else:
      process_directory['unaccepted'] += [ Item['path'].lower() ]
  # convert FROM nav
  load_list_files()

def opt_reset_program ():
  result_list = {}
  dictionaryRESET()
  load_list_files()

def opt_do_all_process ():
  global do_all_process_alone, process_directory
  #raw_input(process_directory) # *!*
  #raw_input(result_list)
  do_all_process_alone = True
  process_patern_list('find_recordset')
  create_recordset_patern()
  drop_all_corrections()
  process_patern_list('modify_recordset')
  process_patern_list('modify_request')
  installObjInFiles()
  save_data_files()
  #correction_multiple_include()
  save_data_files()
  make_full_correction()
  #raw_input(result_list)
  do_all_process_alone = False

def opt_print_log ():
  execute = consoleShow(_T+'Exportar o log.Html?'+_N, 'YesOrNo')
  if execute:
    writeLogFile()
    #raw_input('Sair...')
    #sys.exit(0)

def opt_abandon_result_list ():
  execute = consoleShow(_A+'Abandonar as alteracoes anteriores (da memoria)?'+_N, 'YesOrNo')
  if execute:
    result_list = {}

def opt_load_data ():
  execute = consoleShow(_T+'Carregar o estado anteriormente salvo?'+_N, 'YesOrNo')
  if execute:
    load_data_files()

def opt_save_data ():
  execute = consoleShow(_T+'Salvar o estado de busca atual?'+_N, 'YesOrNo')
  if execute:
    save_data_files()

def load_data_files ():
  global path_log, rsets_names, result_list, erro_list, process_directory, patern_data_files_div
  hourglass_START(-1)
  print 'Carregando Data...'
  filePath = path_log +'/save.data'
  if not os.path.isfile(filePath):
    print _A+'nao foi encontrado o save anterior'+_N
    raw_input('Continue...')
    return
  file = open(filePath, 'r')
  tmp_data = pickle.load(file)
  file.close()
  if 'rsets_names' in tmp_data.keys():
    rsets_names = tmp_data['rsets_names']
  if 'erro_list' in tmp_data.keys():
    erro_list = tmp_data['erro_list']
  else:
    erro_list = {}
  if 'process_directory' in tmp_data.keys():
    process_directory = tmp_data['process_directory']
  else:
    process_directory = {}
  if 'result_list' in tmp_data.keys():
    result_list = tmp_data['result_list']
  else:
    result_list = {}

def printDictionary (dictionary):
  for Id, Item in dictionary.iteritems():
    print _T+'id:'+_N+Id+_T+'\nvalue:{\n'+_N
    if type(Item) == dict:
      print printDictionary(Item)
    else:
      print Item
    print _T+'}'+_N

def printErroList ():
  global erro_list, path_file
  for Err in [0, 1]:
    print '\n------'
    for Id, Erro in erro_list.iteritems():
      if 'code' in Erro.keys() and Erro['code'] == Err:
        print '\n\t###'
        print 'ID:', Id
        print 'MSG:', Erro['msg']
        print 'NAME:', Erro['data']['name']
        print 'PATH:', Erro['data']['path']
        if Erro['from'] != None:
          print 'FROM'
          ID = Erro['from']
          print 'NAME:', result_list[ID]['name']
          print 'PATH:', result_list[ID]['path']
        print '\t###\n'
  raw_input('LISTA DE ERROS')

def print_rsets_names ():
  print rsets_names
  print _T+'Lista de nomes para RecordSet'
  print 'Aceitos:'+_N
  for RS in rsets_names['accepted']:
    print ' *  '+RS
  print '\n'+_T+'Recusados'+_N
  for RS in rsets_names['unaccepted']:
    print ' *  '+RS
  raw_input('\nContinue...')

def extractOneGroupStr (group, position):
  extract = ''
  for extract in list( group ):
    extract = extract.group(position)
    break
  return extract

def save_data_files ():
  global path_log, rsets_names, result_list, erro_list, process_directory
  hourglass_START(-1)
  filePath = path_log +'/save.data'
  file = open(filePath, 'w')
  tmp_process_directory = copy.deepcopy(process_directory)
  tmp_rsets_names = copy.deepcopy(rsets_names)
  tmp_result_list = copy.deepcopy(result_list)
  tmp_erro_list = copy.deepcopy(erro_list)
  tmp_data = {'rsets_names': tmp_rsets_names, 'result_list': tmp_result_list, 'erro_list': tmp_erro_list, 'process_directory': tmp_process_directory}
  pickle.dump(tmp_data, file)
  file.close()

def load_list_files ():
  global path_file
  if process_directory == {}:
    return
  hourglass_START(-1)
  temP_file_list = os.listdir( path_file );
  fileList = recursive_mount_file_list('', temP_file_list, True, [])
  process_file_list(fileList)

def recursive_mount_file_list (Directory, Nodes, isProcess, fileList):
  global path_file, process_directory
  if isProcess:
    if Directory.lower() in process_directory['unaccepted']:
      isProcess = False
  for node in Nodes:
    if os.path.isdir( path_file+Directory+node ):
      tmp_Nodes = os.listdir( path_file+Directory+node );
      recursive_mount_file_list(Directory+node+'/', tmp_Nodes, isProcess, fileList)
    else:
      N = node.split('.')
      L = len(N)
      if N[L-1].lower() == 'asp':
        fileList.append({'path': Directory, 'name': node, 'process': isProcess, 'store': isProcess})
  return fileList

def process_file_list (fileList):
  global path_file, result_list, patern_find_all_includes, patern_find_all_functions, include_file_list
  FindIncludes = regularGo(patern_find_all_includes, True)
  FindFunctions = regularGo(patern_find_all_functions, True)
  include_file_list = {}
  result_list = {}
  add_to_file_list(fileList, True, FindIncludes, FindFunctions)
  limit_erro = 10
  while len(include_file_list):
    limit_erro -= 1
    if limit_erro == 0:
      raise ValueError('Erro ao tentar carregar os arquivos do HD')
    fileList_noProcess = create_fileList_from_include_file_list()
    add_to_file_list(fileList_noProcess, False, FindIncludes, FindFunctions)

def create_fileList_from_include_file_list ():
  global include_file_list, result_list
  del_include = []
  for Id, File in include_file_list.iteritems():
    if Id in result_list.keys():
      del_include += [Id]
  for Id in del_include:
    del include_file_list[Id]
  fileList = []
  for Id, File in include_file_list.iteritems():
    # if not asp
    N = File['name'].split('.')
    if N[len(N)-1].lower() != 'asp':
      continue
    # if not asp
    if File['path'] != None:
      path = File['path']
    else:
      path = ''
    fileList.append({'path': path, 'name': File['name'], 'process': False, 'store': True, 'from':File['from']})
  include_file_list = {}
  return fileList

def add_to_file_list (fileList, isProcss, FindIncludes, FindFunctions):
  global result_list, include_file_list, path_file
  for File in fileList:
    hourglass()
    if not File['store']:
      continue
    # var def
    full_file_id = getMD5( File['path'] )+'_'+getMD5( File['name'] )
    # var def
    # check if is load file
    if full_file_id in result_list.keys():
      continue
    # check if is load file
    result_list[ full_file_id ] = { 'name':  File['name'],
                    'path': File['path'],
                    'includes': [],
                    'functions': [],
                    'maths': {'data': {}, 'include': None},
                    'recordsets': [],
                    'no_rs': [],
                    'process': File['process'],
                    'sha': None }
    # check if exist in diretory
    full_path = path_file+File['path']+File['name']
    if os.path.exists(full_path):
      full_file_data = open(full_path).read()
    else:
      # remove erro
      result_list[full_file_id]['process'] = False
      erro_item = result_list[full_file_id]
      erro_item['path'] = File['path']
      erro_list[full_file_id] = {'data':erro_item, 'from':None, 'msg': 'file not found', 'code': 0}
      if 'from' in File.keys():
        erro_list[full_file_id]['from'] = File['from']['id']
      # del itens
      #if 'from' in File.keys():
      father = File['from']['id']
      includes = []
      for I in result_list[father]['includes']:
        if I != full_file_id:
          includes += [I]
      result_list[father]['includes'] = includes
      #del result_list[full_file_id]
      # del itens
      continue
      # remove erro
    # check if exist in diretory
    IncludesMaths = FindIncludes.finditer(full_file_data)
    Includes = []
    for math in list(IncludesMaths):
      # if not asp
      N = ( math.group(3) ).split('.')
      if N[len(N)-1].lower() != 'asp':
        continue
      # if not asp
      # ref def
      if math.group(1).lower() == 'file':
        ref = True
      elif math.group(1).lower() == 'virtual':
        ref = False
      if math.group(2) != None:
        path = math.group(2)
      else:
        path = ''
      name = math.group(3)
      # ref def
      # ref path def
      inc_path = relativeLoadFile(path, name, {'id':full_file_id, 'mode':ref})
      # ref path def
      IncludeId = getMD5( inc_path )+'_'+getMD5( name )
      Includes += [IncludeId]
      include_file_list[IncludeId] = {'name':math.group(3), 'path':inc_path, 'from':{'id':full_file_id, 'mode':ref, 'inc_path':path}}
    FunctionsMaths = FindFunctions.finditer(full_file_data)
    Functions = []
    for math in list(FunctionsMaths):
      Functions += [math.group(1)]
    sha = getSHA1(full_path)
    result_list[full_file_id]['no_rs'] = find_other_object(full_file_data)
    result_list[full_file_id]['includes'] = Includes
    result_list[full_file_id]['functions'] = Functions
    result_list[full_file_id]['sha'] = sha

def relativeLoadFile (path, name, From): # INCOMPLETO ******************************************************************!!!
  #global path_file
  # if is virtual
  if not From['mode']:
    if path[0] == '/':
      return 'WEB'+path
    else:
      return 'WEB/'+path
  # if is virtual
  # if is root
  if path == '/' or (len(path) >= 1 and path[0] == '/'):
    return 'WEB'+path
  # if is root
  # def var
  arr = path.split('../')
  last = arr[len(arr)-1]
  back = len(arr)-1
  if   len(last) >= 1 and last[0] == '/':
    last = last[1:]
  elif len(last) >= 2 and last[0:2] == './':
    last = last[2:]
  ID = From['id']
  father = result_list[ID]['path']
  # def var
  # if no back
  if back == 0:
    return father+last
  # if no back
  # back path
  arr = father.split('/')
  father = []
  for folder in arr:
    if folder != '':
      father += [folder]
  folders = father[:-back]
  father = '/'.join(folders)+'/'
  # back path
  return father+last

def dictionaryRESET ():
  global rsets_names, rsets_names_DEF
  rsets_names = copy.copy(rsets_names_DEF)

def dictionaryFIND (FIND):
  global rsets_names
  find = FIND.lower()
  if find in rsets_names['accepted']:
    return True
  else:
    return False

def dictionarySTORE (Store, isAccepted):
  global rsets_names
  if len(Store) > 0:
    if isAccepted:
      typeItem = 'accepted'
    else:
      typeItem = 'unaccepted'
    if not dictionaryFIND(Store):
      rsets_names[typeItem] += [Store]

def dictionaryMOUNTdeny (Id):
  dictionaryRESET()
  rs_deny_list = recusrive_find_no_rs(Id, {})
  for no_rs, dummy in rs_deny_list.iteritems():
    dictionarySTORE(no_rs, False)

def dictionaryMOUNTpass (Id):
  recordsets = result_list[Id]['recordsets']
  dictionaryRESET()
  for no_rs in recordsets:
    dictionarySTORE(no_rs, True)

def recusrive_find_no_rs (Id, rs_deny_list):
  global result_list
  no_rs = result_list[Id]['no_rs']
  includes = result_list[Id]['includes']
  functions = result_list[Id]['functions']
  if len(no_rs):
    for Item in no_rs:
      rs_deny_list[Item] = 1
  if len(functions):
    for Item in functions:
      rs_deny_list[Item] = 1
  for Id in includes:
    rs_deny_list = recusrive_find_no_rs(Id, rs_deny_list)
  return rs_deny_list

def regularGo (patern, ismultline):
  if patern == None or len(patern) == 0:
    raise Exception('Fatal erro in regularGO, patern is empty.') 
  if ismultline:
    return re.compile(patern, re.IGNORECASE|re.MULTILINE )
  else:
    return re.compile(patern, re.IGNORECASE )

def regularFind (patern, ismultline, file_data):
  FP = regularGo(patern, ismultline)
  return FP.finditer(file_data)

def consoleNav (nav_list, text):
  tmp_text = ''
  tmp_console = ''
  pointer = 0
  maxP = len(nav_list) -1
  while True:
    tmp_nav_list = []
    for Item in nav_list:
      if Item['sel']:
        tmp_nav_list += [_G+Item['path']+_N]
      else:
        tmp_nav_list += [Item['path']]
    pt = 0
    for line in tmp_nav_list:
      if pt == pointer:
        tmp_nav_list[pt] = ' '+_A+'*'+_N+' '+tmp_nav_list[pointer]
      else:
        tmp_nav_list[pt] = '   '+line
      pt += 1
    tmp_console = text%('\n'.join(tmp_nav_list) )
    execute = consoleShow(tmp_console,'Navigate')
    if execute == 'ESC':
      break;
    elif execute == 'ENTER':
      nav_list[pointer]['sel'] = not nav_list[pointer]['sel']
    elif execute == '^':
      pointer -= 1
    elif execute == 'v':
      pointer += 1
    if pointer < 0:
      pointer = 0
    elif pointer > maxP:
      pointer = maxP
  return nav_list

def consoleShow (text, mode):
  global mark_all_files_to_execute, mark_for_this_files
  erroCode = False
  saveCmd = False
  whaitCode = True
  while whaitCode:
    os.system('cls')
    if erroCode:
      erroCode = False
      print _A+'\t\t\t\t!COMANDO INVALIDO!\t\t\t\t'+_N
    elif saveCmd:
      saveCmd = False
      print _G+'\t\t\t\t  !ESTADO SALVO!  \t\t\t\t'+_N
      if execute == '*':
        raw_input('Sair...')
        sys.exit(0)
    if isinstance(text, basestring):
      print text
    else:
      for line in text:
        print line
    if mode == None:
      raw_input('Continue...')
      return None
    elif mode == 'YesOrNo':
      print _T+'[s]=sim [n]=nao'+_N
      execute = raw_input('=>').lower()
      if execute == 'n':
        print 'selecionado: NAO'
        return False
      elif execute == 's':
        print 'selecionado: SIM'
        return True
      else:
        erroCode = True
    elif mode == 'Navigate':
      key = getch()
      keyCode = ord(key)
      if keyCode == 27:
        return 'ESC'
      elif keyCode == 13:
        return 'ENTER'
      elif keyCode == 224:
        keyCode = ord(getch())
        if keyCode == 72:
          return '^'
        elif keyCode == 77:
          return '>'
        elif keyCode == 80:
          return 'v'
        elif keyCode == 75:
          return '<'
      else:
        # key = key.lower()
        return ''
    elif mode == 'Select':
      print _T+'[S]=sim [N]=nao [T]=todos neste arquivo [L]=para todos arquivos\n[A]=salvar estado [E]=Guardar erro de busca [*]=Abortar e voltar ao menu'+_N
      execute = raw_input('=>').lower()
      if execute == 'n':
        print 'selecionado: NAO'
        return False
      elif execute == 's':
        print 'selecionado: SIM'
        return True
      elif execute == 't':
        mark_for_this_files = True
        print 'selecionado: TODOS NESTE'
        return False
      elif execute == 'l':
        mark_all_files_to_execute = True
        print 'selecionado: TODOS ARQUIVOS'
        return False
      elif execute == 'a':
        print 'selecionado: SALVAR'
        save_data_files()
        saveCmd = True
      elif execute == 'e':
        print 'selecionado: ERRO'
        return -1
      elif execute == '*':
        print 'selecionado: VOLTAR'
        return -2
      else:
        erroCode = True
    elif mode == 'Generic':
      execute = raw_input('=>').lower()
      if execute.isdigit():
        return int(execute)
      else:
        return execute
    else:
      erroCode = True

def getSHA1 (filePath): # FROM ranman LINK: http://stackoverflow.com/questions/22058048/hashing-a-file-in-python
  BUF_SIZE = 65536
  #md5 = hashlib.md5()
  sha1 = hashlib.sha1()
  with open(filePath, 'rb') as f:
    while True:
      data = f.read(BUF_SIZE)
      if not data:
        break
      #md5.update(data)
      sha1.update(data)
  return sha1.hexdigest() #return {'MD5':md5.hexdigest(), 'SHA1':sha1.hexdigest()}

def getMD5 (data):
  md5 = hashlib.md5()
  md5.update(data)
  return md5.hexdigest()

def executeChange (math, work_mode, sub_type):
  #var def
  out = {'work_type': work_mode+'_'+sub_type}
  directive = {'find_recordset':     None,
         'modify_recordset':     {'function': 'oSeg.StripNodes',         'mode': 'encapsulate'},
         'modify_request.enc':   {'function': 'oSeg.RequestEnc',         'mode': 'change_function'},
         'modify_request.query': {'function': 'oSeg.RequestQueryString', 'mode': 'change_function'},
         'modify_request.array': {'function': 'oSeg.RequestQueryArray',  'mode': 'change_function'},
         'modify_request.form':  {'function': 'oSeg.RequestForm',        'mode': 'change_function'}}
  if work_mode not in ['find_recordset', 'modify_recordset']:
    work_mode += '.'+sub_type
  #var def
  if directive[work_mode] == None:
    #var def
    out['start']  = math.start()
    out['end']    = math.end()
    out['start_g']  = math.start(1)
    out['end_g']  = math.end(1)
    g0 = math.group()
    #var def
    out['change'] = g0
    return out
  else:
    function = directive[work_mode]['function'] 
    if directive[work_mode]['mode']   == 'encapsulate':
      ### DO encapsulate
      out['start']  = math.start()
      out['end']    = math.end()
      out['start_g']  = out['start']
      out['end_g']  = out['end']
      g0 = math.group()
      out['change'] = function+'('+ g0 +')'
      ### END encapsulate
    elif directive[work_mode]['mode'] == 'change_function':
      ### DO change_function
      out['start']  = math.start()
      out['end']    = math.end()
      out['start_g']  = math.start(1)
      out['end_g']  = math.end(1)
      g2 = math.group(2)
      if g2 == None:
        if sub_type == 'array':
          g2 = ''
        else:
          g2 = '(Null)'
      out['change'] = function+g2
      ### END change_function
  return out

def makeNewLine (line, Maths, Tags, isShow, Simplify):
  #var def
  html   = ('html' in Tags)    if True else False
  console = ('console' in Tags) if True else False
  out = {'normal': {'old': '', 'new': ''}}
  if console:
    out['console'] = {'old': '', 'new': ''}
  if html:
    out['html'] = {'old': '', 'new': ''}
  out['normal']['old'] = line
  ASC = sorted(Maths)
  pE = None
  #var def
  for key in ASC:
    #var caller
    math = Maths[key]['data']
    #var caller
    if not isShow:
      if Maths[key]['work_type'] in ['find_recordset_dim', 'find_recordset_call']:
        continue
    #var def
    # *! print '\n', math, '\n'
    change = math['change']
    s = math['start']
    e = math['end']
    s1 = math['start_g']
    e1 = math['end_g']    
    normal_s = line[pE:s]
    sel_s = line[s:s1]
    group1 = line[s1:e1]
    sel_e = line[e1:e]
    pE = e
    #var def
    out['normal']['new'] += normal_s + change
    if console:
      out['console']['old'] += normal_s +_B+ sel_s +_G+ group1 +_B+ sel_e +_W
      out['console']['new'] += normal_s +_B+ change +_W
    if html:
      out['html']['old'] += escape(normal_s) +'<i>'+ escape(sel_s + group1 + sel_e) +'</i>'
      out['html']['new'] += escape(normal_s) +'<i>'+ escape(change) +'</i>'
  out['normal']['new'] += line[pE:]
  if console:
    out['console']['old'] += line[pE:]
    out['console']['new'] += line[pE:]
  if html:
    out['html']['old'] += escape(line[pE:])
    out['html']['new'] += escape(line[pE:])
    out['html']['old'] = (out['html']['old']).replace('\n', '<br>')
    out['html']['new'] = (out['html']['new']).replace('\n', '<br>')
  if not Simplify:
    out
  else:
    return out['normal']['new']

def createConsoleDialogs (dtLine, work, UpView):
  out = {}
  if UpView == None:
    if work in ['find_recordset']:
      old = dtLine['console']['old']
      out['highlight'] = _A+'Encontrado:\n'+_W+ old +_A+'\nFIM'+_N+'\n'
      out['dialog'] = 'Isto é uma variavel de RecordSet?'
    elif work in ['modify_recordset', 'modify_request']:
      old = dtLine['console']['old']
      new = dtLine['console']['new']
      out['highlight'] = _A+'ANTES:\n'+_W+ old +_A+'\nDEPOIS:\n'+_W+ new +_A+'\nFIM'+_N+'\n'
      out['dialog'] = 'Esta é uma alteração valida?'
  else:
    File = UpView['F']
    P = UpView['P']
    M = 5
    S = P -M -2
    S = S if S >= 0 else 0
    E = P +M
    E = E if E <= len(File) else len(File)
    Select_S = File[S:P-1]
    Select_E = File[P:E]
    old = ( dtLine['console']['old'] ).replace('\n','')
    new = ( dtLine['console']['new'] ).replace('\n','')
    if work in ['find_recordset']:
      old_txt = Select_S+[ old ]+Select_E
      old_txt = '\n'.join(old_txt)
      out['highlight'] = _A+'Encontrado:\n'+_W+ old_txt +_A+'\nFIM'+_N+'\n'
      out['dialog'] = 'Isto é uma variavel de RecordSet?'
    elif work in ['modify_recordset', 'modify_request']:
      old_txt = Select_S+[ old ]+Select_E
      new_txt = Select_S+[ new ]+Select_E
      old_txt = '\n'.join(old_txt)
      new_txt = '\n'.join(new_txt)
      out['highlight'] = _A+'ANTES:\n'+_W+ old_txt +_A+'\nDEPOIS:\n'+_W+ new_txt +_A+'\nFIM'+_N+'\n'
      out['dialog'] = 'Esta é uma alteração valida?'
  return out

def find_other_object (FileData):
  global patern_other_objects
  file_data = copy.copy(FileData)
  FP = regularGo(patern_other_objects, True)
  maths = FP.finditer(file_data)
  others = []
  for m in maths:
    others += [m.group(1)]
  return others

def find_in (Map, find):
  for K, Data in Map.iteritems():
    if Data['start'] <= find.start() and find.end() <= Data['end']:
      return True
  return False

def in_if_condition (found, if_map):
  for Start, Data in if_map.iteritems():
    if Data['t'] == 'If_Then':
      if Start <= found.start() and found.end() <= Data['e']:
        return True
  return False

def make_map_for (patern_map, FileData):
  file_data = copy.copy(FileData)+'\n' # this is a POG =(
  FP = regularGo(patern_map, True)
  maths = FP.finditer(file_data)
  out = {}
  i = 0
  for m in maths:
    i += 1
    out[i] = {'start':m.start(1), 'end':m.end(1)}
  return out

def map_line_break (FileData):
  global patern_line_break
  file_data = copy.copy(FileData)+'\n' # this is a POG =(
  FP = regularGo(patern_line_break, True)
  maths = FP.finditer(file_data)
  out = {}
  i = 0
  for m in maths:
    i += 1
    out[i] = {'start':m.start(), 'end':m.end()}
  return {'data':out, 'max':len(file_data)}

def find_line_position (find, Line_Map):
  line_list = Line_Map['data']
  msg = 'Erro on find line position:: max:'+str(Line_Map['max'])
  ASC = sorted(line_list)
  c = 0
  if type(find) == dict:
    for key in ASC:
      L = line_list[key]
      ''' if c < lineZero:
        continue '''
      c += 1
      if L['start'] <= find['start']:
        if find['end'] <= L['end']:
          return c
    #msg += ' m.s:'+str(find['start'])+' m.e:'+str(find['end'])
  else:
    for key in ASC:
      L = line_list[key]
      ''' if c < lineZero:
        continue '''
      c += 1
      if L['start'] <= find.start():
        if find.end() <= L['end']:
          return c
    #msg += ' m.s:'+str(find.start())+' m.e:'+str(find.end())
  print '\nLine_Map' #, Line_Map
  C = 0
  for key in ASC:
    L = line_list[key]
    print L
    C += 1
    if C > 5:
      break
  print 'find', ' m.s:'+str(find.start())+' m.e:'+str(find.end())
  raise Exception(msg)

def get_refLine (Line_Map, position):
  line = Line_Map['data'][position]
  return line['start']

def get_line (data_file, Line_Map, position):
  limit = get_line_limiter(data_file, Line_Map, position)
  s = limit['start']
  e = limit['end']
  return data_file[s:e]

def get_line_limiter (data_file, Line_Map, position):
  limit = Line_Map['data'][position]
  return limit

def find_if_zones (full_file):
  Tags = {}
  Tags['If'] = '(?:(?<!end)[ \t]+|[()\n]|<%=?)(If)(?:%>|[( \t\n])'
  Tags['Then'] = '(?:[() \t\n]|<%=?)(Then)(?:%>|[( \t\n])'
  #Tags['Then'] = '(?:[() \t\n]|<%=?)(End[ \t]+If)(?:%>|[( \t\n])'
  Founds = {}
  CountIfs = 0
  # find and store all If's Then's and End If's in a fast array search
  for key, patern in Tags.iteritems():
    FP = regularGo(patern, True)
    iter = FP.finditer(full_file)
    for it in iter:
      if key == 'If':
        CountIfs += 1
      Founds[it.start(1)] = {'t':key, 'e':it.end(1)}
  Ords = sorted(Founds)
  return createZones({}, Ords, Founds, CountIfs)

def createZones (Result, Ords, Founds, CountIfs):
  bound = len(Ords)
  # break if IN CASE dont have enough itens
  if bound <= 1:
    return Result
  CountNone = 0
  StartZone = 0
  State = 'FirstIf'
  Level = 0
  key = None
  Pos = -1
  while True:
    # break if IN CASE all is none
    if CountNone == bound or CountIfs <= 0:
      return Result
    #var def
    Pos += 1
    if Pos >= bound:
      # remove if IN CASE no then for this if
      if State == 'Then':
        Founds[key]['t'] = None
        CountIfs -= 1
      Pos = 0
      Level = 0
      State = 'If'
    start = Ords[Pos]
    #var def
    end = Founds[start]['e']
    tag = Founds[start]['t']
    #var def
    if tag == None:
      continue
    else:
      if State == 'FirstIf':
        if tag == 'If':
          StartZone = end
          State = 'Then'
          key = start
        Founds[start]['t'] = None
        CountNone += 1
      elif State == 'Then':
        if tag == 'Then':
          if Level > 0:
            Level -= 1
          else:
            CountIfs -= 1
            Result[StartZone] = {'t':'If_Then', 'e':start}
            Founds[start]['t'] = None
            CountNone += 1
            State = 'If'
        elif tag == 'If':
          Level += 1
      elif State == 'If':
        if tag == 'If':
          StartZone = end
          State = 'Then'
          key = start
  return Result

def drop_all_corrections ():
  global result_list
  for Id, File in result_list.iteritems():
    result_list[Id]['maths'] = {'data': {}, 'include': None}

def drop_all_includes ():
  global result_list
  for Id in result_list.keys():
    if result_list[Id]['maths']['include'] != None:
      M = result_list[Id]['maths']['include']
      del result_list[Id]['maths']['data'][M]
      result_list[Id]['maths']['include'] = None

def find_maths_in_file_list (patern_to_find, work, mode):
  global path_file, result_list, open_quest, do_all_process_alone, mark_all_files_to_execute, erro_list
  global patern_asp_tag, patern_is_in_seguranca, patern_for_each
  hourglass_START(-1)
  #var def
  mark_all_files_to_execute = do_all_process_alone
  if work == 'find_recordset' or work != 'modify_recordset':
    FP = regularGo(patern_to_find, True)
  #var def
  for Id, File in result_list.iteritems():
    # not process and empty
    if not File['process']:
      continue
    # not process and empty
    hourglass()
    #var def
    recordsets = []
    maths_selecteds = {}
    full_file_data = open(path_file+File['path']+File['name']).read()
    #var def
    # file BY PASS case
    if is_JSCript_file(full_file_data):
      continue
    # file BY PASS case
    # create maps
    asp_map  = make_map_for(patern_asp_tag, full_file_data)
    oseg_map = make_map_for(patern_is_in_seguranca, full_file_data)
    each_map = make_map_for(patern_for_each, full_file_data)
    if_map   = find_if_zones(full_file_data)
    # create maps
    # recordset patern MOUNT case
    if   work == 'find_recordset':
      dictionaryMOUNTdeny(Id)
      Maths = FP.finditer(full_file_data)
    elif work == 'modify_recordset':
      dictionaryMOUNTpass(Id)
      patern_to_find = create_recordset_patern()
      Maths = []
      if patern_to_find != '':
        Maths = regularFind(patern_to_find, True, full_file_data)
    else:
      Maths = FP.finditer(full_file_data)
    # recordset patern MOUNT case
    for math in list(Maths):
      #!except correction
      if not find_in(asp_map, math):
        continue
      elif in_if_condition(math, if_map):
        continue
      elif find_in(oseg_map, math):
        continue
      elif work == 'find_recordset':
        if dictionaryFIND(math.group(1)):
          continue
      elif work == 'modify_request' and mode in ['array', 'query']:
        if find_in(each_map, math):
          mode = 'array'
        else:
          mode = 'query'
      #!except correction
      #var def
      open_quest = True
      mDta = executeChange(math, work, mode)
      #var def
      if work == 'find_recordset':
        recordsets += [math.group(1)]
      else:
        maths_selecteds[mDta['start']] = {'data': mDta, 'work_type': work+'_'+mode}
    if len(maths_selecteds) > 0:
      if work == 'find_recordset':
        result_list[Id]['recordsets'] = recordsets
      else:
        for key, mADD in maths_selecteds.iteritems():
          result_list[Id]['maths']['data'][key] = mADD

def opt_make_full_correction ():
  execute = consoleShow(_A+'Efetuar as correcoes em todos os arquivos selecionados?'+_N, 'YesOrNo')
  if execute:
    make_full_correction()

def correction_multiple_include ():
  global result_list
  hourglass_START(-1)
  RES = GRAFO_execute()
  return RES['include']

def recursive_find_have_include_instaled (includes_list):
  for Id in includes_list:
    if have_include_instaled(Id):
      return True
    Includes = result_list[Id]['includes']
    if recursive_find_have_include_instaled(Includes):
      return True
  return False

def have_include_instaled (file_id):
  global result_list
  if file_id in result_list.keys():
    if result_list[file_id]['maths']['include'] != None:
      return True
    else:
      for key, math in result_list[file_id]['maths']['data'].iteritems():
        if math['work_type'] == 'install_include':
          return True
  return False

def make_full_correction ():
  global result_list, path_file
  hourglass_START( count_files_process() )
  for Id, File in result_list.iteritems():
    # not process and empty
    if not File['process']:
      continue
    if File['maths'] == {'data': {}, 'include': None}:
      continue
    # not process and empty
    hourglass()
    full_path_file = path_file+File['path']+File['name']
    #if file not exist
    if not os.path.exists(full_path_file):
      raise ValueError('\nERRO\nArquivo nao existe na origem de copia.\nNome: '+File['name'])
    #if file not exist
    if getSHA1(full_path_file) == File['sha']:
      hourglass()
      makeChangesInFile(File)
    else:
      raise ValueError('\nERRO\nAo tentar criar arquivo, sha1 nao confere. arquivo:'+File['name'])
  consoleShow( _T+'Termino do processo...'+_N, None)

def opt_install_obj ():
  execute = consoleShow(_A+'Efetuar as includes para objeto utilizado'+_N, 'YesOrNo')
  if execute:
    installObjInFiles()
    consoleShow( _T+'Fim das alterações...'+_N, None)

def is_JSCript_file (full_file_data):
  global patern_have_JSCript
  FP = regularGo(patern_have_JSCript, True)
  maths = FP.finditer(full_file_data)
  for math in list(maths):
    return True
  return False

def installObjInFiles ():
  global path_file, fileList, result_list, patern_line_break, patern_have_layout_link_ARR, patern_findtoMAKE_layout_link, patern_have_obj_include, patern_findtoMAKE_obj_include, patern_findtoMAKE_obj_include_force
  # find all oLayout's
  hourglass_START(-1)
  FP = regularGo(patern_findtoMAKE_layout_link, True)
  for Id, File in result_list.iteritems():
    # not process and empty
    if not File['process']:
      continue
    # not process and empty
    hourglass()
    #var def
    full_file_data = open(path_file+File['path']+File['name']).read()  
    line_map = map_line_break(full_file_data)
    #var def
    maths = FP.finditer(full_file_data)
    for math in list(maths):
      #var def
      line_position = find_line_position(math, line_map)
      #var def
      obj_name = math.group(1)
      patern = patern_have_layout_link_ARR[0]+obj_name+patern_have_layout_link_ARR[1]
      ### print '\n*', patern_have_layout_link_ARR, '\n', patern, '\n', math.group()
      if not existMathIn(full_file_data ,patern):
        #var def
        Start = math.start()
        End = math.end()
        line = get_line(full_file_data, line_map, line_position)
        change = line+ 'Set '+obj_name+'.Seguranca = oSeg\n'
        #var def
        mDta = {'start': Start, 'end': End, 'start_g': Start, 'end_g': End, 'change': change}
        result_list[Id]['maths']['data'][mDta['start']] = {'data': mDta, 'work_type': 'install_link'}
  # find all install need's
  FP = regularGo(patern_findtoMAKE_obj_include, False)
  FP_unique = regularGo(patern_findtoMAKE_obj_include_unique, False)
  FP_force = regularGo(patern_findtoMAKE_obj_include_force, False)
  drop_all_includes()
  white_list = correction_multiple_include()
  for Id, File in result_list.iteritems():
    # not process and empty and not in white list
    if not File['process']:
      continue
    if File['maths']['data'] == {}:
      continue
    if Id not in white_list:
      continue
    # not process and empty and not in white list
    hourglass()
    if have_include_instaled(Id):
      continue
    #var def
    not_install_in_first_mode = True
    full_file_data = open(path_file+File['path']+File['name']).read()    
    line_map = map_line_break(full_file_data)
    #var def
    if not existMathIn(full_file_data, patern_have_obj_include):
      #var def
      change = '\n<!--#include virtual="/Classes/Seguranca.asp"-->\n<% Dim oSeg : Set oSeg = New Seguranca %>\n'
      #var def
      maths = FP.finditer(full_file_data)
      for math in list(maths):
        #var def
        Start = math.start(1)
        End = math.end(1)
        #var def
        not_install_in_first_mode = False
        break
      if not_install_in_first_mode:
        maths = FP_unique.finditer(full_file_data)
        for math in list(maths):
          #var def
          Start = math.start(1)
          End = math.end(1)
          #var def
          not_install_in_first_mode = False
          break
      if not_install_in_first_mode:
        maths = FP_force.finditer(full_file_data)
        for math in list(maths):
          #var def
          Start = math.start(1)
          End = math.end(1)
          #var def
          not_install_in_first_mode = False
          break
      if not not_install_in_first_mode:
        mDta = {'start': Start, 'end': End, 'start_g': Start, 'end_g': End, 'change': change}
        result_list[Id]['maths']['data'][mDta['start']] = {'data': mDta, 'work_type': 'install_include'}
        result_list[Id]['maths']['include'] = mDta['start']
      else:
        mDta = {'start': 0, 'end': 0, 'start_g': 0, 'end_g': 0, 'change': change}
        result_list[Id]['maths']['data'][-1] = {'data': mDta, 'work_type': 'install_include'}
        result_list[Id]['maths']['include'] = -1

def existMathIn (file_data ,patern):
  FP = regularGo(patern, False)
  maths = FP.finditer(file_data)
  for math in list(maths):
    return True
  return False

def makeChangesInFile (File):
  global path_file, path_file_change
  #var def
  Maths = File['maths']['data']
  filePath = path_file+File['path']+File['name']
  #if file not exist
  if not os.path.exists(filePath):
    raise ValueError('\nERRO\nArquivo nao existe na origem de copia.\nNome: '+File['name'])
    return
  #if file not exist
  file = open(filePath, 'r')
  file_data = file.read()
  file.close()
  #var def
  file_data = makeNewLine(file_data, Maths, [], False, True)
  '''if File['maths']['include'] != None:
    M = File['maths']['include']
    change = result_list[Id]['maths']['data'][M]
    file_data = change +file_data'''
  create_path_if_not_exit(File['path'])
  #var def
  filePath = path_file_change+File['path']+File['name']
  file = open(filePath, 'w')
  file.write(file_data)

def create_path_if_not_exit(directory):
  global path_file_change
  if not os.path.exists(path_file_change+directory):
    os.makedirs(path_file_change+directory)

def hourglass_START (limit):
  global hourglass_pass
  hourglass_pass['limit'] = float(limit)
  hourglass_pass['status'] = 0
  hourglass_pass['point'] = 0
  os.system('cls')
  if hourglass_pass['limit'] == -1:
    sys.stdout.write('\n\nAguarde...')
  else:
    print '\n\tCriando copias\n\tArquivos modificados: '+str(int(hourglass_pass['limit']))
    sys.stdout.write('\n  Aguarde:\n')

def hourglass ():
  global hourglass_pass
  if hourglass_pass['limit'] == -1:
    hourglass_pass['status'] += 1
    sys.stdout.write('.')
    if hourglass_pass['status'] > 388:
      os.system('cls')
      hourglass_pass['status'] = 0
      sys.stdout.write('\n\nAguarde...')
  else:
    hourglass_pass['status'] += 1
    old_point = hourglass_pass['point']
    hourglass_pass['point'] = hourglass_pass['status'] / hourglass_pass['limit'] * 40 #char lim 80
    if old_point < int(hourglass_pass['point']):
      sys.stdout.write('=')

def writeLogFile ():
  global path_log, result_list
  print "\n>>>Criando Log"
  filePath = path_log +'/log.html'
  f = open(filePath, 'w')
  f.write( htmlCss() );
  for kF, file in result_list.iteritems():
    #var def
    name = file['name']
    LineWorks = file['line_works']
    ocorrencia = 0
    MathGroup = ''
    #var def
    for kW, LineData in LineWorks.iteritems():
      #var def
      position = LineData['position']
      old_line = LineData['old']
      Maths = LineData['maths']
      MathLine = ''
      #var def
      for kM, math in Maths.iteritems():
        if math['work_type'] not in ['find_recordset_dim', 'find_recordset_call']:
          ocorrencia += 1
          MathLine =  MathLine + htmlDiv_Math(math['start'], math['end'])
      if len(MathLine):
        dtLine = makeNewLine(old_line, Maths, ['html'], False)
        old_line_tag = dtLine['html']['old']
        new_line_tag = dtLine['html']['new']
        MathGroup = MathGroup + htmlDiv_Line(position, MathLine, old_line_tag, new_line_tag);
    f.write( htmlDiv_File(name, ocorrencia, MathGroup) );
  f.close()
  webbrowser.open(path_log +'/log.html')
#FUNCTION
#########

######
#GRAFO

def GRAFO_find_Roots ():
  global grafo, woodlist, rootlist, all_rootlist
  woodlist = {}
  rootlist = []
  all_rootlist = {}
  for N in grafo.keys():
    for L in grafo[N]['links']:
      woodlist[L] = 0
  woodlist = woodlist.keys()
  for N in grafo.keys():
    if N not in woodlist:
      if len(grafo[N]['links']) > 0:
        all_rootlist[N] = 0
  all_rootlist = all_rootlist.keys()

def GRAFO_easy_process ():
  global grafo, woodlist, seedlist, rootlist, all_rootlist, Processed_Roots
  Processed_Roots = []
  # process roots
  for R in all_rootlist:
    if grafo[R]['active']:
      Processed_Roots += [R]
      grafo[R]['*'] = True
    else:
      rootlist = [R]

def GRAFO_recursive_setRoots (Root, N):
  global grafo
  grafo[Root]['groups'] += grafo[N]['links']
  grafo[N]['roots'] += [Root]
  for L in grafo[N]['links']:
    GRAFO_recursive_setRoots(Root, L)

def GRAFO_setRoots_setGroups ():
  global grafo, rootlist
  for R in all_rootlist:
    grafo[R]['groups'] = grafo[R]['links']
    for L in grafo[R]['links']:
      GRAFO_recursive_setRoots(R, L)

def GRAFO_find_and_process_seeds ():
  global grafo, rootlist, seedlist, Processed_Roots
  seedlist = {}
  for S in grafo:
    if grafo[S]['links'] == [] and grafo[S]['roots'] == []:
      seedlist[S] = 0
      grafo[S]['*'] = True
      Processed_Roots += [S]
  seedlist = seedlist.keys()

def GRAFO_add_group_roots (key, Roots):
  global crosslist, crossgroup
  for R in Roots:
    if R not in crossgroup[key]:
      crossgroup[key] += [R]
      crosslist[R] = 0

def GRAFO_group_roots ():
  global grafo, woodlist, rootlist, alonelist, crosslist, crossgroup
  crossgroup = {}
  alonelist  = []
  crosslist  = {}
  for W in woodlist:
    hourglass()   #*------!  
    thisRoots = grafo[W]['roots']
    if len(thisRoots) > 0:
      found = False
      for k, group in crossgroup.iteritems():
        for R in thisRoots:
          if R in group:
            GRAFO_add_group_roots(k, thisRoots)
            found = True
            break
      if not found:
        key = len(crossgroup)
        crossgroup[key] = thisRoots
        for R in thisRoots:
          crosslist[R] = 0
  crosslist = crosslist.keys()
  for R in rootlist:
    if R not in crosslist:
      alonelist += [R]
  crosslist = None

def GRAFO_recursive_setRanks (N, pt):
  global grafo
  grafo[N]['rank'] += 1+pt
  pt = grafo[N]['rank']
  for L in grafo[N]['links']:
    GRAFO_recursive_setRanks(L, pt)

def GRAFO_rank_all ():
  global grafo, woodlist, alonelist
  for R in rootlist:
    if R not in alonelist:
      for L in grafo[R]['links']:
        GRAFO_recursive_setRanks(L, 0)
  for W in woodlist:
    grafo[W]['rank'] *= len(grafo[W]['roots'])

def GRAFO_find_best (List):
  first = True
  best = None
  for N in List:
    if grafo[N]['active']:
      if first:      
        best = N
        score = grafo[N]['rank']
        first = False
      elif grafo[N]['rank'] < score:
        best = N
        score = grafo[N]['rank']
  return best

def GRAFO_process_alone ():
  global grafo, alonelist, Processed_Roots
  for A in alonelist:
    best = GRAFO_find_best(select)
    if best == None:
      Processed_Roots += [R]
      grafo[R]['*'] = True

def GRAFO_remove_black_nodes (List, Blacklist):
  white = []
  for N in List:
    if N not in Blacklist:
      white += [N]
  return white

def GRAFO_feed_processed_Noods (thisRoots, Processed_Noods):
  Noods = {}
  for R in thisRoots:
    Noods[R] = 0
    for N in grafo[R]['groups']:
      Noods[N] = 0
  for N in Noods.keys():
    Processed_Noods[N] = 0
  return Processed_Noods

def GRAFO_process_cross ():
  global grafo, crossgroup, Processed_Roots
  Processed_Noods = {}
  for pR in Processed_Roots:
    Nodos = grafo[pR]['groups']
    if Nodos != None:
      for N in Nodos:
        Processed_Noods[N] = 0
  '''raw_input(Processed_Roots)
  raw_input(Processed_Noods)'''
  limit = 10
  while limit > 0:
    if len(crossgroup) > 0:
      limit -= 1
      remove = []
      for k, group in crossgroup.iteritems():
        hourglass()   #*------!  
        select = []
        for R in group:
          if R not in Processed_Roots:
            select += [R] + grafo[R]['groups']
        select = GRAFO_remove_black_nodes(select, Processed_Noods.keys())
        if len(select) == 0:
          remove += [k]
          continue
        best = GRAFO_find_best(select)
        if best == None:
          remove += [k]
          continue
        else:
          grafo[best]['*'] = True
          Processed_Noods[best] = 0
          thisRoots = grafo[best]['roots']
          Processed_Roots += thisRoots
          Processed_Noods = GRAFO_feed_processed_Noods(thisRoots, Processed_Noods)
        #*-*-*-*-
        '''print best, '\n<S>', select, '\n<R>', Processed_Roots, '\n<B>', Processed_Noods.keys()
        raw_input()'''
        #*-*-*-*-
      for D in remove:
        del crossgroup[D]
    else:
      break

def GRAFO_process ():
  time = (datetime.now()).microsecond
  GRAFO_find_Roots()
  GRAFO_easy_process()
  GRAFO_setRoots_setGroups()
  GRAFO_find_and_process_seeds()
  GRAFO_group_roots()
  GRAFO_rank_all()
  GRAFO_process_alone()
  GRAFO_process_cross()
  time = (datetime.now()).microsecond - time
  #raw_input('END:'+str(time))

def GRAFO_in ():
  global grafo, GRAFO_index_list, result_list
  grafo = {}
  GRAFO_index_list = {}
  for Id in result_list.keys():
    # correcao temporaria
    '''if result_list[Id]['path'] == 'WEB/popup/':
      continue'''
    # correcao temporaria
    hourglass()   #*------!  
    active = result_list[Id]['process']# and result_list[Id]['maths']['include'] != None:
    if Id not in GRAFO_index_list.values():
      newKey = len(GRAFO_index_list)
      GRAFO_index_list[newKey] = Id
      includes = result_list[Id]['includes']
      grafo[newKey] = {'*':False, 'active':active, 'links':includes, 'rank':0, 'roots':[], 'groups':None}
  for N in grafo.keys():
    hourglass()   #*------!  
    links = []
    for LinkID in grafo[N]['links']:
      for Key, ID in GRAFO_index_list.iteritems():
        if ID == LinkID:
          links += [Key]
          break
    grafo[N]['links'] = links
  '''for G in grafo.keys():
    print G, '\t', grafo[G]
  for N, ID in GRAFO_index_list.iteritems():
    GRAFO_index_list[N] = result_list[ID]['name']
    print N, '\t', GRAFO_index_list[N]
  ''for k, N in grafo.iteritems():
    #print 'k', k, '\tR', N['rank'], '\tC', N['cross'], '\trefs', grafo[k]['refs'], '\t*', N['*']
    print '\tk', k, '\tlinks', grafo[k]['links']
    print grafo[k]
    print 'id:'+str(GRAFO_index_list[k])+'\n'
    #raw_input('_')'''

def GRAFO_find_erro ():
  global grafo, all_rootlist, GRAFO_index_list, result_list, erro_list
  for R in all_rootlist:
    if grafo[R]['*']:
      continue
    group = grafo[R]['groups']
    if group != None:
      for N in group:
        if grafo[N]['*']:
          continue
    # get erro
    ID = GRAFO_index_list[R]
    erro_item  = result_list[ID]
    #del result_list[ID]
    erro_list[ID] = {'data':erro_item, 'from':None ,'msg': 'cant process in grafo', 'code': 1}

def GRAFO_out ():
  global GRAFO_index_list, grafo, rootlist, woodlist, seedlist, crossgroup, crosslist, Processed_Noods, Processed_Roots
  white = []
  black = []
  for N in grafo.keys():
    ID = GRAFO_index_list[N]
    if grafo[N]['*']:
      white += [ID]
    else:
      black += [ID]
  GRAFO_find_erro()
  '''print 'GRAFO>>>'
  for G in grafo:
    ID = GRAFO_index_list[G]
    name = result_list[ID]['name']
    path = result_list[ID]['path']
    print '\t', G, 'path', path, 'name', name, '*', grafo[G]['*'], 'P', grafo[G]['active']
    print '\t', 'links', grafo[G]['links'], 'groups', grafo[G]['groups'], name, '\t', 'roots', grafo[G]['roots']
    print 'ID:', ID, '\n'
  print '<<<GRAFO\tWHITE>>>'
  print white
  print '<<<WHITE\tBLACK>>>'
  print black
  print 'WHITE>>>'
  print len(white)
  print '<<<WHITE\tBLACK>>>'
  print len(black)
  raw_input('<<<BLACK')#'''
  grafo = None
  rootlist = None
  woodlist = None
  seedlist = None
  crossgroup = None
  crosslist = None
  Processed_Noods = None
  Processed_Roots = None
  GRAFO_index_list = None
  return {'include':white, 'remove':black}

def GRAFO_execute ():
  global grafo
  GRAFO_in()
  GRAFO_process()
  return GRAFO_out()

#GRAFO
######

#####
#HTML
def htmlDiv_File(Filename, ocorrencia, List):
  return """
  <div id=file >
    <div id=name>
      Nome:<b>%s</b><br />
      Ocorrencia(s): <b>%s</b>
    </div>
    <div id=linelist>
      %s
    </div>
  </div>
  """ % (Filename, ocorrencia, List)

def htmlDiv_Line(lineKey, changes, oldLine, newLine):
  return """
  <div id=line>
    <div id=linepos>
      Linha: <b>%s</b>
    </div>
    <div id=changes>
      <b>%s</b>
    </div>
    <div id=linechange>
      <div id=old>
        <b>%s</b>
      </div>
      <div id=new>
        <b>%s</b>
      </div>
    </div>
  </div>
  """ % (lineKey, changes, oldLine, newLine)

def htmlDiv_Math(start, end):
  return """
  <div id=math>
    <div id=start>
      Start: <b>%s</b>
    </div>
    <div id=end>
      End: <b>%s</b>
    </div>
  </div>
  """ % (start, end)

def htmlCss():
  return """
  <style>
    b {
      font-weight: bold;
    }
    i {
      color: white;
      font-weight: bold;
      background: #DAD629;
    }
    div {
      margin: 0.45em;
    }
    div#filename {
      font-weight: bold;
    }
    div#changes {
      display: inline-block;
    }
    div#line {
      background-color: #B9B7B7;
    }
    div#math {
      float: left;
    }
    div#math, div#old, div#new {
      display: -webkit-box;
      background-color: lightgray;
    }
    div#file {
        margin: 2em;
        background-color: gray;
    }
  </style>
  """
#HTML
#####

########
#EXECUTE
MAIN()
#EXECUTE
########
