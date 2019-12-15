import wx.grid
import random
import math

#Para crear una aplicación con wx es necesario encapsular el código entre las linas app = wx.App() y app.MainLoop()
app = wx.App()

#Utility Classes*************************************************************************************************

class ContinuousColumn:
    def __init__(self, continuousColumnValues, classColumnValues, uniqueClassValues):
        self.continuousColumnValues = continuousColumnValues
        self.classColumnValues = classColumnValues
        self.uniqueClassValues = uniqueClassValues
        self.classesItems = dict()
        self.classesMeans = dict()
        self.classesVariances = dict()

        self.createStatisticClasses()

    def createStatisticClasses(self):
        for u in self.uniqueClassValues:
            self.classesItems[u] = []
            self.classesMeans[u] = 0
            self.classesVariances[u] = 0

    def getContinuousColumnDetails(self):
        for i in range(0, len(self.classColumnValues)):
            self.classesItems[self.classColumnValues[i]].append(self.continuousColumnValues[i])

        self.calculateMean()
        self.calculateVariance()

        return ContinuousColumnStatistics(self.classesMeans, self.classesVariances, self.classesItems)

    #calcula la media
    def calculateMean(self):
        for k in self.classesItems.keys():
            self.classesItems[k]
            mean = sum(self.classesItems[k]) / len(self.classesItems[k])
            self.classesMeans[k] = mean

    def calculateVariance(self):
        for k in self.classesItems.keys():
            values = self.classesItems[k]
            sumatory = 0
            for i in values:
                sumatory += pow(i - self.classesMeans[k], 2)

            if len(values)>1:
                self.classesVariances[k] = sumatory / (len(values)-1)
            else:
                self.classesVariances[k] = 1

class ContinuousColumnStatistics:
    def __init__(self, classesMean, classesVariances, classesItems):
        self.classesMeans = classesMean
        self.classesVariances = classesVariances
        self.classesItems = classesItems

class RuleSet:
    #rules = dict(), classColumnValues = list(), uniqueClassValues = set(), uniqueSuffixValues = set()
    def __init__(self, rules, classColumnValues, uniqueClassValues, uniqueSuffixesValues):
        #EN PYTHON LOS ATRIBUTOS DE CLASE SE DECLARAN EN EL CONSTRUCTOR
        self.rules = rules
        self.classColumnValues = classColumnValues
        self.uniqueSuffixesValues = uniqueSuffixesValues
        self.uniqueClassValues = uniqueClassValues
        self.rulesProbabilities = []

    def setRulesetProbability(self, rulesetProbability):
        self.rulesProbabilities.append(rulesetProbability)

class RulesetProbability:
    def __init__(self, variable, ecuacion, probabilityResult):
        self.variable = variable
        self.ecuacion = ecuacion
        self.probabilityResult = probabilityResult

class BayesianTable:
    def __init__(self):
        self.columns = []

    def addColumn(self, bayesianColumn):
        self.columns.append(bayesianColumn)

#Widgets Properties*************************************************************************************************
columnsList = []
classesProbabilities = {}
ruleset = []
continuousColumns = []
bayesianTable = None

MAIN_WINDOW_PARENT = None
MAIN_WINDOW_TITLE = "Naive Bayes"
FILL_TABLE_BTN_TXT = "Llenar Tabla"
CLEAR_TABLE_BTN_TXT = "Limpiar Tabla"
TRAINING_BTN_TXT = "Entrenar"
PREDICT_TUPLE_BTN_TXT = "Tupla a Predecir"
ADD_COLUMN_BTN_TXT = "Agregar Columna"
REMOVE_COLUMN_BTN_TXT = "Eliminar Columna"
ADD_ROW_BTN_TXT = "Agregar Fila"
REMOVE_ROW_BTN_TXT = "Eliminar Fila"
NEW_COLUMN_DIALOG = "Por Favor Checa la caja de verificación si la columna es Numerica";
NEW_COLUMN_CHECK_BOX_MESSAGE = "La columna es numérica?"

