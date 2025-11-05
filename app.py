import os

from flask import Flask, render_template, request, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)
Session(app)

db = os.getenv('DB')
engine = create_engine(db)
db = scoped_session(sessionmaker(bind=engine))

consonants = ('b', 'c', 'd', 'f', 'g', 'h', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'z')
vowels = ('a', 'e', 'i', 'o', 'u')

province = db.execute("SELECT * FROM province").fetchall()
province.sort()

@app.route("/")
def index():
    return render_template("index.html", province=province)

@app.route("/calcola", methods=["POST"])
def calcola():
    nome = request.form.get("nome")
    cognome = request.form.get("cognome")
    gender = str(request.form.get("gender"))
    comune = request.form.get("comune")
    if comune == 'Comune...':
        return render_template("error.html", message="Per favore compilare tutti i campi")
    date = request.form.get("date")
    giorno, mese, anno = date.split('/')


    cogn_cons = cognome.lower()
    cogn_voc = cognome.lower()
    nom_cons = nome.lower()
    nom_voc = nome.lower()
    anno = anno[2], anno[3]

    ''' COGNOME (3) '''
    for x in cogn_cons:
        if x in vowels:
            cogn_cons = cogn_cons.replace(x, "")

    for x in cogn_voc:
        if x in consonants:
            cogn_voc = cogn_voc.replace(x, "")

    if len(cogn_cons) >= 3:
        fin_cogn = cogn_cons[0], cogn_cons[1], cogn_cons[2]
    elif len(cogn_cons) >= 2:
        fin_cogn = cogn_cons[0], cogn_cons[1], cogn_voc[0]
    else:
        fin_cogn = cognome[0], cognome[1], 'x'

    ''' NOME (3) '''
    for x in nom_cons:
        if x in vowels:
            nom_cons = nom_cons.replace(x, "")

    for x in nom_voc:
        if x in consonants:
            nom_voc = nom_voc.replace(x, "")

    if len(nom_cons) >= 4:
        fin_nom = nom_cons[0], nom_cons[2], nom_cons[3]
    elif len(nom_cons) >= 3:
        fin_nom = nom_cons[0], nom_cons[1], nom_cons[2]
    elif len(nom_cons) >= 2:
        fin_nom = nom_cons[0], nom_cons[1], nom_voc[0]
    else:
        fin_nom = nome[0], nome[1], 'x'

    ''' ANNO MESE (5) '''
    fin_anno = anno
    fin_mese = ''
    if int(mese) == 1:
        fin_mese = 'a'
    elif int(mese) == 2:
        fin_mese = 'b'
    elif int(mese) == 3:
        fin_mese = 'c'
    elif int(mese) == 4:
        fin_mese = 'd'
    elif int(mese) == 5:
        fin_mese = 'e'
    elif int(mese) == 6:
        fin_mese = 'h'
    elif int(mese) == 7:
        fin_mese = 'l'
    elif int(mese) == 8:
        fin_mese = 'm'
    elif int(mese) == 9:
        fin_mese = 'p'
    elif int(mese) == 10:
        fin_mese = 'r'
    elif int(mese) == 11:
        fin_mese = 's'
    elif int(mese) == 12:
        fin_mese = 't'

    ''' GIORNO SESSO (2) '''
    if gender == "m":
        fin_giorno = int(giorno)
        if fin_giorno < 10:
            fin_giorno = '0' + str(fin_giorno)
    else:
        fin_giorno = int(giorno) + 40

    ''' COMUNE (4) '''
    codfisico = str(db.execute("SELECT codfisico FROM comuni WHERE lower(comune) = :comune", {"comune": comune}).fetchone())
    fin_codfisico = codfisico.replace('(', '')
    fin_codfisico = fin_codfisico.replace(')', '')
    fin_codfisico = fin_codfisico.replace(',', '')
    fin_codfisico = fin_codfisico.replace("'", '')
    fin_codfisico = fin_codfisico.replace('u', '')
    #print(fin_codfisico)

    ''' CODE '''
    code =  ''.join(fin_cogn)
    code =  code + ''.join(fin_nom)
    code =  code + ''.join(fin_anno)
    code =  code + fin_mese
    code =  code + str(fin_giorno)
    code =  code + fin_codfisico

    ''' CIN (1) '''
    even = []
    odd = []

    for i in range(len(code)):
        if i % 2 == 0:
            odd.append(code[i])
        else:
            even.append(code[i])
