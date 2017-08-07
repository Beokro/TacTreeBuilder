# Todo
# check if entity already exist before adding it to Dict

filename = "../Lag/LacpAgent.tac"
file = open(filename, "r")

currentNameSpace = []
entityDict = {}

class entity:
    def __init__( self, name ):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.members = []
        self.inputOf = []
        self.outputOf = []
        self.memberOf = []

    def addInput( self, name ):
        self.inputs.append( name )

    def addOutput( self, name ):
        self.outputs.append( name )

    def addMember( self, name ):
        self.members.append( name )

    def isInputOf( self, name ):
        self.inputOf.append( name )

    def isOutputOf( self, name ):
        self.OutputOf.append( name )

    def isMemberOf( self, name ):
        self.memberOf.append( name )

def getNameSpace():
    prefix = ''
    for namespace in currentNameSpace:
        prefix += ( namespace + '::' )
    return prefix

def getEntityName():
    prefix = ''
    for namespace in currentNameSpace:
        prefix += ( namespace + '::' )
    if len( prefix ) > 2:
        return prefix[ : -2 ]

def getTypeName( word ):
    if word[ -1 ] == ';':
        word = word[ : -1 ]

    if word.endswith( '::Ptr' ):
        word = word[ : -5 ]
    elif word.endswith( '::PtrConst' ):
        word = word[ : -10 ]
    return word

# return extra line it read
def skipIntro ( file ):
    while True:
        pos = file.tell()
        words = file.readline().split()
        if len( words ) == 0 or words[ 0 ] == '//' or words[ 0 ] == '<<=':
            # skip comment and import tac module
            continue
        # undo the readline or next function can see the first not intro line
        file.seek( pos )
        return

def incompleteType( words ):
    if len( words ) < 3 or words[ 1 ] != ':' or not words[ 2 ].startswith( 'Tac::Type' ):
        return False
    # this line is a entity defination, look for the second ':'
    for i in range( 3, len( words ) - 1 ):
        if words[ i ] == ':':
            return False
    return True

def getCompleteLine( file ):
    line = file.readline()
    words = line.split()

    # skip the empty line, comment and line start with '
    while len( words ) == 0 or words[ 0 ] == '//' or words[ 0 ][ 0 ] == '`':
        line = file.readline()
        # if end of file return empty
        if not line:
            return []
        words = line.split()

    # check if there is '//' in this line, if there is one
    # strip the rest of the line
    for i in range( len( words ) ):
        if words[ i ] == '//':
            return words[ :i ]


    # if line ended with a ',' combine it with next line
    while words[ -1 ][ -1 ] == ',' or words[ -1 ][ -1 ] == ':' or incompleteType( words ):
        line = file.readline()
        words.extend( line.split() )
    return words

def isNameSpace( words ):
    # assunming all namespace decls have format xxx : Tac::Namespace {
    return len( words ) == 4 and words[ 2] == 'Tac::Namespace' and words[ 3 ] == '{'

def handleNameSpace( words ):
    currentNameSpace.append( words[ 0 ] );

def isForwardDecl( words ):
    return len( words ) == 5 and words[ 2 ] == 'Tac::Type()' and\
        words[ 4 ] == 'Tac::Constrainer;';

def handleForwardDecl( words ):
    return

def isEntity( words ):
    return len( words ) > 5 and words[ -1 ] == '{' and words[ -2 ] == 'Tac::Entity'

def handleEntity( words ):
    newEntity = entity( getNameSpace() + words[ 0 ] )
    currentNameSpace.append( words[ 0 ] )
    entityDict[ newEntity.name ] = newEntity

def isElement( words ):
    return len( words ) == 3 and words[ 1 ] == ':'

def handleElement( words ):
    # add current element to the entity member list
    typeName = getTypeName( words[ 2 ] )
    entityDict[ getEntityName() ].addMember( typeName )

    # check if entity is already in the map

def analyzeFile( file ):
    skipIntro( file )
    words = getCompleteLine( file )
    typeCheckers = [ isNameSpace,
                     isForwardDecl,
                     isEntity,
                     isElement ]
    handlers = [ handleNameSpace,
                 handleForwardDecl,
                 handleEntity,
                 handleElement ]

    while len( words ):
        for i in range( len( typeCheckers ) ):
            if typeCheckers[ i ]( words ):
                handlers[ i ]( words )
                break
        words = getCompleteLine( file )

analyzeFile( file )
print entityDict