NEW_ENTRY_WINDOW_TITLE = "Tupla a Predecir"
PREDICT_BTN_TXT = "Predecir Tupla"
#Widgets*************************************************************************************************

    #mainWindow*************************************************************************************************

mainWindow = wx.Frame(MAIN_WINDOW_PARENT, wx.ID_ANY, MAIN_WINDOW_TITLE, wx.Point(90, 50), wx.Size(750, 650))
panel = wx.Panel(mainWindow, wx.ID_ANY)

fillTableBtn = wx.Button(panel, wx.ID_ANY, FILL_TABLE_BTN_TXT, wx.Point(20, 20), wx.Size(90, 30))
trainingBtn = wx.Button(panel, wx.ID_ANY, TRAINING_BTN_TXT, wx.Point(120, 20), wx.Size(90, 30))
addPredictableTupleBtn = wx.Button(panel, wx.ID_ANY, PREDICT_TUPLE_BTN_TXT, wx.Point(220, 20), wx.Size(100, 30))
clearTableBtn = wx.Button(panel, wx.ID_ANY, CLEAR_TABLE_BTN_TXT, wx.Point(330, 20), wx.Size(90, 30))

mainGrid = wx.grid.Grid(panel, wx.ID_ANY, wx.Point(20, 80), wx.Size(400, 210))
mainGrid.CreateGrid(4, 1)

columnListBox = wx.ListBox(panel, wx.ID_ANY, wx.Point(450, 200), wx.Size(240, 350))

addColumnBtn = wx.Button(panel, wx.ID_ANY, ADD_COLUMN_BTN_TXT, wx.Point(450, 80),wx.Size(110, 30))
removeColumnBtn = wx.Button(panel, wx.ID_ANY, REMOVE_COLUMN_BTN_TXT, wx.Point(580, 80), wx.Size(110, 30))
addRowBtn = wx.Button(panel, wx.ID_ANY, ADD_ROW_BTN_TXT, wx.Point(450, 130),wx.Size(110, 30))
removeRowBtn = wx.Button(panel, wx.ID_ANY, REMOVE_ROW_BTN_TXT, wx.Point(580, 130), wx.Size(110, 30))

clearLogBtn = wx.Button(panel, wx.ID_ANY, "Limpiar Log", wx.Point(20, 310), wx.Size(400, 30))
log = wx.TextCtrl(panel, wx.ID_ANY, "", wx.Point(20, 350), wx.Size(400, 250), style=wx.TE_MULTILINE)

    #newEntryWindow*************************************************************************************************

newEntryWindow = wx.Frame(panel, wx.ID_ANY, NEW_ENTRY_WINDOW_TITLE, wx.Point(300, 200), wx.Size(400,400))
newEntryPanel = wx.Panel(newEntryWindow, wx.ID_ANY)
newEntryGrid = wx.grid.Grid(newEntryPanel, wx.ID_ANY, wx.DefaultPosition, wx.Size(200, 300))
newEntryGrid.CreateGrid(mainGrid.NumberCols-1, 1)
predictBtn = wx.Button(newEntryPanel, wx.ID_ANY, PREDICT_BTN_TXT, wx.Point(230, 30), wx.Size(110, 30))

#Utilities*************************************************************************************************

def buildClasses():
    '''
            se utiliza la palabra reservada global para poder acceder al scope global.
        Es necesario tomar la referencia de la variable global debido a que este metodo se ejecuta dentro de un evento
    '''
    global classesProbabilities
    classesProbabilities = {}
    classColumnValues = getColumnValues(0)
    uniqueClassValues = set(classColumnValues)
    classes = {}
    count = 0
    for u in uniqueClassValues:
        count = 0
        for i in range(0, len(classColumnValues)):
            if classColumnValues[i] == u:
                count+=1
                classes[u] = count

    for k in classes.keys():
        classesProbabilities[k] = int(classes[k]) / mainGrid.NumberRows