#        char_odd = code[i]
#        odd = odd + char_odd
#        i += 2

#    for b in range(c, code_len + 1):
#        char_even = code[c]
#        even = even + char_even
#        c += 2

    even = [x.lower() for x in even]
    odd = [x.lower() for x in odd]

    #even = even.lower()
    #odd = odd.lower()

    num_odd = [
            ['0', 1],
            ['1', 0],
            ['2', 5],
            ['3', 7],
            ['4', 9],
            ['5', 13],
            ['6', 15],
            ['7', 17],
            ['8', 19],
            ['9', 21],
            ['a', 1],
            ['b', 0],
            ['c', 5],
            ['d', 7],
            ['e', 9],
            ['f', 13],
            ['g', 15],
            ['h', 17],
            ['i', 19],
            ['j', 21],
            ['k', 2],
            ['l', 4],
            ['m', 18],
            ['n', 20],
            ['o', 11],
            ['p', 3],
            ['q', 6],
            ['r', 8],
            ['s', 12],
            ['t', 14],
            ['u', 16],
            ['v', 10],
            ['w', 22],
            ['x', 25],
            ['y', 24],
            ['z', 23]
    ]

    num_even = [
            ['0', 0],
            ['1', 1],
            ['2', 2],
            ['3', 3],
            ['4', 4],
            ['5', 5],
            ['6', 6],
            ['7', 7],
            ['8', 8],
            ['9', 9],
            ['a', 0],
            ['b', 1],
            ['c', 2],
            ['d', 3],
            ['e', 4],
            ['f', 5],
            ['g', 6],
            ['h', 7],
            ['i', 8],
            ['j', 9],
            ['k', 10],
            ['l', 11],
            ['m', 12],
            ['n', 13],
            ['o', 14],
            ['p', 15],
            ['q', 16],
            ['r', 17],
            ['s', 18],
            ['t', 19],
            ['u', 20],
            ['v', 21],
            ['w', 22],
            ['x', 23],
            ['y', 24],
            ['z', 25]
    ]
    num = 0
    print(num)
    for c in range(0, len(even) - 1):
        for b in range(0, 35):
            if even[c] in num_even[b]:
                num += num_even[b][1]
                print(num)

    for c in range(0, len(odd) - 1):
        for b in range(0, 35):
            if odd[c] in num_odd[b]:
                num += num_odd[b][1]
                print(num)

    
    fin_num = num % 26
    print(fin_num)

    #fin_num  = num - 26 * (num // 26)
    num_cin = [
            [0, 'a'],
            [1, 'b'],
            [2, 'c'],
            [3, 'd'],
            [4, 'e'],
            [5, 'f'],
            [6, 'g'],
            [7, 'h'],
            [8, 'i'],
            [9, 'j'],
            [10, 'k'],
            [11, 'l'],
            [12, 'm'],
            [13, 'n'],
            [14, 'o'],
            [15, 'p'],
            [16, 'q'],
            [17, 'r'],
            [18, 's'],
            [19, 't'],
            [20, 'u'],
            [21, 'v'],
            [22, 'w'],
            [23, 'x'],
            [24, 'y'],
            [25, 'z']
        ]
    for i in range(0, 26):
        if fin_num in num_cin[i]:
            code =  code + num_cin[i][1]

    #code =  code + fin_cin

    ''' PRINT '''
    #return render_template("index.html", extra=code.upper(), even=even, odd=odd, num=num, date=date, province=province)
    return render_template("index.html", extra=code.upper(), date=date, province=province)

@socketio.on('select provincia')
def select_provincia(data):
    prov = data["prov"]
    print(prov)
    comuni = db.execute("SELECT comune FROM comuni WHERE provincia = :provincia", {"provincia": prov}).fetchall()
    comuni.sort()
    for comune in comuni:
        comune = str(comune)
        comune = comune.replace("'", '')
        comune = comune.replace('"', '')
        comune = comune.replace('(', '')
        comune = comune.replace(')', '')
        comune = comune.replace(',', '')
        #print(comune)
        emit("selected provincia", {'comune':comune}, broadcast=False)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug=True)