#mapea un valor booleano a un valor String
def getColumnType(boolValue):
    if boolValue == True:
        return "DISCRETE"
    else:
        return "CONTINUOUS"

#agrega una columna al grid
def addColumn(evt):
    #Se crea un cuadro de Dialogo con un checkbox
    dialog = wx.RichMessageDialog(panel, NEW_COLUMN_DIALOG)
    dialog.ShowCheckBox(NEW_COLUMN_CHECK_BOX_MESSAGE)
    dialog.ShowModal()

    mainGrid.AppendCols(1)
    newEntryGrid.AppendRows(1)

    columnsList.append({'columnName': mainGrid.GetColLabelValue(mainGrid.NumberCols - 1), 'type' : getColumnType(dialog.IsCheckBoxChecked())})
    columnListBox.Append(columnsList[len(columnsList)-1].get('columnName') + " || " + columnsList[len(columnsList)-1].get('type'))

#mapea una columna a un arreglo
def getColumnValues(columnIndex):
    columnValues = []
    for i in range(0, mainGrid.NumberRows):
        columnValues.append(mainGrid.GetCellValue(i, columnIndex))
    return columnValues

#convert String array values to float array values
def transformColumnValues(columnValues):
    values = []
    for i in columnValues:
        values.append(float(i))
    return values

#clasifica los valores de una columna
def classiffyContinuousColumn(continuousColumnIndex):
    #first column contains the classes
    classColumnValues = getColumnValues(0)
    uniqueClassValues = set(classColumnValues)
    continuousColumnValues = transformColumnValues(getColumnValues(continuousColumnIndex))

    return ContinuousColumn(continuousColumnValues, classColumnValues, uniqueClassValues)

#construye las reglas
def getRules(suffixColumnIndex):
    #first column contains the classes
    classColumnValues = getColumnValues(0)
    suffixColumnValues = getColumnValues(suffixColumnIndex)
    uniqueClassValues = set(classColumnValues)
    uniqueSuffixesValues = set(suffixColumnValues)
    '''
        Fue necesario mandar el ciclo que recorre a toda la tabla al nivel mas bajo para hacer las comparaciones
    '''
    rules = dict()
    for c in uniqueClassValues:
        for s in uniqueSuffixesValues:
            count = 0
            for i in range(0, mainGrid.NumberRows):
                if classColumnValues[i] == c and suffixColumnValues[i] == s:
                    count += 1
            rules[c+"->"+s] = count
    return RuleSet(rules, classColumnValues, uniqueClassValues, uniqueSuffixesValues)

#escribe un valor en el log
def logValue(description, value):
    log.write(description + ": " + str(value) + "\n")

#escribe los resumenes numericos en el log de una columna continua
def logContinuousColumn(continuousColumn):
    for k in continuousColumn.classesItems.keys():
        logValue("Media de "+k+": ", continuousColumn.classesMeans[k])
        logValue("Varianza de "+k+": ", continuousColumn.classesVariances[k])
    log.write("************************************************ \n")

#escribe los resultados del conteo de las reglas en el log de una columna Discreta
def logRuleset(ruleset):
    for k in ruleset.rules.keys():
        log.write(str(k) + ": " + str(ruleset.rules.get(k)) + "\n")
    log.write("************************************************ \n")

    for p in ruleset.rulesProbabilities:
        log.write("p("+p.variable+"):"+p.ecuacion + "\n")
    log.write("************************************************ \n")

def logNormalizedValues(normalizedValues, predictibleList):
    predictableTuple = tuple(predictibleList)
    for k in normalizedValues.keys():
        #para concatenar un valor con una lista se usa la comma en lugar del simbolo +
        resultString = str(("p(" + k + " |", predictableTuple, ") = " + str(normalizedValues[k])))

        #se limpia la string generada
        resultString = resultString.replace("'", "")
        resultString = resultString.replace(",", "")

        log.write( resultString + "\n")
    log.write("************************************************ \n")

#construye la ecuación en lenguaje matemático
def getEcuacionString(ruleCount, classItemCount, possibleValues, ruleProbabilityResult):
    return "(" + str(ruleCount) + " + 1)/(" + str(classItemCount) + " + " + str(possibleValues) + ") = " + str(ruleProbabilityResult)

#calcula la probabilidad de un conjunto de reglas
def calculateRulesetProbability(ruleset):
    classes = dict()

    if len(ruleset) > 0:
        #en todos los objetos estan presentes los valores clase, por lo que para obtenerlos solo es necesario extraerlos de un objeto
        for i in ruleset[0].uniqueClassValues:
            count = 0
            for j in ruleset[0].classColumnValues:
                if i == j:
                    count += 1
            classes[i] = count

    for r in ruleset:
        for rule in r.rules:
            classRule = getClass(rule)
            classes.get(classRule)
            #ecuacion de probabilidad de una regla
            ruleProbabilityResult = (r.rules[rule] + 1)/(classes.get(classRule) + len(r.uniqueSuffixesValues))
            ecuacionString = getEcuacionString(r.rules[rule], classes.get(classRule), len(r.uniqueSuffixesValues), ruleProbabilityResult)
            r.setRulesetProbability(RulesetProbability(rule, ecuacionString, ruleProbabilityResult))

#obtiene la clase de una determinada regla
def getClass(rule):
    return rule.split("->")[0]

#regresa el caracter ascii en funcion de un código numérico
def getAscii(code):
    return chr(code)

#Events*************************************************************************************************
def fillClassColum():
    for i in range(0, mainGrid.NumberRows):
        mainGrid.SetCellValue(i, 0, str(random.randint(0, 1)))

def fillDiscreteColumn(columIndex):
    for i in range(0, mainGrid.NumberRows):
        mainGrid.SetCellValue(i, columIndex, getAscii(random.randint(65, 67)))

def fillCountinuousColumn(columnIndex):
    for i in range(0, mainGrid.NumberRows):
        mainGrid.SetCellValue(i, columnIndex, str((random.randrange(155, 389) / 100)))

def fillTable(evt):
    fillClassColum()
    for i in range(0, len(columnsList)):
        if(columnsList[i].get('type') == "DISCRETE"):
            fillDiscreteColumn(i+1)
        elif(columnsList[i].get('type') == "CONTINUOUS"):
            fillCountinuousColumn(i+1)

def removeColumn(evt):
    #se borra la ultima columna del mainGrid
    mainGrid.DeleteCols(mainGrid.NumberCols - 1)
    #se borra la ultima fila del listbox
    columnListBox.Delete(len(columnsList)-1)
    #se borra el ultimo elemento de la lista
    del columnsList[-1]
    #se borra la ultima fila del newEntryGrid
    newEntryGrid.DeleteRows(newEntryGrid.NumberRows-1)

def clearTable(evt):
    mainGrid.ClearGrid()

def buildBayesianTable():
    '''
            se utiliza la palabra reservada global para poder acceder al scope global.
        Es necesario tomar la referencia de la variable global debido a que este metodo se ejecuta dentro de un evento
    '''
    global bayesianTable
    bayesianTable = BayesianTable()

    #se obtienen hacen los calculos necesarios a partir del tipo de la columna
    for i in range(0, len(columnsList)):
        if columnsList[i].get('type') == "DISCRETE":
            ruleset.append(getRules(i+1))
            bayesianTable.addColumn((columnsList[i].get('type'), ruleset[len(ruleset) - 1]))
        elif columnsList[i].get('type') == "CONTINUOUS":
            continuousColumn = classiffyContinuousColumn(i + 1)
            continuousColumns.append(continuousColumn)
            classification = continuousColumn.getContinuousColumnDetails()
            bayesianTable.addColumn((columnsList[i].get('type'), classification))

    #se agregan las probabilidades al ruleset
    calculateRulesetProbability(ruleset)

    #se construyen las classes
    buildClasses()

    #se calculan las probabilidades de las clases
    for k in classesProbabilities.keys():
        logValue("p(" + str(k) + ")", classesProbabilities[k])
    log.write("************************************************ \n")

    #se escriben en el log los resultados bayesianos construida
    for c in bayesianTable.columns:
        if c[0] == "DISCRETE":
            logRuleset(c[1])
        elif c[0] == "CONTINUOUS":
            logContinuousColumn(c[1])

def training(evt):
    buildBayesianTable()

def getPredictibleValue(evt):
    newEntryWindow.Show(True)

def naibeBayes(x, mean, variance):
    return ( ( 1 / ( math.sqrt( 2 * math.pi ) * math.sqrt(variance) ) ) * ( math.exp( -( pow( ( x - mean ), 2 ) / ( 2 * variance ) ) ) ) )

def normalization(probabilities):
    return sum(probabilities.values())

def predictValue(evt):
    global bayesianTable
    predictibleList = []
    nb = dict()
    cMapFactors = {}

    for k in classesProbabilities.keys():
        #se crean las clases de los factores
        cMapFactors[k] = list()
        #se agrega a la propia lista el elemento de la llave actual k
        cMapFactors[k].append(classesProbabilities[k])

    for i in range(0, len(bayesianTable.columns)):
        predictibleList.append(newEntryGrid.GetCellValue(i, 0))
        if bayesianTable.columns[i][0] == "DISCRETE":
            for k in bayesianTable.columns[i][1].uniqueClassValues:
                for j in range(0, len(bayesianTable.columns[i][1].rulesProbabilities)):
                    x = newEntryGrid.GetCellValue(i, 0)
                    if bayesianTable.columns[i][1].rulesProbabilities[j].variable == k+"->"+x:
                        cMapFactors[k].append(bayesianTable.columns[i][1].rulesProbabilities[j].probabilityResult)
        elif bayesianTable.columns[i][0] == "CONTINUOUS":
            x = float(newEntryGrid.GetCellValue(i, 0))
            nb = dict()
            for k in bayesianTable.columns[i][1].classesItems.keys():
                mean = bayesianTable.columns[i][1].classesMeans[k]
                variance = bayesianTable.columns[i][1].classesVariances[k]
                nb[k] = naibeBayes(x, mean, variance)
                cMapFactors[k].append(nb[k])

    #se hace la multiplicacion de los factores para obtener las probabilidades de cada clase
    m = 1
    #forma nativa de crear un diccionario vacio a partir de otro diccionario
    p = dict.fromkeys(cMapFactors.keys())
    #se multiplican todos los factores de cada lista dentro de cMapFactors
    for k in cMapFactors.keys():
        m = 1
        for i in range(0, len(cMapFactors[k])):
            m *= cMapFactors[k][i]
        p[k] = m

    total = normalization(p)
    normalizedValues = dict.fromkeys(p.keys())
    for k in normalizedValues.keys():
        normalizedValues[k] = p[k] / total

    logNormalizedValues(normalizedValues, predictibleList)

#Listeners*************************************************************************************************
fillTableBtn.Bind(wx.EVT_BUTTON, fillTable)
clearTableBtn.Bind(wx.EVT_BUTTON, clearTable)
trainingBtn.Bind(wx.EVT_BUTTON, training)
addPredictableTupleBtn.Bind(wx.EVT_BUTTON, getPredictibleValue)
addColumnBtn.Bind(wx.EVT_BUTTON, addColumn)
removeColumnBtn.Bind(wx.EVT_BUTTON, removeColumn)
addRowBtn.Bind(wx.EVT_BUTTON, lambda evt: mainGrid.AppendRows(1))
removeRowBtn.Bind(wx.EVT_BUTTON, lambda evt: mainGrid.DeleteRows(mainGrid.NumberRows-1, 1))
clearLogBtn.Bind(wx.EVT_BUTTON, lambda evt: log.Clear())
newEntryWindow.Bind(wx.EVT_CLOSE, lambda evt: newEntryWindow.Show(False))
predictBtn.Bind(wx.EVT_BUTTON, predictValue)
mainWindow.Show(True)
app.MainLoop()
